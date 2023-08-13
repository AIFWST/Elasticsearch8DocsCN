

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Percentiles aggregation](search-aggregations-metrics-percentile-
aggregation.md) [Scripted metric aggregation »](search-aggregations-metrics-
scripted-metric-aggregation.md)

## 速率聚合

"速率"指标聚合只能在"date_histogram"或"复合"聚合中使用。它计算每个存储桶中的文档或字段的速率。可以从文档中的特定数值或直方图字段中提取字段值。

对于"复合"聚合，必须只有一个"date_histogram"源才能支持"速率"聚合。

###Syntax

"rate"聚合单独如下所示：

    
    
    {
      "rate": {
        "unit": "month",
        "field": "requests"
      }
    }

以下请求会将所有销售记录分组到每月存储桶中，然后将每个存储桶中的销售事务数转换为每年的销售率。

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        aggregations: {
          by_date: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            },
            aggregations: {
              my_rate: {
                rate: {
                  unit: 'year'
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
      "size": 0,
      "aggs": {
        "by_date": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"  __},
          "aggs": {
            "my_rate": {
              "rate": {
                "unit": "year" __}
            }
          }
        }
      }
    }

__

|

直方图按月分组。   ---|---    __

|

但该费率转换为年费率。   响应将返回每个存储桶中的年事务率。由于每年有 12 个月，因此年费率将通过将每月费率乘以 12 来自动计算。

    
    
    {
      ...
      "aggregations" : {
        "by_date" : {
          "buckets" : [
            {
              "key_as_string" : "2015/01/01 00:00:00",
              "key" : 1420070400000,
              "doc_count" : 3,
              "my_rate" : {
                "value" : 36.0
              }
            },
            {
              "key_as_string" : "2015/02/01 00:00:00",
              "key" : 1422748800000,
              "doc_count" : 2,
              "my_rate" : {
                "value" : 24.0
              }
            },
            {
              "key_as_string" : "2015/03/01 00:00:00",
              "key" : 1425168000000,
              "doc_count" : 2,
              "my_rate" : {
                "value" : 24.0
              }
            }
          ]
        }
      }
    }

除了计算文档数量外，还可以计算每个存储桶中文档中字段的所有值的总和或每个存储桶中的值数。以下请求会将所有销售记录分组到每月存储桶中，然后计算每月总销售额并将其转换为平均每日销售额。

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        aggregations: {
          by_date: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            },
            aggregations: {
              avg_price: {
                rate: {
                  field: 'price',
                  unit: 'day'
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
      "size": 0,
      "aggs": {
        "by_date": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"  __},
          "aggs": {
            "avg_price": {
              "rate": {
                "field": "price", __"unit": "day" __}
            }
          }
        }
      }
    }

__

|

直方图按月分组。   ---|---    __

|

计算所有销售价格的总和 __

|

转换为平均每日销售额 响应将包含每月的平均每日销售价格。

    
    
    {
      ...
      "aggregations" : {
        "by_date" : {
          "buckets" : [
            {
              "key_as_string" : "2015/01/01 00:00:00",
              "key" : 1420070400000,
              "doc_count" : 3,
              "avg_price" : {
                "value" : 17.741935483870968
              }
            },
            {
              "key_as_string" : "2015/02/01 00:00:00",
              "key" : 1422748800000,
              "doc_count" : 2,
              "avg_price" : {
                "value" : 2.142857142857143
              }
            },
            {
              "key_as_string" : "2015/03/01 00:00:00",
              "key" : 1425168000000,
              "doc_count" : 2,
              "avg_price" : {
                "value" : 12.096774193548388
              }
            }
          ]
        }
      }
    }

您还可以利用"复合"聚合来计算库存中每件商品的平均每日销售价格

    
    
    response = client.search(
      index: 'sales',
      filter_path: 'aggregations',
      size: 0,
      body: {
        aggregations: {
          buckets: {
            composite: {
              sources: [
                {
                  month: {
                    date_histogram: {
                      field: 'date',
                      calendar_interval: 'month'
                    }
                  }
                },
                {
                  type: {
                    terms: {
                      field: 'type'
                    }
                  }
                }
              ]
            },
            aggregations: {
              avg_price: {
                rate: {
                  field: 'price',
                  unit: 'day'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET sales/_search?filter_path=aggregations&size=0
    {
      "aggs": {
        "buckets": {
          "composite": { __"sources": [
              {
                "month": {
                  "date_histogram": { __"field": "date",
                    "calendar_interval": "month"
                  }
                }
              },
              {
                "type": { __"terms": {
                    "field": "type"
                  }
                }
              }
            ]
          },
          "aggs": {
            "avg_price": {
              "rate": {
                "field": "price", __"unit": "day" __}
            }
          }
        }
      }
    }

__

|

具有日期直方图源和项类型源的复合聚合。   ---|---    __

|

每月 __ 的日期直方图源分组

|

每个销售物料类型的术语来源分组 __

|

计算每月和商品的所有销售价格的总和 __

|

转换为每件商品的平均每日销售额 响应将包含每个物料每月的平均每日销售价格。

    
    
    {
      "aggregations" : {
        "buckets" : {
          "after_key" : {
            "month" : 1425168000000,
            "type" : "t-shirt"
          },
          "buckets" : [
            {
              "key" : {
                "month" : 1420070400000,
                "type" : "bag"
              },
              "doc_count" : 1,
              "avg_price" : {
                "value" : 4.838709677419355
              }
            },
            {
              "key" : {
                "month" : 1420070400000,
                "type" : "hat"
              },
              "doc_count" : 1,
              "avg_price" : {
                "value" : 6.451612903225806
              }
            },
            {
              "key" : {
                "month" : 1420070400000,
                "type" : "t-shirt"
              },
              "doc_count" : 1,
              "avg_price" : {
                "value" : 6.451612903225806
              }
            },
            {
              "key" : {
                "month" : 1422748800000,
                "type" : "hat"
              },
              "doc_count" : 1,
              "avg_price" : {
                "value" : 1.7857142857142858
              }
            },
            {
              "key" : {
                "month" : 1422748800000,
                "type" : "t-shirt"
              },
              "doc_count" : 1,
              "avg_price" : {
                "value" : 0.35714285714285715
              }
            },
            {
              "key" : {
                "month" : 1425168000000,
                "type" : "hat"
              },
              "doc_count" : 1,
              "avg_price" : {
                "value" : 6.451612903225806
              }
            },
            {
              "key" : {
                "month" : 1425168000000,
                "type" : "t-shirt"
              },
              "doc_count" : 1,
              "avg_price" : {
                "value" : 5.645161290322581
              }
            }
          ]
        }
      }
    }

通过添加值为"value_count"的 'mode' 参数，我们可以将计算从 'sum' 更改为字段的值数量：

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        aggregations: {
          by_date: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            },
            aggregations: {
              avg_number_of_sales_per_year: {
                rate: {
                  field: 'price',
                  unit: 'year',
                  mode: 'value_count'
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
      "size": 0,
      "aggs": {
        "by_date": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"  __},
          "aggs": {
            "avg_number_of_sales_per_year": {
              "rate": {
                "field": "price", __"unit": "year", __"mode": "value_count" __}
            }
          }
        }
      }
    }

__

|

直方图按月分组。   ---|---    __

|

计算所有销售价格的数量 __

|

转换为年度计数 __

|

将模式更改为值计数 响应将包含每个月的平均每日销售价格。

    
    
    {
      ...
      "aggregations" : {
        "by_date" : {
          "buckets" : [
            {
              "key_as_string" : "2015/01/01 00:00:00",
              "key" : 1420070400000,
              "doc_count" : 3,
              "avg_number_of_sales_per_year" : {
                "value" : 36.0
              }
            },
            {
              "key_as_string" : "2015/02/01 00:00:00",
              "key" : 1422748800000,
              "doc_count" : 2,
              "avg_number_of_sales_per_year" : {
                "value" : 24.0
              }
            },
            {
              "key_as_string" : "2015/03/01 00:00:00",
              "key" : 1425168000000,
              "doc_count" : 2,
              "avg_number_of_sales_per_year" : {
                "value" : 24.0
              }
            }
          ]
        }
      }
    }

默认情况下使用"总和"模式。

"模式"："总和"

     calculate the sum of all values field 
`"mode": "value_count"`

     use the number of values in the field 

### 存储桶大小和速率之间的关系

"速率"聚合支持可用于"date_histogram"聚合calendar_intervalsparameter的所有速率。指定的速率应与"date_histogram"聚合间隔兼容，即应该可以将存储桶大小转换为速率。默认情况下，使用"date_histogram"的间隔。

"速率"： "秒"

     compatible with all intervals 
`"rate": "minute"`

     compatible with all intervals 
`"rate": "hour"`

     compatible with all intervals 
`"rate": "day"`

     compatible with all intervals 
`"rate": "week"`

     compatible with all intervals 
`"rate": "month"`

     compatible with only with `month`, `quarter` and `year` calendar intervals 
`"rate": "quarter"`

     compatible with only with `month`, `quarter` and `year` calendar intervals 
`"rate": "year"`

     compatible with only with `month`, `quarter` and `year` calendar intervals 

如果日期直方图不是速率直方图的直接父级，则还有一个额外的限制。在这种情况下，速率区间和直方图区间必须在同一组中：["秒"、"分钟"、"小时"、"天"、"周"]或["月"、"季度"、"年"]。例如，如果日期直方图基于"月"，则仅支持"月"、"季度"或"年"的速率间隔。如果日期直方图基于"天"，则仅支持"秒"、"分钟"、"小时"、"天"和"周"速率间隔。

###Script

如果需要针对未编制索引的值运行聚合，请在运行时字段上运行聚合。例如，如果我们需要在计算费率之前调整价格：

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        runtime_mappings: {
          "price.adjusted": {
            type: 'double',
            script: {
              source: "emit(doc['price'].value * params.adjustment)",
              params: {
                adjustment: 0.9
              }
            }
          }
        },
        aggregations: {
          by_date: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            },
            aggregations: {
              avg_price: {
                rate: {
                  field: 'price.adjusted'
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
      "size": 0,
      "runtime_mappings": {
        "price.adjusted": {
          "type": "double",
          "script": {
            "source": "emit(doc['price'].value * params.adjustment)",
            "params": {
              "adjustment": 0.9
            }
          }
        }
      },
      "aggs": {
        "by_date": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"
          },
          "aggs": {
            "avg_price": {
              "rate": {
                "field": "price.adjusted"
              }
            }
          }
        }
      }
    }
    
    
    {
      ...
      "aggregations" : {
        "by_date" : {
          "buckets" : [
            {
              "key_as_string" : "2015/01/01 00:00:00",
              "key" : 1420070400000,
              "doc_count" : 3,
              "avg_price" : {
                "value" : 495.0
              }
            },
            {
              "key_as_string" : "2015/02/01 00:00:00",
              "key" : 1422748800000,
              "doc_count" : 2,
              "avg_price" : {
                "value" : 54.0
              }
            },
            {
              "key_as_string" : "2015/03/01 00:00:00",
              "key" : 1425168000000,
              "doc_count" : 2,
              "avg_price" : {
                "value" : 337.5
              }
            }
          ]
        }
      }
    }

[« Percentiles aggregation](search-aggregations-metrics-percentile-
aggregation.md) [Scripted metric aggregation »](search-aggregations-metrics-
scripted-metric-aggregation.md)
