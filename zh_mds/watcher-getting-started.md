

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« Watcher](xpack-alerting.md) [How Watcher works »](how-watcher-works.md)

## 观察者入门

要设置手表以开始发送提醒，请执行以下操作：

* 安排手表并定义输入。  * 添加一个条件，用于检查是否需要发送警报。  * 配置在满足条件时发送警报的操作。

### 调度监视并定义输入

监视计划控件通常显示触发监视。监视输入获取要评估的数据。

要定期搜索日志数据并将结果加载到监视中，可以使用间隔计划和搜索输入。例如，以下监视每 10 秒在"日志"索引中搜索一次错误：

    
    
    PUT _watcher/watch/log_error_watch
    {
      "trigger" : {
        "schedule" : { "interval" : "10s" } __},
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
      }
    }

__

|

计划通常配置为运行频率较低。本示例将间隔设置为 10 秒，以便您可以轻松查看正在触发的监视。由于这款手表运行得如此频繁，因此当您重新进行实验时，不要忘记删除手表。   ---|--- 如果您查看观看历史记录，您会发现手表每 10 秒触发一次。但是，搜索不会返回任何结果，因此不会将任何内容加载到监视有效负载中。

例如，以下请求从监视历史记录中检索最近十次监视执行(监视记录)：

    
    
    response = client.search(
      index: '.watcher-history*',
      pretty: true,
      body: {
        sort: [
          {
            "result.execution_time": 'desc'
          }
        ]
      }
    )
    puts response
    
    
    GET .watcher-history*/_search?pretty
    {
      "sort" : [
        { "result.execution_time" : "desc" }
      ]
    }

### 添加条件

条件评估已加载到监视中的数据，并确定是否需要执行任何操作。现在，您已将日志错误加载到监视中，您可以定义一个条件来检查是否发现任何错误。

例如，以下比较条件只是检查搜索输入是否返回任何命中。

    
    
    PUT _watcher/watch/log_error_watch
    {
      "trigger" : { "schedule" : { "interval" : "10s" }},
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
        "compare" : { "ctx.payload.hits.total" : { "gt" : 0 }} __}
    }

__

|

比较条件使您可以轻松地与执行上下文中的值进行比较。   ---|--- 要使此比较条件的计算结果为"true"，您需要将一个包含错误的事件添加到包含错误的"logs"索引中。例如，以下请求将 404 错误添加到"logs"索引：

    
    
    POST logs/_doc
    {
      "timestamp": "2015-05-17T18:12:07.613Z",
      "request": "GET index.html",
      "status_code": 404,
      "message": "Error: File not found"
    }

添加此事件后，手表下次执行其条件时，计算结果将为"true"。每次执行监视时，条件结果都会记录为"watch_record"的一部分，因此您可以通过搜索监视历史记录来验证是否满足条件：

    
    
    response = client.search(
      index: '.watcher-history*',
      pretty: true,
      body: {
        query: {
          bool: {
            must: [
              {
                match: {
                  "result.condition.met": true
                }
              },
              {
                range: {
                  "result.execution_time": {
                    from: 'now-10s'
                  }
                }
              }
            ]
          }
        }
      }
    )
    puts response
    
    
    GET .watcher-history*/_search?pretty
    {
      "query" : {
        "bool" : {
          "must" : [
            { "match" : { "result.condition.met" : true }},
            { "range" : { "result.execution_time" : { "from" : "now-10s" }}}
          ]
        }
      }
    }

### 配置操作

在手表历史记录中记录手表记录固然很好，但 Watcher 的真正功能是在满足手表条件时能够执行某些操作。Awatch 的操作定义了当监视条件评估结果为"true"时要执行的操作。您可以发送电子邮件、调用第三方 Webhook、将文档写入 Elasticsearch 索引或将消息记录到标准 Elasticsearch 日志文件。

例如，当检测到错误时，以下操作会将消息写入 Elasticsearch 日志。

    
    
    PUT _watcher/watch/log_error_watch
    {
      "trigger" : { "schedule" : { "interval" : "10s" }},
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

### 删除监视

由于"log_error_watch"配置为每 10 秒运行一次，因此请确保在完成试验后将其删除。否则，此示例手表的噪音将使您很难看到监视历史记录和日志文件中还发生了什么。

要删除监视，请使用删除监视 API：

    
    
    response = client.watcher.delete_watch(
      id: 'log_error_watch'
    )
    puts response
    
    
    DELETE _watcher/watch/log_error_watch

### 所需的安全权限

若要使用户能够创建和操作监视，请为其分配"watcher_admin"安全角色。观察者管理员还可以查看监视、监视历史记录和触发的监视。

要允许用户查看监视和监视历史记录，请为其分配"watcher_user"安全角色。观察程序用户无法创建或操作监视;只允许它们执行只读监视操作。

### 去哪里下一步

* 请参阅_How观察者works_，了解有关手表解剖结构和手表生命周期的更多信息。  * 有关设置手表的更多示例，请参阅_Example watches_。  * 请参阅 Elastic 示例存储库中的示例监视，了解可用作构建自定义监视的起点的其他示例监视。

[« Watcher](xpack-alerting.md) [How Watcher works »](how-watcher-works.md)
