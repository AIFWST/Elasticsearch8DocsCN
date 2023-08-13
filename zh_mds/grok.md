

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md) ›[How to write scripts](modules-
scripting-using.md)

[« Dissecting data](dissect.md) [Access fields in a document with the
`field` API »](script-fields-api.md)

## 格罗金格罗克

Grok 是一种正则表达式方言，支持可重用的别名表达式。Grok可以很好地处理syslog日志，Apache和其他Web服务器日志，mysql日志，以及通常为人类而不是计算机消费编写的任何日志格式。

Grok 位于 Oniguruma 正则表达式库之上，因此任何正则表达式在 grok 中都是有效的。Grok 使用这种正则表达式语言来命名现有模式，并将它们组合成与您的字段匹配的更复杂的模式。

### 凹槽模式

Elastic Stack 附带了许多预定义的 grokpatterns，可简化 grok 的使用。重用 grokpatterns 的语法采用以下形式之一：

`%{SYNTAX}`

|

`%{SYNTAX:ID}`

|

'%{SYNTAX：ID：TYPE}' ---|---|--- 'SYNTAX'

     The name of the pattern that will match your text. For example, `NUMBER` and `IP` are both patterns that are provided within the default patterns set. The `NUMBER` pattern matches data like `3.44`, and the `IP` pattern matches data like `55.3.244.1`. 
`ID`

     The identifier you give to the piece of text being matched. For example, `3.44` could be the duration of an event, so you might call it `duration`. The string `55.3.244.1` might identify the `client` making a request. 
`TYPE`

     The data type you want to cast your named field. `int`, `long`, `double`, `float` and `boolean` are supported types. 

例如，假设您有如下所示的消息数据：

    
    
    3.44 55.3.244.1

第一个值是一个数字，后跟一个似乎是 IP 地址的值。您可以使用以下 grok 表达式匹配此文本：

    
    
    %{NUMBER:duration} %{IP:client}

### 迁移到弹性云服务器

为了简化向弹性通用模式 (ECS) 的迁移，除了现有模式之外，还提供了一组新的符合 ECS 标准的模式。新的 ECS 模式定义捕获符合架构的事件字段名称。

ECS 模式集具有旧版集中的所有模式定义，是直接替换。使用"ecs 兼容性"设置切换模式。

新功能和增强功能将添加到符合 ECS 的文件中。旧模式可能仍会收到向后兼容的错误修复。

### 在无痛脚本中使用 grok 模式

您可以将预定义的 grok 模式合并到无痛脚本中以提取数据。要测试脚本，请使用无痛执行 API 的字段上下文或创建包含脚本的运行时字段。运行时字段提供了更大的灵活性并接受多个文档，但如果您在重新测试脚本的集群上没有写入访问权限，则 Painless executeAPI 是一个不错的选择。

如果您需要帮助构建 grok 模式以匹配您的数据，请使用 Kibana 中的 GrokDebugger 工具。

