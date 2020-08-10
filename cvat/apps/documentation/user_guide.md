- [用户指南](#用户指南)
  - [Getting started](#getting-started)
    - [Authorization](#authorization)
    - [Administration panel](#administration-panel)
    - [Creating an annotation task](#creating-an-annotation-task)
    - [Models](#models)
    - [Search](#search)
  - [Interface of the annotation tool](#interface-of-the-annotation-tool)
    - [Basic navigation](#basic-navigation)
    - [Types of shapes (basics)](#types-of-shapes-basics)
    - [Shape mode (basics)](#shape-mode-basics)
    - [Track mode (basics)](#track-mode-basics)
    - [Attribute annotation mode (basics)](#attribute-annotation-mode-basics)
    - [Downloading annotations](#downloading-annotations)
    - [Task synchronization with a repository](#task-synchronization-with-a-repository)
    - [Vocabulary](#vocabulary)
    - [Workspace](#workspace)
    - [Settings](#settings)
    - [Top Panel](#top-panel)
    - [Controls sidebar](#controls-sidebar)
    - [Objects sidebar](#objects-sidebar)
      - [Objects](#objects)
      - [Labels](#labels)
  - [Shape mode (advanced)](#shape-mode-advanced)
  - [Track mode (advanced)](#track-mode-advanced)
  - [Attribute annotation mode (advanced)](#attribute-annotation-mode-advanced)
  - [Annotation with rectangle by 4 points](#annotation-with-rectangle-by-4-points)
  - [Annotation with polygons](#annotation-with-polygons)
  - [Annotation with polylines](#annotation-with-polylines)
  - [Annotation with points](#annotation-with-points)
    - [Points in shape mode](#points-in-shape-mode)
    - [Linear interpolation with one point](#linear-interpolation-with-one-point)
  - [Annotation with cuboids](#annotation-with-cuboids)
  - [Annotation with tags](#annotation-with-tags)
  - [Automatic annotation](#automatic-annotation)
  - [Shape grouping](#shape-grouping)
  - [Filter](#filter)
  - [Analytics](#analytics)
  - [Shortcuts](#shortcuts)

# 用户指南

计算机视觉标注工具(CVAT)是基于 Web 为计算机视觉算法标注视频和图像的在线工具。

它的灵感来自[Vatic](http://carlvondrick.com/vatic/)免费的、在线的、交互式的视频注释工具。

CVAT有许多强大的功能:
- 在关键帧之间插入边界框
- 使用深度学习模型自动标注
- 大多数关键行动的捷径
- 带有注释任务列表的仪表板
- LDAP和基本授权
- 等……

它是为一个专业的数据标注团队创建和使用的，特别针对我们团队开发的计算机视觉任务进行了用户体验和用户界面优化。

## 入门

### 授权

-   首先，登录到 CVAT 工具。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801115204438.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)

-   如果没有账号，想创建一个非管理员用户，请点击“注册”按钮

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801115252314.jpg#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801115754105.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)

-   注册用户在默认情况下无权查看任务列表，需要管理员通过后台管理系统为新用户分配正确的组。
    以下命令创建管理员帐户：

    ``docker exec -it cvat bash -ic '/usr/bin/python3 ~/manage.py createsuperuser'``

### 后台管理系统

后台管理系统可以：
-   创建/编辑/删除用户
-   控制用户的权限和对工具的访问。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801120013183.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)

### 创建标注任务

1.  点击主页面上的 ``Create new task`` 按钮创建标注任务。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801120321568.jpg#pic_center)


1.  指定任务的参数：

    #### 基本配置

    **Name** 要创建的任务的名称。
	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801120445372.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)
    **Labels**. 使用标签有两种方法：
    -   ``Constructor``是添加和调整标签的简单方法。要添加新标签，请单击``Add label``按钮。![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801120837327.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)
        可以在``Label name``字段中设置标签的名称。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801121016717.jpg#pic_center)
        如有必要，您可以通过单击``Add an attribute``来添加属性并设置其属性：

		![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801121149502.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)
        此处提供以下操作：
        1. 设置属性的名称。
        2. 选择显示属性的方式：
           - Select — 下拉列表选值
           - Radio — 从建议的几个选项中只选择一个时使用
           - Checkbox — 从建议的选项中选择任意数量的选项时使用
           - Text — 属性作为文本输入，默认属性
           - Number — 属性作为数字输入
        3. 为属性设置值。按``Enter``键可以分隔这些值。输入的值显示为一个单独的元素，可以通过按``Backspace``或单击“关闭”按钮（x）来删除该元素。
        如果指定的属性显示方式是文本或数字，则默认情况下输入的值将显示为文本。
        4. 复选框``Mutable``确定属性是否将被逐帧更改。
        5. 可以通过单击``关闭``按钮（x）删除该属性。
       单击``Continue``按钮添加更多标签。
        如果需要取消添加标签-请按``Cancel``按钮。
        添加完所有必要的标签后，单击``Done``按钮。
        单击``Done``后，添加的标签将显示为不同颜色的单独元素。
        您可以通过单击``Update attributes``或``Delete label``来编辑或删除标签。
    -   ``Raw`` 是高级用户使用标签的一种方式。
	``Raw`` 以 json 格式显示标签数据，并提供了编辑和复制标签作为文本的选项。
    ``Done`` 按钮应用更改，``Reset`` 按钮取消更改。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801122959376.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)
    在``Raw``和``Constructor``模式下，可以按“Copy”按钮复制标签列表。

    **Select files**. 点击``My computer``从您的电脑中选择一些要添加批注的文件。
    如果点击``Connected file share``，则可以从网络中选择要标注的文件。
    如果选择`` Remote source``，您将看到一个字段，您可以在其中输入URL列表（每行一个URL）。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080112354746.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)
    #### 高级配置

	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801123905501.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)

    **Z-Order**. 定义绘制多边形的顺序。选中启用分层显示复选框。

    **Use zip chunks**. 强制使用压缩块作为压缩数据。实际只用于视频。

    **Image Quality**. 使用此选项可指定上载图像的质量。
    该选项有助于更快地加载高分辨率数据集。
	使用从``1``（完全压缩的图像）到``95``（几乎不是压缩图像）的值。

    **Overlap Size**. 使用此选项可生成重叠段。
    该选项使轨迹从一个线段连续到另一个线段。
    将其用于插值模式。使用该参数有几个选项：
    - 用于插值任务（视频序列）。
    如果在两个相邻的线段上标注边界框，它们将合并为一个边界框。
    如果重叠等于零或标注在转储的标注文件中的相邻段上较差，则将有多个轨迹，每个段对应一个对象。
    - 标注（独立图像）。
    如果一个对象存在于重叠的线段上，重叠大于零，并且相邻线段上的标注足够好，则该对象将自动合并为一个对象。
    如果重叠等于零或标注在转储标注文件内的相邻段上较差，则同一对象将有多个边界框。
    因此，可以在第一个线段上注释对象。
    在第二个线段上标注同一个对象，如果您做得对，标注中就有一个轨迹。
    如果不同段（重叠框架上）上的标注非常不同，则同一对象将有两个形状。
 	此功能仅适用于边界框。
    多边形、多段线、点不支持重叠段上的自动合并，即使重叠参数不为零，相邻线段上相应形状之间的匹配也非常完美。

    **Segment size**. 使用此选项可以将一个巨大的数据集分成几个较小的段。
    例如，一个作业不能由多个贴标器标注（不支持）。
    因此，使用"segment size"可以为同一注释任务创建多个作业。
    它将有助于您并行数据标注过程。

    **Start frame**. 任务中的视频开始的帧。

    **Stop frame**. 任务中的视频结束的帧。

    **Frame Step**. 使用此选项可过滤视频帧。
    例如，输入“25”可在视频中每隔二十五帧或每二十五幅图像保留一次。

    **Chunk size**. 定义从客户端发送到服务器时要打包在块中的帧数。
    如果为空，服务器将自动定义。

    推荐值：
    - 1080p or less: 36
    - 2k or less: 8 - 16
    - 4k or less: 4 - 8
    - More: 1 - 4

    **Dataset Repository**.  存储库的URL链接可选地指定存储库的路径 (``default: annotation / <dump_file_name> .zip``).
    支持注解的.zip和.xml文件扩展名。
    Field format: ``URL [PATH]`` example: ``https://github.com/project/repos.git  [1/2/3/4/annotation.xml]``

    支持的URL格式：
    - ``https://github.com/project/repos[.git]``
    - ``github.com/project/repos[.git]``
    - ``git@github.com:project/repos[.git]``

    如果标注与存储库不同步，则创建后任务将以红色突出显示。

    **Use LFS**. 如果标注文件很大，可以使用[LFS](https://git-lfs.github.com/)创建一个存储库支持。

    **Issue tracker**. 如果需要，请指定问题跟踪程序的完整URL。

    按``Submit``按钮，它将被添加到注释任务列表中。
    然后，创建的任务将显示在仪表板上：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801131624551.jpg#pic_center)
1.  仪表板包含元素，每个元素都与单独的任务相关。它们按创建顺序排序。
    每个元素包含：任务名称、预览、进度条、按钮“打开”和菜单“操作”。
    每个按钮负责菜单内“操作”特定功能：
    - ``Dump Annotation``和``Export as a dataset``—下载特定格式的批注或批注和图像。以下格式可用：
      - [CVAT for video](/cvat/apps/documentation/xml_format.md#interpolation)
      如果任务具有插值模式，则突出显示。
      - [CVAT for images](/cvat/apps/documentation/xml_format.md#annotation)
      如果任务具有批注模式，则突出显示。
      - [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/)
      - [(VOC) Segmentation mask](http://host.robots.ox.ac.uk/pascal/VOC/) —
          archive包含png格式的每个帧的类和实例掩码，以及一个文本文件，其中包含每个颜色的值。
      - [YOLO](https://pjreddie.com/darknet/yolo/)
      - [COCO](http://cocodataset.org/#format-data)
      - [TFRecord](https://www.tensorflow.org/tutorials/load_data/tf_records)
      - [MOT](https://motchallenge.net/)
      - [LabelMe 3.0](http://labelme.csail.mit.edu/Release3.0/)
      - [Datumaro](https://github.com/opencv/cvat/blob/develop/datumaro/)
    - ``Upload annotation``的格式与``Dump annotation``中的格式相同。
      - [CVAT](/cvat/apps/documentation/xml_format.md) 同时接受视频和图像子格式。
    - ``Automatic Annotation``—使用OpenVINO toolkit进行自动注释。
      存在性取决于如何构建CVAT实例。
    - ``Open bug tracker`` — 打开指向问题跟踪程序的链接。
    - ``Delete`` — 删除任务。

    按``Open`` 按钮转到任务详细信息。

1.  任务详细信息是一个任务页面，其中包含预览、进度条、任务的详细信息（在创建任务时指定）和“作业”部分。

    [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-t0hODpHu-1596171611932)(static/documentation/images/image131_detrac.jpg)]

    - 此页上提供了以下操作：
      1. 更改任务的标题
      2. 打开“Actions”菜单
      3. 更改问题跟踪程序或打开问题跟踪程序（如果已指定）
      4. 更换标签。
      可以在原始模式或构造函数模式下为现有标签添加新标签或添加属性。
      单击``Copy``可将标签复制到剪贴板。
      1. Assigned to — 用于将任务分配给某人。开始输入被派遣人的姓名和/或从下拉列表中选择合适的人。
    - ``Jobs`` — 是特定任务的所有作业的列表。在这里您可以找到下一个数据：
      - 带有超链接的作业名称。
      - Frames — 帧间隔。
      - 任务的状态。 状态由用户在任务内的菜单中指定。
      有三种类型的状态：标注、质检或已完成。
      作业的状态是根据任务的进度条变化的。
      - Started on — 此任务的开始日期。
      - Duration — 是任务的时间量。
      - Assignee是正在处理任务的用户。
      你可以开始输入被派遣人的姓名和/或从下拉列表中选择合适的人。
      - ``Copy``. 单击“复制”可将作业列表复制到剪贴板。
      任务列表包含指向任务的直接链接。

1.  按照“作业”部分中的链接开始标注过程。
	在某些情况下，可以有多个链接。它取决于任务的大小以及“重叠大小”和“段大小”参数。为了提高用户体验，只会加载几个帧的第一个块，并且您可以对第一个图像进行注释。其他帧将在后台加载。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802102158327.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)

### 模型

在“模型”页面上，您可以管理为自动标注而上载的深度学习（DL）模型。
使用该功能，您可以上载、更新或删除特定的DL模型。
要打开模型管理器，请单击导航栏上的“模型”按钮。
“模型”页面包含有关所有现有模型的信息。
模型列表分为两部分：
- Primary — 包含默认的CVAT模型。每个模型都是一个单独的元素。
它包含模型的名称、模型所基于的框架和“支持的标签”（所有支持标签的下拉列表）。
- Uploaded by a user — 包含用户上载的模型。
用户模型列表中有其他列，其中包含以下信息：
上传模型的用户名以及上传日期。
在这里，您可以在“操作”菜单中删除模型。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802102938896.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)


要添加模型，请单击“创建新模型”。
输入模型名称，然后使用“选择文件”按钮选择模型文件。
要使用自定义模型标注任务，您需要准备4个文件：
- ``Model config`` (*.xml) - 具有网络配置的文本文件。
- ``Model weights`` (*.bin) - 经过训练的权重的二进制文件。
- ``Label map`` (*.json) - 一个简单的json文件，带有label_map的字典，类似于一个带有标签号字符串值的对象。
- ``Interpretation script`` (*.py) - 用于将网络输出层转换为可由CVAT处理的预定义结构的文件。

了解有关创建模型文件的详细信息可以阅读：[自动标注]()
如果希望每个人都能使用模型，请选中“全局加载”。
单击“提交”按钮提交模型。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802103919704.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)

上传完成后，您的模型可以在“由用户上载”部分找到。
使用“Auto annotation”按钮使用您的一个DL模型对任务进行预注释。

### 搜索

对于搜索有几个选项。

- 在所有字段中搜索（所有者、代理人、任务名称、任务状态、任务模式）。
在搜索字段中输入搜索字符串执行。
- 如何执行搜索特定字段：
  - ``owner: admin`` - 由名称中有子字符串“admin”的用户创建的所有任务
  - ``assignee: employee``  - 分配给名称中有子字符串“employee”的用户的所有任务
  - ``name: mighty`` - 所有名称中带有子字符串“mighty”的任务
  - ``mode: annotation`` or ``mode: interpolation`` - 所有带有图像或视频的任务。
  - ``status: annotation`` or ``status: validation`` or ``status: completed``  - 按状态搜索
  - ``id: 5`` - id=5的任务。
- Multiple filters. 可以使用关键字``AND``组合筛选器（标识符除外）:
  - ``mode: interpolation AND owner: admin``
  - ``mode: annotation and status: annotation``

搜索不区分大小写。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802104842887.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


## 标注工具的界面

该工具包括：
- ``Header`` -  用于导航CVAT部分和帐户设置的固定标题;
- ``Top panel`` — 包含导航按钮、主要功能和菜单访问；
- ``Workspace`` — 显示图像的空间；
- ``Controls sidebar`` — 包含用于导航图像、缩放、创建形状和编辑轨迹的工具（合并、拆分、分组）
- ``Objects sidebar`` — 包含标签过滤器，两个列表：
  对象（帧上的）和标签（帧上对象的）和外观设置。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802105159970.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

### 基本导航

1.  使用下面的箭头移动到下一帧/上一帧。
    使用滚动条滑块在帧之间滚动。
    几乎每个按钮都有一个快捷方式。
    To get a hint about a shortcut, just move your mouse pointer over an UI element.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802105637670.jpg#pic_center)


1.  要导航图像，请使用控件侧栏上的按钮。
    另一种可以移动/移动图像的方法是在没有注释对象的区域内按住鼠标左键。
    如果按下“鼠标滚轮”，则忽略所有带注释的对象。否则，将移动高亮显示的边界框而不是图像本身。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802105808791.jpg#pic_center)

1.  您可以使用边栏控件上的按钮缩放感兴趣的区域。
    使用“调整图像大小”按钮在工作区中调整图像大小。
    您也可以使用鼠标滚轮缩放图像（图像将相对于当前光标位置进行缩放）。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807095857292.jpg)

### 形状类型（基础）

有五种形状可以为图像添加标注：
- ``Rectangle`` or ``Bounding box``
- ``Polygon``
- ``Polyline``
- ``Points``
- ``Cuboid``
- ``Tag``

它们看起来都是这样的：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802105858292.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802105938229.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802110024859.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70#pic_center)

``Tag`` - 工作区中没有形状，但显示在对象侧栏中。

### 形状模式（基础）
使用示例：
- 为一组图像创建新标注。
- 为现有标注添加/修改/删除对象。

1.  您需要在控件侧栏上选择“矩形”：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807102035631.jpg)


    开始之前，请选择正确的“标签”（创建任务时应指定）和“绘图方法”（两点或四点）：
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080710213362.jpg)

1.  在“形状模式”中创建新标注：

    -   单击“形状”创建一个单独的“矩形”。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807102223203.jpg)


    -   选择相反的点。你的第一个矩形准备好了！
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807102455213.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

    -   了解如何使用“按4点”绘制方法创建矩形的步骤, ([read here](#annotation-by-rectangle-4-points)).

    -   使用鼠标可以调整矩形的边界和位置。
        Rectangle's size is shown in the top right corner , you can check it by clicking on any point of the shape.
        You can also undo your actions using ``Ctrl+Z`` and redo them with ``Shift+Ctrl+Z`` or ``Ctrl+Y``.

1.  You can see the ``Object card`` in the objects sidebar or open it by right-clicking on the object.
    You can change the attributes in the details section.
    You can perform basic operations or delete an object by clicking on the action menu button.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807102736651.jpg)


1.  The following figure is an example of a fully annotated frame with separate shapes.

    [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-oRxUV641-1596171611968)(static/documentation/images/image013_detrac.jpg)]

    Read more in the section [shape mode (advanced)](#shape-mode-advanced).

### 轨迹模式（基础）
使用示例：
- 为帧序列创建新标注。
- 为现有标注添加/修改/删除对象。
- 编辑轨迹，将几个矩形合并为一个轨迹。

1.  与“形状模式”一样，您需要在侧栏上选择一个“矩形”，在出现的表单中，选择所需的“标签”和“绘图方法”。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807104327351.jpg)

2.  为对象创建轨迹（以选定的汽车为例）：
    - 通过单击“Track”在“Track mode”下创建一个“Rectangle”。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807104409798.jpg)

    - In ``Track mode`` the rectangle will be automatically interpolated on the next frames.
    - The cyclist starts moving on frame #2270. Let's mark the frame as a key frame.
      You can press ``K`` for that or click the ``star`` button (see the screenshot below).

        [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-8XFejoDU-1596171611971)(static/documentation/images/image016.jpg)]

    - If the object starts to change its position, you need to modify the rectangle where it happens.
      It isn't necessary to change the rectangle on each frame, simply update several keyframes
      and the frames between them will be interpolated automatically.
    - Let's jump 30 frames forward and adjust the boundaries of the object. See an example below:

        [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-xiedw6RV-1596171611972)(static/documentation/images/image017_detrac.jpg)]

    -   After that the rectangle of the object will be changed automatically on frames 2270 to 2300:

        [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-bwvIrfna-1596171611973)(static/documentation/images/gif019_detrac.gif)]

3.  When the annotated object disappears or becomes too small, you need to
    finish the track. You have to choose ``Outside Property``, shortcut ``O``.

    [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-9FX70dWo-1596171611975)(static/documentation/images/image019.jpg)]

4.  If the object isn't visible on a couple of frames and then appears again,
    you can use the ``Merge`` feature to merge several individual tracks
    into one.

    [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-nxg8MdWG-1596171611977)(static/documentation/images/image020.jpg)]

    -   Create tracks for moments when the cyclist is visible:

        [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-a9DNXklL-1596171611979)(static/documentation/images/gif001_detrac.gif)]

    -   Click ``Merge`` button or press key ``M`` and click on any rectangle of the first track
        and on any rectangle of the second track and so on:

        [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-ISGPgo4d-1596171611980)(static/documentation/images/image162_detrac.jpg)]

    -   Click ``Merge`` button or press ``M`` to apply changes.

        [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-wqXg6XXv-1596171611982)(static/documentation/images/image020.jpg)]

    -   The final annotated sequence of frames in ``Interpolation`` mode can
        look like the clip below:

        [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-lJEPfF0l-1596171611983)(static/documentation/images/gif003_detrac.gif)]

        Read more in the section [track mode (advanced)](#track-mode-advanced).

### 属性标注模式（基础）

-   在此模式下，可以使用键盘在对象和帧之间快速导航来编辑属性。
    打开顶部面板中的下拉列表，然后选择“属性标注模式”。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807104519185.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

-   在此模式下，对象面板更改为特殊面板：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807104613676.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

-   The active attribute will be red. In this case it is ``gender`` . Look at the bottom side panel to see all possible shortcuts for changing the attribute. Press key ``2`` on your keyboard to assign a value (female) for the attribute or select from the drop-down list.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807104821549.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

-   Press ``Up Arrow``/``Down Arrow`` on your keyboard or click the buttons in the UI to go to the next/previous
    attribute. In this case, after pressing ``Down Arrow`` you will be able to edit the ``Age`` attribute.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807104844880.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

-   Use ``Right Arrow``/``Left Arrow`` keys to move to the previous/next image with annotation.

To see all the hot keys available in the attribute annotation mode, press ``F2``.
Read more in the section [attribute annotation mode (advanced)](#attribute-annotation-mode-advanced).

### 下载标注

1.  要下载最新的标注，必须先保存所有更改。点击“保存”按钮，或者“Ctrl+S”快捷键可以快速保存标注。
1.  然后，点击“菜单”按钮。
1.  按“转储标注”按钮。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802111422527.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


1.  选择转储标注文件的格式.：
    - [CVAT for video](/cvat/apps/documentation/xml_format.md#interpolation)
      如果任务具有插值模式，则突出显示。
    - [CVAT for images](/cvat/apps/documentation/xml_format.md#annotation)
      如果任务具有标注模式，则突出显示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802111650976.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

    - [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/)
    - [(VOC) Segmentation mask](http://host.robots.ox.ac.uk/pascal/VOC/) — archive包含png格式的每个帧的类和实例掩码，以及一个文本文件，其中包含每个颜色的值。
    - [YOLO](https://pjreddie.com/darknet/yolo/)
    - [COCO](http://cocodataset.org/#format-data)
    - [TFRecord](https://www.tensorflow.org/tutorials/load_data/tf_records)
    - [MOT](https://motchallenge.net/)
    - [LabelMe 3.0](http://labelme.csail.mit.edu/Release3.0/)
    - [Datumaro](https://github.com/opencv/cvat/blob/develop/datumaro/)

### 同步存储库任务

1.  在注释过程结束时，通过单击任务页上的“同步”来同步任务。注意：只有在创建任务时指定了git存储库时，此功能才有效。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807105053946.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


1.  同步后，按钮“Sync”以绿色突出显示。注释现在位于存储库中的临时分支中。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807105159288.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

1.  下一步是转到存储库并手动创建对主分支的请求。
1.  确认PR后，当注释保存在主分支中时，任务的颜色变为蓝色。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807105329792.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

### 词汇

**Label** 是带标注对象的一种类型（例如人、车等）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802111749794.jpg)


---

**Attribute** 是标注对象的属性（例如颜色、模型、质量等），有两种类型的属性：

-   **Unique**: 不可变，不能在帧之间更改（例如年龄、性别、颜色等）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802111841546.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

-   **Temporary**: 可变，可在任何帧上更改（例如质量、姿势、截断等）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802111921330.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


---
**Track** 是不同框架上对应于一个对象的一组形状。
轨迹是在``轨迹模式``下创建的
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802112014746.gif)


---
**Annotation** 是一组形状和轨迹。有几种类型的标注：
- _Manual_ 是个人创造的
- _Semi-automatic_ 主要是自动创建，但用户提供一些数据（例如插值）
- _Automatic_ 它是在没有人参与的情况下自动创建的
---
### 工作区

这是用于绘制和编辑对象的主字段。
此外，工作区还具有以下功能：
-   右键单击一个对象会调用“对象卡”—这是一个包含更改对象标签和属性以及操作菜单所需控件的元素。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802154617918.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

-   右键单击一个点将删除该点。![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802154635241.jpg)

-   ``Z-axis slider`` - 允许您切换隐藏上层的批注层（如果帧上有多个z层，则启用滑块）。
    此元素有一个用于添加新层的按钮。按下时，会添加一个新层并切换到该层。
    可以使用`+``和`-``键在层中移动对象。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802154559600.jpg)

---
### 设置

要打开“设置”，请打开标题中的“用户”菜单，然后选择“设置”项。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802112137439.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


``Settings`` 有两个选项卡：

在``Player``选项卡中，您可以：
-   Control step of ``C`` and ``V`` shortcuts.
-   控制``Space``/``Play``按钮的速度。
-   显示“网格”，更改网格大小，选择颜色和透明度：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802112241948.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


-   以全尺寸显示每个图像或像以前一样缩小（默认情况下，插值模式启用，注释模式禁用）。
- ``Rotate all images``  checkbox — 切换所有帧或单个帧的旋转。
-   调整``Brightness``/``Contrast``/``Saturation`` 太暴露或太暗的图像使用 ``F3`` — 颜色设置（更改显示设置而不是图像本身）。

Shortcuts:
-   ``Shift+B+=``/``Shift+B+-`` for brightness.
-   ``Shift+C+=``/``Shift+C+-`` for contrast.
-   ``Shift+S+=``/``Shift+S+-`` for saturation.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802112304449.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


-   ``Reset color settings`` to 默认值。

---

在“工作区”选项卡中，您可以：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802112324316.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


- ``Enable auto save`` 复选框-默认情况下处于禁用状态。
- ``Auto save interval (min)`` 输入框-默认为15分钟。
- ``Show all interpolation tracks`` 复选框-在侧面板上为每个插值对象显示隐藏对象（默认情况下禁用）。
- ``Always show object details`` - 不仅在激活对象时在画布上显示对象的文本：
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080211234424.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


- ``Automatic bordering`` - 在绘图/编辑期间启用多边形和多段线的自动边界。
  For more information To find out more, go to the section [annotation with polygons](#Annotation-with-polygons).
- ``Attribute annotation mode (AAM) zoom margin`` 输入框-定义属性标注模式下形状的边距（以px为单位）。
- Press `` Go back`` or ``F3`` to return to the annotation.

---

### 顶部面板
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802112406493.jpg)


---

#### 菜单按钮

它是标注工具的主菜单。它可以用来下载，上传和删除标注。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080211244810.jpg)

按钮分配：

- ``Dump Annotations`` — 从任务下载标注。
- ``Upload Annotations`` — 将批注上载到任务中。
- ``Remove Annotations`` — 从当前作业中删除标注。
- ``Export as a dataset`` — 从任务下载数据集。有几种格式可用：
  - [Datumaro](https://github.com/opencv/cvat/blob/develop/datumaro/docs/design.md)
  - [Pascal VOC 2012](http://host.robots.ox.ac.uk/pascal/VOC/)
  - [MS COCO](http://cocodataset.org/#format-data)
  - [YOLO](https://pjreddie.com/darknet/yolo/)
- ``Open the task`` — 打开包含任务详细信息的页面。
- ``Run ReID merge`` —  形状或轨迹的自动合并。
  它用于在单个轨迹中组合由自动标注创建的单个对象。
  更多信息请点击[这里](cvat/apps/reid/README.md)。

#### 保存工作

保存当前作业的批注。该按钮指示保存过程。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802112929554.jpg)

#### 撤消重做按钮

使用按钮撤消或重做操作。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113019542.jpg)

---

#### Player

转到第一帧/最后一帧。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113036170.jpg)


Go to the next/previous frame with a predefined step. Shortcuts:
``V`` — step backward, ``C`` — step forward. By default the step is ``10`` frames
(change at ``Account Menu`` —> ``Settings`` —> ``Player Step``).
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113105899.jpg)


Go to the next/previous frame (the step is 1 frame). Shortcuts: ``D`` — previous, ``F`` — next.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113123129.jpg)


Play the sequence of frames or the set of images.
Shortcut: ``Space`` (change at ``Account Menu`` —> ``Settings`` —> ``Player Speed``).
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113137438.jpg)


Go to a specific frame. Press ``~`` to focus on the element.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113152656.jpg)


---

#### 全屏播放器
全屏播放模式。键盘快捷键是“F11”。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113331523.jpg)


#### Info
Open the job info.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-Cw3RtBeZ-1596171612020)(static/documentation/images/image144_detrac.jpg)]

- Job status: ``annotation``, ``validation`` or ``completed`` task

_Overview_:

-  ``Assinger`` - the one to whom the job is assigned.
-  ``Start Frame`` - the number of the first frame in this job.
-  ``End Frame`` - the number of the last frame in this job.
-  ``Frames`` - the total number of all frames in the job.
-  ``Z-Order`` - z-order enable indicator.

_Annotations statistics_:

  This is a table number of created shapes, sorted by labels (e.g. vehicle, person)
  and type of annotation (shape, track). As well as the number of manual and interpolated frames.

#### UI switcher
Switching between user interface modes.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-yklCr3i6-1596171612022)(static/documentation/images/image145.jpg)]

---

### 控件边栏

**Navigation block** - 包含用于移动和旋转图像的工具。

|Icon                                         |Description                                                           |
|--                                           |--                                                                    |
|![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080211342813.jpg)|``Cursor`` (``Esc``)- a basic annotation pedacting tool.              |
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-tU6iHk4u-1596171612023)(static/documentation/images/image149.jpg)]|``Move the image``- a tool for moving around the image without<br/> the possibility of editing.|
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-Bw0lVxrL-1596171612024)(static/documentation/images/image102.jpg)]|``Rotate``- two buttons to rotate the current frame<br/> a clockwise (``Ctrl+R``) and anticlockwise (``Ctrl+Shift+R``).<br/> You can enable ``Rotate all images`` in the settings to rotate all the images in the job

**Zoom block** - contains tools for image zoom.
|Icon                                         |Description                                                           |
|--                                           |--                                                                    |
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-DDYuWn0b-1596171612025)(static/documentation/images/image151.jpg)]|``Fit image``- fits image into the workspace size.<br/> Shortcut - double click on an image|
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-cvEN197d-1596171612027)(static/documentation/images/image166.jpg)]|``Select a region of interest``- zooms in on a selected region.<br/> You can use this tool to quickly zoom in on a specific part of the frame.|

**Shapes block** - contains all the tools for creating shapes.
|Icon                                         |Description   |Links to section  |
|--                                           |--            |--                |
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-lxhHLtW9-1596171612028)(static/documentation/images/image167.jpg)]|``Rectangle``|[Shape mode](#shape-mode-basics); [Track mode](#track-mode-basics);<br/> [Drawing by 4 points](#annotation-with-rectangle-by-4-points)|
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-HJ3fmllq-1596171612029)(static/documentation/images/image168.jpg)]|``Polygon``  |[Annotation with polygons](#annotation-with-polygons)  |
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-I4Lb4jxW-1596171612030)(static/documentation/images/image169.jpg)]|``Polyline`` |[Annotation with polylines](#annotation-with-polylines)|
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-elI2Xwb5-1596171612030)(static/documentation/images/image170.jpg)]|``Points``   |[Annotation with points](#annotation-with-points)      |
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-CHTtzaws-1596171612031)(static/documentation/images/image176.jpg)]|``Cuboid``   |[Annotation with cuboids](#annotation-with-cuboids)    |
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-2r1dheNM-1596171612032)(static/documentation/images/image171.jpg)]|``Tag``      |[Annotation with tags](#annotation-with-tag)s            |

**Edit block** - contains tools for editing tracks and shapes.
|Icon                                         |Description                                        |Links to section  |
|--                                           |--                                                 |--                |
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-BECK3ozg-1596171612033)(static/documentation/images/image172.jpg)]|``Merge Shapes``(``M``) — starts/stops the merging shapes mode.  |[Track mode (basics)](#track-mode-basics)|
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-Kceg3Cro-1596171612034)(static/documentation/images/image173.jpg)]|``Group Shapes`` (``G``) — starts/stops the grouping shapes mode.|[Shape grouping](#shape-grouping)|
|[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-GZPRgbEJ-1596171612035)(static/documentation/images/image174.jpg)]|``Split`` — splits a track.                                      |[Track mode (advanced)](#track-mode-advanced)|

---

### 对象提要栏
``Hide`` - 该按钮隐藏对象的侧栏。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113523901.jpg)


#### Objects

**Filter** input box
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113542639.jpg)

The way how to use filters is described in the advanced guide [here](#filter).

**List of objects**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113600704.jpg)


  - Switch lock property for all - switches  lock property of all objects in the frame.
  - Switch hidden property for all - switches hide property of all objects in the frame.
  - Expand/collapse all - collapses/expands the details field of all objects in the frame.
  - Sorting - sort the list of objects: updated time, ID - accent, ID -  descent

In the objects sidebar you can see the list of available objects on the current
frame. The following figure is an example of how the list might look like:

| Shape mode                                    | Track mode                                    |
|--                                             |--                                             |
| [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-Qod8ZqOE-1596171612040)(static/documentation/images/image044.jpg)] | [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-4vcy4vWx-1596171612041)(static/documentation/images/image045.jpg)] |

---
**Objects** on the side bar

The type of a shape can be changed by selecting **Label** property. For instance, it can look like shown on the figure below:

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-wb0mblHM-1596171612043)(static/documentation/images/image050.jpg)]

**Object action menu**

The action menu calls up the button:

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-DQfRhG12-1596171612044)(static/documentation/images/image047.jpg)]

The action menu contains:

- ``Create object URL`` - puts a link to an object on the clipboard. After you open the link, this object will be filtered.
- ``Make a copy``- copies an object. The keyboard shortcut is ``Ctrl + C`` ``Ctrl + V``.
- ``Propagate`` - Сopies the form to several frames,
  invokes a dialog box in which you can specify the number of copies
  or the frame onto which you want to copy the object. The keyboard shortcut ``Ctrl + B``.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-6Kodjp9M-1596171612045)(static/documentation/images/image053.jpg)]

