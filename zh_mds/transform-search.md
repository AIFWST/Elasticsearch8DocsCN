

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Payload transforms](transform.md)

[« Payload transforms](transform.md) [Watcher script payload transform
»](transform-script.md)

## 观察程序搜索有效负载转换

一种有效负载转换，用于在集群上执行搜索，并将监视执行上下文中的当前有效负载替换为返回的搜索响应。以下代码片段演示如何在监视级别定义简单的搜索转换：

    
    
    {
      "transform" : {
        "search" : {
          "request" : {
            "body" : { "query" : { "match_all" : {} }}
          }
        }
      }
    }

像所有其他基于搜索的构造一样，可以使用Elasticsearch支持的完整搜索API。例如，以下搜索有效负载转换对所有事件索引执行搜索，将事件与"错误"优先级匹配：

    
    
    {
      "transform" : {
        "search" : {
          "request" : {
            "indices" : [ "events-*" ],
            "body" : {
              "size" : 0,
              "query" : {
                "match" : { "priority" : "error"}
              }
            }
          }
        }
      }
    }

下表列出了搜索有效负载转换的所有可用设置：

**表 87.搜索有效负载转换设置**

姓名 |必填 |默认 |描述 ---|---|---|--- 'request.search_type'

|

no

|

query_then_fetch

|

搜索类型。   'request.index'

|

no

|

所有指数

|

要搜索的一个或多个索引。   '请求.正文'

|

no

|

"match_all"查询

|

请求的正文。请求正文遵循通常在 REST "_search"请求正文中发送的相同结构。正文可以是静态文本或包含"胡须"模板。   'request.indices_options.expand_wildcards'

|

no

|

`open`

|

确定如何展开索引通配符。由"开放"、"封闭"和"隐藏"组合组成的数组。或者值为"无"或"全部"。(请参阅多目标语法)"request.indices_options.ignore_unavailable"

|

no

|

`true`

|

一个布尔值，用于确定搜索是否应宽容地忽略不可用的索引(请参阅多目标语法)'request.indices_options.allow_no_indices'

|

no

|

`true`

|

一个布尔值，用于确定在没有解析索引时搜索是否应宽松地返回 noresults(请参阅多目标语法) 'request.template'

|

no

|

-

|

搜索模板的正文。有关详细信息，请参阅配置模板。   "超时"

|

no

|

30s

|

等待搜索 api 调用返回的超时。如果在此时间内未返回任何响应，则搜索有效负载转换将超时并失败。此设置将覆盖默认超时。   ### 模板支持它

搜索有效负载转换支持胡须模板。这可以作为正文定义的一部分，也可以指向现有模板(在文件中定义或作为脚本存储在 Elasticsearch 中)。

例如，以下代码片段显示了引用监视计划时间的搜索：

    
    
    {
      "transform" : {
        "search" : {
          "request" : {
            "indices" : [ "logstash-*" ],
            "body" : {
              "size" : 0,
              "query" : {
                "bool" : {
                  "must" : {
                    "match" : { "priority" : "error"}
                  },
                  "filter" : [
                    {
                      "range" : {
                        "@timestamp" : {
                          "from" : "{{ctx.trigger.scheduled_time}}||-30s",
                          "to" : "{{ctx.trigger.triggered_time}}"
                        }
                      }
                    }
                  ]
                }
              }
            }
          }
        }
      }
    }

模板的模型是提供的"template.params"设置与标准监视执行上下文模型之间的联合。

以下是使用引用所提供参数的模板的示例：

    
    
    {
      "transform" : {
        "search" : {
          "request" : {
            "indices" : [ "logstash-*" ],
            "template" : {
              "source" : {
                "size" : 0,
                "query" : {
                  "bool" : {
                    "must" : {
                      "match" : { "priority" : "{{priority}}"}
                    },
                    "filter" : [
                      {
                        "range" : {
                          "@timestamp" : {
                            "from" : "{{ctx.trigger.scheduled_time}}||-30s",
                            "to" : "{{ctx.trigger.triggered_time}}"
                          }
                        }
                      }
                    ]
                  }
                },
                "params" : {
                  "priority" : "error"
                }
              }
            }
          }
        }
      }
    }

[« Payload transforms](transform.md) [Watcher script payload transform
»](transform-script.md)
