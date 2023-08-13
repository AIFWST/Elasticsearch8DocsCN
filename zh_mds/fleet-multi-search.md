

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Fleet APIs](fleet-apis.md)

[« Fleet search API](fleet-search.md) [Find structure API »](find-
structure.md)

## 舰队多搜索API

使用单个 API 请求执行多个队列搜索。

该 API 遵循与多搜索 API 相同的结构。但是，与队列搜索API类似，它支持"wait_for_checkpoints"参数。

队列多搜索 API 旨在通过队列服务器间接使用。不支持直接使用。Elastic 保留在未来版本中更改或删除此功能的权利，恕不另行通知。

###Request

"获取/_fleet/_fleet_msearch"

"获取/<index>/_fleet/_fleet_msearch"

### 路径参数

`<target>`

     (Optional, string) A single target to search. If the target is an index alias, it must resolve to a single index. 

### 查询参数

`wait_for_checkpoints`

     (Optional, list) A comma separated list of checkpoints. When configured, the search API will only be executed on a shard after the relevant checkpoint has become visible for search. Defaults to an empty list which will cause Elasticsearch to immediately execute the search. 
`allow_partial_search_results`

     (Optional, Boolean) If `true`, returns partial results if there are shard request timeouts or [shard failures](docs-replication.html#shard-failures "Shard failures"). If `false`, returns an error with no partial results. Defaults to the configured cluster setting `search.default_allow_partial_results` which is `true` by default. 

[« Fleet search API](fleet-search.md) [Find structure API »](find-
structure.md)
