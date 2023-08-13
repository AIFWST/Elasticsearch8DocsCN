

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Runtime fields](runtime.md)

[« Index a runtime field](runtime-indexed.md) [Field data types »](mapping-
types.md)

## 使用运行时字段浏览数据

考虑要从中提取字段的大量日志数据。为数据编制索引非常耗时且会占用大量磁盘空间，您只想探索数据结构，而无需预先提交架构。

您知道日志数据包含要提取的特定字段。在这种情况下，我们希望关注"@timestamp"和"消息"字段。通过使用运行时字段，您可以定义脚本以在搜索时计算这些字段的值。

### 将索引字段定义为起点

您可以从一个简单的示例开始，将"@timestamp"和"消息"字段作为索引字段添加到"my-index-000001"映射中。为了保持灵活性，请使用"通配符"作为"消息"的字段类型：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
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
    
    
    PUT /my-index-000001/
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

### 摄取一些数据

映射要检索的字段后，将日志数据中的一些记录索引到 Elasticsearch 中。以下请求使用批量 API 将原始日志数据索引到"my-index-000001"中。您可以使用一个小样本来试验运行时字段，而不是为所有日志数据编制索引。

最终文档不是有效的 Apache 日志格式，但我们可以在脚本中说明这种情况。

    
    
    response = client.bulk(
      index: 'my-index-000001',
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
    
    
    POST /my-index-000001/_bulk?refresh
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

此时，您可以查看 Elasticsearch 如何存储原始数据。

    
    
    response = client.indices.get(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001

映射包含两个字段："@timestamp"和"消息"。

    
    
    {
      "my-index-000001" : {
        "aliases" : { },
        "mappings" : {
          "properties" : {
            "@timestamp" : {
              "type" : "date",
              "format" : "strict_date_optional_time||epoch_second"
            },
            "message" : {
              "type" : "wildcard"
            },
            "timestamp" : {
              "type" : "date"
            }
          }
        },
        ...
      }
    }

### 使用 grokpattern 定义运行时字段

如果要检索包含"clientip"的结果，可以将该字段添加为映射中的运行时字段。以下运行时脚本定义了一个 grok 模式，该模式从文档中的单个文本字段中提取结构化字段。grok 模式类似于支持可重用的别名表达式的正则表达式。

该脚本与"%{COMMONAPACHELOG}"日志模式匹配，该模式理解Apache日志的结构。如果模式匹配('clientip ！= null')，脚本将发出匹配 IP 地址的值。如果模式不匹配，脚本只会返回字段值而不会崩溃。

    
    
    PUT my-index-000001/_mappings
    {
      "runtime": {
        "http.client_ip": {
          "type": "ip",
          "script": """
            String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
            if (clientip != null) emit(clientip); __"""
        }
      }
    }

__

|

此条件可确保即使消息的模式不匹配，脚本也不会崩溃。   ---|--- 或者，您可以在搜索请求的上下文中定义相同的运行时字段。运行时定义和脚本与之前在索引映射中定义的完全相同。只需将该定义复制到"runtime_mappings"部分下的搜索请求中，并包含与运行时字段匹配的查询。此查询返回的结果与您在索引映射中为"http.clientip"运行时字段定义搜索查询的结果相同，但仅在此特定搜索的上下文中：

    
    
    GET my-index-000001/_search
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

### 定义复合运行时字段

您还可以定义 _composite_ 运行时字段以从单个脚本发出多个字段。您可以定义一组类型化子字段并发出值映射。在搜索时，每个子字段都会检索与其在地图中的名称关联的值。这意味着您只需要指定一次 grokpattern 并可以返回多个值：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        runtime: {
          http: {
            type: 'composite',
            script: 'emit(grok("%<COMMONAPACHELOG>s").extract(doc["message"].value))',
            fields: {
              clientip: {
                type: 'ip'
              },
              verb: {
                type: 'keyword'
              },
              response: {
                type: 'long'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_mappings
    {
      "runtime": {
        "http": {
          "type": "composite",
          "script": "emit(grok(\"%{COMMONAPACHELOG}\").extract(doc[\"message\"].value))",
          "fields": {
            "clientip": {
              "type": "ip"
            },
            "verb": {
              "type": "keyword"
            },
            "response": {
              "type": "long"
            }
          }
        }
      }
    }

#### 搜索特定 IP 地址

使用"http.clientip"运行时字段，您可以定义一个简单的查询来运行搜索特定 IP 地址并返回所有相关字段。

    
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "http.clientip": "40.135.0.0"
        }
      },
      "fields" : ["*"]
    }

API 返回以下结果。由于"http"是"复合"运行时字段，因此响应包括"fields"下的每个子字段，包括与查询匹配的任何关联值。无需提前构建数据结构，即可以有意义的方式搜索和浏览数据，以试验并确定要编制索引的字段。

    
    
    {
      ...
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "sRVHBnwBB-qjgFni7h_O",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : "2020-04-30T14:30:17-05:00",
              "message" : "40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
            },
            "fields" : {
              "http.verb" : [
                "GET"
              ],
              "http.clientip" : [
                "40.135.0.0"
              ],
              "http.response" : [
                200
              ],
              "message" : [
                "40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
              ],
              "http.client_ip" : [
                "40.135.0.0"
              ],
              "timestamp" : [
                "2020-04-30T19:30:17.000Z"
              ]
            }
          }
        ]
      }
    }

