

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Scalability and resilience: clusters, nodes, and shards](scalability.md)
[Set up Elasticsearch »](setup.md)

# 8.9 中的新功能

在 8.9 中推出。

以下是 Elasticsearch 8.9 中新增和改进的亮点！有关此版本的详细信息，请参阅发行说明和迁移指南。

其他版本：

8.8 |8.7 |8.6 |8.5 |8.4 |8.3 |8.2 |8.1 |8.0

### 在并发索引和搜索下更好的索引和搜索性能

当匹配短语查询或术语查询等查询以 constantkeyword 字段为目标时，我们可以跳过对分片的查询执行，其中查询被重写为不匹配任何文档。我们利用包含常量关键字字段的索引映射，并以这样的方式重写查询，如果 constantkeyword 字段与索引映射中定义的值不匹配，则编写查询以匹配任何文档。这将导致分片级别请求在数据节点上执行查询之前立即返回，从而完全跳过分片。在这里，我们利用尽可能跳过分片的功能来避免不必要的分片刷新并改善查询延迟(通过不执行任何与搜索相关的 I/O)。避免此类不必要的分片刷新可改善查询延迟，因为搜索线程不再需要等待不必要的分片刷新。与查询条件不匹配的分片将保持搜索空闲状态，索引吞吐量不会受到刷新的负面影响。在引入此更改之前，命中多个分片的查询，包括那些没有与搜索条件匹配的文档的查询(考虑使用具有许多支持索引的索引模式或数据流)，可能会导致"分片刷新风暴"增加查询延迟，因为搜索线程在能够启动和执行搜索操作之前等待所有分片刷新完成。引入此更改后，搜索线程只需等待在包括相关数据在内的分片上完成刷新即可。请注意，分片预过滤器的执行和发生重写的相应"canmatch"阶段取决于所涉及的分片总数以及其中是否至少有一个返回非空结果(请参阅_pre_filter_shard_size_设置以了解如何控制此行为)。Elasticsearch 在所谓的"可以匹配"阶段对数据节点执行重写操作，利用了这样一个事实，即此时我们可以访问索引映射并提取有关常量关键字字段及其值的信息。这意味着我们仍然将搜索查询从协调器节点"扇出"到所涉及的数据节点。无法在协调器节点上基于索引映射重写查询，因为协调器节点缺少索引映射信息。

[#96161](https://github.com/elastic/elasticsearch/pull/96161)

### 向搜索终结点添加多个用于排名的查询

搜索终结点添加一个名为"sub_searches"的新顶级元素。这个顶级元素是用于排名的搜索列表，其中每个"子搜索"都是独立执行的。使用"sub_searches"元素代替"查询"，以允许使用排名进行搜索以执行多个查询。"sub_searches"和"查询"元素不能一起使用。

[#96224](https://github.com/elastic/elasticsearch/pull/96224)

### 为 kNN 搜索进行文本嵌入GA

从 8.9 开始，kNN 搜索的"text_embedding"query_vector_builder"扩展已正式发布。通过将文本转换为密集向量来执行语义搜索需要此功能。

[#96735](https://github.com/elastic/elasticsearch/pull/96735)

### 资产跟踪 - 时间序列聚合中的geo_line

"geo_line"聚合从"geo_points"构建轨道。它以前需要使用内存中的大型数组将点收集到多个存储桶中并对这些存储桶进行排序。

随着 TSDB 功能的进步，特别是"time_series"聚合，现在可以依赖按 TSID 和时间戳顺序聚合的数据，从而可以删除所有排序，以及仅使用单个存储桶的内存，从而显着改善内存占用。此外，我们可以使用 <https://github.com/elastic/elasticsearch/pull/94859> 中引入的流线简化器算法，用更可取的简化这些轨道的方法替换以前截断非常大的轨道的行为。

!科迪亚克岛北部缩短为100点

在此图中，灰线是原始几何图形，蓝线是原始"geo_line"聚合生成的截断几何图形，洋红色线是新的简化几何图形。

[#94954](https://github.com/elastic/elasticsearch/pull/94954)

[« Scalability and resilience: clusters, nodes, and shards](scalability.md)
[Set up Elasticsearch »](setup.md)
