

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Max bucket aggregation](search-aggregations-pipeline-max-bucket-
aggregation.md) [Moving function aggregation »](search-aggregations-
pipeline-movfn-aggregation.md)

## 最小桶聚合

同级管道聚合，用于标识具有同级聚合中指定指标的最小值的存储桶，并输出存储桶的值和键。指定的指标必须是数字，并且同级聚合必须是多存储桶聚合。

###Syntax

"min_bucket"聚合单独如下所示：

    
    
    {
      "min_bucket": {
        "buckets_path": "the_sum"
      }
    }

**表 63.'min_bucket' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

我们希望找到最小值的存储桶的路径(有关更多详细信息，请参阅"buckets_path"语法)

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

"null" 以下代码段计算每月总"销售额"的最小值：

    
    
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
          min_monthly_sales: {
            min_bucket: {
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
        "min_monthly_sales": {
          "min_bucket": {
            "buckets_path": "sales_per_month>sales" __}
        }
      }
    }

__

|

"buckets_path"指示此min_bucket聚合，我们希望在"sales_per_month"日期直方图中显示"sales"聚合的最小值。   ---|--- 以下可能是响应：

    
    
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
          "min_monthly_sales": {
              "keys": ["2015/02/01 00:00:00"], __"value": 60.0
          }
       }
    }

__

|

"keys"是一个字符串数组，因为最小值可能存在于多个存储桶中 ---|--- « 最大桶聚合 移动函数聚合 »