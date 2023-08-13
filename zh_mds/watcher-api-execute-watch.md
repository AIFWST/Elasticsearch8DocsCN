

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Delete watch API](watcher-api-delete-watch.md) [Get watch API »](watcher-
api-get-watch.md)

## 执行监视接口

强制执行存储的监视。

###Request

"发布_watcher/监视/<watch_id>/_execute"

"发布_watcher/观看/_execute"

###Prerequisites

* 您必须具有"manage_watcher"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

此 API 可用于在其触发逻辑之外强制执行监视，或模拟监视执行以进行调试。

出于测试和调试目的，您还可以对手表的运行方式进行精细控制。您可以在不执行其所有操作的情况下执行监视，也可以通过模拟它们来执行监视。您还可以通过忽略监视条件来强制执行，并控制在执行后是否将监视记录写入监视历史记录。

#### 内联监视执行

您可以使用执行 API 通过内联指定监视定义来执行尚未注册的监视。这是在将手表添加到观察程序之前测试和调试手表的绝佳工具。

### 路径参数

`<watch_id>`

     (Optional, string) Identifier for the watch. 

### 查询参数

`debug`

     (Optional, Boolean) Defines whether the watch runs in debug mode. The default value is `false`. 

### 请求正文

此接口支持以下字段：

姓名 |必填 |默认 |描述 ---|---|---|--- 'trigger_data'

|

no

|

|

此结构被解析为将在监视执行"ignore_condition"期间使用的触发器事件的数据

|

no

|

false

|

当设置为"true"时，监视执行将使用 always 条件。这也可以指定为 HTTP参数。   "alternative_input"

|

no

|

null

|

如果存在，手表将此对象用作有效负载，而不是执行自己的输入。   "action_modes"

|

no

|

null

|

确定如何在监视执行过程中处理监视操作。有关详细信息，请参阅操作执行模式。   "record_execution"

|

no

|

false

|

当设置为"true"时，表示监视执行结果的监视记录将保留到当前时间的".watcher-history"索引中。此外，监视的状态会更新，可能会限制后续执行。这也可以指定为 HTTP 参数。   "看"

|

no

|

null

|

如果存在，则使用此监视，而不是请求中指定的监视。此监视未保存到索引，无法设置record_execution。   #### 操作执行模式编辑

操作模式定义在监视执行期间如何处理操作。操作可以与五种可能的模式相关联：

姓名 |描述 ---|--- "模拟"

|

模拟操作执行。每种操作类型都定义自己的模拟操作模式。例如，"电子邮件"操作创建本应发送但实际上并未发送的电子邮件。在此模式下，如果监视的当前状态指示应限制操作，则操作可能会受到限制。   "force_simulate"

|

与"模拟"模式类似，不同之处在于即使手表的当前状态指示它应该受到限制，操作也不会受到限制。   "执行"

|

执行操作，就像如果手表由其自己的触发器触发时执行的操作一样。如果监视的当前状态指示应限制执行，则可能会限制执行。   "force_execute"

|

与"执行"模式类似，不同之处在于即使手表的当前状态指示它应该受到限制，操作也不会受到限制。   "跳过"

|

操作将被跳过，并且不会执行或模拟。有效地强制限制操作。   #### 安全集成编辑

在集群上启用 Elasticsearch 安全功能后，将以存储监视的用户的权限执行监视。如果您的用户被允许读取索引"a"，但不允许读取索引"b"，则在执行监视期间将应用完全相同的规则集。

使用执行监视 API 时，调用 API 的用户的授权数据将用作基础，而不是存储监视的信息。

###Examples

以下示例执行"my_watch"监视：

    
    
    POST _watcher/watch/my_watch/_execute

以下示例显示了执行"my-watch"手表的综合示例：

    
    
    POST _watcher/watch/my_watch/_execute
    {
      "trigger_data" : { __"triggered_time" : "now",
         "scheduled_time" : "now"
      },
      "alternative_input" : { __"foo" : "bar"
      },
      "ignore_condition" : true, __"action_modes" : {
        "my-action" : "force_simulate" __},
      "record_execution" : true __}

__

|

提供了触发时间和计划时间。   ---|---    __

|

监视定义的输入将被忽略，而是将提供的输入用作执行有效负载。   __

|

监视定义的条件将被忽略，并假定其计算结果为"true"。   __

|

强制模拟"我的动作"。强制模拟意味着将忽略限制，并且监视由观察者模拟，而不是正常执行。   __

