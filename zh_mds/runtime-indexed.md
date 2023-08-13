

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Runtime fields](runtime.md)

[« Retrieve a runtime field](runtime-retrieving-fields.md) [Explore your
data with runtime fields »](runtime-examples.md)

## 为运行时字段编制索引

运行时字段由其运行的上下文定义。例如，您可以在搜索查询的上下文中或在索引映射的"运行时"部分中定义运行时字段。如果您决定为运行时字段编制索引以获得更高的性能，只需将完整的运行时字段定义(包括脚本)移动到索引映射的上下文中即可。Elasticsearch 自动使用这些索引字段来驱动查询，从而缩短响应时间。此功能意味着您只能编写一次脚本，并将其应用于支持运行时字段的任何上下文。

目前不支持为"复合"运行时字段编制索引。

然后，您可以使用运行时字段来限制 Elasticsearch 需要计算值的字段数。在运行时字段中同时使用索引字段可以灵活地编制索引数据以及如何定义其他字段的查询。

为运行时字段编制索引后，无法更新包含的脚本。如果需要更改脚本，请使用更新的脚本创建新字段。

例如，假设您的公司想要更换一些旧的压力阀。连接的传感器只能报告一小部分真实读数。您决定根据报告的读数计算值，而不是为压力阀配备新的传感器。根据报告的数据，您可以在映射中为 'my-index-000001' 定义以下字段：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            timestamp: {
              type: 'date'
            },
            temperature: {
              type: 'long'
            },
            voltage: {
              type: 'double'
            },
            node: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/
    {
      "mappings": {
        "properties": {
          "timestamp": {
            "type": "date"
          },
          "temperature": {
            "type": "long"
          },
          "voltage": {
            "type": "double"
          },
          "node": {
            "type": "keyword"
          }
        }
      }
    }

然后，对来自传感器的一些示例数据进行批量索引。此数据包括每个传感器的"电压"读数：

    
    
    response = client.bulk(
      index: 'my-index-000001',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          timestamp: 1_516_729_294_000,
          temperature: 200,
          voltage: 5.2,
          node: 'a'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_642_894_000,
          temperature: 201,
          voltage: 5.8,
          node: 'b'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_556_494_000,
          temperature: 202,
          voltage: 5.1,
          node: 'a'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_470_094_000,
          temperature: 198,
          voltage: 5.6,
          node: 'b'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_383_694_000,
          temperature: 200,
          voltage: 4.2,
          node: 'c'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_297_294_000,
          temperature: 202,
          voltage: 4,
          node: 'c'
        }
      ]
    )
    puts response
    
    
    POST my-index-000001/_bulk?refresh=true
    {"index":{}}
    {"timestamp": 1516729294000, "temperature": 200, "voltage": 5.2, "node": "a"}
    {"index":{}}
    {"timestamp": 1516642894000, "temperature": 201, "voltage": 5.8, "node": "b"}
    {"index":{}}
    {"timestamp": 1516556494000, "temperature": 202, "voltage": 5.1, "node": "a"}
    {"index":{}}
    {"timestamp": 1516470094000, "temperature": 198, "voltage": 5.6, "node": "b"}
    {"index":{}}
    {"timestamp": 1516383694000, "temperature": 200, "voltage": 4.2, "node": "c"}
    {"index":{}}
    {"timestamp": 1516297294000, "temperature": 202, "voltage": 4.0, "node": "c"}

