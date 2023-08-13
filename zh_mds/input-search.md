

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher inputs](input.md)

[« Watcher simple input](input-simple.md) [Watcher HTTP input »](input-
http.md)

## 观察程序搜索输入

使用"搜索"输入在触发监视时将 Elasticsearch 搜索请求的结果加载到执行上下文中。有关所有支持的属性，请参阅搜索输入属性。

在搜索输入的"请求"对象中，您可以指定：

* 您要搜索的索引 * 搜索类型 * 搜索请求正文

搜索请求正文支持完整的 Elasticsearch Query DSL，它与 Elasticsearch '_search' 请求的正文相同。

例如，以下输入从"日志"索引中检索所有"事件"文档：

    
    
    "input" : {
      "search" : {
        "request" : {
          "indices" : [ "logs" ],
          "body" : {
            "query" : { "match_all" : {}}
          }
        }
      }
    }

指定索引时可以使用日期数学和通配符。例如，以下输入从今天的每日报价指数加载最新的 VIXZ 报价：

    
    
    {
      "input" : {
        "search" : {
          "request" : {
            "indices" : [ "<stock-quotes-{now/d}>" ],
            "body" : {
              "size" : 1,
              "sort" : {
                "timestamp" : { "order" : "desc"}
              },
              "query" : {
                "term" : { "symbol" : "vix"}
              }
            }
          }
        }
      }
    }

### 提取特定字段

您可以使用"extract"属性指定要加载到监视有效负载中的搜索响应中的哪些字段。当搜索生成大量响应并且您只对特定字段感兴趣时，这很有用。

例如，以下输入仅将命中总数加载到监视有效负载中：

    
    
    "input": {
        "search": {
          "request": {
            "indices": [ ".watcher-history*" ]
          },
          "extract": [ "hits.total.value" ]
        }
      },

### 使用模板

"搜索"输入支持搜索模板。例如，以下代码片段引用名为"my_template"的索引模板，并传递值 23 以填充模板的"value"参数：

    
    
    {
      "input" : {
        "search" : {
          "request" : {
            "indices" : [ "logs" ],
            "template" : {
              "id" : "my_template",
              "params" : {
                "value" : 23
              }
            }
          }
        }
      }
      ...
    }

### 申请条件

"搜索"输入通常与"脚本"条件结合使用。例如，以下代码片段添加一个条件来检查搜索是否返回了五个以上的命中：

    
    
    {
      "input" : {
        "search" : {
          "request" : {
            "indices" : [ "logs" ],
            "body" : {
              "query" : { "match_all" : {} }
            }
          }
        }
      },
      "condition" : {
        "compare" : { "ctx.payload.hits.total" : { "gt" : 5 }}
      }
      ...
    }

### 访问搜索结果

条件、转换和操作可以通过监视执行上下文访问搜索结果。例如：

* 要将所有搜索命中加载到电子邮件正文中，请使用"ctx.payload.hits"。  * 要引用总点击数，请使用"ctx.payload.hits.total"。  * 要访问特定命中，请使用其从零开始的数组索引。例如，要获得第三次命中，请使用"ctx.payload.hits.hits.2"。  * 要从特定命中获取字段值，请使用 'ctx.payload.hits.hits。<index>。领域。<fieldname>'。例如，要从第一次命中获取消息字段，请使用"ctx.payload.hits.hits.0.fields.message"。

搜索响应中的命中总数作为响应中的对象返回。它包含一个"值"、命中数和一个"关系"，该关系指示值是否准确("eq")或与查询匹配的总命中数的下限("gte")。您可以在搜索请求中将"track_total_hits"设置为 true，以告诉 Elasticsearch 始终准确跟踪点击数。

### 搜索输入属性

姓名 |必填 |默认 |描述 ---|---|---|--- 'request.search_type'

|

no

|

`query_then_fetch`

|

要执行的搜索请求的类型。有效值为："dfs_query_then_fetch"和"query_then_fetch"。Elasticsearchdefault 是 'query_then_fetch'。   'request.index'

|

no

|

-

|

要搜索的索引。如果省略，则搜索所有索引，这是 Elasticsearch 中的默认行为。   '请求.正文'

|

no

|

-

|

请求的正文。请求正文遵循通常在 REST "_search"请求正文中发送的相同结构。正文可以是静态文本或包含"胡须"模板。   '请求模板'

|

no

|

-

|

搜索模板的正文。有关详细信息，请参阅配置模板。   'request.indices_options.expand_wildcards'

|

no

|

`open`

|

如何展开通配符。有效值为："全部"、"打开"、"关闭"和"无"有关详细信息，请参阅"expand_wildcards"。   'request.indices_options.ignore_unavailable'

|

no

|

`true`

|

搜索是否应忽略不可用的索引。有关详细信息，请参阅"ignore_unavailable"。   'request.indices_options.allow_no_index'

|

no

|

`true`

|

是否允许通配符索引表达式生成具体索引的搜索。有关详细信息，请参阅allow_no_indices。   "提取"

|

no

|

-

|

要从搜索响应中提取并作为有效负载加载的 JSON 键数组。当搜索生成大型响应时，您可以使用"提取"来选择相关字段，而不是加载整个响应。   "超时"

|

no

|

30s

|

等待搜索 api 调用返回的超时。如果在此时间内未返回响应，则搜索输入超时并失败。此设置将覆盖默认搜索操作超时。   指定请求"body"时，您可以在执行上下文中引用以下变量：

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

与监视关联的任何元数据。   « 观察者简单输入 观察者 HTTP 输入 »