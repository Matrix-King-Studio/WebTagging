## 身份验证

### 登录

**Request URL**: http://alexking.site:8080/api/v1/auth/login

**Request Method**: POST

**Form Data**:

	username: ""
	password: ""

**Response**：Token Key

	{"key":"e7b5b0363cae7fe9c455636d6b21fc09f526aff0"}

### 注销

**Request URL**: http://alexking.site:8080/api/v1/auth/logout

**Request Method**: POST

### 注册

**Request URL**: http://alexking.site:8080/api/v1/auth/register

**Request Method**: POST

**Form Data**:

	{
	    "username":"",
	    "first_name":"",
	    "last_name":"",
	    "email":"",
	    "password1":"",
	    "password2":"",
	}

### 用户

返回当前已被授权的用户的实例信息。

**Request URL**: http://alexking.site:8080/api/v1/users/self

**Request Method**: GET

**Response**：

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

## 任务

![](http://assets.processon.com/chart_image/5f2a37d907912906dbf8edab.png)

### 创建任务

1. 上传 Task 基本信息

**Request URL**: http://alexking.site:8080/api/v1/tasks

**Request Method**: POST

**Request Data**：

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

3. 获取任务创建状态

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

### 标注工作台

获取当前标注情况

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
            },
            {
                "type":"rectangle",
                "occluded":false,
                "z_order":0,
                "points":[
                    265.5,
                    440.37890625,
                    949.4398803710938,
                    826.9536437988281
                ],
                "id":6,
                "frame":1,
                "label_id":11,
                "group":0,
                "attributes":[
                    {
                        "spec_id":11,
                        "value":"BMW"
                    }
                ]
            },
            {
                "type":"polyline",
                "occluded":false,
                "z_order":0,
                "points":[
                    248.486328125,
                    308.3876953125,
                    116.8235734331156,
                    210.529840972873,
                    111.48587464920638,
                    150.03592142188973,
                    114.45126286248887,
                    118.60280636108655,
                    136.39513564078698,
                    98.4381665107594,
                    173.1659494855012,
                    73.52890551917699,
                    255.60374181478073,
                    71.74967259120785,
                    300.0845650140327,
                    75.90121608980371,
                    342.19307764265795,
                    85.3904583723106,
                    416.92086061739974,
                    135.80205799812938,
                    490.46248830683,
                    174.94518241347214,
                    504.6963517305903,
                    213.49522918615548,
                    502.3240411599636,
                    268.6514499532277,
                    481.56632366697886,
                    289.40916744621245,
                    419.29317118802646,
                    306.6084190832571,
                    354.64770813844734,
                    304.82918615528615,
                    327.9592142188976,
                    313.7253507951373,
                    248.48681010290056,
                    308.38765201122624
                ],
                "id":7,
                "frame":5,
                "label_id":11,
                "group":0,
                "attributes":[
                    {
                        "spec_id":11,
                        "value":"s"
                    }
                ]
            },
            {
                "type":"rectangle",
                "occluded":false,
                "z_order":0,
                "points":[
                    62.6875,
                    94.7421875,
                    500.0170593261719,
                    333.68536376953125
                ],
                "id":8,
                "frame":7,
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


保存当前标注数据

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

### 下载标注结果

**Request URL**: http://alexking.site:8080/api/v1/tasks/:id/annotations?format=COCO%201.0

**Request Method**: GET

**Response**：

    Status Code:
        '202': '已开始转储标注'
        '201': '标注文件已准备好下载'
        '200': '已开始下载文件'