在与几位现场工程师交谈后，您意识到传感器报告的电流值至少应为当前值的两倍，但可能更高。创建一个名为"voltage_corrected"的运行时字段，该字段检索当前电压并将其乘以"2"：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        runtime: {
          voltage_corrected: {
            type: 'double',
            script: {
              source: "\n        emit(doc['voltage'].value * params['multiplier'])\n        ",
              params: {
                multiplier: 2
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_mapping
    {
      "runtime": {
        "voltage_corrected": {
          "type": "double",
          "script": {
            "source": """
            emit(doc['voltage'].value * params['multiplier'])
            """,
            "params": {
              "multiplier": 2
            }
          }
        }
      }
    }

您可以使用"_search"API 上的"字段"参数检索计算值：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        fields: [
          'voltage_corrected',
          'node'
        ],
        size: 2
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "fields": [
        "voltage_corrected",
        "node"
      ],
      "size": 2
    }

查看传感器数据并运行一些测试后，确定报告的传感器数据的乘数应为"4"。为了获得更高的性能，您决定使用新的"乘数"参数为"voltage_corrected"运行时字段编制索引。

在名为"my-index-000001"的新索引中，将"voltage_corrected"运行时字段定义复制到新索引的映射中。就是这么简单！您可以添加一个名为"on_script_error"的可选参数，该参数确定如果脚本在索引时引发错误(默认)，是否拒绝整个文档。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            timestamp: {
              type: 'date'
            },
            temperature: {
              type: 'long'
            },
            voltage: {
              type: 'double'
            },
            node: {
              type: 'keyword'
            },
            voltage_corrected: {
              type: 'double',
              on_script_error: 'fail',
              script: {
                source: "\n        emit(doc['voltage'].value * params['multiplier'])\n        ",
                params: {
                  multiplier: 4
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/
    {
      "mappings": {
        "properties": {
          "timestamp": {
            "type": "date"
          },
          "temperature": {
            "type": "long"
          },
          "voltage": {
            "type": "double"
          },
          "node": {
            "type": "keyword"
          },
          "voltage_corrected": {
            "type": "double",
            "on_script_error": "fail", __"script": {
              "source": """
            emit(doc['voltage'].value * params['multiplier'])
            """,
              "params": {
                "multiplier": 4
              }
            }
          }
        }
      }
    }

__

|

如果脚本在索引时间引发错误，则导致整个文档被拒绝。将值设置为"忽略"将在文档的"_ignored"元数据字段中注册该字段并继续编制索引。   ---|--- 将传感器中的一些示例数据批量索引到"my-index-000001"索引中：

    
    
    response = client.bulk(
      index: 'my-index-000001',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          timestamp: 1_516_729_294_000,
          temperature: 200,
          voltage: 5.2,
          node: 'a'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_642_894_000,
          temperature: 201,
          voltage: 5.8,
          node: 'b'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_556_494_000,
          temperature: 202,
          voltage: 5.1,
          node: 'a'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_470_094_000,
          temperature: 198,
          voltage: 5.6,
          node: 'b'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_383_694_000,
          temperature: 200,
          voltage: 4.2,
          node: 'c'
        },
        {
          index: {}
        },
        {
          timestamp: 1_516_297_294_000,
          temperature: 202,
          voltage: 4,
          node: 'c'
        }
      ]
    )
    puts response
    
    
    POST my-index-000001/_bulk?refresh=true
    { "index": {}}
    { "timestamp": 1516729294000, "temperature": 200, "voltage": 5.2, "node": "a"}
    { "index": {}}
    { "timestamp": 1516642894000, "temperature": 201, "voltage": 5.8, "node": "b"}
    { "index": {}}
    { "timestamp": 1516556494000, "temperature": 202, "voltage": 5.1, "node": "a"}
    { "index": {}}
    { "timestamp": 1516470094000, "temperature": 198, "voltage": 5.6, "node": "b"}
    { "index": {}}
    { "timestamp": 1516383694000, "temperature": 200, "voltage": 4.2, "node": "c"}
    { "index": {}}
    { "timestamp": 1516297294000, "temperature": 202, "voltage": 4.0, "node": "c"}

现在，您可以在搜索查询中检索计算值，并根据精确值查找文档。以下范围查询返回计算的"voltage_corrected"大于或等于"16"但小于或等于"20"的所有文档。同样，使用"_search"API 上的"字段"参数来检索所需的字段：

    
    
    POST my-index-000001/_search
    {
      "query": {
        "range": {
          "voltage_corrected": {
            "gte": 16,
            "lte": 20,
            "boost": 1.0
          }
        }
      },
      "fields": ["voltage_corrected", "node"]
    }

响应包括与范围查询匹配的文档的"voltage_corrected"字段，具体取决于所包含脚本的计算值：

    
    
    {
      "hits" : {
        "total" : {
          "value" : 2,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "yoSLrHgBdg9xpPrUZz_P",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : 1516383694000,
              "temperature" : 200,
              "voltage" : 4.2,
              "node" : "c"
            },
            "fields" : {
              "voltage_corrected" : [
                16.8
              ],
              "node" : [
                "c"
              ]
            }
          },
          {
            "_index" : "my-index-000001",
            "_id" : "y4SLrHgBdg9xpPrUZz_P",
            "_score" : 1.0,
            "_source" : {
              "timestamp" : 1516297294000,
              "temperature" : 202,
              "voltage" : 4.0,
              "node" : "c"
            },
            "fields" : {
              "voltage_corrected" : [
                16.0
              ],
              "node" : [
                "c"
              ]
            }
          }
        ]
      }
    }

[« Retrieve a runtime field](runtime-retrieving-fields.md) [Explore your
data with runtime fields »](runtime-examples.md)
