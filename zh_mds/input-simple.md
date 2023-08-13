

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher inputs](input.md)

[« Watcher inputs](input.md) [Watcher search input »](input-search.md)

## 观察程序简单输入

使用"简单"输入在触发监视时将静态数据加载到执行上下文中。这使您能够集中存储数据并使用模板引用数据。

您可以将静态数据定义为字符串("str")，数值("num")，oran对象("obj")：

    
    
    "input" : {
      "simple" : {
        "str" : "val1",
        "num" : 23,
        "obj" : {
          "str" : "val2"
        }
      }
    }

例如，以下手表使用"简单"输入来设置每日提醒电子邮件的收件人姓名：

    
    
    {
      "trigger" : {
        "schedule" : {
          "daily" : { "at" : "noon" }
        }
      },
      "input" : {
        "simple" : {
          "name" : "John"
        }
      },
      "actions" : {
        "reminder_email" : {
          "email" : {
            "to" : "to@host.domain",
            "subject" : "Reminder",
            "body" : "Dear {{ctx.payload.name}}, by the time you read these lines, I'll be gone"
          }
        }
      }
    }

[« Watcher inputs](input.md) [Watcher search input »](input-search.md)