- ``To background`` - moves the object to the background. The keyboard shortcut ``-``,``_``.
- ``To foreground`` - moves the object to the foreground. The keyboard shortcut ``+``,``=``.
- ``Remove`` - removes the object. The keyboard shortcut ``Del``,``Shift+Del``.

A shape can be locked to prevent its modification or moving by an accident. Shortcut to lock an object: ``L``.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-MvfGUOW4-1596171612046)(static/documentation/images/image046.jpg)]

A shape can be **Occluded**. Shortcut: ``Q``. Such shapes have dashed boundaries.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-4rGP0SaB-1596171612047)(static/documentation/images/image048.jpg)]

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-9NajWWCM-1596171612048)(static/documentation/images/image049_detrac.jpg)]

You can change the way an object is displayed on a frame (show or hide).

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-R7xQHxdn-1596171612048)(static/documentation/images/image055.jpg)]

``Switch pinned property`` - when enabled, a shape cannot be moved by dragging or dropping.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-rNnliAlA-1596171612049)(static/documentation/images/image052.jpg)]

You can change an object's color.
To do so, click on the color bar of the object and select a color from the palette that appears.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-etCLn1m8-1596171612050)(static/documentation/images/image153.jpg)]

By clicking on the ``Details`` button you can collapse or expand the field with all the attributes of the object.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-DEPNyTd2-1596171612051)(static/documentation/images/image154.jpg)]

