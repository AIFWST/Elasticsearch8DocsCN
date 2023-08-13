

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Execute watch API](watcher-api-execute-watch.md) [Get Watcher stats API
»](watcher-api-stats.md)

## 获取监视接口

按监视的 ID 检索监视。

###Request

"获取_watcher/观看/<watch_id>"

###Prerequisites

* 您必须具有"manage_watcher"或"monitor_watcher"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

### 路径参数

`<watch_id>`

     (Required, string) Identifier for the watch. 

###Examples

以下示例获取 id 为"my_watch"的监视：

    
    
    GET _watcher/watch/my_watch

Response:

    
    
    {
      "found": true,
      "_id": "my_watch",
      "_seq_no": 0,
      "_primary_term": 1,
      "_version": 1,
      "status": { __"version": 1,
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
        }
      },
      "watch": {
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
        "trigger": {
          "schedule": {
            "hourly": {
              "minute": [0, 5]
            }
          }
        },
        "actions": {
          "test_index": {
            "index": {
              "index": "test"
            }
          }
        }
      }
    }

__

|

手表的当前状态 ---|--- « 执行监视 API 获取观察者统计信息 API»