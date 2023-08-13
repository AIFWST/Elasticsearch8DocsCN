

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Bucket sort aggregation](search-aggregations-pipeline-bucket-sort-
aggregation.md) [Cumulative cardinality aggregation »](search-aggregations-
pipeline-cumulative-cardinality-aggregation.md)

## 更改点聚合

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

检测指标中的点、峰值、下降和更改点的同级管道。给定同级多桶聚合提供的值分布，此聚合指示任何峰值或低谷的桶和/或值分布变化最大的桶(如果它们具有统计意义)。

建议使用更改点聚合来检测基于时间的数据中的更改，但是，您可以使用任何指标来创建存储桶。

###Parameters

`buckets_path`

     (Required, string) Path to the buckets that contain one set of values in which to detect a change point. There must be at least 22 bucketed values. Fewer than 1,000 is preferred. For syntax, see [`buckets_path` Syntax](search-aggregations-pipeline.html#buckets-path-syntax "buckets_path Syntax"). 

###Syntax

"change_point"聚合单独如下所示：

    
    
    {
      "change_point": {
        "buckets_path": "date_histogram>_count" __}
    }

__

|

包含要测试的值的存储桶。   ---|--- ### 响应正文编辑

`bucket`

    

(可选，对象)指示发现的更改点的存储桶的值。如果未找到更改点，则不返回。存储桶中的所有聚合也会返回。

桶的属性

`key`

     (value) The key of the bucket matched. Could be string or numeric. 
`doc_count`

     (number) The document count of the bucket. 

`type`

    

(对象)找到的更改点类型及其相关值。可能的类型：

* "下降"：在此变化点出现显著下降 * "distribution_change"：值的整体分布发生了显著变化 * "non_stationary"：没有变化点，但值不是来自平稳分布 * "峰值"：此时出现显著峰值 * "平稳"：未找到变化点 * "step_change"：变化表示值分布在统计上显着上升或下降 * "trend_change"： 此时正在发生整体趋势变化

###Example

以下示例使用 Kibana 示例数据日志数据集。

    
    
    GET kibana_sample_data_logs/_search
    {
      "aggs": {
        "date":{ __"date_histogram": {
            "field": "@timestamp",
            "fixed_interval": "1d"
          },
          "aggs": {
            "avg": { __"avg": {
                "field": "bytes"
              }
            }
          }
        },
        "change_points_avg": { __"change_point": {
            "buckets_path": "date >avg" __}
        }
      }
    }

__

|

日期直方图聚合，用于创建间隔为一天的存储桶。   ---|---    __

|

"date"聚合的同级聚合，用于计算每个存储桶中"字节"字段的平均值。   __

|

更改点检测聚合配置对象。   __

|

用于检测更改点的聚合值的路径。在这种情况下，变化点聚合的输入是"avg"的值，它是"date"的同级聚合。   该请求返回类似于以下内容的响应：

    
    
        "change_points_avg" : {
          "bucket" : {
            "key" : "2023-04-29T00:00:00.000Z", __"doc_count" : 329, __"avg" : { __"value" : 4737.209726443769
            }
          },
          "type" : { __"dip" : {
              "p_value" : 3.8999455212466465e-10, __"change_point" : 41 __}
          }
        }

__

|

作为更改点的存储桶键。   ---|---    __

|

该存储桶中的文档数。   __

|

存储桶中的聚合值。   __

|

找到的更改类型。   __

|

"p_value"表示变化的极端程度;值越低表示变化越大。   __

|

发生更改的特定存储桶(索引从"0"开始)。   « 桶排序聚合 累积基数聚合 »