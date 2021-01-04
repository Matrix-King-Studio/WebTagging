import os
import shutil
import traceback
import django_rq
import os.path as osp

from datetime import datetime
from tempfile import mkstemp
from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.inspectors import CoreAPICompatInspector, NotHandled
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from sendfile import sendfile

import cvat.apps.dataset_manager as dm
import cvat.apps.dataset_manager.views
from cvat.apps.authentication import auth
from cvat.apps.authentication.decorators import login_required
from cvat.apps.dataset_manager.serializers import DatasetFormatsSerializer
from cvat.apps.engine.frame_provider import FrameProvider
from cvat.apps.engine.models import Job, StatusChoice, Task, Log, Segment
from cvat.apps.engine.serializers import (
    AnnotationFileSerializer, BasicUserSerializer,
    DataMetaSerializer, DataSerializer, ExceptionSerializer, FileInfoSerializer, JobSerializer, LabeledDataSerializer,
    LogEventSerializer, ProjectSerializer, RqStatusSerializer, TaskSerializer, UserSerializer, LogSerializer)
from cvat.settings.base import CSS_3RDPARTY, JS_3RDPARTY

from . import models, task
from .log import clogger, slogger


# drf-yasg component doesn't handle correctly URL_FORMAT_OVERRIDE and
# send requests with ?format=openapi suffix instead of ?scheme=openapi.
# We map the required paramater explicitly and add it into query arguments
# on the server side.
def wrap_swagger(view):
    @login_required
    def _map_format_to_schema(request, scheme=None):
        if 'format' in request.GET:
            request.GET = request.GET.copy()
            format_alias = settings.REST_FRAMEWORK['URL_FORMAT_OVERRIDE']
            request.GET[format_alias] = request.GET['format']
        return view(request, format=scheme)

    return _map_format_to_schema


# Server REST API
@login_required
def dispatch_request(request):
    """分派遗留请求的入口点"""
    print(request)
    if 'dashboard' in request.path or (request.path == '/' and 'id' not in request.GET):
        return RedirectView.as_view(
            url=settings.UI_URL,
            permanent=True,
            query_string=True
        )(request)
    elif request.method == 'GET' and 'id' in request.GET and request.path == '/':
        return render(request, 'engine/annotation.html', {
            'css_3rdparty': CSS_3RDPARTY.get('engine', []),
            'js_3rdparty': JS_3RDPARTY.get('engine', []),
            'status_list': [str(i) for i in StatusChoice],
            'ui_url': settings.UI_URL
        })
    else:
        return HttpResponseNotFound()


