

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md) ›[Common scripting use cases](common-
script-uses.md)

[« Common scripting use cases](common-script-uses.md) [Accessing document
fields and special variables »](modules-scripting-fields.md)

## 字段提取

现场提取的目标很简单;数据中的字段包含大量信息，但您只想提取片段和零件。

有两种选择供您使用：

* Grok 是一种正则表达式方言，支持可重复使用的别名表达式。由于 Grok 位于正则表达式 (regex) 之上，因此任何正则表达式在 grok 中也有效。  * 剖析从文本中提取结构化字段，使用分隔符定义匹配模式。与 grok 不同，dissect 不使用正则表达式。

让我们从一个简单的示例开始，将"@timestamp"和"消息"字段作为索引字段添加到"my-index"映射中。为了保持灵活性，请使用"通配符"作为"消息"的字段类型：

    
    
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

映射要检索的字段后，将日志数据中的一些记录索引到 Elasticsearch 中。以下请求使用批量 API 将原始日志数据索引到"my-index"中。您可以使用一个小样本来试验运行时字段，而不是为所有日志数据编制索引。

    
    
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

#### 从日志消息中提取 IP 地址(Grok)

如果要检索包含"clientip"的结果，可以将该字段添加为映射中的运行时字段。以下运行时脚本定义了从"消息"字段中提取结构化字段的 grok 模式。

该脚本与"%{COMMONAPACHELOG}"日志模式匹配，该模式理解Apache日志的结构。如果模式匹配('clientip ！= null')，脚本将发出匹配 IP 地址的值。如果模式不匹配，脚本只会返回字段值而不会崩溃。

    
    
    PUT my-index/_mappings
    {
      "runtime": {
        "http.clientip": {
          "type": "ip",
          "script": """
            String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
            if (clientip != null) emit(clientip); __"""
        }
      }
    }

__

|

此条件可确保即使消息的模式不匹配，脚本也不会发出任何内容。   ---|--- 您可以定义一个简单的查询来运行对特定 IP 地址的搜索并返回所有相关字段。使用搜索 API 的"字段"参数检索"http.clientip"运行时字段。

    
    
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

响应包括"http.clientip"的值与"40.135.0.0"匹配的文档。

    
    
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
            "_id" : "Rq-ex3gBA_A0V6dYGLQ7",
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

#### 解析字符串以提取部分字段(剖析)

而不是像前面的例子那样在日志模式上匹配")，你可以只定义一个剖析模式来包含你想要丢弃的字符串部分。

例如，本节开头的日志数据包括"消息"字段。此字段包含几条数据：

    
    
    "message" : "247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"

您可以在运行时字段中定义剖析模式以提取 HTTPresponse 代码，即上例中的"304"。

    
    
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

然后，您可以使用"http.response"运行时字段运行查询以检索特定的 HTTP 响应：

    
    
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

响应包括一个文档，其中 HTTP 响应为"304"：

    
    
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
            "_id" : "Sq-ex3gBA_A0V6dYGLQ7",
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

#### 通过分隔符拆分字段中的值(剖析)

假设您想像上一个示例一样提取字段的一部分，但您想拆分特定值。可以使用剖析模式仅提取所需的信息，并以特定格式返回该数据。

例如，假设您有一堆来自 Elasticsearch 的垃圾回收 (gc) 日志数据，格式如下：

    
    
    [2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]   class space    used 266K, capacity 384K, committed 384K, reserved 1048576K

您只想提取"已用"、"容量"和"已提交"数据以及关联的值。让我们索引一些包含日志数据的文档作为示例：

    
    
    response = client.bulk(
      index: 'my-index',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          gc: '[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]   class space    used 266K, capacity 384K, committed 384K, reserved 1048576K'
        },
        {
          index: {}
        },
        {
          gc: '[2021-03-24T20:27:24.184+0000][90239][gc,heap,exit]   class space    used 15255K, capacity 16726K, committed 16844K, reserved 1048576K'
        },
        {
          index: {}
        },
        {
          gc: '[2021-03-24T20:27:24.184+0000][90239][gc,heap,exit]  Metaspace       used 115409K, capacity 119541K, committed 120248K, reserved 1153024K'
        },
        {
          index: {}
        },
        {
          gc: '[2021-04-19T15:03:21.735+0000][84408][gc,heap,exit]   class space    used 14503K, capacity 15894K, committed 15948K, reserved 1048576K'
        },
        {
          index: {}
        },
        {
          gc: '[2021-04-19T15:03:21.735+0000][84408][gc,heap,exit]  Metaspace       used 107719K, capacity 111775K, committed 112724K, reserved 1146880K'
        },
        {
          index: {}
        },
        {
          gc: '[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]  class space  used 266K, capacity 367K, committed 384K, reserved 1048576K'
        }
      ]
    )
    puts response
    
    
    POST /my-index/_bulk?refresh
    {"index":{}}
    {"gc": "[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]   class space    used 266K, capacity 384K, committed 384K, reserved 1048576K"}
    {"index":{}}
    {"gc": "[2021-03-24T20:27:24.184+0000][90239][gc,heap,exit]   class space    used 15255K, capacity 16726K, committed 16844K, reserved 1048576K"}
    {"index":{}}
    {"gc": "[2021-03-24T20:27:24.184+0000][90239][gc,heap,exit]  Metaspace       used 115409K, capacity 119541K, committed 120248K, reserved 1153024K"}
    {"index":{}}
    {"gc": "[2021-04-19T15:03:21.735+0000][84408][gc,heap,exit]   class space    used 14503K, capacity 15894K, committed 15948K, reserved 1048576K"}
    {"index":{}}
    {"gc": "[2021-04-19T15:03:21.735+0000][84408][gc,heap,exit]  Metaspace       used 107719K, capacity 111775K, committed 112724K, reserved 1146880K"}
    {"index":{}}
    {"gc": "[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]  class space  used 266K, capacity 367K, committed 384K, reserved 1048576K"}