---

#### Labels
You can also change the color of any object to random, to do so just hover
the mouse over the object on the frame and highlight them by clicking on a label you need.
In this tab, you can lock or hide objects of a certain label.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-49LY3VIq-1596171612051)(static/documentation/images/image062.jpg)]

---

#### Appearance

**Color By** options

Change the color scheme of annotation:
-   ``Instance`` — every  shape has random color

    [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-mHqmzAQt-1596171612052)(static/documentation/images/image095_detrac.jpg)]

-   ``Group`` — every group of shape has its own random color, ungrouped shapes are white

    [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-6SvfwThS-1596171612053)(static/documentation/images/image094_detrac.jpg)]

-   ``Label`` — every label (e.g. car, person) has its own random color

    [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-GbkZocQQ-1596171612054)(static/documentation/images/image093_detrac.jpg)]

    You can change any random color pointing to a needed box on a frame or on an
    object sidebar.

**Fill Opacity** slider

Change the opacity of every shape in the annotation.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-UeteOcRo-1596171612055)(static/documentation/images/image086_detrac.jpg)]

**Selected Fill Opacity** slider

Change the opacity of the selected object's fill.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-zghcnStt-1596171612055)(static/documentation/images/image089_detrac.jpg)]

**Black Stroke** checkbox

Changes the shape border from colored to black.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-CIXr81rO-1596171612056)(static/documentation/images/image088_detrac.jpg)]

