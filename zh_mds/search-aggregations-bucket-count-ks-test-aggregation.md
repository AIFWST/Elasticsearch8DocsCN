

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Bucket script aggregation](search-aggregations-pipeline-bucket-script-
aggregation.md) [Bucket correlation aggregation »](search-aggregations-
bucket-correlation-aggregation.md)

## 桶计数 K-S 测试相关性聚合

一个同级管道聚合，它针对提供的发行版执行两个样本 Kolmogorov-Smirnovtest(从现在开始称为"K-S 测试")，并且文档隐含的分布计入配置的同级聚合中。具体来说，对于某些指标，假设指标的百分位间隔是事先已知的或已由聚合计算的，那么将使用同级的范围聚合来计算度量之间的分布差异的 p 值，并将该指标限制为文档的子集。非自然用例是，如果同级聚合范围聚合嵌套在术语聚合中，在这种情况下，将度量的整体分布与其对每个术语的限制进行比较。

###Parameters

`buckets_path`

     (Required, string) Path to the buckets that contain one set of values to correlate. Must be a `_count` path For syntax, see [`buckets_path` Syntax](search-aggregations-pipeline.html#buckets-path-syntax "buckets_path Syntax"). 
`alternative`

     (Optional, list) A list of string values indicating which K-S test alternative to calculate. The valid values are: "greater", "less", "two_sided". This parameter is key for determining the K-S statistic used when calculating the K-S test. Default value is all possible alternative hypotheses. 
`fractions`

     (Optional, list) A list of doubles indicating the distribution of the samples with which to compare to the `buckets_path` results. In typical usage this is the overall proportion of documents in each bucket, which is compared with the actual document proportions in each bucket from the sibling aggregation counts. The default is to assume that overall documents are uniformly distributed on these buckets, which they would be if one used equal percentiles of a metric to define the bucket end points. 
`sampling_method`

     (Optional, string) Indicates the sampling methodology when calculating the K-S test. Note, this is sampling of the returned values. This determines the cumulative distribution function (CDF) points used comparing the two samples. Default is `upper_tail`, which emphasizes the upper end of the CDF points. Valid options are: `upper_tail`, `uniform`, and `lower_tail`. 

###Syntax

"bucket_count_ks_test"聚合单独如下所示：

    
    
    {
      "bucket_count_ks_test": {
        "buckets_path": "range_values>_count", __"alternative": ["less", "greater", "two_sided"], __"sampling_method": "upper_tail" __}
    }

__

|

包含要测试的值的存储桶。   ---|---    __

|

要计算的替代方案。   __

|

K-S 统计量的抽样方法。   ###Exampleedit

以下代码片段针对统一分布对"版本"字段中的各个术语运行"bucket_count_ks_test"。均匀分布反映了"延迟"百分位数桶。未显示的是"延迟"指标值的预计算，这是利用百分位数聚合完成的。

此示例仅使用"延迟"的十分位数。

    
    
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
                  { "to": 0 },
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
            "ks_test": { __"bucket_count_ks_test": {
                "buckets_path": "latency_ranges >_count",
                "alternative": ["less", "greater", "two_sided"]
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

桶计数 K-S 测试聚合，用于测试桶计数是否来自与"分数"相同的分布;其中"分数"是均匀分布。   以下是可能的响应：

    
    
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
              "ks_test" : {
                "less" : 2.248673241788478E-4,
                "greater" : 1.0,
                "two_sided" : 5.791639181800257E-4
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
              "ks_test" : {
                "less" : 0.9642895789647244,
                "greater" : 4.58718174664754E-9,
                "two_sided" : 5.916656831139733E-9
              }
            }
          ]
        }
      }
    }

[« Bucket script aggregation](search-aggregations-pipeline-bucket-script-
aggregation.md) [Bucket correlation aggregation »](search-aggregations-
bucket-correlation-aggregation.md)
