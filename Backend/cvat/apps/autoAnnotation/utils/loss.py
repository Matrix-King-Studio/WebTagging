# Loss functions

import torch
import torch.nn as nn

from utils.general import bbox_iou
from utils.torch_utils import is_parallel


def smooth_BCE(eps=0.1):  # https://github.com/ultralytics/yolov3/issues/238#issuecomment-598028441
    # return positive, negative label smoothing BCE targets
    return 1.0 - 0.5 * eps, 0.5 * eps


class BCEBlurWithLogitsLoss(nn.Module):
    # BCEwithLogitLoss() with reduced missing label effects.
    def __init__(self, alpha=0.05):
        super(BCEBlurWithLogitsLoss, self).__init__()
        self.loss_fcn = nn.BCEWithLogitsLoss(reduction='none')  # must be nn.BCEWithLogitsLoss()
        self.alpha = alpha

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)
        pred = torch.sigmoid(pred)  # prob from logits
        dx = pred - true  # reduce only missing label effects
        # dx = (pred - true).abs()  # reduce missing label and false label effects
        alpha_factor = 1 - torch.exp((dx - 1) / (self.alpha + 1e-4))
        loss *= alpha_factor
        return loss.mean()


class FocalLoss(nn.Module):
    # Wraps focal loss around existing loss_fcn(), i.e. criteria = FocalLoss(nn.BCEWithLogitsLoss(), gamma=1.5)
    def __init__(self, loss_fcn, gamma=1.5, alpha=0.25):
        super(FocalLoss, self).__init__()
        self.loss_fcn = loss_fcn  # must be nn.BCEWithLogitsLoss()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = loss_fcn.reduction
        self.loss_fcn.reduction = 'none'  # required to apply FL to each element

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)
        pred_prob = torch.sigmoid(pred)  # prob from logits
        p_t = true * pred_prob + (1 - true) * (1 - pred_prob)
        alpha_factor = true * self.alpha + (1 - true) * (1 - self.alpha)
        modulating_factor = (1.0 - p_t) ** self.gamma
        loss *= alpha_factor * modulating_factor

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:  # 'none'
            return loss


class QFocalLoss(nn.Module):
    # Wraps Quality focal loss around existing loss_fcn(), i.e. criteria = FocalLoss(nn.BCEWithLogitsLoss(), gamma=1.5)
    def __init__(self, loss_fcn, gamma=1.5, alpha=0.25):
        super(QFocalLoss, self).__init__()
        self.loss_fcn = loss_fcn  # must be nn.BCEWithLogitsLoss()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = loss_fcn.reduction
        self.loss_fcn.reduction = 'none'  # required to apply FL to each element

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)

        pred_prob = torch.sigmoid(pred)  # prob from logits
        alpha_factor = true * self.alpha + (1 - true) * (1 - self.alpha)
        modulating_factor = torch.abs(true - pred_prob) ** self.gamma
        loss *= alpha_factor * modulating_factor

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:  # 'none'
            return loss


