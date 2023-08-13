

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md) ›[How to write scripts](modules-
scripting-using.md)

[« Scripts, caching, and search speed](scripts-and-search-speed.md)
[Grokking grok »](grok.md)

## 剖析数据

剖析将单个文本字段与定义的模式进行匹配。剖析模式由要丢弃的字符串部分定义。特别注意字符串的每个部分有助于建立成功的剖析模式。

如果您不需要正则表达式的强大功能，请使用剖析模式而不是 grok。Dissect 使用的语法比 grok 简单得多，并且总体上通常更快。dissect 的语法是透明的：告诉 dissect 你想要什么，它会把这些结果返回给你。

### 剖析模式

剖析模式由变量和分隔符组成。由百分号和大括号"%{}"定义的任何内容都被视为变量，例如"%{clientip}"。您可以将变量分配给字段中数据的任何部分，然后仅返回所需的部分。分隔符是变量之间的任何值，可以是空格、短划线或其他分隔符。

例如，假设您有日志数据，其中包含如下所示的"消息"字段：

    
    
    "message" : "247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"

您将变量分配给数据的每个部分以构建成功的剖析模式。记住，准确地告诉剖析你想要匹配的内容。

数据的第一部分看起来像一个 IP 地址，因此您可以分配一个变量，例如"%{clientip}"。接下来的两个字符是破折号，两侧各有一个空格。您可以为每个短划线分配一个变量，也可以为单个变量指定一个变量来表示短划线和空格。接下来是一组包含时间戳的括号。括号是分隔符，因此您可以在剖析模式中包含括号。到目前为止，数据和匹配的剖析模式如下所示：

    
    
    247.37.0.0 - - [30/Apr/2020:14:31:22 -0500]  __%{clientip} %{ident} %{auth} [%{@timestamp}] __

__

|

"消息"字段中的第一个数据块---|---__

|

剖析模式以匹配所选数据块 使用相同的逻辑，您可以为剩余的数据块创建变量。双引号是分隔符，因此请在剖析模式中包含这些分隔符。该模式将"GET"替换为"%{verb}"变量，但保留"HTTP"作为模式的一部分。

    
    
    \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0
    
    "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}

将这两种模式结合起来会产生如下所示的剖析模式：

    
    
    %{clientip} %{ident} %{auth} [%{@timestamp}] \"%{verb} %{request} HTTP/%{httpversion}\" %{status} %{size}

现在您已经有了剖析模式，如何测试和使用它？

### 测试解剖模式无痛

您可以将剖析模式合并到无痛脚本中以提取数据。要测试脚本，请使用无痛执行 API 的字段上下文或创建包含脚本的运行时字段。运行时字段提供了更大的灵活性并接受多个文档，但如果您在重新测试脚本的集群上没有写入访问权限，则 Painless executeAPI 是一个不错的选择。

例如，使用无痛执行 API 测试剖析模式，方法是包括无痛脚本和与数据匹配的单个文档。首先将"消息"字段索引为"通配符"数据类型：

    
    
    response = client.indices.create(
      index: 'my-index',
      body: {
        mappings: {
          properties: {
            message: {
              type: 'wildcard'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index
    {
      "mappings": {
        "properties": {
          "message": {
            "type": "wildcard"
          }
        }
      }
    }

如果要检索 HTTP 响应代码，请将剖析模式添加到提取"响应"值的无痛脚本中。要从字段中提取值，请使用以下函数：

    
    
    `.extract(doc["<field_name>"].value)?.<field_value>`

在此示例中，"消息"是"，"<field_name>响应"是"<field_value>：

    
    
    POST /_scripts/painless/_execute
    {
      "script": {
        "source": """
          String response=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}').extract(doc["message"].value)?.response;
            if (response != null) emit(Integer.parseInt(response)); __"""
      },
      "context": "long_field", __"context_setup": {
        "index": "my-index",
        "document": { __"message": """247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] "GET /images/hm_nbg.jpg HTTP/1.0" 304 0"""
        }
      }
    }

__

|

运行时字段需要"emit"方法返回值。   ---|---    __

|

由于响应代码是整数，因此请使用"long_field"上下文。   __

|

包括与数据匹配的示例文档。   结果包括 HTTP 响应代码：

    
    
    {
      "result" : [
        304
      ]
    }

### 在运行时字段中使用剖析模式和脚本

如果您有功能剖析模式，则可以将其添加到运行时字段以操作数据。由于运行时字段不需要您为字段编制索引，因此您可以非常灵活地修改脚本及其功能。如果您已经使用无痛执行 API 测试了剖析模式，则可以在运行时字段中使用该 _exact_ 无痛脚本。

首先，将"消息"字段添加为"通配符"类型，如上一节所述，但也添加"@timestamp"作为"日期"，以防您想对该字段进行操作用于其他用例：

    
    
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

如果要使用剖析模式提取 HTTP 响应代码，可以创建一个运行时字段，例如 'http.response'：

    
    
    PUT my-index/_mappings
    {
      "runtime": {
        "http.response": {
          "type": "long",
          "script": """
            String response=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}').extract(doc["message"].value)?.response;
            if (response != null) emit(Integer.parseInt(response));
          """
        }
      }
    }

映射要检索的字段后，将日志数据中的一些记录索引到 Elasticsearch 中。以下请求使用批量 API 将原始日志数据索引到"my-index"中：

    
    
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
    
    
    POST /my-index/_bulk?refresh=true
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

您可以定义一个简单的查询来运行对特定 HTTP 响应的搜索并返回所有相关字段。使用搜索 API 的"字段"参数检索"http.response"运行时字段。

    
    
    response = client.search(
      index: 'my-index',
      body: {
        query: {
          match: {
            "http.response": '304'
          }
        },
        fields: [
          'http.response'
        ]
      }
    )
    puts response
    
    
    GET my-index/_search
    {
      "query": {
        "match": {
          "http.response": "304"
        }
      },
      "fields" : ["http.response"]
    }

或者，您可以在搜索请求的上下文中定义相同的运行时字段。运行时定义和脚本与之前在索引映射中定义的完全相同。只需将该定义复制到"runtime_mappings"部分下的搜索请求中，并包含与运行时字段匹配的查询。此查询返回的结果与之前在索引映射中为 'http.response' 运行时字段定义的搜索查询相同，但仅在此特定搜索的上下文中：

    
    
    GET my-index/_search
    {
      "runtime_mappings": {
        "http.response": {
          "type": "long",
          "script": """
            String response=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}').extract(doc["message"].value)?.response;
            if (response != null) emit(Integer.parseInt(response));
          """
        }
      },
      "query": {
        "match": {
          "http.response": "304"
        }
      },
      "fields" : ["http.response"]
    }
    
    
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
            "_id" : "D47UqXkBByC8cgZrkbOm",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : "2020-04-30T14:31:22-05:00",
              "message" : "247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"
            },
            "fields" : {
              "http.response" : [
                304
              ]
            }
          }
        ]
      }
    }

[« Scripts, caching, and search speed](scripts-and-search-speed.md)
[Grokking grok »](grok.md)
