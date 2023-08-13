

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Payload transforms](transform.md)

[« Watcher script payload transform](transform-script.md) [Managing watches
»](managing-watches.md)

## 观察程序链有效负载转换

在链中执行已配置有效负载转换的有序列表的有效负载转换，其中一个转换的输出用作链中下一个转换的输入。此转换接受的有效负载充当链中第一个转换的输入，链中最后一个转换的输出是整个"链"转换的输出。

您可以使用链有效负载转换从其他可用转换中构建更复杂的转换。例如，可以组合"搜索"有效负载转换和"脚本"有效负载转换，如以下代码片段所示：

    
    
    "transform" : {
      "chain" : [ __{
          "search" : { __"request": {
              "indices" : [ "logstash-*" ],
              "body" : {
                "size" : 0,
                "query" : {
                  "match" : { "priority" : "error" }
                }
              }
            }
          }
        },
        {
          "script" : "return [ 'error_count' : ctx.payload.hits.total ]" __}
      ]
    }

__

|

"链"有效负载转换定义 ---|--- __

|

链中的第一个转换(在本例中为"搜索"有效负载转换)__

|

链中的第二个也是最后一个转换(在本例中为"脚本"有效负载转换) 此示例在群集上执行"计数"搜索以查找"错误"事件。然后将搜索结果传递到第二个"脚本"有效负载转换。"脚本"有效负载转换提取总命中计数，并将其分配给新生成的有效负载中的"error_count"字段。此 newpayload 是"链"有效负载转换的输出，并替换监视执行上下文中的有效负载。

[« Watcher script payload transform](transform-script.md) [Managing watches
»](managing-watches.md)