**Show bitmap** checkbox

If enabled all shapes are displayed in white and the background is black.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-WntHqkZe-1596171612057)(static/documentation/images/image087_detrac.jpg)]

**Show projections** checkbox

Enables / disables the display of auxiliary perspective lines. Only relevant for cuboids
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802153033686.jpg)

## Shape mode (advanced)

Basic operations in the mode were described in section [shape mode (basics)](#shape-mode-basics).

**Occluded**
Occlusion is an attribute used if an object is occluded by another object or
isn't fully visible on the frame. Use ``Q`` shortcut to set the property
quickly.

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-BnWehcKu-1596171612060)(static/documentation/images/image065.jpg)]

Example: the three cars on the figure below should be labeled as **occluded**.
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080215301486.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

If a frame contains too many objects and it is difficult to annotate them
due to many shapes placed mostly in the same place, it makes sense
to lock them. Shapes for locked objects are transparent, and it is easy to
annotate new objects. Besides, you can't change previously annotated objects
by accident. Shortcut: ``L``.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802152959786.jpg)


## Track mode (advanced)

Basic operations in the mode were described in section [track mode (basics)](#track-mode-basics).

Shapes that were created in the track mode, have extra navigation buttons.
-   These buttons help to jump to the previous/next keyframe.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802152940871.jpg)

