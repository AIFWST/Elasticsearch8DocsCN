

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Fleet APIs](fleet-apis.md)

[« Get global checkpoints API](get-global-checkpoints.md) [Fleet multi
search API »](fleet-multi-search.md)

## 车队搜索API

队列搜索 API 的目的是提供一个搜索 API，其中搜索只有在提供的检查点被处理后才会执行，并且对于 Elasticsearch 内部的搜索是可见的。

队列搜索 API 旨在通过队列服务器间接使用。不支持直接使用。Elastic 保留在未来版本中更改或删除此功能的权利，恕不另行通知。

## 等待检查点功能

队列搜索 API 支持可选参数"wait_for_checkpoints"。此参数是序列号检查点的列表。当此参数存在时，只有在搜索对提供的序列号检查点(包括提供的序列号检查点)的所有操作可见后，才会在本地分片上执行搜索。索引操作在刷新后变得可见。检查点按分片编制索引。

如果在将检查点刷新到 Elasticsearch 之前发生超时，则搜索请求将超时。

队列搜索 API 仅支持针对单个目标的搜索。如果提供索引别名作为搜索目标，则必须将其解析为单个具体索引。

## 允许部分结果

默认情况下，Elasticsearch 搜索 API 将允许部分搜索结果。使用此队列 API，通常将其配置为"false"或检查响应以确保每个分片搜索成功。如果不采取这些预防措施，即使一个或多个分片超时，也有可能成功返回搜索结果。

###Request

"获取/<target>/_fleet/_fleet_search"

### 路径参数

`<target>`

     (Required, string) A single target to search. If the target is an index alias, it must resolve to a single index. 

### 查询参数

`wait_for_checkpoints`

     (Optional, list) A comma separated list of checkpoints. When configured, the search API will only be executed on a shard after the relevant checkpoint has become visible for search. Defaults to an empty list which will cause Elasticsearch to immediately execute the search. 
`allow_partial_search_results`

     (Optional, Boolean) If `true`, returns partial results if there are shard request timeouts or [shard failures](docs-replication.html#shard-failures "Shard failures"). If `false`, returns an error with no partial results. Defaults to the configured cluster setting `search.default_allow_partial_results` which is `true` by default. 

[« Get global checkpoints API](get-global-checkpoints.md) [Fleet multi
search API »](fleet-multi-search.md)
