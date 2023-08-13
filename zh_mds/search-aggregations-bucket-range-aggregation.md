

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Random sampler aggregation](search-aggregations-random-sampler-
aggregation.md) [Rare terms aggregation »](search-aggregations-bucket-rare-
terms-aggregation.md)

## 范围聚合

基于多存储桶值源的聚合，使用户能够定义一组范围 - 每个范围代表一个存储桶。在聚合过程中，将从每个文档中提取的值与每个存储桶范围进行检查，并"存储桶"相关/匹配文档。请注意，此聚合包括"from"值，并排除每个范围的"to"值。

Example:

    
    
    response = client.search(
      index: 'sales',
      body: {
        aggregations: {
          price_ranges: {
            range: {
              field: 'price',
              ranges: [
                {
                  to: 100
                },
                {
                  from: 100,
                  to: 200
                },
                {
                  from: 200
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET sales/_search
    {
      "aggs": {
        "price_ranges": {
          "range": {
            "field": "price",
            "ranges": [
              { "to": 100.0 },
              { "from": 100.0, "to": 200.0 },
              { "from": 200.0 }
            ]
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "price_ranges": {
          "buckets": [
            {
              "key": "*-100.0",
              "to": 100.0,
              "doc_count": 2
            },
            {
              "key": "100.0-200.0",
              "from": 100.0,
              "to": 200.0,
              "doc_count": 2
            },
            {
              "key": "200.0-*",
              "from": 200.0,
              "doc_count": 3
            }
          ]
        }
      }
    }

### 键控响应

将"keyed"标志设置为"true"会将一个唯一的字符串键与每个存储桶相关联，并将范围作为哈希而不是数组返回：

    
    
    response = client.search(
      index: 'sales',
      body: {
        aggregations: {
          price_ranges: {
            range: {
              field: 'price',
              keyed: true,
              ranges: [
                {
                  to: 100
                },
                {
                  from: 100,
                  to: 200
                },
                {
                  from: 200
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET sales/_search
    {
      "aggs": {
        "price_ranges": {
          "range": {
            "field": "price",
            "keyed": true,
            "ranges": [
              { "to": 100 },
              { "from": 100, "to": 200 },
              { "from": 200 }
            ]
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "price_ranges": {
          "buckets": {
            "*-100.0": {
              "to": 100.0,
              "doc_count": 2
            },
            "100.0-200.0": {
              "from": 100.0,
              "to": 200.0,
              "doc_count": 2
            },
            "200.0-*": {
              "from": 200.0,
              "doc_count": 3
            }
          }
        }
      }
    }

还可以为每个范围自定义键：

    
    
    response = client.search(
      index: 'sales',
      body: {
        aggregations: {
          price_ranges: {
            range: {
              field: 'price',
              keyed: true,
              ranges: [
                {
                  key: 'cheap',
                  to: 100
                },
                {
                  key: 'average',
                  from: 100,
                  to: 200
                },
                {
                  key: 'expensive',
                  from: 200
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET sales/_search
    {
      "aggs": {
        "price_ranges": {
          "range": {
            "field": "price",
            "keyed": true,
            "ranges": [
              { "key": "cheap", "to": 100 },
              { "key": "average", "from": 100, "to": 200 },
              { "key": "expensive", "from": 200 }
            ]
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "price_ranges": {
          "buckets": {
            "cheap": {
              "to": 100.0,
              "doc_count": 2
            },
            "average": {
              "from": 100.0,
              "to": 200.0,
              "doc_count": 2
            },
            "expensive": {
              "from": 200.0,
              "doc_count": 3
            }
          }
        }
      }
    }

###Script

如果文档中的数据与要聚合的数据不完全匹配，请使用运行时字段。例如，如果您需要应用特定的货币兑换率：

    
    
    response = client.search(
      index: 'sales',
      body: {
        runtime_mappings: {
          "price.euros": {
            type: 'double',
            script: {
              source: "\n          emit(doc['price'].value * params.conversion_rate)\n        ",
              params: {
                conversion_rate: 0.835526591
              }
            }
          }
        },
        aggregations: {
          price_ranges: {
            range: {
              field: 'price.euros',
              ranges: [
                {
                  to: 100
                },
                {
                  from: 100,
                  to: 200
                },
                {
                  from: 200
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET sales/_search
    {
      "runtime_mappings": {
        "price.euros": {
          "type": "double",
          "script": {
            "source": """
              emit(doc['price'].value * params.conversion_rate)
            """,
            "params": {
              "conversion_rate": 0.835526591
            }
          }
        }
      },
      "aggs": {
        "price_ranges": {
          "range": {
            "field": "price.euros",
            "ranges": [
              { "to": 100 },
              { "from": 100, "to": 200 },
              { "from": 200 }
            ]
          }
        }
      }
    }

### 子聚合

以下示例不仅将文档"存储桶"到不同的存储桶，而且还计算每个价格范围内价格的统计信息

    
    
    response = client.search(
      index: 'sales',
      body: {
        aggregations: {
          price_ranges: {
            range: {
              field: 'price',
              ranges: [
                {
                  to: 100
                },
                {
                  from: 100,
                  to: 200
                },
                {
                  from: 200
                }
              ]
            },
            aggregations: {
              price_stats: {
                stats: {
                  field: 'price'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET sales/_search
    {
      "aggs": {
        "price_ranges": {
          "range": {
            "field": "price",
            "ranges": [
              { "to": 100 },
              { "from": 100, "to": 200 },
              { "from": 200 }
            ]
          },
          "aggs": {
            "price_stats": {
              "stats": { "field": "price" }
            }
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "price_ranges": {
          "buckets": [
            {
              "key": "*-100.0",
              "to": 100.0,
              "doc_count": 2,
              "price_stats": {
                "count": 2,
                "min": 10.0,
                "max": 50.0,
                "avg": 30.0,
                "sum": 60.0
              }
            },
            {
              "key": "100.0-200.0",
              "from": 100.0,
              "to": 200.0,
              "doc_count": 2,
              "price_stats": {
                "count": 2,
                "min": 150.0,
                "max": 175.0,
                "avg": 162.5,
                "sum": 325.0
              }
            },
            {
              "key": "200.0-*",
              "from": 200.0,
              "doc_count": 3,
              "price_stats": {
                "count": 3,
                "min": 200.0,
                "max": 200.0,
                "avg": 200.0,
                "sum": 600.0
              }
            }
          ]
        }
      }
    }

### 直方图字段

对直方图字段运行范围聚合将计算每个配置范围的计数总数。

此操作无需在直方图字段值之间进行插值。因此，可以有一个"介于"双直方图值之间的范围。生成的范围存储桶的文档计数为零。

以下示例针对以下索引执行范围聚合，该索引存储了不同网络的预聚合直方图和延迟指标(以毫秒为单位)：

    
    
    PUT metrics_index
    {
      "mappings": {
        "properties": {
          "network": {
            "properties": {
              "name": {
                "type": "keyword"
              }
            }
          },
          "latency_histo": {
             "type": "histogram"
          }
        }
      }
    }
    
    PUT metrics_index/_doc/1?refresh
    {
      "network.name" : "net-1",
      "latency_histo" : {
          "values" : [1, 3, 8, 12, 15],
          "counts" : [3, 7, 23, 12, 6]
       }
    }
    
    PUT metrics_index/_doc/2?refresh
    {
      "network.name" : "net-2",
      "latency_histo" : {
          "values" : [1, 6, 8, 12, 14],
          "counts" : [8, 17, 8, 7, 6]
       }
    }
    
    GET metrics_index/_search?size=0&filter_path=aggregations
    {
      "aggs": {
        "latency_ranges": {
          "range": {
            "field": "latency_histo",
            "ranges": [
              {"to": 2},
              {"from": 2, "to": 3},
              {"from": 3, "to": 10},
              {"from": 10}
            ]
          }
        }
      }
    }

"范围"聚合将对基于"值"计算的每个范围的计数求和，并返回以下输出：

    
    
    {
      "aggregations": {
        "latency_ranges": {
          "buckets": [
            {
              "key": "*-2.0",
              "to": 2.0,
              "doc_count": 11
            },
            {
              "key": "2.0-3.0",
              "from": 2.0,
              "to": 3.0,
              "doc_count": 0
            },
            {
              "key": "3.0-10.0",
              "from": 3.0,
              "to": 10.0,
              "doc_count": 55
            },
            {
              "key": "10.0-*",
              "from": 10.0,
              "doc_count": 31
            }
          ]
        }
      }
    }

范围聚合是一种存储桶聚合，它将文档分区到存储桶中，而不是像指标聚合那样通过字段计算指标。每个存储桶表示运行子聚合扫描的文档集合。另一方面，直方图字段是一个预先聚合的字段，表示单个字段中的多个值：数字数据的桶和每个桶的项目/文档计数。范围聚合预期输入(需要原始文档)和直方图字段(提供摘要信息)之间的这种不匹配将聚合的结果限制为每个存储桶的文档计数。

**因此，在直方图字段上执行范围聚合时，允许无子聚合。

[« Random sampler aggregation](search-aggregations-random-sampler-
aggregation.md) [Rare terms aggregation »](search-aggregations-bucket-rare-
terms-aggregation.md)
