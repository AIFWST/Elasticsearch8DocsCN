

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Median absolute deviation aggregation](search-aggregations-metrics-median-
absolute-deviation-aggregation.md) [Percentile ranks aggregation »](search-
aggregations-metrics-percentile-rank-aggregation.md)

## 最小聚合

"单值"指标聚合，用于跟踪并返回从聚合文档中提取的数值中的最小值。

"最小"和"最大"聚合对数据的"双重"表示进行操作。因此，在绝对值大于 '2^53' 的长整型上运行时，结果可能是近似值。

计算所有文档的最小价格值：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          min_price: {
            min: {
              field: 'price'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "min_price": { "min": { "field": "price" } }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "min_price": {
          "value": 10.0
        }
      }
    }

可以看出，聚合的名称(上面的"min_price")也充当从返回的响应中检索聚合结果的键。

###Script

如果需要获取比单个字段更复杂的内容的"min"，请在运行时字段上运行聚合。

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        runtime_mappings: {
          "price.adjusted": {
            type: 'double',
            script: "\n        double price = doc['price'].value;\n        if (doc['promoted'].value) {\n          price *= 0.8;\n        }\n        emit(price);\n      "
          }
        },
        aggregations: {
          min_price: {
            min: {
              field: 'price.adjusted'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search
    {
      "size": 0,
      "runtime_mappings": {
        "price.adjusted": {
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
      "aggs": {
        "min_price": {
          "min": { "field": "price.adjusted" }
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      index: 'sales',
      body: {
        aggregations: {
          grade_min: {
            min: {
              field: 'grade',
              missing: 10
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search
    {
      "aggs": {
        "grade_min": {
          "min": {
            "field": "grade",
            "missing": 10 __}
        }
      }
    }

__

|

"grade"字段中没有值的文档将与值为"10"的文档属于同一存储桶。   ---|--- ### 直方图字段编辑

当在直方图字段上计算"min"时，聚合的结果是"values"数组中所有元素的最小值。请注意，直方图的"计数"数组将被忽略。

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
          min_latency: {
            min: {
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
        "min_latency" : { "min" : { "field" : "latency_histo" } }
      }
    }

"min"聚合将返回所有直方图字段的最小值：

    
    
    {
      "aggregations": {
        "min_latency": {
          "value": 0.1
        }
      }
    }

[« Median absolute deviation aggregation](search-aggregations-metrics-median-
absolute-deviation-aggregation.md) [Percentile ranks aggregation »](search-
aggregations-metrics-percentile-rank-aggregation.md)
