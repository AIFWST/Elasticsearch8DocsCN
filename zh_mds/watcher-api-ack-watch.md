

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Watcher APIs](watcher-api.md) [Activate watch API »](watcher-api-
activate-watch.md)

## Ack watchAPI

通过确认监视，您可以手动限制监视操作的执行。

###Request

"放_watcher/看/<watch_id>/_ack"

"放_watcher/观察/<watch_id>/_ack/<action_id>"

###Prerequisites

* 您必须具有"manage_watcher"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

操作的_acknowledgement state_存储在"状态.actions"中。.<id>ack.state"结构。

如果当前正在执行指定的监视，则此 API 将返回错误。这样做的原因是防止从手表执行中覆盖监视状态。

### 路径参数

`<action_id>`

     (Optional, list) A comma-separated list of the action IDs to acknowledge. If you omit this parameter, all of the actions of the watch are acknowledged. 
`<watch_id>`

     (Required, string) Identifier for the watch. 

###Examples

为了演示，让我们创建一个新手表：

    
    
    PUT _watcher/watch/my_watch
    {
      "trigger" : {
        "schedule" : {
          "yearly" : { "in" : "february", "on" : 29, "at" : "noon" }
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
          "throttle_period": "15m",
          "index": {
            "index": "test"
          }
        }
      }
    }

调用获取监视 API 时，将随监视定义一起返回监视的当前状态及其操作状态：

    
    
    GET _watcher/watch/my_watch

新创建的手表的操作状态为"awaits_successful_execution"：

    
    
    {
      "found": true,
      "_seq_no": 0,
      "_primary_term": 1,
      "_version": 1,
      "_id": "my_watch",
      "status": {
        "version": 1,
        "actions": {
          "test_index": {
            "ack": {
              "timestamp": "2015-05-26T18:04:27.723Z",
              "state": "awaits_successful_execution"
            }
          }
        },
        "state": ...
      },
      "watch": ...
    }

当手表执行并且条件匹配时，"ack.state"的值将更改为"ackable"。让我们强制执行手表并再次获取它以检查状态：

    
    
    POST _watcher/watch/my_watch/_execute
    {
      "record_execution" : true
    }
    
    GET _watcher/watch/my_watch

并且操作现在处于"可操作"状态：

    
    
    {
      "found": true,
      "_id": "my_watch",
      "_seq_no": 1,
      "_primary_term": 1,
      "_version": 2,
      "status": {
        "version": 2,
        "actions": {
          "test_index": {
            "ack": {
              "timestamp": "2015-05-26T18:04:27.723Z",
              "state": "ackable"
            },
            "last_execution" : {
              "timestamp": "2015-05-25T18:04:27.723Z",
              "successful": true
            },
            "last_successful_execution" : {
              "timestamp": "2015-05-25T18:04:27.723Z",
              "successful": true
            }
          }
        },
        "state": ...,
        "execution_state": "executed",
        "last_checked": ...,
        "last_met_condition": ...
      },
      "watch": ...
    }

现在我们可以承认它：

    
    
    PUT _watcher/watch/my_watch/_ack/test_index
    GET _watcher/watch/my_watch
    
    
    {
      "found": true,
      "_id": "my_watch",
      "_seq_no": 2,
      "_primary_term": 1,
      "_version": 3,
      "status": {
        "version": 3,
        "actions": {
          "test_index": {
            "ack": {
              "timestamp": "2015-05-26T18:04:27.723Z",
              "state": "acked"
            },
            "last_execution" : {
              "timestamp": "2015-05-25T18:04:27.723Z",
              "successful": true
            },
            "last_successful_execution" : {
              "timestamp": "2015-05-25T18:04:27.723Z",
              "successful": true
            }
          }
        },
        "state": ...,
        "execution_state": "executed",
        "last_checked": ...,
        "last_met_condition": ...
      },
      "watch": ...
    }

确认操作会限制该操作的进一步执行，直到其"ack.state"重置为"awaits_successful_execution"。当不满足手表的条件(条件计算结果为"false")时，就会发生这种情况。

您可以通过分配"actions"参数逗号分隔的操作 ID 列表来确认多个操作：

    
    
    POST _watcher/watch/my_watch/_ack/action1,action2

要确认手表的所有操作，只需省略"actions"参数：

    
    
    POST _watcher/watch/my_watch/_ack

响应看起来像"获取监视"响应，但仅包含以下状态：

    
    
    {
      "status": {
        "state": {
          "active": true,
          "timestamp": "2015-05-26T18:04:27.723Z"
        },
        "last_checked": "2015-05-26T18:04:27.753Z",
        "last_met_condition": "2015-05-26T18:04:27.763Z",
        "actions": {
          "test_index": {
            "ack" : {
              "timestamp": "2015-05-26T18:04:27.713Z",
              "state": "acked"
            },
            "last_execution" : {
              "timestamp": "2015-05-25T18:04:27.733Z",
              "successful": true
            },
            "last_successful_execution" : {
              "timestamp": "2015-05-25T18:04:27.773Z",
              "successful": true
            }
          }
        },
        "execution_state": "executed",
        "version": 2
      }
    }

[« Watcher APIs](watcher-api.md) [Activate watch API »](watcher-api-
activate-watch.md)
