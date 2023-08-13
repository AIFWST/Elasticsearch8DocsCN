

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Bucket count K-S test correlation aggregation](search-aggregations-bucket-
count-ks-test-aggregation.md) [Bucket selector aggregation »](search-
aggregations-pipeline-bucket-selector-aggregation.md)

## 桶关联聚合

同级管道聚合，对配置的同级多桶聚合执行关联函数。

###Parameters

`buckets_path`

     (Required, string) Path to the buckets that contain one set of values to correlate. For syntax, see [`buckets_path` Syntax](search-aggregations-pipeline.html#buckets-path-syntax "buckets_path Syntax"). 
`function`

    

(必填，对象)要执行的相关函数。

"函数"的属性

`count_correlation`

    

(必填*，对象)用于计算计数相关性的配置。此函数旨在确定术语值和给定指标的相关性。因此，它需要满足以下要求。

* "buckets_path"必须指向"_count"指标。  * 所有"bucket_path"计数值的总计数必须小于或等于"指示器.doc_计数"。  * 使用此功能时，需要进行初始计算以收集所需的"指标"值。

"count_correlation"的属性

`indicator`

    

(必填，对象)用于关联配置的"bucket_path"值的指示器。

"指标"的属性

`doc_count`

     (Required, integer) The total number of documents that initially created the `expectations`. It's required to be greater than or equal to the sum of all values in the `buckets_path` as this is the originating superset of data to which the term values are correlated. 
`expectations`

     (Required, array) An array of numbers with which to correlate the configured `bucket_path` values. The length of this value must always equal the number of buckets returned by the `bucket_path`. 
`fractions`

     (Optional, array) An array of fractions to use when averaging and calculating variance. This should be used if the pre-calculated data and the `buckets_path` have known gaps. The length of `fractions`, if provided, must equal `expectations`. 

###Syntax

"bucket_correlation"聚合单独如下所示：

    
    
    {
      "bucket_correlation": {
        "buckets_path": "range_values>_count", __"function": {
          "count_correlation": { __"indicator": {
              "expectations": [...],
              "doc_count": 10000
            }
          }
        }
      }
    }

__

|

包含要关联的值的存储桶。   ---|---    __

|

相关函数定义。   ###Exampleedit

以下代码片段将"版本"字段中的各个术语与"延迟"指标相关联。未显示的是"延迟"指标值的预计算，这是使用百分位数聚合完成的。

此示例仅使用 10s 百分位数。

    
    
    POST correlate_latency/_search?size=0&filter_path=aggregations
    {
      "aggs": {
        "buckets": {
          "terms": { __"field": "version",
            "size": 2
          },
          "aggs": {
            "latency_ranges": {
              "range": { __"field": "latency",
                "ranges": [
                  { "to": 0.0 },
                  { "from": 0, "to": 105 },
                  { "from": 105, "to": 225 },
                  { "from": 225, "to": 445 },
                  { "from": 445, "to": 665 },
                  { "from": 665, "to": 885 },
                  { "from": 885, "to": 1115 },
                  { "from": 1115, "to": 1335 },
                  { "from": 1335, "to": 1555 },
                  { "from": 1555, "to": 1775 },
                  { "from": 1775 }
                ]
              }
            },
            "bucket_correlation": { __"bucket_correlation": {
                "buckets_path": "latency_ranges >_count",
                "function": {
                  "count_correlation": {
                    "indicator": {
                       "expectations": [0, 52.5, 165, 335, 555, 775, 1000, 1225, 1445, 1665, 1775],
                       "doc_count": 200
                    }
                  }
                }
              }
            }
          }
        }
      }
    }

__

|

包含范围聚合和存储桶关联聚合的术语存储桶。两者都用于计算项值与延迟的相关性。   ---|---    __

|

延迟字段上的范围聚合。这些范围是参考延迟字段的百分位数创建的。   __

|

存储桶相关性聚合，用于计算每个范围内的术语值数与先前计算的指标值的相关性。   以下是可能的响应：

    
    
    {
      "aggregations" : {
        "buckets" : {
          "doc_count_error_upper_bound" : 0,
          "sum_other_doc_count" : 0,
          "buckets" : [
            {
              "key" : "1.0",
              "doc_count" : 100,
              "latency_ranges" : {
                "buckets" : [
                  {
                    "key" : "*-0.0",
                    "to" : 0.0,
                    "doc_count" : 0
                  },
                  {
                    "key" : "0.0-105.0",
                    "from" : 0.0,
                    "to" : 105.0,
                    "doc_count" : 1
                  },
                  {
                    "key" : "105.0-225.0",
                    "from" : 105.0,
                    "to" : 225.0,
                    "doc_count" : 9
                  },
                  {
                    "key" : "225.0-445.0",
                    "from" : 225.0,
                    "to" : 445.0,
                    "doc_count" : 0
                  },
                  {
                    "key" : "445.0-665.0",
                    "from" : 445.0,
                    "to" : 665.0,
                    "doc_count" : 0
                  },
                  {
                    "key" : "665.0-885.0",
                    "from" : 665.0,
                    "to" : 885.0,
                    "doc_count" : 0
                  },
                  {
                    "key" : "885.0-1115.0",
                    "from" : 885.0,
                    "to" : 1115.0,
                    "doc_count" : 10
                  },
                  {
                    "key" : "1115.0-1335.0",
                    "from" : 1115.0,
                    "to" : 1335.0,
                    "doc_count" : 20
                  },
                  {
                    "key" : "1335.0-1555.0",
                    "from" : 1335.0,
                    "to" : 1555.0,
                    "doc_count" : 20
                  },
                  {
                    "key" : "1555.0-1775.0",
                    "from" : 1555.0,
                    "to" : 1775.0,
                    "doc_count" : 20
                  },
                  {
                    "key" : "1775.0-*",
                    "from" : 1775.0,
                    "doc_count" : 20
                  }
                ]
              },
              "bucket_correlation" : {
                "value" : 0.8402398981360937
              }
            },
            {
              "key" : "2.0",
              "doc_count" : 100,
              "latency_ranges" : {
                "buckets" : [
                  {
                    "key" : "*-0.0",
                    "to" : 0.0,
                    "doc_count" : 0
                  },
                  {
                    "key" : "0.0-105.0",
                    "from" : 0.0,
                    "to" : 105.0,
                    "doc_count" : 19
                  },
                  {
                    "key" : "105.0-225.0",
                    "from" : 105.0,
                    "to" : 225.0,
                    "doc_count" : 11
                  },
                  {
                    "key" : "225.0-445.0",
                    "from" : 225.0,
                    "to" : 445.0,
                    "doc_count" : 20
                  },
                  {
                    "key" : "445.0-665.0",
                    "from" : 445.0,
                    "to" : 665.0,
                    "doc_count" : 20
                  },
                  {
                    "key" : "665.0-885.0",
                    "from" : 665.0,
                    "to" : 885.0,
                    "doc_count" : 20
                  },
                  {
                    "key" : "885.0-1115.0",
                    "from" : 885.0,
                    "to" : 1115.0,
                    "doc_count" : 10
                  },
                  {
                    "key" : "1115.0-1335.0",
                    "from" : 1115.0,
                    "to" : 1335.0,
                    "doc_count" : 0
                  },
                  {
                    "key" : "1335.0-1555.0",
                    "from" : 1335.0,
                    "to" : 1555.0,
                    "doc_count" : 0
                  },
                  {
                    "key" : "1555.0-1775.0",
                    "from" : 1555.0,
                    "to" : 1775.0,
                    "doc_count" : 0
                  },
                  {
                    "key" : "1775.0-*",
                    "from" : 1775.0,
                    "doc_count" : 0
                  }
                ]
              },
              "bucket_correlation" : {
                "value" : -0.5759855613334943
              }
            }
          ]
        }
      }
    }

[« Bucket count K-S test correlation aggregation](search-aggregations-bucket-
count-ks-test-aggregation.md) [Bucket selector aggregation »](search-
aggregations-pipeline-bucket-selector-aggregation.md)
