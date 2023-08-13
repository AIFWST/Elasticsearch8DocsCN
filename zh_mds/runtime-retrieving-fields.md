

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Runtime fields](runtime.md)

[« Override field values at query time](runtime-override-values.md) [Index a
runtime field »](runtime-indexed.md)

## 检索运行时字段

使用"_search"API 上的"字段"参数检索运行时字段的值。运行时字段不会显示在"_source"中，但"字段"API 适用于所有字段，即使是那些不是作为原始"_source"的一部分发送的字段。

### 定义运行时字段以计算星期几

例如，以下请求添加一个名为"day_of_week"的运行时字段。运行时字段包含一个脚本，该脚本根据"@timestamp"字段的值计算星期几。我们将在请求中包含"动态"："运行时"，以便将新字段作为运行时字段添加到映射中。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic: 'runtime',
          runtime: {
            day_of_week: {
              type: 'keyword',
              script: {
                source: "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
              }
            }
          },
          properties: {
            "@timestamp": {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/
    {
      "mappings": {
        "dynamic": "runtime",
        "runtime": {
          "day_of_week": {
            "type": "keyword",
            "script": {
              "source": "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
            }
          }
        },
        "properties": {
          "@timestamp": {"type": "date"}
        }
      }
    }

### 摄取一些数据

让我们引入一些示例数据，这将产生两个索引字段："@timestamp"和"消息"。

    
    
    response = client.bulk(
      index: 'my-index-000001',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          "@timestamp": '2020-06-21T15:00:01-05:00',
          message: '211.11.9.0 - - [2020-06-21T15:00:01-05:00] "GET /english/index.html HTTP/1.0" 304 0'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-06-21T15:00:01-05:00',
          message: '211.11.9.0 - - [2020-06-21T15:00:01-05:00] "GET /english/index.html HTTP/1.0" 304 0'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-04-30T14:30:17-05:00',
          message: '40.135.0.0 - - [2020-04-30T14:30:17-05:00] "GET /images/hm_bg.jpg HTTP/1.0" 200 24736'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-04-30T14:30:53-05:00',
          message: '232.0.0.0 - - [2020-04-30T14:30:53-05:00] "GET /images/hm_bg.jpg HTTP/1.0" 200 24736'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-04-30T14:31:12-05:00',
          message: '26.1.0.0 - - [2020-04-30T14:31:12-05:00] "GET /images/hm_bg.jpg HTTP/1.0" 200 24736'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-04-30T14:31:19-05:00',
          message: '247.37.0.0 - - [2020-04-30T14:31:19-05:00] "GET /french/splash_inet.html HTTP/1.0" 200 3781'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-04-30T14:31:27-05:00',
          message: '252.0.0.0 - - [2020-04-30T14:31:27-05:00] "GET /images/hm_bg.jpg HTTP/1.0" 200 24736'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-04-30T14:31:29-05:00',
          message: '247.37.0.0 - - [2020-04-30T14:31:29-05:00] "GET /images/hm_brdl.gif HTTP/1.0" 304 0'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-04-30T14:31:29-05:00',
          message: '247.37.0.0 - - [2020-04-30T14:31:29-05:00] "GET /images/hm_arw.gif HTTP/1.0" 304 0'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-04-30T14:31:32-05:00',
          message: '247.37.0.0 - - [2020-04-30T14:31:32-05:00] "GET /images/nav_bg_top.gif HTTP/1.0" 200 929'
        },
        {
          index: {}
        },
        {
          "@timestamp": '2020-04-30T14:31:43-05:00',
          message: '247.37.0.0 - - [2020-04-30T14:31:43-05:00] "GET /french/images/nav_venue_off.gif HTTP/1.0" 304 0'
        }
      ]
    )
    puts response
    
    
    POST /my-index-000001/_bulk?refresh
    { "index": {}}
    { "@timestamp": "2020-06-21T15:00:01-05:00", "message" : "211.11.9.0 - - [2020-06-21T15:00:01-05:00] \"GET /english/index.html HTTP/1.0\" 304 0"}
    { "index": {}}
    { "@timestamp": "2020-06-21T15:00:01-05:00", "message" : "211.11.9.0 - - [2020-06-21T15:00:01-05:00] \"GET /english/index.html HTTP/1.0\" 304 0"}
    { "index": {}}
    { "@timestamp": "2020-04-30T14:30:17-05:00", "message" : "40.135.0.0 - - [2020-04-30T14:30:17-05:00] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
    { "index": {}}
    { "@timestamp": "2020-04-30T14:30:53-05:00", "message" : "232.0.0.0 - - [2020-04-30T14:30:53-05:00] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
    { "index": {}}
    { "@timestamp": "2020-04-30T14:31:12-05:00", "message" : "26.1.0.0 - - [2020-04-30T14:31:12-05:00] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
    { "index": {}}
    { "@timestamp": "2020-04-30T14:31:19-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:19-05:00] \"GET /french/splash_inet.html HTTP/1.0\" 200 3781"}
    { "index": {}}
    { "@timestamp": "2020-04-30T14:31:27-05:00", "message" : "252.0.0.0 - - [2020-04-30T14:31:27-05:00] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
    { "index": {}}
    { "@timestamp": "2020-04-30T14:31:29-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:29-05:00] \"GET /images/hm_brdl.gif HTTP/1.0\" 304 0"}
    { "index": {}}
    { "@timestamp": "2020-04-30T14:31:29-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:29-05:00] \"GET /images/hm_arw.gif HTTP/1.0\" 304 0"}
    { "index": {}}
    { "@timestamp": "2020-04-30T14:31:32-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:32-05:00] \"GET /images/nav_bg_top.gif HTTP/1.0\" 200 929"}
    { "index": {}}
    { "@timestamp": "2020-04-30T14:31:43-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:43-05:00] \"GET /french/images/nav_venue_off.gif HTTP/1.0\" 304 0"}

### 搜索计算出的星期几

以下请求使用搜索 API 检索"day_of_week"字段，原始请求在映射中定义为运行时字段。此字段的值是在查询时动态计算的，无需重新索引文档或为"day_of_week"字段编制索引。这种灵活性允许您在不更改任何字段值的情况下修改映射。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        fields: [
          '@timestamp',
          'day_of_week'
        ],
        _source: false
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "fields": [
        "@timestamp",
        "day_of_week"
      ],
      "_source": false
    }

上一个请求返回所有匹配文档的"day_of_week"字段。我们可以定义另一个名为 'client_ip' 的运行时字段，该字段也对 'message' 字段进行操作，并将进一步细化查询：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        runtime: {
          client_ip: {
            type: 'ip',
            script: {
              source: 'String m = doc["message"].value; int end = m.indexOf(" "); emit(m.substring(0, end));'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_mapping
    {
      "runtime": {
        "client_ip": {
          "type": "ip",
          "script" : {
          "source" : "String m = doc[\"message\"].value; int end = m.indexOf(\" \"); emit(m.substring(0, end));"
          }
        }
      }
    }

运行另一个查询，但使用"client_ip"运行时字段搜索特定 IP 地址：

    
    
    GET my-index-000001/_search
    {
      "size": 1,
      "query": {
        "match": {
          "client_ip": "211.11.9.0"
        }
      },
      "fields" : ["*"]
    }

这一次，响应仅包含两个匹配。"day_of_week"("星期日")的值是在查询时使用映射中定义的运行时脚本计算的，结果仅包括与"211.11.9.0"IP 地址匹配的文档。

    
    
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
            "_id" : "oWs5KXYB-XyJbifr9mrz",
            "_score" : 1.0,
            "_source" : {
              "@timestamp" : "2020-06-21T15:00:01-05:00",
              "message" : "211.11.9.0 - - [2020-06-21T15:00:01-05:00] \"GET /english/index.html HTTP/1.0\" 304 0"
            },
            "fields" : {
              "@timestamp" : [
                "2020-06-21T20:00:01.000Z"
              ],
              "client_ip" : [
                "211.11.9.0"
              ],
              "message" : [
                "211.11.9.0 - - [2020-06-21T15:00:01-05:00] \"GET /english/index.html HTTP/1.0\" 304 0"
              ],
              "day_of_week" : [
                "Sunday"
              ]
            }
          }
        ]
      }
    }

### 从相关索引中检索字段

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"_search"API 上的"fields"参数还可用于通过具有"查找"类型的运行时字段从相关索引中检索字段。

由类型为"lookup"的运行时字段检索的字段可用于丰富搜索响应中的命中。无法查询或聚合这些字段。

    
    
    response = client.index(
      index: 'ip_location',
      refresh: true,
      body: {
        ip: '192.168.1.1',
        country: 'Canada',
        city: 'Montreal'
      }
    )
    puts response
    
    response = client.index(
      index: 'logs',
      id: 1,
      refresh: true,
      body: {
        host: '192.168.1.1',
        message: 'the first message'
      }
    )
    puts response
    
    response = client.index(
      index: 'logs',
      id: 2,
      refresh: true,
      body: {
        host: '192.168.1.2',
        message: 'the second message'
      }
    )
    puts response
    
    response = client.search(
      index: 'logs',
      body: {
        runtime_mappings: {
          location: {
            type: 'lookup',
            target_index: 'ip_location',
            input_field: 'host',
            target_field: 'ip',
            fetch_fields: [
              'country',
              'city'
            ]
          }
        },
        fields: [
          'host',
          'message',
          'location'
        ],
        _source: false
      }
    )
    puts response
    
    
    POST ip_location/_doc?refresh
    {
      "ip": "192.168.1.1",
      "country": "Canada",
      "city": "Montreal"
    }
    
    PUT logs/_doc/1?refresh
    {
      "host": "192.168.1.1",
      "message": "the first message"
    }
    
    PUT logs/_doc/2?refresh
    {
      "host": "192.168.1.2",
      "message": "the second message"
    }
    
    POST logs/_search
    {
      "runtime_mappings": {
        "location": {
            "type": "lookup", __"target_index": "ip_location", __"input_field": "host", __"target_field": "ip", __"fetch_fields": ["country", "city"] __}
      },
      "fields": [
        "host",
        "message",
        "location"
      ],
      "_source": false
    }

__

|

使用"查找"类型在主搜索请求中定义一个运行时字段，该类型使用"term"查询从目标索引中检索字段。   ---|---    __

|

针对 __ 执行查找查询的目标索引

|

主索引上的一个字段，其值用作查找词查询 __ 的输入值

|

查找查询针对 __ 搜索的查找索引上的字段

|

要从查找索引中检索的字段列表。请参阅搜索请求的"字段"参数。   上面的搜索从返回的搜索命中每个 IP 地址的"ip_location"索引中返回国家和城市。

    
    
    {
      "took": 3,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 2,
          "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
          {
            "_index": "logs",
            "_id": "1",
            "_score": 1.0,
            "fields": {
              "host": [ "192.168.1.1" ],
              "location": [
                {
                  "city": [ "Montreal" ],
                  "country": [ "Canada" ]
                }
              ],
              "message": [ "the first message" ]
            }
          },
          {
            "_index": "logs",
            "_id": "2",
            "_score": 1.0,
            "fields": {
              "host": [ "192.168.1.2" ],
              "message": [ "the second message" ]
            }
          }
        ]
      }
    }

查阅字段的响应被分组，以保持每个文档与查阅索引的独立性。每个输入值的查找查询应最多匹配查找索引上的一个文档。如果查找查询匹配多个文档，则将选择一个随机文档。

[« Override field values at query time](runtime-override-values.md) [Index a
runtime field »](runtime-indexed.md)