例如，如果您正在使用 Apache 日志数据，则可以使用"%{COMMONAPACHELOG}"语法，该语法了解 Apache 日志的结构。示例文档可能如下所示：

    
    
    "timestamp":"2020-04-30T14:30:17-05:00","message":"40.135.0.0 - -
    [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"

要从"消息"字段中提取IP地址，您可以编写一个包含"%{COMMONAPACHELOG}"语法的Painlessscript。您可以使用无痛执行 API 的"ip"字段上下文来测试此脚本，但让我们改用运行时字段。

根据示例文档，为"@timestamp"和"消息"字段编制索引。为了保持灵活性，请使用"通配符"作为"消息"的字段类型：

    
    
    response = client.indices.create(
      index: 'my-index',
      body: {
        mappings: {
          properties: {
            "@timestamp": {
              format: 'strict_date_optional_time||epoch_second',
              type: 'date'
            },
            message: {
              type: 'wildcard'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index/
    {
      "mappings": {
        "properties": {
          "@timestamp": {
            "format": "strict_date_optional_time||epoch_second",
            "type": "date"
          },
          "message": {
            "type": "wildcard"
          }
        }
      }
    }

接下来，使用批量 API 将一些日志数据索引到"my-index"中。

    
    
    response = client.bulk(
      index: 'my-index',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          timestamp: '2020-04-30T14:30:17-05:00',
          message: '40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] "GET /images/hm_bg.jpg HTTP/1.0" 200 24736'
        },
        {
          index: {}
        },
        {
          timestamp: '2020-04-30T14:30:53-05:00',
          message: '232.0.0.0 - - [30/Apr/2020:14:30:53 -0500] "GET /images/hm_bg.jpg HTTP/1.0" 200 24736'
        },
        {
          index: {}
        },
        {
          timestamp: '2020-04-30T14:31:12-05:00',
          message: '26.1.0.0 - - [30/Apr/2020:14:31:12 -0500] "GET /images/hm_bg.jpg HTTP/1.0" 200 24736'
        },
        {
          index: {}
        },
        {
          timestamp: '2020-04-30T14:31:19-05:00',
          message: '247.37.0.0 - - [30/Apr/2020:14:31:19 -0500] "GET /french/splash_inet.html HTTP/1.0" 200 3781'
        },
        {
          index: {}
        },
        {
          timestamp: '2020-04-30T14:31:22-05:00',
          message: '247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] "GET /images/hm_nbg.jpg HTTP/1.0" 304 0'
        },
        {
          index: {}
        },
        {
          timestamp: '2020-04-30T14:31:27-05:00',
          message: '252.0.0.0 - - [30/Apr/2020:14:31:27 -0500] "GET /images/hm_bg.jpg HTTP/1.0" 200 24736'
        },
        {
          index: {}
        },
        {
          timestamp: '2020-04-30T14:31:28-05:00',
          message: 'not a valid apache log'
        }
      ]
    )
    puts response
    
    
    POST /my-index/_bulk?refresh
    {"index":{}}
    {"timestamp":"2020-04-30T14:30:17-05:00","message":"40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
    {"index":{}}
    {"timestamp":"2020-04-30T14:30:53-05:00","message":"232.0.0.0 - - [30/Apr/2020:14:30:53 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
    {"index":{}}
    {"timestamp":"2020-04-30T14:31:12-05:00","message":"26.1.0.0 - - [30/Apr/2020:14:31:12 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
    {"index":{}}
    {"timestamp":"2020-04-30T14:31:19-05:00","message":"247.37.0.0 - - [30/Apr/2020:14:31:19 -0500] \"GET /french/splash_inet.html HTTP/1.0\" 200 3781"}
    {"index":{}}
    {"timestamp":"2020-04-30T14:31:22-05:00","message":"247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"}
    {"index":{}}
    {"timestamp":"2020-04-30T14:31:27-05:00","message":"252.0.0.0 - - [30/Apr/2020:14:31:27 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
    {"index":{}}
    {"timestamp":"2020-04-30T14:31:28-05:00","message":"not a valid apache log"}

### 在运行时字段中合并 grok 模式和脚本

现在，您可以在映射中定义一个运行时字段，其中包含您的 Painlessscript 和 grok 模式。如果模式匹配，脚本将发出匹配 IP 地址的值。如果模式不匹配('clientip ！= null')，脚本只返回字段值而不会崩溃。

    
    
    PUT my-index/_mappings
    {
      "runtime": {
        "http.clientip": {
          "type": "ip",
          "script": """
            String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
            if (clientip != null) emit(clientip);
          """
        }
      }
    }

或者，您可以在搜索请求的上下文中定义相同的运行时字段。运行时定义和脚本与之前在索引映射中定义的完全相同。只需将该定义复制到"runtime_mappings"部分下的搜索请求中，并包含与运行时字段匹配的查询。此查询返回的结果与您在索引映射中为"http.clientip"运行时字段定义搜索查询的结果相同，但仅在此特定搜索的上下文中：

    
    
    GET my-index/_search
    {
      "runtime_mappings": {
        "http.clientip": {
          "type": "ip",
          "script": """
            String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
            if (clientip != null) emit(clientip);
          """
        }
      },
      "query": {
        "match": {
          "http.clientip": "40.135.0.0"
        }
      },
      "fields" : ["http.clientip"]
    }

### 返回计算结果

使用"http.clientip"运行时字段，您可以定义一个简单的查询来运行搜索特定 IP 地址并返回所有相关字段。"_search"API 上的"字段"参数适用于所有字段，即使是那些未作为原始"_source"的一部分发送的字段：

    
    
    response = client.search(
      index: 'my-index',
      body: {
        query: {
          match: {
            "http.clientip": '40.135.0.0'
          }
        },
        fields: [
          'http.clientip'
        ]
      }
    )
    puts response
    
    
    GET my-index/_search
    {
      "query": {
        "match": {
          "http.clientip": "40.135.0.0"
        }
      },
      "fields" : ["http.clientip"]
    }

响应包括搜索查询中指示的特定 IP 地址。Painless 脚本中的 grok 模式在运行时从"消息"字段中提取此值。

    
    
    {
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index",
            "_id" : "1iN2a3kBw4xTzEDqyYE0",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : "2020-04-30T14:30:17-05:00",
              "message" : "40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
            },
            "fields" : {
              "http.clientip" : [
                "40.135.0.0"
              ]
            }
          }
        ]
      }
    }

[« Dissecting data](dissect.md) [Access fields in a document with the
`field` API »](script-fields-api.md)
