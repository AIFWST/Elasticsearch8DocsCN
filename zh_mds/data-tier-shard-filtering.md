

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md) ›[Index Shard Allocation](index-modules-
allocation.md)

[« Total shards per node](allocation-total-shards.md) [Index blocks
»](index-modules-blocks.md)

## 索引级数据层分配筛选

可以使用索引级别的"_tier_preference"设置来控制将索引分配到哪个数据层。

此设置对应于数据节点角色：

* data_content * data_hot * data_warm * data_cold * data_frozen

数据角色不是有效的数据层，不能与"_tier_preference"设置一起使用。冻结的层以独占方式存储部分挂载的索引。

#### 数据层分配设置

`index.routing.allocation.include._tier_preference`

     Assign the index to the first tier in the list that has an available node. This prevents indices from remaining unallocated if no nodes are available in the preferred tier. For example, if you set `index.routing.allocation.include._tier_preference` to `data_warm,data_hot`, the index is allocated to the warm tier if there are nodes with the `data_warm` role. If there are no nodes in the warm tier, but there are nodes with the `data_hot` role, the index is allocated to the hot tier. Used in conjunction with [data tiers](data-tiers.html#data-tier-allocation "Data tier index allocation"). 

[« Total shards per node](allocation-total-shards.md) [Index blocks
»](index-modules-blocks.md)
