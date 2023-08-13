

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Serial differencing aggregation](search-aggregations-pipeline-serialdiff-
aggregation.md) [Sum bucket aggregation »](search-aggregations-pipeline-sum-
bucket-aggregation.md)

## 统计桶聚合

同级管道聚合，用于计算同级聚合中指定指标的所有存储桶的各种统计信息。指定的指标必须是数字，同级聚合必须是多存储桶聚合。

###Syntax

"stats_bucket"聚合单独如下所示：

    
    
    {
      "stats_bucket": {
        "buckets_path": "the_sum"
      }
    }

**表 78.'stats_bucket' 参数**

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

"null" 以下代码段计算每月"销售额"的统计信息：

    
    
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
            stats_bucket: {
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
          "stats_bucket": {
            "buckets_path": "sales_per_month>sales" __}
        }
      }
    }

__

|

"bucket_paths"指示此"stats_bucket"聚合，我们希望在"sales_per_month"日期直方图中计算"销售"聚合的统计信息。   ---|--- 以下可能是响应：

    
    
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
             "sum": 985.0
          }
       }
    }

[« Serial differencing aggregation](search-aggregations-pipeline-serialdiff-
aggregation.md) [Sum bucket aggregation »](search-aggregations-pipeline-sum-
bucket-aggregation.md)
