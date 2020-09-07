## 身份验证

### 登录

**Request URL**: http://alexking.site:8080/api/v1/auth/login

**Request Method**: POST

**Form Data**:

```json
{
	"username": "",
	"password": ""
}
```

**Response**：Token Key

```json
	{"key":"e7b5b0363cae7fe9c455636d6b21fc09f526aff0"}
```

### 注销

**Request URL**: http://alexking.site:8080/api/v1/auth/logout

**Request Method**: POST

### 注册

**Request URL**: http://alexking.site:8080/api/v1/auth/register

**Request Method**: POST

**Form Data**:

```json
	{
	    "username":"",
	    "first_name":"",
	    "last_name":"",
	    "email":"",
	    "password1":"",
	    "password2":""
	}
```

### 用户

返回当前已被授权的用户的实例信息。

**Request URL**: http://alexking.site:8080/api/v1/users/self

**Request Method**: GET

**Response**：

```json
    {
        "url": "http://alexking.site:8080/api/v1/users/1",
        "id": 1,
        "username": "root",
        "first_name": "",
        "last_name": "",
        "email": "2426671397@qq.com",
        "groups": [
            "admin"
        ],
        "is_staff": true,
        "is_superuser": true,
        "is_active": true,
        "last_login": "2020-08-03T09:49:09.829369Z",
        "date_joined": "2020-08-03T09:49:00.616248Z"
    }
```

## 任务