-   The button helps to jump to the initial frame and to the last keyframe.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802152923987.jpg)

You can use the `` Split '' function to split one track into two tracks:
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802152826786.gif)

## Attribute annotation mode (advanced)

Basic operations in the mode were described in section [attribute annotation mode (basics)](#attribute-annotation-mode-basics).

It is possible to handle lots of objects on the same frame in the mode.
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080215254159.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

It is more convenient to annotate objects of the same type. In this case you can apply the appropriate filter. For example, the following filter will hide all objects except person: ``label=="Person"``.

To navigate between objects (person in this case),
use the following buttons ``switch between objects in the frame`` on the special panel:
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802152524636.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

or shortcuts:
- ``Tab`` — go to the next object
- ``Shift+Tab`` — go to the previous object.

In order to change the zoom level, go to settings (press ``F3``)
in the workspace tab and set the value Attribute annotation mode (AAM) zoom margin in px.

## Annotation with rectangle by 4 points
It is an efficient method of bounding box annotation, proposed
[here](https://arxiv.org/pdf/1708.02750.pdf).
Before starting, you need to make sure that the drawing method by 4 points is selected.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802152457598.jpg)

Press ``Shape`` or ``Track`` for entering drawing mode. Click on four extreme points:
the top, bottom, left- and right-most physical points on the object.
Drawing will be automatically completed right after clicking the fourth point.
Press ``Esc`` to cancel editing.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802152438683.gif)


