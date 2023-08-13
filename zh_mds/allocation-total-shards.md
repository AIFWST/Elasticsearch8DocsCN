

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md) ›[Index Shard Allocation](index-modules-
allocation.md)

[« Index recovery prioritization](recovery-prioritization.md) [Index-level
data tier allocation filtering »](data-tier-shard-filtering.md)

## 每个节点的总分片数

集群级分片分配器尝试将单个索引的分片分布在尽可能多的节点上。但是，根据您拥有的分片和索引的数量以及它们的大小，可能并不总是能够均匀分布分片。

以下 _dynamic_ 设置允许您指定每个节点允许的单个索引的分片总数的硬限制：

`index.routing.allocation.total_shards_per_node`

     The maximum number of shards (replicas and primaries) that will be allocated to a single node. Defaults to unbounded. 

您还可以限制节点可以拥有的分片数量，而不管索引如何：

`cluster.routing.allocation.total_shards_per_node`

    

(动态)分配给每个节点的主分片和副本分片的最大数量。默认为"-1"(无限制)。

Elasticsearch 在分片分配期间检查此设置。例如，集群的"cluster.routing.allocation.total_shards_per_node"设置为"100"，三个节点具有以下分片分配：

* 节点 A：100 个分片 * 节点 B：98 个分片 * 节点 C：1 个分片

如果节点 C 发生故障，Elasticsearch 会将其分片重新分配给节点 B，将分片重新分配给节点 A 将超过节点 A 的分片限制。

这些设置施加了一个硬限制，这可能会导致某些分片无法分配。

请谨慎使用。

[« Index recovery prioritization](recovery-prioritization.md) [Index-level
data tier allocation filtering »](data-tier-shard-filtering.md)
