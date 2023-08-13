

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« Watcher Jira action](actions-jira.md) [Watcher search payload transform
»](transform-search.md)

## 有效负载转换

_payload transform_处理和更改监视执行上下文中的有效负载，以便为监视操作做好准备。观察程序支持三种类型的有效负载转换：

* "搜索" * "脚本" * "链"

有效负载转换是可选的。如果未定义任何内容，则操作有权访问监视输入加载的有效负载。

您可以在两个位置定义有效负载转换：

* 作为监视定义中的顶级构造。在这种情况下，在执行任何监视操作之前转换有效负载。  * 作为操作定义的一部分。在这种情况下，将在执行该操作之前转换有效负载。转换仅应用于该特定操作的有效负载。

如果所有操作都需要相同的有效负载视图，请将有效负载转换定义为监视定义的一部分。如果每个操作都需要不同的有效负载视图，请将不同的有效负载转换定义为操作定义的一部分，以便每个操作都有由其自己的专用有效负载转换准备的有效负载。

以下示例定义了两个有效负载转换，一个在监视级别，另一个作为"my_webhook"操作定义的一部分。

    
    
    {
      "trigger" : { ...}
      "input" : { ... },
      "condition" : { ... },
      "transform" : { __"search" : {
          "request": {
            "body" : { "query" : { "match_all" : {} } }
          }
        }
      },
      "actions" : {
        "my_webhook": {
          "transform" : { __"script" : "return ctx.payload.hits"
          },
          "webhook" : {
          	"host" : "host.domain",
          	"port" : 8089,
          	"path" : "/notify/{{ctx.watch_id}}"
          }
        }
      ]
    }

__

|

监视级别"转换"---|--- __

|

操作级别"转换" « 观察者 Jira 操作观察程序搜索有效负载转换»