## 带多边形的标注

### 手工绘图
一般被被用于语义分割。

如果要标注多边形，请确保启用了“创建新任务”对话框中的“Z-Order”标志。

Z-Order标志定义绘图顺序。有必要获得正确的注释蒙版而不需要额外的工作（额外的边界绘制）。

按``+``/``-``可改变Z-Order，相应地设置最大/最小Z-Order。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151756850.jpg)
开始之前，您需要选择控件侧栏上的``Polygon``并选择正确的标签。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151934875.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)
- 单击``Shape``进入绘图模式。
  有两种绘制多边形的方法：通过单击创建点，或者在按住“Shift”的同时在屏幕上拖动鼠标。

| 点击点 | 按住Shift+拖动 |
| -- | -- |
| ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802152026101.gif) | ![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080215204832.gif) |

- 未按“Shift”时，您可以放大/缩小（滚动鼠标滚轮时）和移动（单击鼠标滚轮并移动鼠标时），也可以通过右键单击删除上一个点。
- 按“N”完成形状。
- 创建多边形后，可以通过右键单击并选择“删除点”来移动或删除这些点或者在上下文菜单中按“Ctrl”键双击。

### Drawing using automatic borders

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-xVPM86Mr-1596171612075)(static/documentation/images/gif025_mapillary_vistas.gif)]

You can use auto borders when drawing a polygon. Using automatic borders allows you to automatically trace
the outline of polygons existing in the annotation.
- To do this, go to settings -> workspace tab and enable ``Automatic Bordering``
  or press ``Ctrl`` while drawing a polygon.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-ONmw5PTS-1596171612076)(static/documentation/images/image161.jpg)]

- Start drawing / editing a polygon.
- Points of other shapes will be highlighted, which means that the polygon can be attached to them.
- Define the part of the polygon path that you want to repeat.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-7qbhZXyO-1596171612079)(static/documentation/images/image157_mapillary_vistas.jpg)]

- Click on the first point of the contour part.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-rRyviGx0-1596171612080)(static/documentation/images/image158_mapillary_vistas.jpg)]

- Then click on any point located on part of the path. The selected point will be highlighted in purple.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-wcB3owkv-1596171612081)(static/documentation/images/image159_mapillary_vistas.jpg)]

- Сlick on the last point and the outline to this point will be built automatically.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-KUffn1b2-1596171612082)(static/documentation/images/image160_mapillary_vistas.jpg)]

Besides, you can set a fixed number of points in the ``Number of points`` field, then
drawing will be stopped automatically. To enable dragging you should right-click
inside the polygon and choose ``Switch pinned property``.

Below you can see results with opacity and black stroke:

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-GpBr65qx-1596171612083)(static/documentation/images/image064_mapillary_vistas.jpg)]

If you need to annotate small objects, increase ``Image Quality`` to
``95`` in ``Create task`` dialog for your convenience.

### Make AI polygon

Used to create a polygon semi-automatically.
- Before starting, you have to make sure that the ``Make AI polygon`` is selected.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-7C4hoVbm-1596171612084)(static/documentation/images/image114.jpg)]

- Click ``Shape`` to enter drawing mode. Now you can start annotating the necessary area.
  A shape must consist of 4 points minimum. You can set a fixed number of points in the ``Number of points`` field,
  then drawing will be stopped automatically. You can zoom in/out and move while drawing.
- Press ``N`` again to finish marking the area. At the end of Auto Segmentation,
  a shape is created and you can work with it as a polygon.

  [外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-71Ym3qTH-1596171612085)(static/documentation/images/gif009_detrac.gif)]

### 编辑多边形

要编辑多边形，您必须双击按“Shift”键，它将打开多边形编辑器。
- 在那里，您可以创建新的点或删除多边形的一部分，使其与另一点上的直线闭合。
- 关闭多边形后，可以选择要离开的多边形部分。
- 您可以按“Esc”取消编辑。



![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807113102976.gif)

## 带多段线的标注

用于道路标记标注等。

在开始之前，您需要选择“折线”。您可以在“点数”字段中设置固定点数，绘图将自动停止。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151442163.jpg)

单击“形状”进入绘图模式。绘制折线有两种方法-您可以通过单击创建点，也可以在按住“Shift”的同时在屏幕上拖动鼠标来创建点。

When ``Shift`` isn't pressed, you can zoom in/out (when scrolling the mouse wheel)
and move (when clicking the mouse wheel and moving the mouse), you can delete
previous points by right-clicking on it. Press ``N`` again to complete the shape.
You can delete a point by double-clicking on it with pressed ``Ctrl`` or right-clicking on a point
and selecting ``Delete point``. Double-click with pressed ``Shift`` will open a polyline editor.
There you can create new points(by clicking or dragging) or delete part of a polygon closing
the red line on another point. Press ``Esc`` to cancel editing.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151423515.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

