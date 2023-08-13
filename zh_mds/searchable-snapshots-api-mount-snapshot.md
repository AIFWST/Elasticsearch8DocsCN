

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Searchable snapshots APIs](searchable-snapshots-
apis.md)

[« Searchable snapshots APIs](searchable-snapshots-apis.md) [Cache stats API
»](searchable-snapshots-api-cache-stats.md)

## 挂载快照接口

将快照挂载为可搜索的快照索引。

###Request

"发布/_snapshot/<repository>/<snapshot>/_mount"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须对任何包含的索引具有"管理"集群权限和"管理"索引权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

### 路径参数

`<repository>`

     (Required, string) The name of the repository containing the snapshot of the index to mount. 
`<snapshot>`

     (Required, string) The name of the snapshot of the index to mount. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`wait_for_completion`

     (Optional, Boolean) If `true`, the request blocks until the operation is complete. Defaults to `false`. 
`storage`

    

(可选，字符串)可搜索快照索引的挂载选项。可能的值为：

"full_copy"(默认)

     [Fully mounted index](searchable-snapshots.html#fully-mounted). 
`shared_cache`

     [Partially mounted index](searchable-snapshots.html#partially-mounted). 

### 请求正文

`index`

     (Required, string) Name of the index contained in the snapshot whose data is to be mounted. 

如果未指定"renamed_index"，则此名称也将用于创建新索引。

`renamed_index`

    

(可选，字符串)将创建的索引的名称。

`index_settings`

    

(可选，对象)装入索引时应添加到索引的设置。

`ignore_index_settings`

    

(可选，字符串数组)装入索引时应从索引中删除的设置的名称。

###Examples

将存储在"my_repository"中的名为"my_snapshot"的现有快照中的索引"my_docs"挂载为新索引"docs"：

    
    
    POST /_snapshot/my_repository/my_snapshot/_mount?wait_for_completion=true
    {
      "index": "my_docs", __"renamed_index": "docs", __"index_settings": { __"index.number_of_replicas": 0
      },
      "ignore_index_settings": [ "index.refresh_interval" ] __}

__

|

快照中要挂载的索引的名称 ---|--- __

|

要创建 __ 的索引的名称

|

要添加到新索引的任何索引设置 __

|

挂载快照索引时要忽略的索引设置列表 « 可搜索快照 API 缓存统计信息 API»