

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Derivative aggregation](search-aggregations-pipeline-derivative-
aggregation.md) [Inference bucket aggregation »](search-aggregations-
pipeline-inference-bucket-aggregation.md)

## 扩展统计信息存储桶聚合

同级管道聚合，用于计算同级聚合中指定指标的所有存储桶的各种统计信息。指定的指标必须是数字，同级聚合必须是多存储桶聚合。

与"stats_bucket"聚合相比，此聚合提供了更多的统计信息(平方和、标准偏差等)。

###Syntax

"extended_stats_bucket"聚合单独如下所示：

    
    
    {
      "extended_stats_bucket": {
        "buckets_path": "the_sum"
      }
    }

**表 60.'extended_stats_bucket' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

我们希望计算其统计信息的存储桶的路径(有关更多详细信息，请参阅"buckets_path"语法)

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

'空' '西格玛'

|

高于/低于要显示的平均值的标准差数

|

Optional

|

2 以下代码段计算了每月"销售"存储桶的扩展统计信息：

    
    
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
              }
            }
          },
          stats_monthly_sales: {
            extended_stats_bucket: {
              buckets_path: 'sales_per_month>sales'
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
            }
          }
        },
        "stats_monthly_sales": {
          "extended_stats_bucket": {
            "buckets_path": "sales_per_month>sales" __}
        }
      }
    }

__

|

"bucket_paths"指示此"extended_stats_bucket"聚合，我们希望计算"sales_per_month"日期直方图中"销售"聚合的统计信息。   ---|--- 以下可能是响应：

    
    
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
                   }
                },
                {
                   "key_as_string": "2015/02/01 00:00:00",
                   "key": 1422748800000,
                   "doc_count": 2,
                   "sales": {
                      "value": 60.0
                   }
                },
                {
                   "key_as_string": "2015/03/01 00:00:00",
                   "key": 1425168000000,
                   "doc_count": 2,
                   "sales": {
                      "value": 375.0
                   }
                }
             ]
          },
          "stats_monthly_sales": {
             "count": 3,
             "min": 60.0,
             "max": 550.0,
             "avg": 328.3333333333333,
             "sum": 985.0,
             "sum_of_squares": 446725.0,
             "variance": 41105.55555555556,
             "variance_population": 41105.55555555556,
             "variance_sampling": 61658.33333333334,
             "std_deviation": 202.74505063146563,
             "std_deviation_population": 202.74505063146563,
             "std_deviation_sampling": 248.3109609609156,
             "std_deviation_bounds": {
               "upper": 733.8234345962646,
               "lower": -77.15676792959795,
               "upper_population" : 733.8234345962646,
               "lower_population" : -77.15676792959795,
               "upper_sampling" : 824.9552552551645,
               "lower_sampling" : -168.28858858849787
             }
          }
       }
    }

[« Derivative aggregation](search-aggregations-pipeline-derivative-
aggregation.md) [Inference bucket aggregation »](search-aggregations-
pipeline-inference-bucket-aggregation.md)