## 点标注

### 形状模式中的点

用于人脸、地标标注等。

开始之前，您需要选择 ``Points``. 如果需要，可以在 ``Number of points`` 字段, 然后绘图将自动停止。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151405645.jpg)

点击``Shape`` 进入绘图模式。现在您可以开始标注所需的区域。点自动分组-所有点将被视为在每个起点和终点之间链接。

按``N`` 再次完成标记区域。可以通过双击并按下来``Ctrl``删除点或者右键单击一个点并选择 ``Delete point``. 按``Shift``键双击将打开点形状编辑器。在那里，可以将新点添加到现有形状中。可以在绘图时放大/缩小（滚动鼠标滚轮时）和移动（单击鼠标滚轮并移动鼠标时）。可以在绘制对象后拖动该对象，并在完成对象后更改各个点的位置。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151347261.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


### 单点线性插值

可以对点使用线性插值来标注移动对象：

1.  开始之前，请选择 ``Points``.
1.  线性插值仅适用于一个点，因此需要设置``Number of points`` 为1.
1.  之后，选择 ``Track``.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151330336.jpg)


1.  点击``Track`` 完成图形后，单击该模式将自动创建一个点。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151310714.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

1.  向前移动几帧并将点移动到所需位置，这样您将创建一个关键帧，中间帧将自动绘制。可以像处理插值轨迹一样处理该对象：可以使用“Outside”隐藏它，在关键帧周围移动等。![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151252180.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


1.  这样你就可以用“点”得到线性插值。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080215123148.gif)


## 长方体标注

它被用来标注三维物体，如汽车、盒子等……
目前，该特征支持单点透视，并具有垂直边与边完全平行的约束。

### 创建长方体

在开始之前，你必须确保长方体被选中，并选择一种绘图方法 ”from rectangle” 或者 “by 4 points”.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802151214103.jpg)

#### 四点画法

选择“按4点”绘制方法，然后单击“形状”进入绘图模式。画长方体的方法有很多种。
您可以通过放置4个点来绘制长方体，然后绘图将自动完成。前3个点确定长方体的平面，而最后一个点确定该平面的深度。对于前3个点，建议只绘制两个最近的侧面以及顶面和底面。

几个例子：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802150917720.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

### 从矩形画长方体

选择绘图方法“from rectangle” 然后单击“形状”进入绘图模式。使用矩形方法绘制时，必须使用边界选择对象的前平面盒子。那个生成的长方体的深度和透视图可以编辑。

例子：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802150858184.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


### 编辑长方体
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080215084057.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


可以通过多种方式编辑长方体：拖动点、拖动某些面或拖动平面。首先请注意，有一张脸只画了灰色的线条，让我们称之为前脸。

只需在前脸后面拖动形状，就可以移动长方体。
长方体可以通过拖动边中间的点来扩展。
也可以通过拖动顶点处的点来上下扩展长方体。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802150821809.gif)


要使用透视效果进行绘制，应假定正面离摄影机最近。若要开始，只需在按住``Shift``时拖动不在灰色/正面上的顶点上的点。然后可以像往常一样编辑长方体。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802150800441.gif)


如果要重置透视效果，可以右键单击长方体，然后选择 ``Reset perspective`` 回到正长方体。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802150738232.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


灰色面的位置可以与相邻的可见侧面交换。你可以通过右击长方体并选择 ``Switch perspective orientation``。请注意，这也将重置透视效果。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802150720528.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

长方体的某些面也可以编辑，这些面是：左、右、背面，相对于灰色面。只需拖动面，就可以独立于长方体的其他部分移动面。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802150631997.gif)

也可以在“轨迹”模式下使用长方体，类似于“轨迹模式”中的矩形 ([basics](#track-mode-basics) and [advanced](#track-mode-advanced))

## 带标记的标注
用于标注框架，工作区中没有形状。在开始标记之前，请确保已选择。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113700502.jpg)

单击标记以创建。您只能在侧栏上使用Tag。可以使用lock函数更改标签和属性。“操作”菜单中提供了其他功能，如传播、复制和删除。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802150438777.jpg)


## 自动标注

自动标注用于创建初步标注。要使用自动标注，您需要一个DL模型。您可以使用主模型或用户上载的模型。
您可以在“models”部分找到可用模型的列表。

1.  要启动自动标注，应打开仪表板并查找要标注的任务。
    然后单击“操作”按钮，从下拉菜单中选择“自动批注”选项。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802113925617.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


1.  在对话框窗口中，选择所需的模型。DL模型是为特定的标签创建的，例如，十字路口模型是使用位于高速公路上方的摄像机的镜头进行教学的，对于具有类似摄像机角度的任务，最好使用此模型。
    如果需要，请选中“清除旧注释”复选框。
	调整标签，使任务标签与DL模型的标签相对应。
    例如，让我们考虑一个任务，其中您必须标注标签“car”和“person”。
    您应该将模型中的“person”标签连接到任务中的“person”标签。
    至于“汽车”标签，你应该选择模型中最合适的标签——“车辆”标签。
    此任务只需要对汽车进行注释，选择“车辆”标签意味着对所有车辆进行注释，在这种情况下，使用自动注释将帮助您更快地完成任务。
    单击“提交”开始自动标注过程。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802114503788.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)

1.  在运行时-您可以看到完成的百分比，您可以单击“取消”按钮取消自动批注。![在这里插入图片描述](https://img-blog.csdnimg.cn/2020080211444943.jpg)


1.  自动批注的最终结果是带有单独矩形（或其他形状）的批注
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802114430432.gif)

1.  可以通过删除误报、添加未标记的对象以及使用“ReID merge”函数合并到轨迹来编辑分离的边界框。单击菜单中的“ReID merge”按钮。
    您可以使用默认设置 (有关详细信息，请单击 [here](cvat/apps/reid/README.md)).
    要启动合并过程，请单击 ``Merge``。轨道的每一帧都是一个关键帧。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802114412309.jpg)

1.  您可以使用“Split”和“Merge”函数删除误报和编辑跟踪。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802114353890.gif)



## 形状分组

此功能允许我们对多个形状进行分组。

您可以使用“分组形状”按钮或快捷方式：
- ``G`` — 在组模式下开始选择/结束选择
- ``Esc`` — 关闭组模式
- ``Shift+G`` — 重置选定形状的组

您可以通过单击形状或选择区域来选择形状。

分组形状将在转储批注中包含“group”id“字段。

也可以将颜色分布从实例（默认）切换到组。
您必须切换“按组颜色”复选框。

Shapes that don't have ``group_id``, will be highlighted in white.
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802114314865.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802114331845.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


## 过滤器


