

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Metadata fields](mapping-fields.md)

[« Metadata fields](mapping-fields.md) [`_field_names` field »](mapping-
field-names-field.md)

## '_doc_count'字段

存储桶聚合始终返回一个名为"doc_count"的字段，显示每个存储桶中聚合和分区的文档数。"doc_count"值的计算非常简单。对于每个存储桶中收集的每个文档，"doc_count"递增 1。

虽然这种简单的方法在计算单个文档的聚合时很有效，但它无法准确表示存储预先聚合数据的文档(例如"直方图"或"aggregate_metric_double"字段)，因为一个汇总字段可能表示多个文档。

为了在处理预聚合数据时正确计算文档数量，我们引入了名为"_doc_count"的元数据字段类型。"_doc_count"必须始终为正整数，表示单个合计字段中聚合的文档数。

将字段"_doc_count"添加到文档时，所有存储桶聚合都将尊重其值，并将存储桶"doc_count"递增字段的值。如果文档不包含任何"_doc_count"字段，则默认暗示"_doc_count = 1"。

* "_doc_count"字段只能为每个文档存储一个正整数。不允许嵌套数组。  * 如果文档不包含"_doc_count"字段，聚合器将递增 1，这是默认行为。

###Example

以下创建索引 API请求使用以下字段映射创建新索引：

* "my_histogram"，用于存储百分位数据的"直方图"字段 * "my_text"，用于存储直方图标题的"关键字"字段

    
    
    response = client.indices.create(
      index: 'my_index',
      body: {
        mappings: {
          properties: {
            my_histogram: {
              type: 'histogram'
            },
            my_text: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my_index
    {
      "mappings" : {
        "properties" : {
          "my_histogram" : {
            "type" : "histogram"
          },
          "my_text" : {
            "type" : "keyword"
          }
        }
      }
    }

以下索引 API 请求存储两个直方图的预聚合数据："histogram_1"和"histogram_2"。

    
    
    response = client.index(
      index: 'my_index',
      id: 1,
      body: {
        my_text: 'histogram_1',
        my_histogram: {
          values: [
            0.1,
            0.2,
            0.3,
            0.4,
            0.5
          ],
          counts: [
            3,
            7,
            23,
            12,
            6
          ]
        },
        _doc_count: 45
      }
    )
    puts response
    
    response = client.index(
      index: 'my_index',
      id: 2,
      body: {
        my_text: 'histogram_2',
        my_histogram: {
          values: [
            0.1,
            0.25,
            0.35,
            0.4,
            0.45,
            0.5
          ],
          counts: [
            8,
            17,
            8,
            7,
            6,
            2
          ]
        },
        _doc_count: 62
      }
    )
    puts response
    
    
    PUT my_index/_doc/1
    {
      "my_text" : "histogram_1",
      "my_histogram" : {
          "values" : [0.1, 0.2, 0.3, 0.4, 0.5],
          "counts" : [3, 7, 23, 12, 6]
       },
      "_doc_count": 45 __}
    
    PUT my_index/_doc/2
    {
      "my_text" : "histogram_2",
      "my_histogram" : {
          "values" : [0.1, 0.25, 0.35, 0.4, 0.45, 0.5],
          "counts" : [8, 17, 8, 7, 6, 2]
       },
      "_doc_count": 62 __}

__

|

字段"_doc_count"必须是正整数，用于存储聚合以生成每个直方图的文档数。   ---|--- 如果我们在"my_index"上运行以下术语聚合：

    
    
    response = client.search(
      body: {
        aggregations: {
          histogram_titles: {
            terms: {
              field: 'my_text'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
        "aggs" : {
            "histogram_titles" : {
                "terms" : { "field" : "my_text" }
            }
        }
    }

我们将收到以下响应：

    
    
    {
        ...
        "aggregations" : {
            "histogram_titles" : {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets" : [
                    {
                        "key" : "histogram_2",
                        "doc_count" : 62
                    },
                    {
                        "key" : "histogram_1",
                        "doc_count" : 45
                    }
                ]
            }
        }
    }

[« Metadata fields](mapping-fields.md) [`_field_names` field »](mapping-
field-names-field.md)
