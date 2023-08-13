

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher conditions](condition.md)

[« Watcher array compare condition](condition-array-compare.md) [Watcher
actions »](actions.md)

## 观察程序脚本条件

评估脚本的监视条件。默认脚本语言是"无痛"。您可以使用 Elasticsearch 支持的任何脚本语言，只要该语言支持将表达式计算为布尔值即可。请注意，"胡须"和"表达"语言太有限，无法在此条件下使用。有关详细信息，请参阅脚本。

### 使用脚本条件

以下代码片段配置始终返回"true"的内联"脚本"条件：

    
    
    "condition" : {
      "script" : "return true"
    }

此示例将脚本定义为简单字符串。这种格式实际上是定义内联脚本的快捷方式。脚本的正式定义是指定脚本类型以及可选语言和参数值的对象。如果省略"lang"属性，则语言默认为"无痛"。Elasticsearch支持两种类型的脚本，内联和存储。

例如，以下代码片段显示了"内联"脚本的正式定义，该定义显式指定语言并定义单个脚本参数"result"：

    
    
    "condition" : {
      "script" : {
        "source" : "return params.result",
        "lang" : "painless",
        "params" : {
          "result" : true
        }
      }
    }

### 内联脚本

内联脚本是在条件本身中定义的脚本。以下代码片段显示了始终返回"true"的简单无痛脚本的正式配置。

    
    
    "condition" : {
      "script" : {
        "source" : "return true"
      }
    }

### 存储脚本

存储的脚本是指存储在 Elasticsearch 中的脚本。以下代码片段演示如何通过脚本的"id"引用脚本：

    
    
    "condition" : {
      "script" : {
        "id" : "my_script"
      }
    }

与内联脚本一样，您还可以指定脚本语言和参数：

    
    
    "condition" : {
      "script" : {
        "id" : "my_script",
        "lang" : "javascript",
        "params" : { "color" : "red" }
      }
    }

### 访问监视有效负载

脚本可以访问当前监视执行上下文，包括有效负载数据，以及通过条件定义传入的任何参数。

例如，以下代码片段定义了一个监视，该监视使用"搜索"输入并使用"脚本"条件来检查命中数是否超过指定的阈值：

    
    
    {
      "input" : {
        "search" : {
          "request": {
            "indices" : "log-events",
            "body" : {
              "size" : 0,
              "query" : { "match" : { "status" : "error" } }
            }
          }
        }
      },
      "condition" : {
        "script" : {
          "source" : "return ctx.payload.hits.total > params.threshold",
          "params" : {
            "threshold" : 5
          }
        }
      }
    }

当您使用脚本化条件来评估 Elasticsearch 响应时，请记住响应中的字段不再具有其原生数据类型。例如，响应中的"@timestamp"是一个字符串，而不是"日期时间"。要将响应"@timestamp"与"ctx.execution_time"进行比较，您需要将"@timestamp"字符串解析为"ZonedDateTime"。例如：

    
    
    java.time.ZonedDateTime.parse(@timestamp)

您可以在监视上下文中引用以下变量：

姓名 |描述 ---|--- 'ctx.watch_id'

|

当前正在执行的监视的 ID。   "ctx.execution_time"

|

此表的时间执行开始。   "ctx.trigger.triggered_time"

|

触发此手表的时间。   "ctx.trigger.scheduled_time"

|

这只手表应该被触发的时间。   'ctx.metadata.*'

|

与监视关联的任何元数据。   'ctx.payload.*'

|

手表输入加载的有效负载数据。   « 观察程序数组比较条件观察程序操作 »