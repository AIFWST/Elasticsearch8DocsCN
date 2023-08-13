

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« String stats aggregation](search-aggregations-metrics-string-stats-
aggregation.md) [T-test aggregation »](search-aggregations-metrics-ttest-
aggregation.md)

## 求和聚合

一种"单值"指标聚合，用于汇总从聚合文档中提取的数值。可以从特定的数值或直方图字段中提取这些值。

假设数据由代表销售记录的文档组成，我们可以将所有帽子的销售价格相加为：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        query: {
          constant_score: {
            filter: {
              match: {
                type: 'hat'
              }
            }
          }
        },
        aggregations: {
          hat_prices: {
            sum: {
              field: 'price'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "query": {
        "constant_score": {
          "filter": {
            "match": { "type": "hat" }
          }
        }
      },
      "aggs": {
        "hat_prices": { "sum": { "field": "price" } }
      }
    }

结果是：

    
    
    {
      ...
      "aggregations": {
        "hat_prices": {
          "value": 450.0
        }
      }
    }

聚合的名称(上面的"hat_prices")也用作可以从返回的响应中检索聚合结果的键。

###Script

如果需要获取比单个字段更复杂的内容的"总和"，请在运行时字段上运行聚合。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        runtime_mappings: {
          "price.weighted": {
            type: 'double',
            script: "\n        double price = doc['price'].value;\n        if (doc['promoted'].value) {\n          price *= 0.8;\n        }\n        emit(price);\n      "
          }
        },
        query: {
          constant_score: {
            filter: {
              match: {
                type: 'hat'
              }
            }
          }
        },
        aggregations: {
          hat_prices: {
            sum: {
              field: 'price.weighted'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "runtime_mappings": {
        "price.weighted": {
          "type": "double",
          "script": """
            double price = doc['price'].value;
            if (doc['promoted'].value) {
              price *= 0.8;
            }
            emit(price);
          """
        }
      },
      "query": {
        "constant_score": {
          "filter": {
            "match": { "type": "hat" }
          }
        }
      },
      "aggs": {
        "hat_prices": {
          "sum": {
            "field": "price.weighted"
          }
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，缺少该值的文档将被忽略，但也可以将它们视为具有值。例如，这会将所有没有价格的帽子销售视为"100"。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        query: {
          constant_score: {
            filter: {
              match: {
                type: 'hat'
              }
            }
          }
        },
        aggregations: {
          hat_prices: {
            sum: {
              field: 'price',
              missing: 100
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "query": {
        "constant_score": {
          "filter": {
            "match": { "type": "hat" }
          }
        }
      },
      "aggs": {
        "hat_prices": {
          "sum": {
            "field": "price",
            "missing": 100 __}
        }
      }
    }

### 直方图字段

在直方图字段上计算总和时，聚合的结果是"值"数组中所有元素的总和乘以"计数"数组中相同位置的数字。

例如，对于以下索引，该索引存储了预聚合的直方图以及不同网络的延迟指标：

    
    
    response = client.indices.create(
      index: 'metrics_index',
      body: {
        mappings: {
          properties: {
            latency_histo: {
              type: 'histogram'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'metrics_index',
      id: 1,
      refresh: true,
      body: {
        "network.name": 'net-1',
        latency_histo: {
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
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'metrics_index',
      id: 2,
      refresh: true,
      body: {
        "network.name": 'net-2',
        latency_histo: {
          values: [
            0.1,
            0.2,
            0.3,
            0.4,
            0.5
          ],
          counts: [
            8,
            17,
            8,
            7,
            6
          ]
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'metrics_index',
      size: 0,
      filter_path: 'aggregations',
      body: {
        aggregations: {
          total_latency: {
            sum: {
              field: 'latency_histo'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT metrics_index
    {
      "mappings": {
        "properties": {
          "latency_histo": { "type": "histogram" }
        }
      }
    }
    
    PUT metrics_index/_doc/1?refresh
    {
      "network.name" : "net-1",
      "latency_histo" : {
          "values" : [0.1, 0.2, 0.3, 0.4, 0.5],
          "counts" : [3, 7, 23, 12, 6]
       }
    }
    
    PUT metrics_index/_doc/2?refresh
    {
      "network.name" : "net-2",
      "latency_histo" : {
          "values" :  [0.1, 0.2, 0.3, 0.4, 0.5],
          "counts" : [8, 17, 8, 7, 6]
       }
    }
    
    POST /metrics_index/_search?size=0&filter_path=aggregations
    {
      "aggs" : {
        "total_latency" : { "sum" : { "field" : "latency_histo" } }
      }
    }

对于每个直方图字段，"sum"聚合会将"values"数组中的每个数字相加，乘以"counts"数组中的关联计数。

最终，它将添加所有直方图的所有值并返回以下结果：

    
    
    {
      "aggregations": {
        "total_latency": {
          "value": 28.8
        }
      }
    }

[« String stats aggregation](search-aggregations-metrics-string-stats-
aggregation.md) [T-test aggregation »](search-aggregations-metrics-ttest-
aggregation.md)