class ServerViewSet(viewsets.ViewSet):
    serializer_class = None

    # 要获得有关ServerViewSet操作的良好文档，必须实现该方法。默认情况下，ViewSet不提供它。
    def get_serializer(self, *args, **kwargs):
        pass

    @staticmethod
    @swagger_auto_schema(method='post', request_body=ExceptionSerializer)
    @action(detail=False, methods=['POST'], serializer_class=ExceptionSerializer)
    def exception(request):
        """从服务器上的客户端保存异常，向ELK发送日志（如果它已连接）"""
        serializer = ExceptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            additional_info = {
                "username": request.user.username,
                "name": "Send exception",
            }
            message = JSONRenderer().render({**serializer.data, **additional_info}).decode('UTF-8')
            jid = serializer.data.get("job_id")
            tid = serializer.data.get("task_id")
            if jid:
                clogger.job[jid].error(message)
            elif tid:
                clogger.task[tid].error(message)
            else:
                clogger.glob.error(message)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    @swagger_auto_schema(method='post', request_body=LogEventSerializer(many=True))
    @action(detail=False, methods=['POST'], serializer_class=LogEventSerializer)
    def logs(request):
        """将来自客户端的日志保存到服务器上，向 ELK 发送日志（如果它已连接）"""
        serializer = LogEventSerializer(many=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = {"username": request.user.username}
        for event in serializer.data:
            message = JSONRenderer().render({**event, **user}).decode('UTF-8')
            jobId = event.get("job_id")
            taskId = event.get("task_id")
            if jobId:
                clogger.job[jobId].info(message)
            elif taskId:
                clogger.task[taskId].info(message)
            else:
                clogger.glob.info(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    @swagger_auto_schema(
        method='get',
        operation_summary='返回服务器上沿指定路径的所有文件和文件夹',
        manual_parameters=[openapi.Parameter('directory',
                                             openapi.IN_QUERY,
                                             type=openapi.TYPE_STRING,
                                             description='要浏览的目录')],
        responses={'200': FileInfoSerializer(many=True)}
    )
    @action(detail=False, methods=['GET'], serializer_class=FileInfoSerializer)
    def share(request):
        param = request.query_params.get('directory', '/')
        if param.startswith("/"):
            param = param[1:]
        directory = os.path.abspath(os.path.join(settings.SHARE_ROOT, param))

        if directory.startswith(settings.SHARE_ROOT) and os.path.isdir(directory):
            data = []
            content = os.scandir(directory)
            for entry in content:
                entry_type = None
                if entry.is_file():
                    entry_type = "REG"
                elif entry.is_dir():
                    entry_type = "DIR"
                if entry_type:
                    data.append({"name": entry.name, "type": entry_type})

            serializer = FileInfoSerializer(many=True, data=data)
            if serializer.is_valid(raise_exception=True):
                return Response(serializer.data)
        else:
            return Response("{} is an invalid directory".format(param), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @swagger_auto_schema(method='get',
                         operation_summary='方法提供支持的标注格式的列表',
                         responses={'200': DatasetFormatsSerializer()})
    @action(detail=False, methods=['GET'], url_path='annotation/formats')
    def annotation_formats(request):
        data = dm.views.get_all_formats()
        return Response(DatasetFormatsSerializer(data).data)


class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    owner = filters.CharFilter(field_name="owner__username", lookup_expr="icontains")
    status = filters.CharFilter(field_name="status", lookup_expr="icontains")
    assignee = filters.CharFilter(field_name="assignee__username", lookup_expr="icontains")

    class Meta:
        model = models.Project
        fields = ("id", "name", "owner", "status", "assignee")


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Returns a paginated list of projects according to query parameters (10 projects per page)',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="A unique number value identifying this project",
                          type=openapi.TYPE_NUMBER),
        openapi.Parameter('name', openapi.IN_QUERY,
                          description="Find all projects where name contains a parameter value",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('owner', openapi.IN_QUERY,
                          description="Find all project where owner name contains a parameter value",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('status', openapi.IN_QUERY, description="Find all projects with a specific status",
                          type=openapi.TYPE_STRING, enum=[str(i) for i in StatusChoice]),
        openapi.Parameter('assignee', openapi.IN_QUERY,
                          description="Find all projects where assignee name contains a parameter value",
                          type=openapi.TYPE_STRING)]))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='Method creates a new project'))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(operation_summary='Method returns details of a specific project'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='Method deletes a specific project'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Methods does a partial update of chosen fields in a project'))
class ProjectViewSet(auth.ProjectGetQuerySetMixin, viewsets.ModelViewSet):
    queryset = models.Project.objects.all().order_by('-id')
    serializer_class = ProjectSerializer
    search_fields = ("name", "owner__username", "assignee__username", "status")
    filterset_class = ProjectFilter
    ordering_fields = ("id", "name", "owner", "status", "assignee")
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_permissions(self):
        http_method = self.request.method
        permissions = [IsAuthenticated]

        if http_method in SAFE_METHODS:
            permissions.append(auth.ProjectAccessPermission)
        elif http_method in ["POST"]:
            permissions.append(auth.ProjectCreatePermission)
        elif http_method in ["PATCH"]:
            permissions.append(auth.ProjectChangePermission)
        elif http_method in ["DELETE"]:
            permissions.append(auth.ProjectDeletePermission)
        else:
            permissions.append(auth.AdminRolePermission)

        return [perm() for perm in permissions]

    def perform_create(self, serializer):
        if self.request.data.get('owner', None):
            serializer.save()
        else:
            serializer.save(owner=self.request.user)

    @swagger_auto_schema(method='get',
                         operation_summary='返回具有选定id的项目任务的信息',
                         responses={'200': TaskSerializer(many=True)})
    @action(detail=True, methods=['GET'], serializer_class=TaskSerializer)
    def tasks(self, request, pk):
        self.get_object()
        queryset = Task.objects.filter(project_id=pk).order_by('-id')
        queryset = auth.filter_task_queryset(queryset, request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class TaskFilter(filters.FilterSet):
    project = filters.CharFilter(field_name="project__name", lookup_expr="icontains")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    owner = filters.CharFilter(field_name="owner__username", lookup_expr="icontains")
    mode = filters.CharFilter(field_name="mode", lookup_expr="icontains")
    status = filters.CharFilter(field_name="status", lookup_expr="icontains")
    assignee = filters.CharFilter(field_name="assignee__username", lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ("id", "project_id", "project", "name", "owner", "mode", "status", "assignee")


class DjangoFilterInspector(CoreAPICompatInspector):
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, DjangoFilterBackend):
            result = super(DjangoFilterInspector, self).get_filter_parameters(filter_backend)
            res = result.copy()
            for param in result:
                if param.get('name') == 'project_id' or param.get('name') == 'project':
                    res.remove(param)
            return res
        return NotHandled


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='根据查询参数返回分页的任务列表（每页10个任务）',
    manual_parameters=[
        openapi.Parameter('id',
                          openapi.IN_QUERY,
                          description="标识此任务的唯一数值",
                          type=openapi.TYPE_NUMBER),
        openapi.Parameter('name',
                          openapi.IN_QUERY,
                          description="查找名称中包含参数值的所有任务",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('owner',
                          openapi.IN_QUERY,
                          description="Find all tasks where owner name contains a parameter value",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('mode',
                          openapi.IN_QUERY,
                          description="Find all tasks with a specific mode",
                          type=openapi.TYPE_STRING,
                          enum=['annotation', 'interpolation']),
        openapi.Parameter('status',
                          openapi.IN_QUERY,
                          description="Find all tasks with a specific status",
                          type=openapi.TYPE_STRING,
                          enum=['annotation', 'validation', 'completed']),
        openapi.Parameter('assignee',
                          openapi.IN_QUERY,
                          description="Find all tasks where assignee name contains a parameter value",
                          type=openapi.TYPE_STRING)
    ],
    filter_inspectors=[DjangoFilterInspector]))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(operation_summary='在没有任何附加的方法的情况下创建一个新的视频数据库和任务'))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(operation_summary='方法返回特定任务的详细信息'))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(operation_summary='方法按id更新任务'))
