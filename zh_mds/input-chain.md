

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher inputs](input.md)

[« Watcher HTTP input](input-http.md) [Watcher triggers »](trigger.md)

## 观察者链输入

触发监视时，使用"链"输入将来自多个源的数据加载到监视执行上下文中。链中的输入按顺序处理，输入加载的数据可以通过链中的后续输入访问。

"链"输入使您能够根据来自多个源的数据执行操作。您还可以使用一个输入收集的数据从另一个源加载数据。

例如，以下链输入使用"简单"输入设置的路径从 HTTP 服务器加载数据：

    
    
    "input" : {
      "chain" : {
        "inputs" : [ __{
            "first" : {
              "simple" : { "path" : "/_search" }
            }
          },
          {
            "second" : {
              "http" : {
                "request" : {
                  "host" : "localhost",
                  "port" : 9200,
                  "path" : "{{ctx.payload.first.path}}" __}
              }
            }
          }
        ]
      }
    }

__

|

链中的输入被指定为数组，以保证处理输入的顺序。(JSON 不保证任意对象的顺序。   ---|---    __

|

加载由"第一个"输入设置的"路径"。   ### 访问链式输入数据编辑

要引用特定输入加载的数据，请使用输入的名称'ctx.payload。<input-name>.<value>'。

### 转换链式输入数据

在某些用例中，第一个输入的输出应用作后续输入的输入。这要求您在将数据传递到下一个输入之前进行转换。

为了实现这一点，您可以在两个指定的输入之间使用转换输入，请参阅以下示例。请注意，第一个输入仍将以原始形式在"ctx.payload.first"中提供。

    
    
    "input" : {
      "chain" : {
        "inputs" : [ __{
            "first" : {
              "simple" : { "path" : "/_search" }
            }
          },
          {
            "second" : {
              "transform" : {
                "script" : "return [ 'path' : ctx.payload.first.path + '/' ]"
              }
            }
          },
          {
            "third" : {
              "http" : {
                "request" : {
                  "host" : "localhost",
                  "port" : 9200,
                  "path" : "{{ctx.payload.second.path}}" __}
              }
            }
          }
        ]
      }
    }

[« Watcher HTTP input](input-http.md) [Watcher triggers »](trigger.md)
