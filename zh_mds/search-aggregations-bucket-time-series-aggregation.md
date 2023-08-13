

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Terms aggregation](search-aggregations-bucket-terms-aggregation.md)
[Variable width histogram aggregation »](search-aggregations-bucket-
variablewidthhistogram-aggregation.md)

## 时间序列聚合

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

时序聚合查询使用时序索引创建的数据。这通常是指标或其他具有时间组件的数据流等数据，需要使用时间序列模式创建索引。

数据可以像其他索引一样添加到时间序列索引中：

    
    
    PUT /my-time-series-index-0/_bulk
    { "index": {} }
    { "key": "a", "val": 1, "@timestamp": "2022-01-01T00:00:10Z" }
    { "index": {}}
    { "key": "a", "val": 2, "@timestamp": "2022-01-02T00:00:00Z" }
    { "index": {} }
    { "key": "b", "val": 2, "@timestamp": "2022-01-01T00:00:10Z" }
    { "index": {}}
    { "key": "b", "val": 3, "@timestamp": "2022-01-02T00:00:00Z" }

这将返回时序中的所有结果，但是更典型的查询将使用子聚合将返回的日期减少到更相关的日期。

###Size

默认情况下，"时间序列"聚合返回 10000 个结果。"size"参数可用于进一步限制结果。或者，使用子聚合可以限制作为时序聚合返回的值的数量。

###Keyed

"keyed"参数确定存储桶是否以映射的形式返回，每个存储桶具有唯一键。默认情况下，将"keyed"设置为 false 时，存储桶将作为数组返回。

[« Terms aggregation](search-aggregations-bucket-terms-aggregation.md)
[Variable width histogram aggregation »](search-aggregations-bucket-
variablewidthhistogram-aggregation.md)
