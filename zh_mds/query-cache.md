

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Networking](modules-network.md) [Search settings »](search-settings.md)

## 节点查询缓存设置

筛选器上下文中使用的查询结果缓存在节点查询缓存中，以便快速查找。每个节点都有一个由所有分片共享的查询缓存。缓存使用 LRU 逐出策略：当缓存已满时，将逐出最近最少使用的查询结果，以便为新数据让路。不能检查查询缓存的内容。

术语查询和在筛选器上下文之外使用的查询不符合强制缓存条件。

默认情况下，缓存最多可容纳 10000 个查询，最多占总堆空间的 10%。为了确定查询是否符合缓存条件，Elasticsearch 会维护查询历史记录以跟踪发生次数。

如果段包含至少 10000 个文档，并且该段至少具有分片总文档的 3%，则缓存将按段执行。由于缓存是按段进行的，因此合并段可能会使缓存查询失效。

以下设置是 _static_，必须在群集中的每个数据节点上配置：

`indices.queries.cache.size`

     ([Static](settings.html#static-cluster-setting)) Controls the memory size for the filter cache. Accepts either a percentage value, like `5%`, or an exact value, like `512mb`. Defaults to `10%`. 

### 查询缓存索引设置

以下设置是可以基于每个索引配置的 _index_ 设置。只能在创建索引时或在闭合索引上设置：

`index.queries.cache.enabled`

     ([Static](index-modules.html#index-modules-settings "Index Settings")) Controls whether to enable query caching. Accepts `true` (default) or `false`. 

[« Networking](modules-network.md) [Search settings »](search-settings.md)
