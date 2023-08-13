

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Runtime fields](runtime.md)

[« Map a runtime field](runtime-mapping-fields.md) [Override field values at
query time »](runtime-override-values.md)

## 在搜索请求中定义运行时字段

您可以在搜索请求中指定"runtime_mappings"部分，以创建仅作为查询的一部分存在的运行时字段。您可以指定"runtime_mappings"部分的脚本，就像向映射添加运行时字段一样。

在搜索请求中定义运行时字段使用的格式与在索引映射中定义运行时字段的格式相同。只需将字段定义从索引映射中的"运行时"复制到搜索请求的"runtime_mappings"部分即可。

以下搜索请求将"day_of_week"字段添加到"runtime_mappings"部分。字段值将动态计算，并且仅在此搜索请求的上下文中计算：

    
    
    GET my-index-000001/_search
    {
      "runtime_mappings": {
        "day_of_week": {
          "type": "keyword",
          "script": {
            "source": "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
          }
        }
      },
      "aggs": {
        "day_of_week": {
          "terms": {
            "field": "day_of_week"
          }
        }
      }
    }

### 创建使用其他运行时字段的运行时字段

您甚至可以在搜索请求中定义从其他运行时字段返回值的运行时字段。例如，假设您批量索引某些传感器数据：

    
    
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
            voltage: '5.2',
            start: '300',
            end: '8675309'
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_642_894_000,
          model_number: 'QVKC92Q',
          measures: {
            voltage: '5.8',
            start: '300',
            end: '8675309'
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_556_494_000,
          model_number: 'QVKC92Q',
          measures: {
            voltage: '5.1',
            start: '300',
            end: '8675309'
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_470_094_000,
          model_number: 'QVKC92Q',
          measures: {
            voltage: '5.6',
            start: '300',
            end: '8675309'
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_383_694_000,
          model_number: 'HG537PU',
          measures: {
            voltage: '4.2',
            start: '400',
            end: '8625309'
          }
        },
        {
          index: {}
        },
        {
          "@timestamp": 1_516_297_294_000,
          model_number: 'HG537PU',
          measures: {
            voltage: '4.0',
            start: '400',
            end: '8625309'
          }
        }
      ]
    )
    puts response
    
    
    POST my-index-000001/_bulk?refresh=true
    {"index":{}}
    {"@timestamp":1516729294000,"model_number":"QVKC92Q","measures":{"voltage":"5.2","start": "300","end":"8675309"}}
    {"index":{}}
    {"@timestamp":1516642894000,"model_number":"QVKC92Q","measures":{"voltage":"5.8","start": "300","end":"8675309"}}
    {"index":{}}
    {"@timestamp":1516556494000,"model_number":"QVKC92Q","measures":{"voltage":"5.1","start": "300","end":"8675309"}}
    {"index":{}}
    {"@timestamp":1516470094000,"model_number":"QVKC92Q","measures":{"voltage":"5.6","start": "300","end":"8675309"}}
    {"index":{}}
    {"@timestamp":1516383694000,"model_number":"HG537PU","measures":{"voltage":"4.2","start": "400","end":"8625309"}}
    {"index":{}}
    {"@timestamp":1516297294000,"model_number":"HG537PU","measures":{"voltage":"4.0","start": "400","end":"8625309"}}

索引后，您意识到数值数据被映射为类型"文本"。您希望在"measure.start"和"measure.end"字段上进行聚合，但聚合失败，因为您无法在"text"类型的字段上进行聚合。运行时字段来救援！您可以添加与索引字段同名的运行时字段并修改数据类型：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        runtime: {
          "measures.start": {
            type: 'long'
          },
          "measures.end": {
            type: 'long'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_mapping
    {
      "runtime": {
        "measures.start": {
          "type": "long"
        },
        "measures.end": {
          "type": "long"
        }
      }
    }

运行时字段优先于在索引映射中使用相同名称定义的字段。这种灵活性允许您隐藏现有字段并计算不同的值，而无需修改字段本身。如果在索引映射中出错，则可以使用运行时字段来计算在搜索请求期间覆盖映射中的值的值。

现在，您可以轻松地在"measure.start"和"measures.end"字段上运行平均聚合：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        aggregations: {
          avg_start: {
            avg: {
              field: 'measures.start'
            }
          },
          avg_end: {
            avg: {
              field: 'measures.end'
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "aggs": {
        "avg_start": {
          "avg": {
            "field": "measures.start"
          }
        },
        "avg_end": {
          "avg": {
            "field": "measures.end"
          }
        }
      }
    }

响应包括聚合结果，而不更改基础数据的值：

    
    
    {
      "aggregations" : {
        "avg_start" : {
          "value" : 333.3333333333333
        },
        "avg_end" : {
          "value" : 8658642.333333334
        }
      }
    }

此外，您可以将运行时字段定义为计算值的搜索查询的一部分，然后在samequery__in对该字段运行统计信息聚合。

索引映射中不存在"持续时间"运行时字段，但我们仍然可以在该字段上进行搜索和聚合。以下查询返回"持续时间"字段的计算值，并运行统计信息聚合以计算从聚合文档中提取的数值的统计信息。

    
    
    GET my-index-000001/_search
    {
      "runtime_mappings": {
        "duration": {
          "type": "long",
          "script": {
            "source": """
              emit(doc['measures.end'].value - doc['measures.start'].value);
              """
          }
        }
      },
      "aggs": {
        "duration_stats": {
          "stats": {
            "field": "duration"
          }
        }
      }
    }

即使"持续时间"运行时字段仅存在于搜索查询的上下文中，您也可以在该字段上进行搜索和聚合。这种灵活性非常强大，使您能够纠正索引映射中的错误，并在单个搜索请求中动态完成计算。

    
    
    {
      "aggregations" : {
        "duration_stats" : {
          "count" : 6,
          "min" : 8624909.0,
          "max" : 8675009.0,
          "avg" : 8658309.0,
          "sum" : 5.1949854E7
        }
      }
    }

[« Map a runtime field](runtime-mapping-fields.md) [Override field values at
query time »](runtime-override-values.md)
