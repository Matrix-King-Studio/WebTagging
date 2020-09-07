# 安软科技 web 标注平台（CVAT）

计算机视觉标注工具(CVAT)是基于 Web 为计算机视觉算法标注视频和图像的在线工具。

它的灵感来自[Vatic](http://carlvondrick.com/vatic/)免费的、在线的、交互式的视频注释工具。

CVAT有许多强大的功能:
- 在关键帧之间插入边界框
- 使用深度学习模型自动标注
- 大多数关键行动的捷径
- 带有注释任务列表的仪表板
- LDAP和基本授权
- 等……

它是为一个专业的数据注释团队创建和使用的。

特别针对我们团队开发的计算机视觉任务进行了用户体验和用户界面优化。

## 文档

- [安装指南](documentation/installation.md)
- [用户手册](documentation/user_guide.md)
- [Datumaro 数据集框架](datumaro/README.md)
- [XML 标注格式](documentation/xml_format.md)

## 支持的标注格式

单击上传标注和转储标注按钮后，可以选择格式。
[Datumaro](datumaro/README.md) 数据库框架允许通过命令行工具和Python库进行额外的数据集转换。

| 标注格式                                                                          | Import | Export |
| ------------------------------------------------------------------------------------------ | ------ | ------ |
| [CVAT for images](documentation/xml_format.md#annotation)                        | √      | √      |
| [CVAT for a video](documentation/xml_format.md#interpolation)                    | √      | √      |
| [Datumaro](datumaro/README.md)                                                             |        | √      |
| [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/)                                      | √      | √      |
| Segmentation masks from [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/)              | √      | √      |
| [YOLO](https://pjreddie.com/darknet/yolo/)                                                 | √      | √      |
| [MS COCO Object Detection](http://cocodataset.org/#format-data)                            | √      | √      |
| [TFrecord](https://www.tensorflow.org/tutorials/load_data/tf_records)                      | √      | √      |
| [MOT](https://motchallenge.net/)                                                           | √      | √      |
| [LabelMe 3.0](http://labelme.csail.mit.edu/Release3.0)                                     | √      | √      |

## 在线演示： [安软科技 Web 标注平台](http://alexking.site:8080/)

这是一个最新版本标注工具的在线演示。在线试用，无需本地安装。只有自己的或分配的任务对用户可见。

禁用功能：
- [分析：数据标注团队的管理和监控](/components/analytics/README.md)
- [支持NVIDIA GPU](/components/cuda/README.md)

限制：
- 每个用户不超过10个任务
- 上传数据限制为500Mb

## REST API

自动生成的Django rest api的Swagger文档 ``<cvat_origin>/api/swagger``(default: ``localhost:8080/api/swagger``).

Swagger 文档让所有允许的 hostes 访问， Update environement variable in docker-compose.yml file with cvat hosted machine IP or domain name.

Example - ``ALLOWED_HOSTS: 'localhost, 127.0.0.1'``)