另外，还记得脚本中的"if"语句吗？

    
    
    if (clientip != null) emit(clientip);

如果脚本不包含此条件，则查询将在与模式不匹配的任何分片上失败。通过包含此条件，查询将跳过与 grok 模式不匹配的数据。

#### 在特定范围内搜索文档

您还可以运行对"时间戳"字段进行操作的范围查询。以下查询返回"时间戳"大于或等于"2020-04-30T14：31：27-05：00"的任何文档：

    
    
    GET my-index-000001/_search
    {
      "query": {
        "range": {
          "timestamp": {
            "gte": "2020-04-30T14:31:27-05:00"
          }
        }
      }
    }

响应包括日志格式不匹配但时间戳在定义范围内的文档。

    
    
    {
      ...
      "hits" : {
        "total" : {
          "value" : 2,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "hdEhyncBRSB6iD-PoBqe",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : "2020-04-30T14:31:27-05:00",
              "message" : "252.0.0.0 - - [30/Apr/2020:14:31:27 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
            }
          },
          {
            "_index" : "my-index-000001",
            "_id" : "htEhyncBRSB6iD-PoBqe",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : "2020-04-30T14:31:28-05:00",
              "message" : "not a valid apache log"
            }
          }
        ]
      }
    }

### 使用剖析模式定义运行时字段

如果您不需要正则表达式的强大功能，则可以使用剖析模式而不是 grokpatterns。剖析模式在固定分隔符上匹配，但通常比 grok 快。

您可以使用 dissect 来获得与解析具有 grok 模式的 Apache 日志相同的结果。不是在日志模式上进行匹配，而是包含要丢弃的字符串部分。特别注意要丢弃的字符串部分将有助于构建成功的剖析模式。

    
    
    PUT my-index-000001/_mappings
    {
      "runtime": {
        "http.client.ip": {
          "type": "ip",
          "script": """
            String clientip=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{status} %{size}').extract(doc["message"].value)?.clientip;
            if (clientip != null) emit(clientip);
          """
        }
      }
    }

同样，您可以定义剖析模式来提取 HTTP 响应代码：

    
    
    PUT my-index-000001/_mappings
    {
      "runtime": {
        "http.responses": {
          "type": "long",
          "script": """
            String response=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}').extract(doc["message"].value)?.response;
            if (response != null) emit(Integer.parseInt(response));
          """
        }
      }
    }

然后，您可以使用"http.responses"运行时字段运行查询以检索特定的 HTTP 响应。使用"_search"请求的"字段"参数来指示要检索的字段：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            "http.responses": '304'
          }
        },
        fields: [
          'http.client_ip',
          'timestamp',
          'http.verb'
        ]
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "http.responses": "304"
        }
      },
      "fields" : ["http.client_ip","timestamp","http.verb"]
    }

响应包括一个文档，其中 HTTP 响应为"304"：

    
    
    {
      ...
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "A2qDy3cBWRMvVAuI7F8M",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : "2020-04-30T14:31:22-05:00",
              "message" : "247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"
            },
            "fields" : {
              "http.verb" : [
                "GET"
              ],
              "http.client_ip" : [
                "247.37.0.0"
              ],
              "timestamp" : [
                "2020-04-30T19:31:22.000Z"
              ]
            }
          }
        ]
      }
    }

[« Index a runtime field](runtime-indexed.md) [Field data types »](mapping-
types.md)