![](http://assets.processon.com/chart_image/5f2a37d907912906dbf8edab.png)

### 创建任务

1. 上传 Task 基本信息

**Request URL**: http://alexking.site:8080/api/v1/tasks

**Request Method**: POST

**Request Data**：

```json
    {
        "name":"testCreate",
        "labels":[
            {
                "name":"label1",
                "attributes":[
                    {
                        "name":"select",
                        "mutable":false,
                        "input_type":"select",
                        "default_value":"select",
                        "values":[
                            "select"
                        ]
                    }
                ]
            },
            {
                "name":"label2",
                "attributes":[
                    {
                        "name":"checkbox",
                        "mutable":false,
                        "input_type":"checkbox",
                        "default_value":"false",
                        "values":[
                            "false"
                        ]
                    }
                ]
            },
            {
                "name":"label3",
                "attributes":[
                    {
                        "name":"text",
                        "mutable":true,
                        "input_type":"text",
                        "default_value":"text",
                        "values":[
                            "text"
                        ]
                    }
                ]
            }
        ],
        "z_order":false
    }
```

**Response**：

```json
    {
        "url":"http://alexking.site:8080/api/v1/tasks/4",
        "id":4,
        "name":"testCreate",
        "mode":"",
        "owner":3,
        "assignee":null,
        "bug_tracker":"",
        "created_date":"2020-08-05T14:14:44.636034+08:00",
        "updated_date":"2020-08-05T14:14:44.636090+08:00",
        "overlap":null,
        "segment_size":0,
        "z_order":false,
        "status":"annotation",
        "labels":[
            {
                "id":6,
                "name":"label1",
                "attributes":[
                    {
                        "id":6,
                        "name":"select",
                        "mutable":false,
                        "input_type":"select",
                        "default_value":"select",
                        "values":[
                            "select"
                        ]
                    }
                ]
            },
            {
                "id":7,
                "name":"label2",
                "attributes":[
                    {
                        "id":7,
                        "name":"checkbox",
                        "mutable":false,
                        "input_type":"checkbox",
                        "default_value":"false",
                        "values":[
                            "false"
                        ]
                    }
                ]
            },
            {
                "id":8,
                "name":"label3",
                "attributes":[
                    {
                        "id":8,
                        "name":"text",
                        "mutable":true,
                        "input_type":"text",
                        "default_value":"text",
                        "values":[
                            "text"
                        ]
                    }
                ]
            }
        ],
        "segments":[

        ],
        "project":null
    }
```

2. 上传 Task 数据集

**Request URL**: http://alexking.site:8080/api/v1/tasks/:id/data

**Request Method**: POST

**Response**：

```json
    {
        "chunk_size":null,
        "size":0,
        "image_quality":70,
        "start_frame":0,
        "stop_frame":0,
        "frame_filter":"",
        "compressed_chunk_type":"imageset",
        "original_chunk_type":"imageset",
        "client_files":[
            "000000001296.jpg",
            "000000000776.jpg",
            "000000000285.jpg"
        ],
        "server_files":[

        ],
        "remote_files":[

        ],
        "use_zip_chunks":false
    }
```

3. 选择共享数据集

**Request URL**: http://alexking.site:8080/api/v1/server/share?directory=path

例如：path = /car/

**Request Method**: GET

**Request Data**：

    directory: /car/

**Response**：

```json
[
    {
        "name":"car5.jpg",
        "type":"REG"
    },
    {
        "name":"car3.jpg",
        "type":"REG"
    }
]
```

4. 获取任务创建状态

**Request URL**: http://alexking.site:8080/api/v1/tasks/:id/status

**Request Method**: GET

**Response**：

    {"state":"Finished","message":""}

**Choices**:

    "Queued"：队列中
    "Started"：开始创建
    "Finished"：创建成功
    "Failed"：创建失败

### 任务列表

根据查询参数返回分页的任务列表（每页10个任务）

**Request URL**: http://alexking.site:8080/api/v1/tasks?page_size=10&page=1

**Request Method**: GET

**Response**：

```json
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "url": "http://alexking.site:8080/api/v1/tasks/2",
                "id": 2,
                "name": "test2",
                "mode": "annotation",
                "owner": 1,
                "assignee": null,
                "bug_tracker": "",
                "created_date": "2020-08-04T05:02:23.690371Z",
                "updated_date": "2020-08-04T05:02:23.690406Z",
                "overlap": 0,
                "segment_size": 0,
                "z_order": false,
                "status": "annotation",
                "labels": [
                    {
                        "id": 2,
                        "name": "name",
                        "attributes": [
                            {
                                "id": 2,
                                "name": "name",
                                "mutable": false,
                                "input_type": "select",
                                "default_value": "name",
                                "values": [
                                    "name"
                                ]
                            }
                        ]
                    }
                ],
                "segments": [
                    {
                        "start_frame": 0,
                        "stop_frame": 2,
                        "jobs": [
                            {
                                "url": "http://alexking.site:8080/api/v1/jobs/2",
                                "id": 2,
                                "assignee": null,
                                "status": "annotation"
                            }
                        ]
                    }
                ],
                "project": null,
                "data_chunk_size": 72,
                "data_compressed_chunk_type": "imageset",
                "data_original_chunk_type": "imageset",
                "size": 3,
                "image_quality": 70,
                "data": 2
            },
            {
                "url": "http://alexking.site:8080/api/v1/tasks/1",
                "id": 1,
                "name": "test",
                "mode": "annotation",
                "owner": 1,
                "assignee": null,
                "bug_tracker": "",
                "created_date": "2020-08-04T04:37:17.438341Z",
                "updated_date": "2020-08-04T04:37:17.438365Z",
                "overlap": 0,
                "segment_size": 0,
                "z_order": false,
                "status": "annotation",
                "labels": [
                    {
                        "id": 1,
                        "name": "test",
                        "attributes": [
                            {
                                "id": 1,
                                "name": "Name",
                                "mutable": false,
                                "input_type": "select",
                                "default_value": "Name",
                                "values": [
                                    "Name"
                                ]
                            }
                        ]
                    }
                ],
                "segments": [
                    {
                        "start_frame": 0,
                        "stop_frame": 2,
                        "jobs": [
                            {
                                "url": "http://alexking.site:8080/api/v1/jobs/1",
                                "id": 1,
                                "assignee": null,
                                "status": "annotation"
                            }
                        ]
                    }
                ],
                "project": null,
                "data_chunk_size": 72,
                "data_compressed_chunk_type": "imageset",
                "data_original_chunk_type": "imageset",
                "size": 3,
                "image_quality": 70,
                "data": 1
            }
        ]
    }
```

### 修改任务

1. 获取 Task 详细信息

**Request URL**: http://alexking.site:8080/git/repository/get/:id

**Request Method**: GET

**Response**：

    {
        "url":{
            "value":null
        },
        "status":{
            "value":null,
            "error":null
        }
    }

2. 获取用户列表（Assign）

**Request URL**: http://alexking.site:8080/api/v1/users?page_size=all

**Request Method**: GET

**Response**：

```json
    {
        "count":9,
        "next":null,
        "previous":null,
        "results":[
            {
                "url":"http://alexking.site:8080/api/v1/users/1",
                "id":1,
                "username":"root",
                "first_name":"",
                "last_name":"",
                "email":"2426671397@qq.com",
                "groups":[
                    "admin"
                ],
                "is_staff":true,
                "is_superuser":true,
                "is_active":true,
                "last_login":"2020-08-03T17:49:09.829369+08:00",
                "date_joined":"2020-08-03T17:49:00.616248+08:00"
            },
            {
                "url":"http://alexking.site:8080/api/v1/users/3",
                "id":3,
                "username":"Alex",
                "first_name":"",
                "last_name":"",
                "email":"alex18812649207@gmail.com",
                "groups":[
                    "admin"
                ],
                "is_staff":true,
                "is_superuser":true,
                "is_active":true,
                "last_login":"2020-08-06T11:37:24.635039+08:00",
                "date_joined":"2020-08-04T11:44:02.974034+08:00"
            },
            {
                "url":"http://alexking.site:8080/api/v1/users/16",
                "id":16,
                "username":"dabai",
                "first_name":"",
                "last_name":"",
                "email":"dabai@qq.com",
                "groups":[

                ],
                "is_staff":false,
                "is_superuser":false,
                "is_active":true,
                "last_login":"2020-08-05T12:22:13.305121+08:00",
                "date_joined":"2020-08-05T12:22:13.135044+08:00"
            }
        ]
    }
```

3. 修改 Task 的信息（Name、Label、Assign）

**Request URL**: http://alexking.site:8080/api/v1/tasks/:id

**Request Method**: PATCH

**Request Data**：

```json
    {
        "assignee":12,
        "name":"test",
        "bug_tracker":"",
        "z_order":false,
        "labels":[
            {
                "name":"label1",
                "attributes":[
                    {
                        "name":"select",
                        "mutable":false,
                        "input_type":"select",
                        "default_value":"select",
                        "values":[
                            "select"
                        ],
                        "id":6
                    }
                ],
                "id":6
            },
            {
                "name":"label2",
                "attributes":[
                    {
                        "name":"checkbox",
                        "mutable":false,
                        "input_type":"checkbox",
                        "default_value":"false",
                        "values":[
                            "false"
                        ],
                        "id":7
                    }
                ],
                "id":7
            },
            {
                "name":"label3",
                "attributes":[
                    {
                        "name":"text",
                        "mutable":true,
                        "input_type":"text",
                        "default_value":"text",
                        "values":[
                            "text"
                        ],
                        "id":8
                    }
                ],
                "id":8
            },
            {
                "name":"label4",
                "attributes":[
                    {
                        "name":"number",
                        "mutable":false,
                        "input_type":"number",
                        "default_value":"0",
                        "values":[
                            "0",
                            "100",
                            "1"
                        ],
                        "id":9
                    }
                ],
                "id":9
            },
            {
                "name":"label5",
                "attributes":[
                    {
                        "name":"radio",
                        "mutable":false,
                        "input_type":"radio",
                        "default_value":"radio",
                        "values":[
                            "radio"
                        ]
                    }
                ]
            }
        ]
    }
```

4. 修改 Task 的 job Assign

**Request URL**: http://alexking.site:8080/api/v1/jobs/:id

**Request Method**: PATCH

**Request Data**：

    {
        "status":"annotation",
        "assignee":14
    }

**Response**：

```json
    {
        "url":"http://alexking.site:8080/api/v1/jobs/4",
        "id":4,
        "assignee":14,
        "status":"annotation",
        "start_frame":0,
        "stop_frame":2,
        "task_id":4
    }
```

5. 重新获取 Task 详细信息

**Request URL**: http://alexking.site:8080/api/v1/tasks?page_size=10&id=:id

**Request Method**: GET

**Request Data**：

```json
    {
        "count":1,
        "next":null,
        "previous":null,
        "results":[
            {
                "url":"http://alexking.site:8080/api/v1/tasks/4",
                "id":4,
                "name":"test",
                "mode":"annotation",
                "owner":3,
                "assignee":12,
                "bug_tracker":"",
                "created_date":"2020-08-05T14:14:44.636034+08:00",
                "updated_date":"2020-08-05T14:14:44.636090+08:00",
                "overlap":0,
                "segment_size":0,
                "z_order":false,
                "status":"annotation",
                "labels":[
                    {
                        "id":6,
                        "name":"label1",
                        "attributes":[
                            {
                                "id":6,
                                "name":"select",
                                "mutable":false,
                                "input_type":"select",
                                "default_value":"select",
                                "values":[
                                    "select"
                                ]
                            }
                        ]
                    },
                    {
                        "id":7,
                        "name":"label2",
                        "attributes":[
                            {
                                "id":7,
                                "name":"checkbox",
                                "mutable":false,
                                "input_type":"checkbox",
                                "default_value":"false",
                                "values":[
                                    "false"
                                ]
                            }
                        ]
                    },
                    {
                        "id":8,
                        "name":"label3",
                        "attributes":[
                            {
                                "id":8,
                                "name":"text",
                                "mutable":true,
                                "input_type":"text",
                                "default_value":"text",
                                "values":[
                                    "text"
                                ]
                            }
                        ]
                    },
                    {
                        "id":9,
                        "name":"label4",
                        "attributes":[
                            {
                                "id":9,
                                "name":"number",
                                "mutable":false,
                                "input_type":"number",
                                "default_value":"0",
                                "values":[
                                    "0",
                                    "100",
                                    "1"
                                ]
                            }
                        ]
                    },
                    {
                        "id":10,
                        "name":"label5",
                        "attributes":[
                            {
                                "id":10,
                                "name":"radio",
                                "mutable":false,
                                "input_type":"radio",
                                "default_value":"radio",
                                "values":[
                                    "radio"
                                ]
                            }
                        ]
                    }
                ],
                "segments":[
                    {
                        "start_frame":0,
                        "stop_frame":2,
                        "jobs":[
                            {
                                "url":"http://alexking.site:8080/api/v1/jobs/4",
                                "id":4,
                                "assignee":14,
                                "status":"annotation"
                            }
                        ]
                    }
                ],
                "project":null,
                "data_chunk_size":72,
                "data_compressed_chunk_type":"imageset",
                "data_original_chunk_type":"imageset",
                "size":3,
                "image_quality":70,
                "data":4
            }
        ]
    }
```

## 标注

### 标注工作台

![](http://assets.processon.com/chart_image/5f349fe463768942471382fe.png)

1. 创建标注日志

**Request URL**: http://alexking.site:8080/api/v1/server/logs

**Request Method**: POST

**Request Data**：

```json
[
    {
        "name":"Send user activity",
        "time":"2020-08-13T01:45:53.569Z",
        "client_id":"642862",
        "is_active":true,
        "payload":{
            "working_time":264149
        }
    }
]
```

**Response**：

```json
[
    {
        "client_id":642862,
        "name":"Send user activity",
        "time":"2020-08-13T09:45:53.569000+08:00",
        "payload":{
            "working_time":264149
        },
        "is_active":true
    }
]
```

2. 获取待标注信息列表

**Request URL**: http://alexking.site:8080/api/v1/tasks/19/data/meta

**Request Method**: GET

**Response**：

```json
{
    "chunk_size":72,
    "size":8,
    "image_quality":70,
    "start_frame":0,
    "stop_frame":7,
    "frame_filter":"",
    "frames":[
        {
            "width":584,
            "height":328,
            "name":"car1.jpg"
        },
        {
            "width":1280,
            "height":919,
            "name":"car2.jpg"
        },
        {
            "width":434,
            "height":326,
            "name":"car3.jpg"
        },
        {
            "width":1600,
            "height":1000,
            "name":"car4.jpg"
        },
        {
            "width":264,
            "height":198,
            "name":"car5.jpg"
        },
        {
            "width":634,
            "height":357,
            "name":"car6.jpg"
        },
        {
            "width":1024,
            "height":768,
            "name":"car7.jpg"
        },
        {
            "width":516,
            "height":387,
            "name":"car8.jpg"
        }
    ]
}
```

3. 获取待标注详细信息压缩包

**Request URL**: http://alexking.site:8080/api/v1/tasks/19/data?type=chunk&number=0&quality=compressed

**Request Method**: GET

4. 前端通过unzip_imgs.worker.js解压待标注文件

5. 获取当前标注情况

**Request URL**: http://alexking.site:8080/api/v1/jobs/:id/annotations

**Request Method**: GET

**Response**：

```json
    {
        "version":18,
        "tracks":[

        ],
        "shapes":[
            {
                "type":"rectangle",
                "occluded":false,
                "z_order":0,
                "points":[
                    38.7734375,
                    52.267578125,
                    537.5498657226562,
                    324.32745361328125
                ],
                "id":5,
                "frame":0,
                "label_id":11,
                "group":0,
                "attributes":[
                    {
                        "spec_id":11,
                        "value":"BMW"
                    }
                ]
            }
        ],
        "tags":[

        ]
    }
```


6. 保存当前标注数据

    首先创建保存任务

**Request URL**: http://alexking.site:8080/api/v1/jobs/5/annotations?action=create

**Request Method**: GET

**Request Data**：

```json
    {
        "shapes":[
            {
                "type":"rectangle",
                "occluded":false,
                "z_order":0,
                "points":[
                    235.4541015625,
                    589.7822265625,
                    1361.490478515625,
                    995.818603515625
                ],
                "attributes":[
                    {
                        "spec_id":"11",
                        "value":""
                    }
                ],
                "frame":3,
                "label_id":11,
                "group":0
            }
        ],
        "tracks":[

        ],
        "tags":[

        ],
        "version":26
    }
```

**Response**：

```json
    {
        "version":28,
        "tracks":[

        ],
        "shapes":[
            {
                "type":"rectangle",
                "occluded":false,
                "z_order":0,
                "points":[
                    235.4541015625,
                    589.7822265625,
                    1361.490478515625,
                    995.818603515625
                ],
                "id":10,
                "frame":3,
                "label_id":11,
                "group":0,
                "attributes":[
                    {
                        "spec_id":11,
                        "value":""
                    }
                ]
            }
        ],
        "tags":[

        ]
    }
```

    然后走一遍升级

**Request URL**: http://alexking.site:8080/api/v1/jobs/5/annotations?action=update

**Request Method**: PATCH

**Request Data**：

```json
    {
        "shapes":[
            {
                "type":"rectangle",
                "occluded":false,
                "z_order":0,
                "points":[
                    47.10546875,
                    232.705078125,
                    991.9782104492188,
                    549.2141723632812
                ],
                "attributes":[
                    {
                        "spec_id":"11",
                        "value":"123"
                    }
                ],
                "id":9,
                "frame":6,
                "label_id":11,
                "group":0
            }
        ],
        "tracks":[

        ],
        "tags":[

        ],
        "version":28
    }
```

**Response**：

```json
{
    "version":29,
    "tracks":[

    ],
    "shapes":[
        {
            "type":"rectangle",
            "occluded":false,
            "z_order":0,
            "points":[
                47.10546875,
                232.705078125,
                991.9782104492188,
                549.2141723632812
            ],
            "id":9,
            "frame":6,
            "label_id":11,
            "group":0,
            "attributes":[
                {
                    "spec_id":11,
                    "value":"123"
                }
            ]
        }
    ],
    "tags":[

    ]
}
```

    如果有删除的数据则走删除API

**Request URL**: http://alexking.site:8080/api/v1/jobs/7/annotations?action=delete

**Request Method**: PATCH

**Request Data**：

```json
{"shapes":[],"tracks":[],"tags":[],"version":2}
```

**Response**：

```json
{"tags":[],"tracks":[],"shapes":[],"version":3}
```

7. 创建日志文件

**Request URL**: http://alexking.site:8080/api/v1/server/logs

**Request Method**: POST

**Request Data**：

```json
[
    {
        "name":"Load job",
        "time":"2020-08-13T01:45:53.569Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "duration":5209,
            "frame count":8,
            "track count":0,
            "object count":0,
            "box count":0,
            "polygon count":0,
            "polyline count":0,
            "points count":0,
            "cuboids count":0,
            "tag count":0
        }
    },
    {
        "name":"Fit image",
        "time":"2020-08-13T01:45:58.799Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{

        }
    },
    {
        "name":"Draw object",
        "time":"2020-08-13T01:46:15.345Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "count":1,
            "duration":8960
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:46:19.895Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":30,
            "value":"gray",
            "object_id":1
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:46:23.889Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":31,
            "value":"YYB",
            "object_id":1
        }
    },
    {
        "name":"Change frame",
        "time":"2020-08-13T01:46:27.376Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "from":0,
            "to":1
        }
    },
    {
        "name":"Fit image",
        "time":"2020-08-13T01:46:27.409Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{

        }
    },
    {
        "name":"Draw object",
        "time":"2020-08-13T01:46:41.282Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "count":1,
            "duration":8449
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:46:45.854Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":30,
            "value":"gray",
            "object_id":2
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:46:49.256Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":31,
            "value":"006M",
            "object_id":2
        }
    },
    {
        "name":"Change frame",
        "time":"2020-08-13T01:46:54.744Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "from":1,
            "to":2
        }
    },
    {
        "name":"Fit image",
        "time":"2020-08-13T01:46:54.764Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{

        }
    },
    {
        "name":"Draw object",
        "time":"2020-08-13T01:47:12.884Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "count":1,
            "duration":14627
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:47:15.774Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":30,
            "value":"black",
            "object_id":3
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:47:21.073Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":31,
            "value":"no",
            "object_id":3
        }
    },
    {
        "name":"Change frame",
        "time":"2020-08-13T01:47:37.703Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "from":2,
            "to":3
        }
    },
    {
        "name":"Fit image",
        "time":"2020-08-13T01:47:37.723Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{

        }
    },
    {
        "name":"Draw object",
        "time":"2020-08-13T01:47:53.511Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "count":1,
            "duration":8503
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:47:56.567Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":30,
            "value":"black",
            "object_id":4
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:47:59.018Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":31,
            "value":"laosilaisi",
            "object_id":4
        }
    },
    {
        "name":"Change frame",
        "time":"2020-08-13T01:48:08.178Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "from":3,
            "to":4
        }
    },
    {
        "name":"Fit image",
        "time":"2020-08-13T01:48:08.206Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{

        }
    },
    {
        "name":"Draw object",
        "time":"2020-08-13T01:48:19.639Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "count":1,
            "duration":7425
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:48:22.541Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":30,
            "value":"gray",
            "object_id":5
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:48:24.391Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":31,
            "value":"no",
            "object_id":5
        }
    },
    {
        "name":"Change frame",
        "time":"2020-08-13T01:48:28.176Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "from":4,
            "to":5
        }
    },
    {
        "name":"Fit image",
        "time":"2020-08-13T01:48:28.192Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{

        }
    },
    {
        "name":"Draw object",
        "time":"2020-08-13T01:49:25.486Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "count":1,
            "duration":11673
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:49:28.996Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":30,
            "value":"gray",
            "object_id":6
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:49:31.169Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":31,
            "value":"no",
            "object_id":6
        }
    },
    {
        "name":"Change frame",
        "time":"2020-08-13T01:49:35.439Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "from":5,
            "to":6
        }
    },
    {
        "name":"Fit image",
        "time":"2020-08-13T01:49:35.462Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{

        }
    },
    {
        "name":"Draw object",
        "time":"2020-08-13T01:49:47.261Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "count":1,
            "duration":8645
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:49:50.318Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":30,
            "value":"gray",
            "object_id":7
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:49:52.123Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":31,
            "value":"no",
            "object_id":7
        }
    },
    {
        "name":"Change frame",
        "time":"2020-08-13T01:49:54.270Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "from":6,
            "to":7
        }
    },
    {
        "name":"Fit image",
        "time":"2020-08-13T01:49:54.288Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{

        }
    },
    {
        "name":"Draw object",
        "time":"2020-08-13T01:50:05.822Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "count":1,
            "duration":7752
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:50:08.976Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":30,
            "value":"gray",
            "object_id":8
        }
    },
    {
        "name":"Change attribute",
        "time":"2020-08-13T01:50:10.710Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "id":31,
            "value":"SUV",
            "object_id":8
        }
    },
    {
        "name":"Save job",
        "time":"2020-08-13T01:50:34.847Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "duration":285
        }
    },
    {
        "name":"Send task info",
        "time":"2020-08-13T01:50:35.133Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "frame count":8,
            "track count":8,
            "object count":8,
            "box count":8,
            "polygon count":0,
            "polyline count":0,
            "points count":0,
            "cuboids count":0,
            "tag count":0
        }
    },
    {
        "name":"Send user activity",
        "time":"2020-08-13T01:50:35.144Z",
        "client_id":"642862",
        "job_id":7,
        "task_id":19,
        "is_active":true,
        "payload":{
            "working_time":281470
        }
    }
]
```

**Response**：

```json
[
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Load job",
        "time":"2020-08-13T09:45:53.569000+08:00",
        "payload":{
            "points count":0,
            "object count":0,
            "cuboids count":0,
            "polyline count":0,
            "duration":5209,
            "frame count":8,
            "polygon count":0,
            "track count":0,
            "tag count":0,
            "box count":0
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Fit image",
        "time":"2020-08-13T09:45:58.799000+08:00",
        "payload":{

        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Draw object",
        "time":"2020-08-13T09:46:15.345000+08:00",
        "payload":{
            "duration":8960,
            "count":1
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:46:19.895000+08:00",
        "payload":{
            "value":"gray",
            "object_id":1,
            "id":30
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:46:23.889000+08:00",
        "payload":{
            "value":"YYB",
            "object_id":1,
            "id":31
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change frame",
        "time":"2020-08-13T09:46:27.376000+08:00",
        "payload":{
            "from":0,
            "to":1
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Fit image",
        "time":"2020-08-13T09:46:27.409000+08:00",
        "payload":{

        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Draw object",
        "time":"2020-08-13T09:46:41.282000+08:00",
        "payload":{
            "duration":8449,
            "count":1
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:46:45.854000+08:00",
        "payload":{
            "value":"gray",
            "object_id":2,
            "id":30
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:46:49.256000+08:00",
        "payload":{
            "value":"006M",
            "object_id":2,
            "id":31
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change frame",
        "time":"2020-08-13T09:46:54.744000+08:00",
        "payload":{
            "from":1,
            "to":2
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Fit image",
        "time":"2020-08-13T09:46:54.764000+08:00",
        "payload":{

        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Draw object",
        "time":"2020-08-13T09:47:12.884000+08:00",
        "payload":{
            "duration":14627,
            "count":1
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:47:15.774000+08:00",
        "payload":{
            "value":"black",
            "object_id":3,
            "id":30
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:47:21.073000+08:00",
        "payload":{
            "value":"no",
            "object_id":3,
            "id":31
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change frame",
        "time":"2020-08-13T09:47:37.703000+08:00",
        "payload":{
            "from":2,
            "to":3
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Fit image",
        "time":"2020-08-13T09:47:37.723000+08:00",
        "payload":{

        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Draw object",
        "time":"2020-08-13T09:47:53.511000+08:00",
        "payload":{
            "duration":8503,
            "count":1
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:47:56.567000+08:00",
        "payload":{
            "value":"black",
            "object_id":4,
            "id":30
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:47:59.018000+08:00",
        "payload":{
            "value":"laosilaisi",
            "object_id":4,
            "id":31
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change frame",
        "time":"2020-08-13T09:48:08.178000+08:00",
        "payload":{
            "from":3,
            "to":4
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Fit image",
        "time":"2020-08-13T09:48:08.206000+08:00",
        "payload":{

        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Draw object",
        "time":"2020-08-13T09:48:19.639000+08:00",
        "payload":{
            "duration":7425,
            "count":1
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:48:22.541000+08:00",
        "payload":{
            "value":"gray",
            "object_id":5,
            "id":30
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:48:24.391000+08:00",
        "payload":{
            "value":"no",
            "object_id":5,
            "id":31
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change frame",
        "time":"2020-08-13T09:48:28.176000+08:00",
        "payload":{
            "from":4,
            "to":5
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Fit image",
        "time":"2020-08-13T09:48:28.192000+08:00",
        "payload":{

        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Draw object",
        "time":"2020-08-13T09:49:25.486000+08:00",
        "payload":{
            "duration":11673,
            "count":1
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:49:28.996000+08:00",
        "payload":{
            "value":"gray",
            "object_id":6,
            "id":30
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:49:31.169000+08:00",
        "payload":{
            "value":"no",
            "object_id":6,
            "id":31
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change frame",
        "time":"2020-08-13T09:49:35.439000+08:00",
        "payload":{
            "from":5,
            "to":6
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Fit image",
        "time":"2020-08-13T09:49:35.462000+08:00",
        "payload":{

        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Draw object",
        "time":"2020-08-13T09:49:47.261000+08:00",
        "payload":{
            "duration":8645,
            "count":1
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:49:50.318000+08:00",
        "payload":{
            "value":"gray",
            "object_id":7,
            "id":30
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:49:52.123000+08:00",
        "payload":{
            "value":"no",
            "object_id":7,
            "id":31
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change frame",
        "time":"2020-08-13T09:49:54.270000+08:00",
        "payload":{
            "from":6,
            "to":7
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Fit image",
        "time":"2020-08-13T09:49:54.288000+08:00",
        "payload":{

        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Draw object",
        "time":"2020-08-13T09:50:05.822000+08:00",
        "payload":{
            "duration":7752,
            "count":1
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:50:08.976000+08:00",
        "payload":{
            "value":"gray",
            "object_id":8,
            "id":30
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Change attribute",
        "time":"2020-08-13T09:50:10.710000+08:00",
        "payload":{
            "value":"SUV",
            "object_id":8,
            "id":31
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Save job",
        "time":"2020-08-13T09:50:34.847000+08:00",
        "payload":{
            "duration":285
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Send task info",
        "time":"2020-08-13T09:50:35.133000+08:00",
        "payload":{
            "tag count":0,
            "object count":8,
            "cuboids count":0,
            "polyline count":0,
            "points count":0,
            "frame count":8,
            "polygon count":0,
            "track count":8,
            "box count":8
        },
        "is_active":true
    },
    {
        "job_id":7,
        "task_id":19,
        "client_id":642862,
        "name":"Send user activity",
        "time":"2020-08-13T09:50:35.144000+08:00",
        "payload":{
            "working_time":281470
        },
        "is_active":true
    }
]
```

### 下载标注结果

**Request URL**: http://alexking.site:8080/api/v1/tasks/:id/annotations?format=COCO%201.0

**Request Method**: GET

**Response**：

    Status Code:
        '202': '已开始转储标注'
        '201': '标注文件已准备好下载'
        '200': '已开始下载文件'

