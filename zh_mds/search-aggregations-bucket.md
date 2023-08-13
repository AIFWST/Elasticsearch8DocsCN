

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md)

[« Aggregations](search-aggregations.md) [Adjacency matrix aggregation
»](search-aggregations-bucket-adjacency-matrix-aggregation.md)

## 桶聚合

存储桶聚合不像指标聚合那样计算字段上的指标，而是创建文档存储桶。每个存储桶都与一个条件相关联(取决于聚合类型)，该条件确定当前上下文中的文档是否"落入"其中。换句话说，存储桶有效地定义了文档集。除了存储桶本身之外，"存储桶"聚合还计算并返回"落入"每个存储桶的文档数。

与"指标"聚合相反，存储桶聚合可以保存子聚合。这些子聚合将针对由其"父"存储桶聚合创建的存储桶进行聚合。

有不同的存储桶聚合器，每个聚合器都有不同的"存储桶"策略。有些定义单个存储桶，有些定义固定数量的多个存储桶，还有一些在聚合过程中动态创建存储桶。

"search.max_buckets"集群设置限制了单个响应中允许的存储桶数量。

[« Aggregations](search-aggregations.md) [Adjacency matrix aggregation
»](search-aggregations-bucket-adjacency-matrix-aggregation.md)
