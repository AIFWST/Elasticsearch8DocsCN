

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Runtime fields](runtime.md)

[« Define runtime fields in a search request](runtime-search-request.md)
[Retrieve a runtime field »](runtime-retrieving-fields.md)

## 在查询时覆盖字段值

如果创建的运行时字段与映射中已存在的字段同名，则该运行时字段将隐藏映射的字段。在查询时，Elasticsearch 计算运行时字段，根据脚本计算值，并将该值作为查询的一部分返回。由于运行时字段隐藏映射字段，因此您可以覆盖搜索中返回的值，而无需修改映射字段。

例如，假设您将以下文档索引到"my-index-000001"中：

    
    
    response = client.bulk(
      index: 'my-index-000001',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          "@timestamp": 1_516_729_294_000,
          model_number: 'QVKC92Q',
          measures: {
            voltage: 5.2
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_642_894_000,
          model_number: 'QVKC92Q',
          measures: {
            voltage: 5.8
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_556_494_000,
          model_number: 'QVKC92Q',
          measures: {
            voltage: 5.1
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_470_094_000,
          model_number: 'QVKC92Q',
          measures: {
            voltage: 5.6
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_383_694_000,
          model_number: 'HG537PU',
          measures: {
            voltage: 4.2
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_297_294_000,
          model_number: 'HG537PU',
          measures: {
            voltage: 4
          }
        }
      ]
    )
    puts response
    
    
    POST my-index-000001/_bulk?refresh=true
    {"index":{}}
    {"@timestamp":1516729294000,"model_number":"QVKC92Q","measures":{"voltage":5.2}}
    {"index":{}}
    {"@timestamp":1516642894000,"model_number":"QVKC92Q","measures":{"voltage":5.8}}
    {"index":{}}
    {"@timestamp":1516556494000,"model_number":"QVKC92Q","measures":{"voltage":5.1}}
    {"index":{}}
    {"@timestamp":1516470094000,"model_number":"QVKC92Q","measures":{"voltage":5.6}}
    {"index":{}}
    {"@timestamp":1516383694000,"model_number":"HG537PU","measures":{"voltage":4.2}}
    {"index":{}}
    {"@timestamp":1516297294000,"model_number":"HG537PU","measures":{"voltage":4.0}}

您后来意识到"HG537PU"传感器没有报告其真实电压。索引值应该比报告值高 1.7 倍！您可以在"_search"请求的"runtime_mappings"部分中定义一个脚本，以隐藏"电压"字段并在查询时计算新值，而不是重新索引数据。

如果搜索型号与"HG537PU"匹配的文档：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            model_number: 'HG537PU'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "model_number": "HG537PU"
        }
      }
    }

响应包括与型号"HG537PU"匹配的文档的索引值：

    
    
    {
      ...
      "hits" : {
        "total" : {
          "value" : 2,
          "relation" : "eq"
        },
        "max_score" : 1.0296195,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "F1BeSXYBg_szTodcYCmk",
            "_score" : 1.0296195,
            "_source" : {
              "@timestamp" : 1516383694000,
              "model_number" : "HG537PU",
              "measures" : {
                "voltage" : 4.2
              }
            }
          },
          {
            "_index" : "my-index-000001",
            "_id" : "l02aSXYBkpNf6QRDO62Q",
            "_score" : 1.0296195,
            "_source" : {
              "@timestamp" : 1516297294000,
              "model_number" : "HG537PU",
              "measures" : {
                "voltage" : 4.0
              }
            }
          }
        ]
      }
    }

以下请求定义了一个运行时字段，脚本在其中计算值为"HG537PU"的"model_number"字段。对于每个匹配项，脚本将"电压"字段的值乘以"1.7"。

使用"_search"API 上的"fields"参数，您可以检索脚本为与搜索请求匹配的文档的"measure.voltage"字段计算的值：

    
    
    POST my-index-000001/_search
    {
      "runtime_mappings": {
        "measures.voltage": {
          "type": "double",
          "script": {
            "source":
            """if (doc['model_number.keyword'].value.equals('HG537PU'))
            {emit(1.7 * params._source['measures']['voltage']);}
            else{emit(params._source['measures']['voltage']);}"""
          }
        }
      },
      "query": {
        "match": {
          "model_number": "HG537PU"
        }
      },
      "fields": ["measures.voltage"]
    }

查看响应，每个结果上的"measure.voltage"的计算值为"7.14"和"6.8"。那更像是它！运行时字段将此值作为搜索请求的一部分进行计算，而不修改映射的值，该值仍会在响应中返回：

    
    
    {
      ...
      "hits" : {
        "total" : {
          "value" : 2,
          "relation" : "eq"
        },
        "max_score" : 1.0296195,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "F1BeSXYBg_szTodcYCmk",
            "_score" : 1.0296195,
            "_source" : {
              "@timestamp" : 1516383694000,
              "model_number" : "HG537PU",
              "measures" : {
                "voltage" : 4.2
              }
            },
            "fields" : {
              "measures.voltage" : [
                7.14
              ]
            }
          },
          {
            "_index" : "my-index-000001",
            "_id" : "l02aSXYBkpNf6QRDO62Q",
            "_score" : 1.0296195,
            "_source" : {
              "@timestamp" : 1516297294000,
              "model_number" : "HG537PU",
              "measures" : {
                "voltage" : 4.0
              }
            },
            "fields" : {
              "measures.voltage" : [
                6.8
              ]
            }
          }
        ]
      }
    }

[« Define runtime fields in a search request](runtime-search-request.md)
[Retrieve a runtime field »](runtime-retrieving-fields.md)
