

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Max aggregation](search-aggregations-metrics-max-aggregation.md) [Min
aggregation »](search-aggregations-metrics-min-aggregation.md)

## 中值绝对偏差聚合

这种"单值"聚合近似于其搜索结果的中位数绝对偏差。

中位数绝对偏差是变异性的度量。它是一个稳健的统计量，这意味着它可用于描述可能具有异常值或可能不呈正态分布的数据。对于此类数据，它可能比标准差更具描述性。

它计算为每个数据点与整个样本中位数的偏差的中位数。也就是说，对于随机变量 X，中位数绝对偏差是中位数(|中位数(X) - Xi|)。

###Example

假设我们的数据代表一到五星的产品评论。此类评论通常总结为平均值，这很容易理解，但不能描述评论的可变性。估计中位数绝对偏差可以深入了解评论之间的差异程度。

在此示例中，我们有一个产品的平均评级为 3 星。让我们看看它的评级中位数绝对偏差，以确定它们的变化程度

    
    
    response = client.search(
      index: 'reviews',
      body: {
        size: 0,
        aggregations: {
          review_average: {
            avg: {
              field: 'rating'
            }
          },
          review_variability: {
            median_absolute_deviation: {
              field: 'rating'
            }
          }
        }
      }
    )
    puts response
    
    
    GET reviews/_search
    {
      "size": 0,
      "aggs": {
        "review_average": {
          "avg": {
            "field": "rating"
          }
        },
        "review_variability": {
          "median_absolute_deviation": {
            "field": "rating" __}
        }
      }
    }

__

|

"rating"必须是数值字段 ---|--- 由此产生的中位数绝对偏差"2"告诉我们，评级存在相当大的变异性。审阅者必须对此产品有不同的意见。

    
    
    {
      ...
      "aggregations": {
        "review_average": {
          "value": 3.0
        },
        "review_variability": {
          "value": 2.0
        }
      }
    }

###Approximation

计算中值绝对偏差的朴素实现将整个样本存储在内存中，因此此聚合改为计算近似值。它使用 TDigest 数据结构来近似样本中位数和与样本中位数的偏差中位数。有关 TDigests 的近似特征的更多信息，请参阅百分位数是(通常)近似近似")。

资源使用与 TDigest 分位数近似的准确性之间的权衡，以及此聚合近似中位数绝对偏差的准确性，由"压缩"参数控制。更高的"压缩"设置以更高的内存使用率为代价提供了更准确的近似值。有关 TDigest"压缩"参数特性的更多信息，请参阅压缩。

    
    
    response = client.search(
      index: 'reviews',
      body: {
        size: 0,
        aggregations: {
          review_variability: {
            median_absolute_deviation: {
              field: 'rating',
              compression: 100
            }
          }
        }
      }
    )
    puts response
    
    
    GET reviews/_search
    {
      "size": 0,
      "aggs": {
        "review_variability": {
          "median_absolute_deviation": {
            "field": "rating",
            "compression": 100
          }
        }
      }
    }

此聚合的默认"压缩"值为"1000"。在此压缩级别下，此聚合通常在确切结果的 5% 以内，但观察到的性能将取决于样本数据。

###Script

在上面的示例中，产品评论的等级为 1 到 5。如果要将它们修改为 1 到 10 的比例，请使用运行时字段。

    
    
    response = client.search(
      index: 'reviews',
      filter_path: 'aggregations',
      body: {
        size: 0,
        runtime_mappings: {
          "rating.out_of_ten": {
            type: 'long',
            script: {
              source: "emit(doc['rating'].value * params.scaleFactor)",
              params: {
                "scaleFactor": 2
              }
            }
          }
        },
        aggregations: {
          review_average: {
            avg: {
              field: 'rating.out_of_ten'
            }
          },
          review_variability: {
            median_absolute_deviation: {
              field: 'rating.out_of_ten'
            }
          }
        }
      }
    )
    puts response
    
    
    GET reviews/_search?filter_path=aggregations
    {
      "size": 0,
      "runtime_mappings": {
        "rating.out_of_ten": {
          "type": "long",
          "script": {
            "source": "emit(doc['rating'].value * params.scaleFactor)",
            "params": {
              "scaleFactor": 2
            }
          }
        }
      },
      "aggs": {
        "review_average": {
          "avg": {
            "field": "rating.out_of_ten"
          }
        },
        "review_variability": {
          "median_absolute_deviation": {
            "field": "rating.out_of_ten"
          }
        }
      }
    }

这将导致：

    
    
    {
      "aggregations": {
        "review_average": {
          "value": 6.0
        },
        "review_variability": {
          "value": 4.0
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

让我们保持乐观，并假设一些评论者非常喜欢该产品，以至于他们忘记给它评分。我们将给他们分配五颗星

    
    
    response = client.search(
      index: 'reviews',
      body: {
        size: 0,
        aggregations: {
          review_variability: {
            median_absolute_deviation: {
              field: 'rating',
              missing: 5
            }
          }
        }
      }
    )
    puts response
    
    
    GET reviews/_search
    {
      "size": 0,
      "aggs": {
        "review_variability": {
          "median_absolute_deviation": {
            "field": "rating",
            "missing": 5
          }
        }
      }
    }

[« Max aggregation](search-aggregations-metrics-max-aggregation.md) [Min
aggregation »](search-aggregations-metrics-min-aggregation.md)
