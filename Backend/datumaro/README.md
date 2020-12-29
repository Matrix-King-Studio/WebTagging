# 数据集框架 (Datumaro)

构建、转换和分析数据集的框架。

<!--lint disable fenced-code-flag-->
```
CVAT annotations  --                              ---> Annotation tool
...                  \                          /
COCO-like dataset -----> Datumaro ---> dataset ------> Model training
...                  /                          \
VOC-like dataset  --                              ---> Publication etc.
```
<!--lint enable fenced-code-flag-->

## Contents

- [文档](#文档)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)

## 文档

- [用户手册](docs/用户手册.md)
- [设计文档](docs/设计.md)
- [Contributing](CONTRIBUTING.md)

## Features

- 数据集格式转换:
  - COCO (`image_info`, `instances`, `person_keypoints`, `captions`, `labels`*)
    - [格式规范](http://cocodataset.org/#format-data)
    - `labels` are our extension - like `instances` with only `category_id`
  - PASCAL VOC (`classification`, `detection`, `segmentation` (class, instances), `action_classification`, `person_layout`)
    - [格式规范](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html)
  - YOLO (`bboxes`)
    - [格式规范](https://github.com/AlexeyAB/darknet#how-to-train-pascal-voc-data)
  - TF Detection API (`bboxes`, `masks`)
    - 格式规范s: [bboxes](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/using_your_own_dataset.md), [masks](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/instance_segmentation.md)
  - CVAT
    - [格式规范](https://github.com/opencv/cvat/blob/develop/cvat/apps/documentation/xml_format.md)
- 数据集生成操作:
  - 将多个数据集合并为一个
  - 例如，使用自定义条件筛选数据集：
    - 删除除某个类的多边形之外的所有注释
    - 删除没有特定类的图像
    - 从图像中删除被遮挡的标注
    - 只保留垂直方向的图像
    - 从标注中删除小区域边界框
  - Annotation conversions, for instance
    - polygons to instance masks and vise-versa
    - apply a custom colormap for mask annotations
    - remap dataset labels
- Dataset comparison
- Model integration:
  - Inference (OpenVINO and custom models)
  - Explainable AI ([RISE algorithm](https://arxiv.org/abs/1806.07421))

> Check the [design document](docs/设计.md) for a full list of features

## Installation

Optionally, create a virtual environment:

``` bash
python -m pip install virtualenv
python -m virtualenv venv
. venv/bin/activate
```

Install Datumaro package:

``` bash
pip install 'git+https://github.com/opencv/cvat#egg=datumaro&subdirectory=datumaro'
```

## Usage

There are several options available:
- [A standalone command-line tool](#standalone-tool)
- [A python module](#python-module)

### Standalone tool

<!--lint disable fenced-code-flag-->
```
    User
        |
        v
+------------------+
|       CVAT       |
+--------v---------+       +------------------+       +--------------+
| Datumaro module  | ----> | Datumaro project | <---> | Datumaro CLI | <--- User
+------------------+       +------------------+       +--------------+
```
<!--lint enable fenced-code-flag-->

``` bash
datum --help
python -m datumaro --help
```

### Python module

Datumaro can be used in custom scripts as a library in the following way:

``` python
from datumaro.components.project import Project # project-related things
import datumaro.components.extractor # annotations and high-level interfaces
# etc.
project = Project.load('directory')
```

## Examples

<!--lint disable list-item-indent-->
<!--lint disable list-item-bullet-indent-->

- Convert [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#data) to COCO, keep only images with `cat` class presented:
  ```bash
  # Download VOC dataset:
  # http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
  datum project import --format voc --input-path <path/to/voc>
  datum project export --format coco --filter '/item[annotation/label="cat"]'
  ```

- Convert only non-occluded annotations from a CVAT-annotated project to TFrecord:
  ```bash
  # export Datumaro dataset in CVAT UI, extract somewhere, go to the project dir
  datum project extract --filter '/item/annotation[occluded="False"]' \
    --mode items+anno --output-dir not_occluded
  datum project export --project not_occluded \
    --format tf_detection_api -- --save-images
  ```

- Annotate COCO, extract image subset, re-annotate it in CVAT, update old dataset:
  ```bash
  # Download COCO dataset http://cocodataset.org/#download
  # Put images to coco/images/ and annotations to coco/annotations/
  datum project import --format coco --input-path <path/to/coco>
  datum project export --filter '/image[images_I_dont_like]' --format cvat \
    --output-dir reannotation
  # import dataset and images to CVAT, re-annotate
  # export Datumaro project, extract to 'reannotation-upd'
  datum project project merge reannotation-upd
  datum project export --format coco
  ```

- Annotate instance polygons in CVAT, export as masks in COCO:
  ```bash
  datum project import --format cvat --input-path <path/to/cvat.xml>
  datum project export --format coco -- --segmentation-mode masks
  ```

- Apply an OpenVINO detection model to some COCO-like dataset,
  then compare annotations with ground truth and visualize in TensorBoard:
  ```bash
  datum project import --format coco --input-path <path/to/coco>
  # create model results interpretation script
  datum model add mymodel openvino \
    --weights model.bin --description model.xml \
    --interpretation-script parse_results.py
  datum model run --model mymodel --output-dir mymodel_inference/
  datum project diff mymodel_inference/ --format tensorboard --output-dir diff
  ```

<!--lint enable list-item-bullet-indent-->
<!--lint enable list-item-indent-->

## Contributing

Feel free to [open an Issue](https://github.com/opencv/cvat/issues/new) if you
think something needs to be changed. You are welcome to participate in development,
development instructions are available in our [developer manual](CONTRIBUTING.md).