|

监视的执行会在监视历史记录中创建监视记录，并且监视的限制状态可能会相应地更新。   下面是输出的示例：

    
    
    {
      "_id": "my_watch_0-2015-06-02T23:17:55.124Z", __"watch_record": { __"@timestamp": "2015-06-02T23:17:55.124Z",
        "watch_id": "my_watch",
        "node": "my_node",
        "messages": [],
        "trigger_event": {
          "type": "manual",
          "triggered_time": "2015-06-02T23:17:55.124Z",
          "manual": {
            "schedule": {
              "scheduled_time": "2015-06-02T23:17:55.124Z"
            }
          }
        },
        "state": "executed",
        "status": {
          "version": 1,
          "execution_state": "executed",
          "state": {
            "active": true,
            "timestamp": "2015-06-02T23:17:55.111Z"
          },
          "last_checked": "2015-06-02T23:17:55.124Z",
          "last_met_condition": "2015-06-02T23:17:55.124Z",
          "actions": {
            "test_index": {
              "ack": {
                "timestamp": "2015-06-02T23:17:55.124Z",
                "state": "ackable"
              },
              "last_execution": {
                "timestamp": "2015-06-02T23:17:55.124Z",
                "successful": true
              },
              "last_successful_execution": {
                "timestamp": "2015-06-02T23:17:55.124Z",
                "successful": true
              }
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
        "result": { __"execution_time": "2015-06-02T23:17:55.124Z",
          "execution_duration": 12608,
          "input": {
            "type": "simple",
            "payload": {
              "foo": "bar"
            },
            "status": "success"
          },
          "condition": {
            "type": "always",
            "met": true,
            "status": "success"
          },
          "actions": [
            {
              "id": "test_index",
              "index": {
                "response": {
                  "index": "test",
                  "version": 1,
                  "created": true,
                  "result": "created",
                  "id": "AVSHKzPa9zx62AzUzFXY"
                }
              },
              "status": "success",
              "type": "index"
            }
          ]
        },
        "user": "test_admin" __}
    }

__

|

监视记录的 ID，因为它将存储在".watcher-history"索引中。   ---|---    __

|

监视记录文档，因为它将存储在".watcher-history"索引中。   __

|

监视执行结果。   __

|

用于执行监视的用户。   您可以通过将模式名称与操作 ID 相关联来为每个操作设置不同的执行模式：

    
    
    POST _watcher/watch/my_watch/_execute
    {
      "action_modes" : {
        "action1" : "force_simulate",
        "action2" : "skip"
      }
    }

您还可以使用"_all"作为操作 ID 将单个执行模式与手表中的所有操作相关联：

    
    
    POST _watcher/watch/my_watch/_execute
    {
      "action_modes" : {
        "_all" : "force_execute"
      }
    }

以下示例演示如何以内联方式执行监视：

    
    
    POST _watcher/watch/_execute
    {
      "watch" : {
        "trigger" : { "schedule" : { "interval" : "10s" } },
        "input" : {
          "search" : {
            "request" : {
              "indices" : [ "logs" ],
              "body" : {
                "query" : {
                  "match" : { "message": "error" }
                }
              }
            }
          }
        },
        "condition" : {
          "compare" : { "ctx.payload.hits.total" : { "gt" : 0 }}
        },
        "actions" : {
          "log_error" : {
            "logging" : {
              "text" : "Found {{ctx.payload.hits.total}} errors in the logs"
            }
          }
        }
      }
    }

此 API 的所有其他设置在内联监视时仍然适用。在以下代码片段中，虽然内联监视定义了"比较"条件，但在执行期间将忽略此条件：

    
    
    POST _watcher/watch/_execute
    {
      "ignore_condition" : true,
      "watch" : {
        "trigger" : { "schedule" : { "interval" : "10s" } },
        "input" : {
          "search" : {
            "request" : {
              "indices" : [ "logs" ],
              "body" : {
                "query" : {
                  "match" : { "message": "error" }
                }
              }
            }
          }
        },
        "condition" : {
          "compare" : { "ctx.payload.hits.total" : { "gt" : 0 }}
        },
        "actions" : {
          "log_error" : {
            "logging" : {
              "text" : "Found {{ctx.payload.hits.total}} errors in the logs"
            }
          }
        }
      }
    }

[« Delete watch API](watcher-api-delete-watch.md) [Get watch API »](watcher-
api-get-watch.md)
