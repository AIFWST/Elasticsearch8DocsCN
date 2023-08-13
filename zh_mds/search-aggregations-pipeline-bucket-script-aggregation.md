

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Average bucket aggregation](search-aggregations-pipeline-avg-bucket-
aggregation.md) [Bucket count K-S test correlation aggregation »](search-
aggregations-bucket-count-ks-test-aggregation.md)

## 桶脚本聚合

父管道聚合，它执行一个脚本，该脚本可以对父多存储桶聚合中的指定指标执行每个存储桶计算。指定的指标必须是数字，并且脚本必须返回数字值。

###Syntax

"bucket_script"聚合单独如下所示：

    
    
    {
      "bucket_script": {
        "buckets_path": {
          "my_var1": "the_sum",                     __"my_var2": "the_value_count"
        },
        "script": "params.my_var1 / params.my_var2"
      }
    }

__

|

此处，"my_var1"是要在脚本中使用的此存储桶路径的变量名称，"the_sum"是要用于该变量的指标的路径。   ---|--- **表 54.'bucket_script' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'script'

|

要为此聚合运行的脚本。脚本可以是内联的、文件或索引的。(有关更多详细信息，请参阅脚本)

|

Required

|   "buckets_path"

|

脚本变量及其关联路径的映射，指向我们希望用于变量的存储桶(有关更多详细信息，请参阅"buckets_path"语法)

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

"null" 以下代码段计算 T 恤销售额与每月总销售额的比率百分比：

    
    
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
              total_sales: {
                sum: {
                  field: 'price'
                }
              },
              "t-shirts": {
                filter: {
                  term: {
                    type: 't-shirt'
                  }
                },
                aggregations: {
                  sales: {
                    sum: {
                      field: 'price'
                    }
                  }
                }
              },
              "t-shirt-percentage": {
                bucket_script: {
                  buckets_path: {
                    "tShirtSales": 't-shirts>sales',
                    "totalSales": 'total_sales'
                  },
                  script: 'params.tShirtSales / params.totalSales * 100'
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
            "total_sales": {
              "sum": {
                "field": "price"
              }
            },
            "t-shirts": {
              "filter": {
                "term": {
                  "type": "t-shirt"
                }
              },
              "aggs": {
                "sales": {
                  "sum": {
                    "field": "price"
                  }
                }
              }
            },
            "t-shirt-percentage": {
              "bucket_script": {
                "buckets_path": {
                  "tShirtSales": "t-shirts>sales",
                  "totalSales": "total_sales"
                },
                "script": "params.tShirtSales / params.totalSales * 100"
              }
            }
          }
        }
      }
    }

以下是可能的响应：

    
    
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
                   "total_sales": {
                       "value": 550.0
                   },
                   "t-shirts": {
                       "doc_count": 1,
                       "sales": {
                           "value": 200.0
                       }
                   },
                   "t-shirt-percentage": {
                       "value": 36.36363636363637
                   }
                },
                {
                   "key_as_string": "2015/02/01 00:00:00",
                   "key": 1422748800000,
                   "doc_count": 2,
                   "total_sales": {
                       "value": 60.0
                   },
                   "t-shirts": {
                       "doc_count": 1,
                       "sales": {
                           "value": 10.0
                       }
                   },
                   "t-shirt-percentage": {
                       "value": 16.666666666666664
                   }
                },
                {
                   "key_as_string": "2015/03/01 00:00:00",
                   "key": 1425168000000,
                   "doc_count": 2,
                   "total_sales": {
                       "value": 375.0
                   },
                   "t-shirts": {
                       "doc_count": 1,
                       "sales": {
                           "value": 175.0
                       }
                   },
                   "t-shirt-percentage": {
                       "value": 46.666666666666664
                   }
                }
             ]
          }
       }
    }

[« Average bucket aggregation](search-aggregations-pipeline-avg-bucket-
aggregation.md) [Bucket count K-S test correlation aggregation »](search-
aggregations-bucket-count-ks-test-aggregation.md)