再次查看数据，有一个时间戳，一些您不感兴趣的其他数据，然后是"已用"、"容量"和"已提交"数据：

    
    
    [2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]   class space    used 266K, capacity 384K, committed 384K, reserved 1048576K

您可以在"gc"字段中为数据的每个部分分配变量，然后仅返回所需的部分。大括号"{}"中的任何内容都被视为变量。例如，变量 '[%{@timestamp}][%{code}][%{desc}]' 将匹配前三个数据块，所有这些数据块都位于方括号 '[]' 中。

    
    
    [%{@timestamp}][%{code}][%{desc}]  %{ident} used %{usize}, capacity %{csize}, committed %{comsize}, reserved %{rsize}

剖析模式可以包含术语"已使用"、"容量"和"已提交"，而不是使用变量，因为您希望准确返回这些术语。还可以将变量分配给要返回的值，例如"%{usize}"、"%{csize}"和"%{comsize}"。日志数据中的分隔符是逗号，因此剖析模式也需要使用该分隔符。

现在您已经有了剖析模式，您可以将其包含在运行时字段的无痛脚本中。该脚本使用剖析模式拆分"gc"字段，然后准确返回所需的信息，由"emit"方法定义。因为 dissect 使用简单的语法，所以你只需要准确地告诉它你想要什么。

以下模式告诉 dissect 返回术语"used"、空格、"gc.usize"中的值和逗号。此模式对要检索的其他数据重复。虽然此模式可能没有那么有用的生产，但它提供了很大的灵活性来试验和操作数据。在生产环境中，您可能只想使用"emit(gc.usize)"，然后聚合该值或在计算中使用它。

    
    
    emit("used" + ' ' + gc.usize + ', ' + "capacity" + ' ' + gc.csize + ', ' + "committed" + ' ' + gc.comsize)

综上所述，您可以在搜索请求中创建一个名为"gc_size"的运行时字段。使用"字段"选项，您可以检索"gc_size"运行时字段的所有值。此查询还包括用于对数据进行分组的存储桶聚合。

    
    
    GET my-index/_search
    {
      "runtime_mappings": {
        "gc_size": {
          "type": "keyword",
          "script": """
            Map gc=dissect('[%{@timestamp}][%{code}][%{desc}]  %{ident} used %{usize}, capacity %{csize}, committed %{comsize}, reserved %{rsize}').extract(doc["gc.keyword"].value);
            if (gc != null) emit("used" + ' ' + gc.usize + ', ' + "capacity" + ' ' + gc.csize + ', ' + "committed" + ' ' + gc.comsize);
          """
        }
      },
      "size": 1,
      "aggs": {
        "sizes": {
          "terms": {
            "field": "gc_size",
            "size": 10
          }
        }
      },
      "fields" : ["gc_size"]
    }

响应包括来自"gc_size"字段的数据，其格式与您在剖析模式中定义的格式完全相同！

    
    
    {
      "took" : 2,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 6,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index",
            "_id" : "GXx3H3kBKGE42WRNlddJ",
            "_score" : 1.0,
            "_source" : {
              "gc" : "[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]   class space    used 266K, capacity 384K, committed 384K, reserved 1048576K"
            },
            "fields" : {
              "gc_size" : [
                "used 266K, capacity 384K, committed 384K"
              ]
            }
          }
        ]
      },
      "aggregations" : {
        "sizes" : {
          "doc_count_error_upper_bound" : 0,
          "sum_other_doc_count" : 0,
          "buckets" : [
            {
              "key" : "used 107719K, capacity 111775K, committed 112724K",
              "doc_count" : 1
            },
            {
              "key" : "used 115409K, capacity 119541K, committed 120248K",
              "doc_count" : 1
            },
            {
              "key" : "used 14503K, capacity 15894K, committed 15948K",
              "doc_count" : 1
            },
            {
              "key" : "used 15255K, capacity 16726K, committed 16844K",
              "doc_count" : 1
            },
            {
              "key" : "used 266K, capacity 367K, committed 384K",
              "doc_count" : 1
            },
            {
              "key" : "used 266K, capacity 384K, committed 384K",
              "doc_count" : 1
            }
          ]
        }
      }
    }

[« Common scripting use cases](common-script-uses.md) [Accessing document
fields and special variables »](modules-scripting-fields.md)
