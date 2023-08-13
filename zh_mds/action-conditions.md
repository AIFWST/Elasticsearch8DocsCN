

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher actions](actions.md)

[« Running an action for each element in an array](action-foreach.md)
[Watcher email action »](actions-email.md)

## 向观察程序操作添加条件

触发监视时，其条件确定是否执行监视操作。在每个操作中，您还可以添加条件操作。这些附加条件使单个警报能够根据其各自的条件执行不同的操作。当从输入搜索中找到命中时，以下手表将始终发送电子邮件，但仅当搜索结果中的命中超过 5 次时才会触发"notify_pager"操作。

    
    
    PUT _watcher/watch/log_event_watch
    {
      "trigger" : {
        "schedule" : { "interval" : "5m" }
      },
      "input" : {
        "search" : {
          "request" : {
            "indices" : "log-events",
            "body" : {
              "size" : 0,
              "query" : { "match" : { "status" : "error" } }
            }
          }
        }
      },
      "condition" : {
        "compare" : { "ctx.payload.hits.total" : { "gt" : 0 } }
      },
      "actions" : {
        "email_administrator" : {
          "email" : {
            "to" : "sys.admino@host.domain",
            "subject" : "Encountered {{ctx.payload.hits.total}} errors",
            "body" : "Too many error in the system, see attached data",
            "attachments" : {
              "attached_data" : {
                "data" : {
                  "format" : "json"
                }
              }
            },
            "priority" : "high"
          }
        },
        "notify_pager" : {
          "condition": { __"compare" : { "ctx.payload.hits.total" : { "gt" : 5 } }
          },
          "webhook" : {
            "method" : "POST",
            "host" : "pager.service.domain",
            "port" : 1234,
            "path" : "/{{watch_id}}",
            "body" : "Encountered {{ctx.payload.hits.total}} errors"
          }
        }
      }
    }

__

|

仅适用于"notify_pager"操作的"条件"，它将执行限制为条件成功时(在本例中至少命中 5 次)。   ---|--- « 为数组中的每个元素运行操作观察者电子邮件操作 »