def compute_loss(predictions, targets, model):
    device = targets.device
    clsL, boxL, objL = torch.zeros(1, device=device), torch.zeros(1, device=device), torch.zeros(1, device=device)
    clsT, boxT, indices, anchors = build_targets(predictions, targets, model)  # targets
    h = model.hyp  # hyperparameters

    # Define criteria
    BCEcls = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([h['cls_pw']], device=device))  # weight=model.class_weights)
    BCEobj = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([h['obj_pw']], device=device))

    # Class label smoothing https://arxiv.org/pdf/1902.04103.pdf eqn 3
    cp, cn = smooth_BCE(eps=0.0)

    # Focal loss
    g = h['fl_gamma']  # focal loss gamma
    if g > 0:
        BCEcls, BCEobj = FocalLoss(BCEcls, g), FocalLoss(BCEobj, g)

    # Losses
    nt = 0  # number of targets
    no = len(predictions)  # number of outputs
    balance = [4.0, 1.0, 0.3, 0.1, 0.03]  # P3-P7
    for i, pi in enumerate(predictions):  # layer index, layer predictions
        b, a, gj, gi = indices[i]  # image, anchor, gridy, gridx
        tobj = torch.zeros_like(pi[..., 0], device=device)  # target obj

        n = b.shape[0]  # number of targets
        if n:
            nt += n  # cumulative targets
            ps = pi[b, a, gj, gi]  # prediction subset corresponding to targets

            # Regression
            pxy = ps[:, :2].sigmoid() * 2. - 0.5
            pwh = (ps[:, 2:4].sigmoid() * 2) ** 2 * anchors[i]
            pbox = torch.cat((pxy, pwh), 1)  # predicted box
            iou = bbox_iou(pbox.T, boxT[i], x1y1x2y2=False, CIoU=True)  # iou(prediction, target)
            boxL += (1.0 - iou).mean()  # iou loss

            # Objectness
            tobj[b, a, gj, gi] = (1.0 - model.gr) + model.gr * iou.detach().clamp(0).type(tobj.dtype)  # iou ratio

            # Classification
            if model.nc > 1:  # cls loss (only if multiple classes)
                t = torch.full_like(ps[:, 5:], cn, device=device)  # targets
                t[range(n), clsT[i]] = cp
                clsL += BCEcls(ps[:, 5:], t)  # BCE

            # Append targets to text file
            # with open('targets.txt', 'a') as file:
            #     [file.write('%11.5g ' * 4 % tuple(x) + '\n') for x in torch.cat((txy[i], twh[i]), 1)]

        objL += BCEobj(pi[..., 4], tobj) * balance[i]  # obj loss

    s = 3 / no  # output count scaling
    boxL *= h['box'] * s
    objL *= h['obj']
    clsL *= h['cls'] * s
    bs = tobj.shape[0]  # batch size

    loss = boxL + objL + clsL
    return loss * bs, torch.cat((boxL, objL, clsL, loss)).detach()


def build_targets(prediction, targets, model):
    """
    Build targets for compute_loss()

    Args:
        prediction:
        targets: image, class, x, y, w, h
        model:

    Returns:
        clsT:
        boxT:
        indices:
        anchor:
    """
    clsT, boxT, indices, anchor = [], [], [], []
    gain = torch.ones(7, device=targets.device)  # normalized to grid space gain

    det = model.module.model[-1] if is_parallel(model) else model.model[-1]  # Detect() module
    anchorNum, targetNum = det.na, targets.shape[0]  # number of anchors, targets
    ai = torch.arange(anchorNum, device=targets.device).float().view(anchorNum, 1).repeat(1, targetNum)
    targets = torch.cat((targets.repeat(anchorNum, 1, 1), ai[:, :, None]), 2)  # append anchor indices

    bias = 0.5  # ↓ 表示5个偏移，原点不动、往右、往下、往左、往上
    off = torch.tensor([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1], ], device=targets.device).float() * bias  # offsets

    for i in range(det.nl):
        anchors = det.anchors[i]
        gain[2:6] = torch.tensor(prediction[i].shape)[[3, 2, 3, 2]]  # xyxy gain

        # Match targets to anchors
        t = targets * gain  # 将 gt 的 cx, cy, w, h 换算到当前 feature map 对应尺寸和 anchor 匹配
        if targetNum:
            # Matches
            radio = t[:, :, 4:6] / anchors[:, None]
            j = torch.max(radio, 1. / radio).max(2)[0] < model.hyp['anchor_t']  # compare
            t = t[j]  # filter

            # Offsets
            gxy = t[:, 2:4]  # grid xy
            gxi = gain[[2, 3]] - gxy  # inverse
            j, k = ((gxy % 1. < bias) & (gxy > 1.)).T
            l, m = ((gxi % 1. < bias) & (gxi > 1.)).T
            j = torch.stack((torch.ones_like(j), j, k, l, m))
            t = t.repeat((5, 1, 1))[j]
            offsets = (torch.zeros_like(gxy)[None] + off[:, None])[j]
        else:
            t = targets[0]
            offsets = 0

        # Define
        b, c = t[:, :2].long().T  # image, class
        gxy = t[:, 2:4]  # grid xy
        gwh = t[:, 4:6]  # grid wh
        gij = (gxy - offsets).long()
        gi, gj = gij.T  # grid xy indices

        # Append
        a = t[:, 6].long()  # anchor indices
        indices.append((b, a, gj.clamp_(0, gain[3] - 1), gi.clamp_(0, gain[2] - 1)))  # image, anchor, grid indices
        boxT.append(torch.cat((gxy - gij, gwh), 1))  # box
        anchor.append(anchors[a])  # anchors
        clsT.append(c)  # class

    return clsT, boxT, indices, anchor
