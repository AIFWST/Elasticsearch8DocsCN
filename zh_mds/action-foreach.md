

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher actions](actions.md)

[« Watcher actions](actions.md) [Adding conditions to Watcher actions
»](action-conditions.md)

## 为数组中的每个元素运行操作

您可以在操作中使用"foreach"字段来触发该数组中每个元素的配置操作。

为了防止长时间运行的监视，可以使用"max_iterations"字段来限制每个监视执行的最大运行量。如果达到此限制，则会正常停止执行。如果未设置，则此字段默认为 100。

    
    
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
              "query" : { "match" : { "status" : "error" } }
            }
          }
        }
      },
      "condition" : {
        "compare" : { "ctx.payload.hits.total" : { "gt" : 0 } }
      },
      "actions" : {
        "log_hits" : {
          "foreach" : "ctx.payload.hits.hits", __"max_iterations" : 500,
          "logging" : {
            "text" : "Found id {{ctx.payload._id}} with field {{ctx.payload._source.my_field}}"
          }
        }
      }
    }

__

|

将针对每个返回的搜索命中执行日志记录语句。   ---|--- « 观察程序操作 向观察程序操作添加条件»