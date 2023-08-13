

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Pipeline aggregations](search-aggregations-pipeline.md) [Bucket script
aggregation »](search-aggregations-pipeline-bucket-script-aggregation.md)

## 平均存储桶聚合

同级管道聚合，用于计算同级聚合中指定指标的平均值。指定的指标必须是数字，同级聚合必须是多存储桶聚合。

###Syntax

    
    
    "avg_bucket": {
      "buckets_path": "sales_per_month>sales",
      "gap_policy": "skip",
      "format": "#,##0.00;(#,##0.00)"
    }

###Parameters

`buckets_path`

     (Required, string) Path to the buckets to average. For syntax, see [`buckets_path` Syntax](search-aggregations-pipeline.html#buckets-path-syntax "buckets_path Syntax"). 
`gap_policy`

     (Optional, string) Policy to apply when gaps are found in the data. For valid values, see [Dealing with gaps in the data](search-aggregations-pipeline.html#gap-policy "Dealing with gaps in the data"). Defaults to `skip`. 
`format`

     (Optional, string) [DecimalFormat pattern](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) for the output value. If specified, the formatted value is returned in the aggregation's `value_as_string` property. 

### 响应正文

`value`

     (float) Mean average value for the metric specified in `buckets_path`. 
`value_as_string`

     (string) Formatted output value for the aggregation. This property is only provided if a `format` is specified in the request. 

###Example

以下"avg_monthly_sales"聚合使用"avg_bucket"来计算每月的平均销售额：

    
    
    POST _search
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
        "avg_monthly_sales": {
    // tag::avg-bucket-agg-syntax[]               __"avg_bucket": {
            "buckets_path": "sales_per_month >sales",
            "gap_policy": "skip",
            "format": "#,##0.00;(#,##0.00)"
          }
    // end::avg-bucket-agg-syntax[]               __}
      }
    }

__

|

"avg_bucket"配置的开始。注释不是示例的一部分。   ---|---    __

|

"avg_bucket"配置结束。注释不是示例的一部分。   请求返回以下响应：

    
    
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
        "avg_monthly_sales": {
          "value": 328.33333333333333,
          "value_as_string": "328.33"
        }
      }
    }

[« Pipeline aggregations](search-aggregations-pipeline.md) [Bucket script
aggregation »](search-aggregations-pipeline-bucket-script-aggregation.md)
