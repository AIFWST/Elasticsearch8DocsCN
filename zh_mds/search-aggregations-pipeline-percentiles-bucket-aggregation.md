

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Normalize aggregation](search-aggregations-pipeline-normalize-
aggregation.md) [Serial differencing aggregation »](search-aggregations-
pipeline-serialdiff-aggregation.md)

## 百分位数存储桶聚合

同级管道聚合，用于计算同级聚合中指定指标的所有存储桶的百分位数。指定的指标必须是数字，同级聚合必须是多存储桶聚合。

###Syntax

"percentiles_bucket"聚合单独如下所示：

    
    
    {
      "percentiles_bucket": {
        "buckets_path": "the_sum"
      }
    }

**表 76.'percentiles_bucket' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

我们希望找到百分位数的存储桶的路径(有关更多详细信息，请参阅"buckets_path"语法)

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

"空""百分比"

|

要计算的百分位数列表

|

Optional

|

'[ 1， 5， 25， 50， 75， 95， 99 ]" '键控'

|

标志，它将范围作为哈希而不是键值对数组返回

|

Optional

|

"true" 以下代码片段计算每月"销售额"存储桶总数的百分位数：

    
    
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
          percentiles_monthly_sales: {
            percentiles_bucket: {
              buckets_path: 'sales_per_month>sales',
              percents: [
                25,
                50,
                75
              ]
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
        "percentiles_monthly_sales": {
          "percentiles_bucket": {
            "buckets_path": "sales_per_month>sales", __"percents": [ 25.0, 50.0, 75.0 ] __}
        }
      }
    }

__

|

"buckets_path"指示此percentiles_bucket聚合，我们要计算"sales_per_month"日期直方图中"销售"聚合的百分位数。   ---|---    __

|

"百分比"指定我们希望计算的百分位数，在本例中为第 25、50 和 75 个百分位数。   以下是可能的响应：

    
    
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
          "percentiles_monthly_sales": {
            "values" : {
                "25.0": 375.0,
                "50.0": 375.0,
                "75.0": 550.0
             }
          }
       }
    }

### Percentiles_bucketimplementation

百分位存储桶返回不大于请求的百分位数的最近输入数据点;它不会在数据点之间进行插值。

百分位数是精确计算的，不是近似值(与百分位数度量不同)。这意味着在丢弃数据之前，实现会维护数据的内存中排序列表以计算百分位数。如果您尝试在单个"percentiles_bucket"中计算数百万个数据点的百分位数，则可能会遇到内存压力问题。

[« Normalize aggregation](search-aggregations-pipeline-normalize-
aggregation.md) [Serial differencing aggregation »](search-aggregations-
pipeline-serialdiff-aggregation.md)