@method_decorator(name='destroy',
                  decorator=swagger_auto_schema(operation_summary='方法删除特定任务、所有附加的作业、批注和数据'))
@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(operation_summary='方法对任务中选定的字段执行部分更新'))
class TaskViewSet(auth.TaskGetQuerySetMixin, viewsets.ModelViewSet):
    filterset_class = TaskFilter
    serializer_class = TaskSerializer
    search_fields = ("name", "owner__username", "mode", "status")
    ordering_fields = ("id", "name", "owner", "status", "assignee")
    queryset = Task.objects.all().prefetch_related("label_set__attributespec_set", "segment_set__job_set").order_by(
        '-id')

    def get_permissions(self):
        http_method = self.request.method
        permissions = [IsAuthenticated]

        if http_method in SAFE_METHODS:
            permissions.append(auth.TaskAccessPermission)
        elif http_method in ["POST"]:
            permissions.append(auth.TaskCreatePermission)
        elif self.action == 'annotations' or http_method in ["PATCH", "PUT"]:
            permissions.append(auth.TaskChangePermission)
        elif http_method in ["DELETE"]:
            permissions.append(auth.TaskDeletePermission)
        else:
            permissions.append(auth.AdminRolePermission)

        return [perm() for perm in permissions]

    def perform_create(self, serializer):
        def validateTaskLimit(master):
            admin_perm = auth.AdminRolePermission()
            isAdmin = admin_perm.has_permission(self.request, self)
            if not isAdmin and settings.RESTRICTIONS['task_limit'] is not None:
                if Task.objects.filter(owner=master).count() >= settings.RESTRICTIONS['task_limit']:
                    raise serializers.ValidationError('用户拥有最大数量的任务')

        owner = self.request.data.get('owner', None)
        if owner:
            validateTaskLimit(owner)
            serializer.save()
        else:
            validateTaskLimit(self.request.user)
            serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        task_dirname = instance.get_task_dirname()
        super().perform_destroy(instance)
        shutil.rmtree(task_dirname, ignore_errors=True)
        if instance.data and not instance.data.tasks.all():
            shutil.rmtree(instance.data.get_data_dirname(), ignore_errors=True)
            instance.data.delete()

    @swagger_auto_schema(method='get', operation_summary='返回特定任务的作业列表', responses={'200': JobSerializer(many=True)})
    @action(detail=True, methods=['GET'], serializer_class=JobSerializer)
    def jobs(self, request, pk):
        self.get_object()  # force to call check_object_permissions
        queryset = Job.objects.filter(segment__task_id=pk)
        serializer = JobSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(method='post',
                         operation_summary='方法将图像或视频永久附加到任务')
    @swagger_auto_schema(method='get',
                         operation_summary='方法返回特定任务的数据',
                         manual_parameters=[
                             openapi.Parameter('type',
                                               in_=openapi.IN_QUERY,
                                               required=True,
                                               type=openapi.TYPE_STRING,
                                               enum=['chunk', 'frame', 'preview'],
                                               description="指定请求数据的类型"),
                             openapi.Parameter('quality',
                                               in_=openapi.IN_QUERY,
                                               required=True,
                                               type=openapi.TYPE_STRING,
                                               enum=['·', 'original'],
                                               description="指定所请求数据的质量级别，对于“预览”类型无所谓"),
                             openapi.Parameter('number',
                                               in_=openapi.IN_QUERY,
                                               required=True,
                                               type=openapi.TYPE_NUMBER,
                                               description="标识块或帧的唯一数值，对于“预览”类型无关紧要"),
                         ]
                         )
    @action(detail=True, methods=['POST', 'GET'])
    def data(self, request, pk):
        if request.method == 'POST':
            db_task = self.get_object()  # call check_object_permissions as well
            serializer = DataSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            db_data = serializer.save()
            db_task.data = db_data
            db_task.save()
            data = {k: v for k, v in serializer.data.items()}
            data['use_zip_chunks'] = serializer.validated_data['use_zip_chunks']
            # if the value of stop_frame is 0, then inside the function we cannot know
            # the value specified by the user or it's default value from the database
            if 'stop_frame' not in serializer.validated_data:
                data['stop_frame'] = None
            task.create(db_task.id, data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            LogViewSet.createLog(taskId=pk, userId=request.user.id, message="Load task data")

            data_type = request.query_params.get('type', None)
            data_id = request.query_params.get('number', None)
            data_quality = request.query_params.get('quality', 'compressed')

            # 管理员或项目创建者调用时没有 jobId 参数则可以拿到所有的图片
            jobId = request.query_params.get('jobId', None)
            if jobId:
                segment = Segment.objects.filter(job__pk=jobId).first()
                segment = model_to_dict(segment)

                # 判断用户请求的图片 index 在所请求 job 的范围内
                if not int(segment["start_frame"]) <= int(data_id) <= int(segment["stop_frame"]):
                    return Response(data="不是你的终究不是你的", status=status.HTTP_403_FORBIDDEN)

            possible_data_type_values = ('chunk', 'frame', 'preview')
            possible_quality_values = ('compressed', 'original')

            if not data_type or data_type not in possible_data_type_values:
                return Response(data='数据类型未指定或值错误', status=status.HTTP_200_OK)
            elif data_type == 'chunk' or data_type == 'frame':
                if not data_id:
                    return Response(data='未指定编号', status=status.HTTP_200_OK)
                elif data_quality not in possible_quality_values:
                    return Response(data='错误的质量值', status=status.HTTP_200_OK)
            try:
                # get_object()获取单个的object对象
                db_task = self.get_object()
                frame_provider = FrameProvider(db_task.data)
                if data_type == 'chunk':
                    data_id = int(data_id)
                    data_quality = FrameProvider.Quality.COMPRESSED \
                        if data_quality == 'compressed' else FrameProvider.Quality.ORIGINAL
                    # 获取当前执行脚本的绝对路径
                    path = os.path.realpath(frame_provider.get_chunk(data_id, data_quality))
                    # 如果块是真实图像上的链接，请遵循符号链接，否则sendfile中的mimetype检测将无法正常工作。
                    return sendfile(request, path)
                elif data_type == 'frame':
                    data_id = int(data_id)
                    data_quality = FrameProvider.Quality.COMPRESSED \
                        if data_quality == 'compressed' else FrameProvider.Quality.ORIGINAL
                    buf, mime = frame_provider.get_frame(data_id, data_quality)
                    return HttpResponse(buf.getvalue(), content_type=mime)
                elif data_type == 'preview':
                    return sendfile(request, frame_provider.get_preview())
                else:
                    return Response(data='unknown data type {}.'.format(data_type), status=status.HTTP_200_OK)
            except APIException as e:
                return Response(data=e.default_detail, status=e.status_code)
            except Exception as e:
                msg = 'cannot get requested data type: {}, number: {}, quality: {}'.format(data_type, data_id,
                                                                                           data_quality)
                slogger.task[pk].error(msg, exc_info=True)
                return Response(data=msg + '\n' + str(e), status=status.HTTP_200_OK)

    @swagger_auto_schema(method='get',
                         operation_summary='方法允许下载任务标注',
                         manual_parameters=[
                             openapi.Parameter('format',
                                               openapi.IN_QUERY,
                                               description="所需的输出格式名称，您可以在以下位置获取支持格式的列表：/server/annotation/formats",
                                               type=openapi.TYPE_STRING,
                                               required=False),
                             openapi.Parameter('filename',
                                               openapi.IN_QUERY,
                                               description="所需的输出文件名",
                                               type=openapi.TYPE_STRING,
                                               required=False),
                             openapi.Parameter('action',
                                               in_=openapi.IN_QUERY,
                                               description='用于在创建批注文件后开始下载进程',
                                               type=openapi.TYPE_STRING,
                                               required=False,
                                               enum=['download'])],
                         responses={
                             '202': openapi.Response(description='开始转储标注数据集'),
                             '201': openapi.Response(description='标注数据集准备下载'),
                             '200': openapi.Response(description='开始下载标注数据集')})
    @swagger_auto_schema(method='put', operation_summary='方法允许上载任务批注',
                         manual_parameters=[
                             openapi.Parameter('format', openapi.IN_QUERY,
                                               description="输入格式名称\n您可以在/server/annotation/formats获取支持格式的列表。",
                                               type=openapi.TYPE_STRING, required=False)],
                         responses={
                             '202': openapi.Response(description='Uploading has been started'),
                             '201': openapi.Response(description='Uploading has finished')})
    @swagger_auto_schema(method='patch',
                         operation_summary='方法对特定任务中的批注执行部分更新',
                         manual_parameters=[
                             openapi.Parameter('action',
                                               in_=openapi.IN_QUERY,
                                               required=True,
                                               type=openapi.TYPE_STRING,
                                               enum=['create', 'update', 'delete'])])
    @swagger_auto_schema(method='delete', operation_summary='方法删除特定任务的所有批注')
    @action(detail=True,
            methods=['GET', 'DELETE', 'PUT', 'PATCH'],
            serializer_class=LabeledDataSerializer)
    def annotations(self, request, pk):
        db_task = self.get_object()  # force to call check_object_permissions
        if request.method == 'GET':
            LogViewSet.createLog(taskId=pk, userId=request.user.id, message="Download task annotation data")
            format_name = request.query_params.get('format')
            if format_name:
                return _export_annotations(db_task=db_task,
                                           rq_id="/api/v1/tasks/{}/annotations/{}".format(pk, format_name),
                                           request=request,
                                           action=request.query_params.get("action", "").lower(),
                                           callback=dm.views.export_task_annotations,
                                           format_name=format_name)
            else:
                data = dm.task.get_task_data(pk)
                serializer = LabeledDataSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    return Response(serializer.data)
        elif request.method == 'PUT':
            LogViewSet.createLog(taskId=pk, userId=request.user.id, message="Upload task annotation data")
            format_name = request.query_params.get('format')
            if format_name:
                return _import_annotations(
                    request=request,
                    rq_id="{}@/api/v1/tasks/{}/annotations/upload".format(request.user, pk),
                    rq_func=dm.task.import_task_annotations,
                    pk=pk,
                    format_name=format_name)
            else:
                serializer = LabeledDataSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    data = dm.task.put_task_data(pk, serializer.data)
                    return Response(data)
        elif request.method == 'DELETE':
            LogViewSet.createLog(taskId=pk, userId=request.user.id, message="Delete task annotation data")
            dm.task.delete_task_data(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PATCH':
            # 获取要执行的操作
            action = self.request.query_params.get("action", None)
            LogViewSet.createLog(taskId=pk, userId=request.user.id, message=action + " task annotation")
            # 判断操作是否允许
            if action not in dm.task.PatchAction.values():
                raise serializers.ValidationError("请为请求指定正确的“操作”")
            serializer = LabeledDataSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                    data = dm.task.patch_task_data(pk, serializer.data, action)
                except (AttributeError, IntegrityError) as e:
                    return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
                return Response(data)

    @swagger_auto_schema(method='get', operation_summary='创建任务时，该方法返回有关创建进程状态的信息')
    @action(detail=True, methods=['GET'], serializer_class=RqStatusSerializer)
    def status(self, request, pk):
        self.get_object()  # force to call check_object_permissions
        response = self._get_rq_response(queue="default", job_id="/api/{}/tasks/{}".format(request.version, pk))
        serializer = RqStatusSerializer(data=response)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)

    @staticmethod
    def _get_rq_response(queue, job_id):
        queue = django_rq.get_queue(queue)
        job = queue.fetch_job(job_id)
        response = {}
        if job is None or job.is_finished:
            response = {"state": "Finished"}
        elif job.is_queued:
            response = {"state": "Queued"}
        elif job.is_failed:
            response = {"state": "Failed", "message": job.exc_info}
        else:
            response = {"state": "Started"}
            if 'status' in job.meta:
                response['message'] = job.meta['status']
        return response

    @staticmethod
    @swagger_auto_schema(method='get',
                         operation_summary='元任务提供了与媒体相关的信息',
                         responses={'200': DataMetaSerializer()})
    @action(detail=True, methods=['GET'], serializer_class=DataMetaSerializer, url_path='data/meta')
    def data_info(request, pk):
        LogViewSet.createLog(taskId=pk, userId=request.user.id, message="Load task data info")

        db_task = models.Task.objects.prefetch_related('data__images').select_related('data__video').get(pk=pk)

        if hasattr(db_task.data, 'video'):
            media = [db_task.data.video]
        else:
            media = list(db_task.data.images.order_by('frame'))

        frame_meta = [{
            'width': item.width,
            'height': item.height,
            'name': item.path,
        } for item in media]

        db_data = db_task.data
        db_data.frames = frame_meta

        serializer = DataMetaSerializer(db_data)
        return Response(serializer.data)

    @swagger_auto_schema(method='get', operation_summary='将任务导出为特定格式的数据集',
                         manual_parameters=[
                             openapi.Parameter('format',
                                               openapi.IN_QUERY,
                                               description="所需的输出格式名称\n您可以在以下位置获取支持格式的列表：\n/server/annotation/formats",
                                               type=openapi.TYPE_STRING, required=True),
                             openapi.Parameter('filename',
                                               openapi.IN_QUERY,
                                               description="所需的输出文件名",
                                               type=openapi.TYPE_STRING,
                                               required=False),
                             openapi.Parameter('action',
                                               in_=openapi.IN_QUERY,
                                               description='用于在创建批注文件后开始下载进程',
                                               type=openapi.TYPE_STRING,
                                               required=False,
                                               enum=['download'])
                         ],
                         responses={'202': openapi.Response(description='已开始导出'),
                                    '201': openapi.Response(description='输出文件已准备好下载'),
                                    '200': openapi.Response(description='已开始下载文件')
                                    }
                         )
    @action(detail=True, methods=['GET'], serializer_class=None, url_path='dataset')
    def dataset_export(self, request, pk):
        LogViewSet.createLog(taskId=pk, userId=request.user.id, message="Download dataset data")
        db_task = self.get_object()  # force to call check_object_permissions

        format_name = request.query_params.get("format", "")
        return _export_annotations(db_task=db_task,
                                   rq_id="/api/v1/tasks/{}/dataset/{}".format(pk, format_name),
                                   request=request,
                                   action=request.query_params.get("action", "").lower(),
                                   callback=dm.views.export_task_as_dataset,
                                   format_name=format_name)


@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(operation_summary='方法返回作业的详细信息'))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(operation_summary='方法按id更新作业'))
@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(
                      operation_summary='方法对作业中的选定字段执行部分更新'))
