

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Cumulative sum aggregation](search-aggregations-pipeline-cumulative-sum-
aggregation.md) [Extended stats bucket aggregation »](search-aggregations-
pipeline-extended-stats-bucket-aggregation.md)

## 导数聚合

父管道聚合，用于计算父直方图(或date_histogram)聚合中指定指标的导数。指定的指标必须是数字，并且封闭直方图必须将"min_doc_count"设置为"0"("直方图"聚合的默认值)。

###Syntax

"衍生"聚合孤立地如下所示：

    
    
    "derivative": {
      "buckets_path": "the_sum"
    }

**表 59."导数"参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

我们希望找到导数的存储桶的路径(有关更多详细信息，请参阅"buckets_path"语法)

|

Required

|   "gap_policy"

|

在数据中发现差距时要应用的策略(有关更多详细信息，请参阅处理数据中的差距)

|

Optional

|

"跳过""格式"

|

十进制格式模式的输出值。如果指定，则在聚合的"value_as_string"属性中返回格式化值

|

Optional

|

'null' ### First OrderDerivativeedit

以下代码片段计算每月总"销售额"的导数：

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        aggregations: {
          sales_per_month: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            },
            aggregations: {
              sales: {
                sum: {
                  field: 'price'
                }
              },
              sales_deriv: {
                derivative: {
                  buckets_path: 'sales'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search
    {
      "size": 0,
      "aggs": {
        "sales_per_month": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"
          },
          "aggs": {
            "sales": {
              "sum": {
                "field": "price"
              }
            },
            "sales_deriv": {
              "derivative": {
                "buckets_path": "sales" __}
            }
          }
        }
      }
    }

__

|

"buckets_path"指示此衍生聚合将"sales"聚合的输出用于衍生---|--- 以下是响应：

    
    
    {
       "took": 11,
       "timed_out": false,
       "_shards": ...,
       "hits": ...,
       "aggregations": {
          "sales_per_month": {
             "buckets": [
                {
                   "key_as_string": "2015/01/01 00:00:00",
                   "key": 1420070400000,
                   "doc_count": 3,
                   "sales": {
                      "value": 550.0
                   } __},
                {
                   "key_as_string": "2015/02/01 00:00:00",
                   "key": 1422748800000,
                   "doc_count": 2,
                   "sales": {
                      "value": 60.0
                   },
                   "sales_deriv": {
                      "value": -490.0 __}
                },
                {
                   "key_as_string": "2015/03/01 00:00:00",
                   "key": 1425168000000,
                   "doc_count": 2, __"sales": {
                      "value": 375.0
                   },
                   "sales_deriv": {
                      "value": 315.0
                   }
                }
             ]
          }
       }
    }

__

|

第一个桶没有导数，因为我们至少需要 2 个数据点来计算导数 ---|--- __

|

衍生值单位由"销售额"聚合和父直方图隐式定义，因此在这种情况下，假设"价格"字段的单位为 $，单位将为 $/月。   __

|

存储桶中的文档数由"doc_count"表示 ### Second OrderDerivativeedit

二阶导数可以通过将导数管道聚合链接到另一个导数管道聚合的结果来计算，如以下示例所示，该示例将计算每月总销售额的一阶和二阶导数：

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        aggregations: {
          sales_per_month: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            },
            aggregations: {
              sales: {
                sum: {
                  field: 'price'
                }
              },
              sales_deriv: {
                derivative: {
                  buckets_path: 'sales'
                }
              },
              "sales_2nd_deriv": {
                derivative: {
                  buckets_path: 'sales_deriv'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search
    {
      "size": 0,
      "aggs": {
        "sales_per_month": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"
          },
          "aggs": {
            "sales": {
              "sum": {
                "field": "price"
              }
            },
            "sales_deriv": {
              "derivative": {
                "buckets_path": "sales"
              }
            },
            "sales_2nd_deriv": {
              "derivative": {
                "buckets_path": "sales_deriv" __}
            }
          }
        }
      }
    }

__

|

二阶导数的"buckets_path"指向一阶导数的名称---|--- 以下是响应：

    
    
    {
       "took": 50,
       "timed_out": false,
       "_shards": ...,
       "hits": ...,
       "aggregations": {
          "sales_per_month": {
             "buckets": [
                {
                   "key_as_string": "2015/01/01 00:00:00",
                   "key": 1420070400000,
                   "doc_count": 3,
                   "sales": {
                      "value": 550.0
                   } __},
                {
                   "key_as_string": "2015/02/01 00:00:00",
                   "key": 1422748800000,
                   "doc_count": 2,
                   "sales": {
                      "value": 60.0
                   },
                   "sales_deriv": {
                      "value": -490.0
                   } __},
                {
                   "key_as_string": "2015/03/01 00:00:00",
                   "key": 1425168000000,
                   "doc_count": 2,
                   "sales": {
                      "value": 375.0
                   },
                   "sales_deriv": {
                      "value": 315.0
                   },
                   "sales_2nd_deriv": {
                      "value": 805.0
                   }
                }
             ]
          }
       }
    }

__

|

前两个桶没有二阶导数，因为我们需要至少 2 个来自一阶导数的数据点来计算二阶导数 ---|--- ###Unitsedit

导数聚合允许指定导数值的单位。这将在响应"normalized_value"中返回一个额外的字段，该字段以所需的 x 轴单位报告导数值。在下面的示例中，我们计算每月总销售额的导数，但要求以每天的销售额单位计算销售额的导数：

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        aggregations: {
          sales_per_month: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            },
            aggregations: {
              sales: {
                sum: {
                  field: 'price'
                }
              },
              sales_deriv: {
                derivative: {
                  buckets_path: 'sales',
                  unit: 'day'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search
    {
      "size": 0,
      "aggs": {
        "sales_per_month": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"
          },
          "aggs": {
            "sales": {
              "sum": {
                "field": "price"
              }
            },
            "sales_deriv": {
              "derivative": {
                "buckets_path": "sales",
                "unit": "day" __}
            }
          }
        }
      }
    }

__

|

"unit"指定用于导数计算的 x 轴的单位 ---|--- 以下是响应：

    
    
    {
       "took": 50,
       "timed_out": false,
       "_shards": ...,
       "hits": ...,
       "aggregations": {
          "sales_per_month": {
             "buckets": [
                {
                   "key_as_string": "2015/01/01 00:00:00",
                   "key": 1420070400000,
                   "doc_count": 3,
                   "sales": {
                      "value": 550.0
                   } __},
                {
                   "key_as_string": "2015/02/01 00:00:00",
                   "key": 1422748800000,
                   "doc_count": 2,
                   "sales": {
                      "value": 60.0
                   },
                   "sales_deriv": {
                      "value": -490.0, __"normalized_value": -15.806451612903226 __}
                },
                {
                   "key_as_string": "2015/03/01 00:00:00",
                   "key": 1425168000000,
                   "doc_count": 2,
                   "sales": {
                      "value": 375.0
                   },
                   "sales_deriv": {
                      "value": 315.0,
                      "normalized_value": 11.25
                   }
                }
             ]
          }
       }
    }

__

|

"值"以 _per month_ ---|--- __ 的原始单位报告。

|

"normalized_value"以所需的_per day_单位报告« 累积总和聚合 扩展统计信息存储桶聚合 »