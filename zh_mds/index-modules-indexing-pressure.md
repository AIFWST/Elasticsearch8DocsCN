

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md)

[« Use index sorting to speed up conjunctions](index-modules-index-sorting-
conjunctions.md) [Mapping »](mapping.md)

## 索引压力

将文档索引到 Elasticsearch 中会以内存和 CPU 负载的形式引入系统负载。每个索引操作都包括协调阶段、主阶段和副本阶段。这些阶段可以跨集群中的多个节点执行。

索引压力可以通过外部操作(如索引请求)或内部机制(如恢复和跨集群复制)累积。如果系统中引入了过多的索引工作，则集群可能会饱和。这可能会对其他操作产生负面影响，例如搜索、群集协调和后台处理。

为了防止这些问题，Elasticsearch 在内部监控索引负载。当负载超过特定限制时，将拒绝新的索引工作

### 索引阶段

外部索引操作经历三个阶段：协调、主索引和副本。请参阅基本写入模型。

### 内存限制

"indexing_pressure.memory.limit"节点设置限制可用于未完成索引请求的字节数。此设置默认为堆的 10%。

在每个索引阶段开始时，Elasticsearch 都会考虑索引请求消耗的字节数。此会计仅在索引阶段结束时发布。这意味着上游阶段将考虑被偷听的请求，直到所有下游阶段完成。例如，在主节点和副本阶段完成之前，协调请求将一直被考虑在内。主请求将一直被考虑在内，直到每个同步副本响应以在必要时启用副本重试。

当未完成的协调、主和复制索引字节数超过配置的限制时，节点将在协调或主阶段开始拒绝新的索引工作。

当未完成的副本索引字节数超过配置限制的 1.5 倍时，节点将在副本阶段开始拒绝新的索引工作。这种设计意味着，随着索引压力在节点上增加，它们自然会停止接受协调和主要工作，转而支持出色的复制工作。

"indexing_pressure.memory.limit"设置的 10% 默认限制是慷慨的。只有在仔细考虑后，您才应该更改它。只有索引请求才会达到此限制。这意味着存在额外的索引开销(缓冲区、侦听器等)，它们也需要堆空间。Elasticsearch 的其他组件也需要内存。将此限制设置得太高可能会拒绝其他操作和组件的操作内存。

###Monitoring

您可以使用节点统计信息 API 检索索引压力指标。

### 分度压力设置

"indexing_pressure.内存.限制" ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     Number of outstanding bytes that may be consumed by indexing requests. When this limit is reached or exceeded, the node will reject new coordinating and primary operations. When replica operations consume 1.5x this limit, the node will reject new replica operations. Defaults to 10% of the heap. 

[« Use index sorting to speed up conjunctions](index-modules-index-sorting-
conjunctions.md) [Mapping »](mapping.md)