class JobViewSet(viewsets.GenericViewSet,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer

    def get_permissions(self):
        http_method = self.request.method
        permissions = [IsAuthenticated]

        if http_method in SAFE_METHODS:
            permissions.append(auth.JobAccessPermission)
        elif http_method in ["PATCH", "PUT", "DELETE"]:
            permissions.append(auth.JobChangePermission)
        else:
            permissions.append(auth.AdminRolePermission)

        return [perm() for perm in permissions]

    @swagger_auto_schema(method='get',
                         operation_summary='方法返回特定作业的批注')
    @swagger_auto_schema(method='put',
                         operation_summary='方法对特定作业中的所有批注执行更新')
    @swagger_auto_schema(method='patch',
                         manual_parameters=[
                             openapi.Parameter('action',
                                               in_=openapi.IN_QUERY,
                                               type=openapi.TYPE_STRING,
                                               required=True,
                                               enum=['create', 'update', 'delete'])],
                         operation_summary='方法对特定作业中的批注执行部分更新')
    @swagger_auto_schema(method='delete',
                         operation_summary='方法删除特定作业的所有批注')
    @action(detail=True,
            methods=['GET', 'DELETE', 'PUT', 'PATCH'],
            serializer_class=LabeledDataSerializer)
    def annotations(self, request, pk):
        self.get_object()  # force to call check_object_permissions
        if request.method == 'GET':
            LogViewSet.createLog(taskId=pk, userId=request.user.id, message="Download job annotation data")
            data = dm.task.get_job_data(pk)
            return Response(data)
        elif request.method == 'PUT':
            LogViewSet.createLog(taskId=pk, userId=request.user.id, message="Upload job annotation data")
            format_name = request.query_params.get("format", "")
            if format_name:
                return _import_annotations(
                    request=request,
                    rq_id="{}@/api/v1/jobs/{}/annotations/upload".format(request.user, pk),
                    rq_func=dm.task.import_job_annotations,
                    pk=pk,
                    format_name=format_name
                )
            else:
                serializer = LabeledDataSerializer(data=request.data)
                if serializer.is_valid():
                    try:
                        data = dm.task.put_job_data(pk, serializer.data)
                    except (AttributeError, IntegrityError) as e:
                        return Response(data=str(e), status=status.HTTP_200_OK)
                    return Response(data)
                else:
                    print(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            LogViewSet.createLog(taskId=pk, userId=request.user.id, message="Delete job annotation data")
            dm.task.delete_job_data(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PATCH':
            action = self.request.query_params.get("action", None)
            LogViewSet.createLog(taskId=pk, userId=request.user.id, message=action + " job annotation")
            if action not in dm.task.PatchAction.values():
                raise serializers.ValidationError("请为请求指定正确的“操作”")
            serializer = LabeledDataSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                    data = dm.task.patch_job_data(pk, serializer.data, action)
                except (AttributeError, IntegrityError) as e:
                    return Response(data=str(e), status=status.HTTP_200_OK)
                return Response(data)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_summary='方法提供在服务器上注册的用户的分页列表'))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_summary='方法提供特定用户的信息'))
