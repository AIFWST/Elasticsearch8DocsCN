

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Get Watcher stats API](watcher-api-stats.md) [Create or update watch API
»](watcher-api-put-watch.md)

## 查询监视接口

检索所有已注册的监视。

###Request

"获取/_watcher/_query/手表"

###Prerequisites

* 您必须具有"manage_watcher"或"monitor_watcher"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

以分页方式检索所有监视，并选择性地按查询筛选监视。

此接口支持以下字段：

姓名 |必填 |默认 |描述 ---|---|---|--- 'from'

|

no

|

0

|

与要获取的第一个结果的偏移量。需要是非负数。   "大小"

|

no

|

10

|

要返回的命中数。需要是非负数。   "查询"

|

no

|

null

|

可选，查询要返回的筛选器监视。   "排序"

|

no

|

null

|

可选的排序定义。   "search_after"

|

no

|

null

|

可选搜索 After 以使用上次命中的排序值进行分页。   请注意，只有"_id"和"元数据.*"字段是可查询或可排序的。

此 api 返回以下顶级字段：

`count`

     The total number of watches found. 
`watches`

     A list of watches based on the `from`, `size` or `search_after` request body parameters. 

###Examples

以下示例列出了所有存储的监视：

    
    
    GET /_watcher/_query/watches

Response:

    
    
    {
        "count": 1,
        "watches": [
            {
                "_id": "my_watch",
                "watch": {
                    "trigger": {
                        "schedule": {
                            "hourly": {
                                "minute": [
                                    0,
                                    5
                                ]
                            }
                        }
                    },
                    "input": {
                        "simple": {
                            "payload": {
                                "send": "yes"
                            }
                        }
                    },
                    "condition": {
                        "always": {}
                    },
                    "actions": {
                        "test_index": {
                            "index": {
                                "index": "test"
                            }
                        }
                    }
                },
                "status": {
                    "state": {
                        "active": true,
                        "timestamp": "2015-05-26T18:21:08.630Z"
                    },
                    "actions": {
                        "test_index": {
                            "ack": {
                                "timestamp": "2015-05-26T18:21:08.630Z",
                                "state": "awaits_successful_execution"
                            }
                        }
                    },
                    "version": -1
                },
                "_seq_no": 0,
                "_primary_term": 1
            }
        ]
    }

[« Get Watcher stats API](watcher-api-stats.md) [Create or update watch API
»](watcher-api-put-watch.md)