![在这里插入图片描述](https://img-blog.csdnimg.cn/20200802114122722.jpg)

使用此功能的原因如下：

1. 使用过滤器时，与过滤器不匹配的对象将被隐藏。
1. 在具有感兴趣对象的帧之间快速导航。Use ``Left Arrow`` / ``Right Arrow`` keys for this purpose. If there are no objects matching the filter,
the will go to arrows the previous/next frames which contains any objects.
1. 该列表包含常用和最近使用的筛选器。

要使用该函数，只需在“Filter”文本中指定一个值就足够了字段并按“回车”键。之后，将应用过滤器。

---
**Supported properties:**

| Properties  | Supported values                  | Description                                                       |
|--           |--                                 | --                                                                |
| ``width``   |number of px or ``height``         | shape width                                                       |
| ``height``  |number of px or ``width``          | shape height                                                      |
| ``label``   |``"text"``  or ``["text"]``        | label name                                                        |
| ``serverID``| number                            | ID of the object on server <br> (You can find out by forming a link to the object through the Action menu)|
| ``clientID``| number                            | ID of the object in your client (indicated on the objects sidebar)|
| ``type``    |``"shape"``, ``"track"``, ``"tag"``| type of object                                                    |
| ``shape``   |``"rectangle"``,``"polygon"``, <br>``"polyline"``,``"points"``| type of shape                          |
| ``occluded``|``true`` or ``false``              | occluded properties                                               |
| ``attr``    |``"text"``                         | attribute name                                                    |

**Supported operators:**

``==`` - Equally; ``!=`` - Not equal; ``>``  - More; ``>=`` - More or equal; ``<``  - Less; ``<=`` - Less or equal;
``()`` - Brackets; ``&``  - And; ``|``- Or.

If you have double quotes in your query string, please escape them using backslash: ``\"`` (see the latest example)
All properties and values are case-sensitive. CVAT uses json queries to perform search.

---

**Examples filters**

- ``label=="car" | label==["road sign"]`` - this filter will show only objects with the car or road sign label.
- ``shape == "polygon"`` - this filter will show only polygons.
- ``width >= height`` - this filter will show only those objects whose width will be greater than
  or equal to the height.
- ``attr["color"] == "black"`` - this filter will show objects whose color attribute is black.
- ``clientID == 50`` - this filter will show the object with id equal to 50 (e.g. rectangle 50).
- ``(label=="car" & attr["parked"]==true) | (label=="pedestrian" & width > 150)`` - this filter will display objects
  with the “car” label and the parking attribute enabled or objects with the “pedestrian” label with a height of more
  than 150 pixels
- ``(( label==["car \"mazda\""]) | (attr["parked"]==true & width > 150)) & (height > 150 & (clientID == serverID)))`` -
  This filter will show objects with the label "car" mazda "" or objects that have the parked attribute turned on
  and have a width of more than 150 pixels, and those listed should have a height of more than 150 pixels
  and their clientID is equal to serverID.

**筛选器历史记录**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807111044808.jpg)

您可以添加以前输入的过滤器并将它们组合起来。为此，单击输入字段，将打开以前输入的过滤器列表。单击过滤器以将其添加到输入字段中。组合过滤器与“或”运算符一起出现。

---

## 分析

如果您的CVAT实例是使用analytics支持创建的，则可以在仪表板中按“analytics”按钮，分析和日志将在新选项卡中打开。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807110850773.jpg)
分析可以让你看到每个用户在每个任务上花费了多少时间，以及他们在任何时间范围内做了多少工作。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807110924674.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)
它还有一个活动图，可以根据显示的用户数和时间范围进行修改。![在这里插入图片描述](https://img-blog.csdnimg.cn/20200807110808521.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzMzNjI4MQ==,size_16,color_FFFFFF,t_70)


## 快捷键

许多UI元素都有快捷方式提示。将指针指向必需的元素以查看它。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200801124233363.jpg#pic_center)


| 快捷键 | 功能 |
|-|-|
|  | 主要功能 |
| ``F2`` | 打开/隐藏可用快捷键列表 |
| ``F3`` | 转到“设置”页或返回 |
| ``Ctrl+S`` | 转到“设置”页或返回 |
| ``Ctrl+Z`` | 取消与对象相关的最新操作 |
| ``Ctrl+Shift+Z`` or ``Ctrl+Y`` | 取消撤消操作 |
| Hold ``Mouse Wheel`` | 移动图像框（例如，在绘图时） |
|                                | _Player_                                                                        |
| ``F``                          | Go to the next frame                                                            |
| ``D``                          | Go to the previous frame                                                        |
| ``V``                          | Go forward with a step                                                          |
| ``C``                          | Go backward with a step                                                         |
| ``Right``                      | Search the next frame that satisfies to the filters <br> or next frame which contain any objects|
| ``Left``                       | Search the previous frame that satisfies to the filters <br> or previous frame which contain any objects|
| ``Space``                      | Start/stop automatic changing frames                                            |
| `` ` `` or ``~``               | Focus on the element to change the current frame                                |
|                                | _Modes_                                                                         |
| ``N``                          | Repeat the latest procedure of drawing with the same parameters                 |
| ``M``                          | Activate or deactivate mode to merging shapes                                   |
| ``G``                          | Activate or deactivate mode to grouping shapes                                  |
| ``Shift+G``                    | Reset group for selected shapes (in group mode)                                 |
| ``Esc``                        | Cancel any active canvas mode                                                   |
|                                | _Image operations_                                                              |
| ``Ctrl+R``                     | Change image angle (add 90 degrees)                                             |
| ``Ctrl+Shift+R``               | Change image angle (substract 90 degrees)                                       |
| ``Shift+B+=``                  | Increase brightness level for the image                                         |
| ``Shift+B+-``                  | Decrease brightness level for the image                                         |
| ``Shift+C+=``                  | Increase contrast level for the image                                           |
| ``Shift+C+-``                  | Decrease contrast level for the image                                           |
| ``Shift+S+=``                  | Increase saturation level for the image                                         |
| ``Shift+S+-``                  | Increase contrast level for the image                                           |
| ``Shift+G+=``                  | Make the grid more visible                                                      |
| ``Shift+G+-``                  | Make the grid less visible                                                      |
| ``Shift+G+Enter``              | Set another color for the image grid                                            |
|                                | _Operations with objects_                                                       |
| ``Ctrl``                       | Switch automatic bordering for polygons and polylines during drawing/editing    |
| Hold ``Ctrl``                  | When the shape is active and fix it                                             |
| ``Ctrl+Double-Click`` on point | Deleting a point (used when hovering over a point of polygon, polyline, points) |
| ``Shift+Double-Click`` on point| Editing a shape (used when hovering over a point of polygon, polyline or points)|
| ``Right-Click`` on shape       | Display of an object element from objects sidebar                               |
| ``T+L``                        | Change locked state for all objects in the sidebar                              |
| ``L``                          | Change locked state for an active object                                        |
| ``T+H``                        | Change hidden state for objects in the sidebar                                  |
| ``H``                          | Change hidden state for an active object                                        |
| ``Q`` or ``/``                 | Change occluded property for an active object                                   |
| ``Del`` or ``Shift+Del``       | Delete an active object. Use shift to force delete of locked objects            |
| ``-`` or ``_``                 | Put an active object "farther" from the user (decrease z axis value)            |
| ``+`` or ``=``                 | Put an active object "closer" to the user (increase z axis value)               |
| ``Ctrl+C``                     | Copy shape to CVAT internal clipboard                                           |
| ``Ctrl+V``                     | Paste a shape from internal CVAT clipboard                                      |
| Hold ``Ctrl`` while pasting    | When pasting shape from the buffer for multiple pasting.                        |
| ``Crtl+B``                     | Make a copy of the object on the following frames                               |
|                                | _Operations are available only for track_                                       |
| ``K``                          | Change keyframe property for an active track                                    |
| ``O``                          | Change outside property for an active track                                     |
| ``R``                          | Go to the next keyframe of an active track                                      |
| ``E``                          | Go to the previous keyframe of an active track                                  |
|                                | _Attribute annotation mode_                                                     |
| ``Up Arrow``                   | Go to the next attribute (up)                                                   |
| ``Down Arrow``                 | Go to the next attribute (down)                                                 |
| ``Tab``                        | Go to the next annotated object in current frame                                |
| ``Shift+Tab``                  | Go to the previous annotated object in current frame                            |
| ``<number>``                   | Assign a corresponding value to the current attribute                           |