@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(
                      operation_summary='更新用户选择的方法字段'))
@method_decorator(name='destroy',
                  decorator=swagger_auto_schema(
                      operation_summary='方法从服务器中删除特定用户'))
class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = User.objects.all().order_by('id')
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff:
            return UserSerializer
        else:
            is_self = int(self.kwargs.get("pk", 0)) == user.id or self.action == "self"
            if is_self and self.request.method in SAFE_METHODS:
                return UserSerializer
            else:
                return BasicUserSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated]
        user = self.request.user

        if not (self.request.method in SAFE_METHODS):
            is_self = int(self.kwargs.get("pk", 0)) == user.id
            if not is_self:
                permissions.append(auth.AdminRolePermission)

        return [perm() for perm in permissions]

    @swagger_auto_schema(method='get',
                         operation_summary='方法返回当前已被授权的用户的实例')
    @action(detail=False, methods=['GET'])
    def self(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(request.user, context={"request": request})
        return Response(serializer.data)


def rq_handler(job, exc_type, exc_value, tb):
    job.exc_info = "".join(
        traceback.format_exception_only(exc_type, exc_value))
    job.save()
    if "tasks" in job.id.split("/"):
        return task.rq_handler(job, exc_type, exc_value, tb)
    return True


# TODO: Method should be reimplemented as a separated view
# @swagger_auto_schema(method='put', manual_parameters=[openapi.Parameter('format', in_=openapi.IN_QUERY,
#         description='A name of a loader\nYou can get annotation loaders from this API:\n/server/annotation/formats',
#         required=True, type=openapi.TYPE_STRING)],
#     operation_summary='Method allows to upload annotations',
#     responses={'202': openapi.Response(description='Load of annotations has been started'),
#         '201': openapi.Response(description='Annotations have been uploaded')},
#     tags=['tasks'])
# @api_view(['PUT'])
def _import_annotations(request, rq_id, rq_func, pk, format_name):
    queue = django_rq.get_queue("default")
    rqJob = queue.fetch_job(rq_id)
    if not rqJob:
        serializer = AnnotationFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if format_name not in [f.DISPLAY_NAME for f in dm.views.get_import_formats()]:
                raise serializers.ValidationError("Unknown input format '{}'".format(format_name))

            annotationFile = serializer.validated_data['annotation_file']
            fd, filename = mkstemp(prefix='cvat_{}'.format(pk))
            with open(filename, 'wb+') as f:
                for chunk in annotationFile.chunks():
                    f.write(chunk)
            rqJob = queue.enqueue_call(
                func=rq_func,
                args=(pk, filename, format_name),
                job_id=rq_id)
            rqJob.meta['tmp_file'] = filename
            rqJob.meta['tmp_file_descriptor'] = fd
            rqJob.save_meta()
    else:
        if rqJob.is_finished:
            os.close(rqJob.meta['tmp_file_descriptor'])
            os.remove(rqJob.meta['tmp_file'])
            rqJob.delete()
            return Response(status=status.HTTP_201_CREATED)
        elif rqJob.is_failed:
            os.close(rqJob.meta['tmp_file_descriptor'])
            os.remove(rqJob.meta['tmp_file'])
            exc_info = str(rqJob.exc_info)
            rqJob.delete()
            return Response(data=exc_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_202_ACCEPTED)


def _export_annotations(db_task, rq_id, request, format_name, action, callback):
    # 如果 action 提供了意外的参数，返回错误结果
    if action not in {"", "download"}:
        raise serializers.ValidationError("为请求指定了意外的操作")

    # 如果 format_name 不是允许的格式，返回错误结果
    if format_name not in [f.DISPLAY_NAME for f in dm.views.get_export_formats()]:
        raise serializers.ValidationError("为请求指定的格式未知")

    queue = django_rq.get_queue("default")
    rqJob = queue.fetch_job(rq_id)
    if rqJob:  # 队列中任务存在
        lastTaskUpdateTime = timezone.localtime(db_task.updated_date)
        request_time = rqJob.meta.get('request_time', None)
        if request_time is None or request_time < lastTaskUpdateTime:
            rqJob.cancel()
            rqJob.delete()
        else:
            if rqJob.is_finished:  # 标注数据集生成成功
                file_path = rqJob.return_value
                if action == "download" and osp.exists(file_path):
                    rqJob.delete()
                    timestamp = datetime.strftime(lastTaskUpdateTime, "%Y_%m_%d_%H_%M_%S")
                    filename = "task_{}-{}-{}{}".format(
                        db_task.name, timestamp, format_name, osp.splitext(file_path)[1])
                    return sendfile(request, file_path, attachment=True, attachment_filename=filename.lower())
                else:
                    if osp.exists(file_path):
                        return Response(status=status.HTTP_201_CREATED)
            elif rqJob.is_failed:  # 标注数据集生成失败
                exc_info = str(rqJob.exc_info)
                rqJob.delete()
                return Response(exc_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:  # 标注数据集正在生成
                return Response(status=status.HTTP_202_ACCEPTED)
    try:
        if request.scheme:
            server_address = request.scheme + '://'
        server_address += request.get_host()
    except Exception:
        server_address = None

    ttl = dm.views.CACHE_TTL.total_seconds()
    queue.enqueue_call(func=callback, args=(db_task.id, format_name, server_address), job_id=rq_id,
                       meta={'request_time': timezone.localtime()}, result_ttl=ttl, failure_ttl=ttl)
    return Response(status=status.HTTP_202_ACCEPTED)


class LogFilter(filters.FilterSet):
    task = filters.CharFilter(field_name="task__name", lookup_expr="icontains")
    user = filters.CharFilter(field_name="user__username", lookup_expr="icontains")
    time = filters.DateTimeFilter(field_name="time", lookup_expr="icontains")
    message = filters.CharFilter(field_name="message", lookup_expr="icontains")

    class Meta:
        model = Log
        fields = ("id", "task_id", "task", "user", "time", "message")


class LogViewSet(ModelViewSet):
    filterset_class = LogFilter
    queryset = Log.objects.all().order_by('time')
    permission_classes = [IsAuthenticated]
    serializer_class = LogSerializer

    @classmethod
    def createLog(cls, taskId, userId, message):
        log = Log(task_id=taskId, user_id=userId, time=timezone.now(), message=message)
        log.save()
