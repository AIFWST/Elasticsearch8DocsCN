

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat segments API](cat-segments.md) [cat snapshots API »](cat-
snapshots.md)

## 猫分片接口

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。

"分片"命令是哪些节点包含哪些分片的详细视图。它会告诉您它是主数据库还是副本数据库、文档数、磁盘上的字节数以及它所在的节点。

对于数据流，API 返回有关流的支持索引的信息。

###Request

'获取/_cat/分片/<target>'

"获取/_cat/分片"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。您还必须对检索到的任何数据流、索引或别名具有"监视"或"管理"索引权限。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`bytes`

     (Optional, [byte size units](api-conventions.html#byte-units "Byte size units")) Unit used to display byte values. 
`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将按下面列出的顺序返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

"索引"、"i"、"IDX"

     (Default) Name of the index. 
`shard`, `s`, `sh`

     (Default) Name of the shard. 
`prirep`, `p`, `pr`, `primaryOrReplica`

     (Default) Shard type. Returned values are `primary` or `replica`. 
`state`, `st`

    

(默认)分片的状态。返回的值为：

* "正在初始化"：分片正在从对等分片或网关恢复。  * "正在重新定位"：分片正在重新定位。  * "已启动"：分片已启动。  * "未分配"：分片未分配给任何节点。

"文档"、"D"、"DC"

     (Default) Number of documents in shard, such as `25`. 
`store`, `sto`

     (Default) Disk space used by the shard, such as `5kb`. 
`ip`

     (Default) IP address of the node, such as `127.0.1.1`. 
`id`

     (Default) ID of the node, such as `k0zy`. 
`node`, `n`

     (Default) Node name, such as `I8hydUG`. 
`completion.size`, `cs`, `completionSize`

     Size of completion, such as `0b`. 
`fielddata.memory_size`, `fm`, `fielddataMemory`

     Used fielddata cache memory, such as `0b`. 
`fielddata.evictions`, `fe`, `fielddataEvictions`

     Fielddata cache evictions, such as `0`. 
`flush.total`, `ft`, `flushTotal`

     Number of flushes, such as `1`. 
`flush.total_time`, `ftt`, `flushTotalTime`

     Time spent in flush, such as `1`. 
`get.current`, `gc`, `getCurrent`

     Number of current get operations, such as `0`. 
`get.time`, `gti`, `getTime`

     Time spent in get, such as `14ms`. 
`get.total`, `gto`, `getTotal`

     Number of get operations, such as `2`. 
`get.exists_time`, `geti`, `getExistsTime`

     Time spent in successful gets, such as `14ms`. 
`get.exists_total`, `geto`, `getExistsTotal`

     Number of successful get operations, such as `2`. 
`get.missing_time`, `gmti`, `getMissingTime`

     Time spent in failed gets, such as `0s`. 
`get.missing_total`, `gmto`, `getMissingTotal`

     Number of failed get operations, such as `1`. 
`indexing.delete_current`, `idc`, `indexingDeleteCurrent`

     Number of current deletion operations, such as `0`. 
`indexing.delete_time`, `idti`, `indexingDeleteTime`

     Time spent in deletions, such as `2ms`. 
`indexing.delete_total`, `idto`, `indexingDeleteTotal`

     Number of deletion operations, such as `2`. 
`indexing.index_current`, `iic`, `indexingIndexCurrent`

     Number of current indexing operations, such as `0`. 
`indexing.index_time`, `iiti`, `indexingIndexTime`

     Time spent in indexing, such as `134ms`. 
`indexing.index_total`, `iito`, `indexingIndexTotal`

     Number of indexing operations, such as `1`. 
`indexing.index_failed`, `iif`, `indexingIndexFailed`

     Number of failed indexing operations, such as `0`. 
`merges.current`, `mc`, `mergesCurrent`

     Number of current merge operations, such as `0`. 
`merges.current_docs`, `mcd`, `mergesCurrentDocs`

     Number of current merging documents, such as `0`. 
`merges.current_size`, `mcs`, `mergesCurrentSize`

     Size of current merges, such as `0b`. 
`merges.total`, `mt`, `mergesTotal`

     Number of completed merge operations, such as `0`. 
`merges.total_docs`, `mtd`, `mergesTotalDocs`

     Number of merged documents, such as `0`. 
`merges.total_size`, `mts`, `mergesTotalSize`

     Size of current merges, such as `0b`. 
`merges.total_time`, `mtt`, `mergesTotalTime`

     Time spent merging documents, such as `0s`. 
`query_cache.memory_size`, `qcm`, `queryCacheMemory`

     Used query cache memory, such as `0b`. 
`query_cache.evictions`, `qce`, `queryCacheEvictions`

     Query cache evictions, such as `0`. 
`recoverysource.type`, `rs`

     Type of recovery source. 
`refresh.total`, `rto`, `refreshTotal`

     Number of refreshes, such as `16`. 
`refresh.time`, `rti`, `refreshTime`

     Time spent in refreshes, such as `91ms`. 
`search.fetch_current`, `sfc`, `searchFetchCurrent`

     Current fetch phase operations, such as `0`. 
`search.fetch_time`, `sfti`, `searchFetchTime`

     Time spent in fetch phase, such as `37ms`. 
`search.fetch_total`, `sfto`, `searchFetchTotal`

     Number of fetch operations, such as `7`. 
`search.open_contexts`, `so`, `searchOpenContexts`

     Open search contexts, such as `0`. 
`search.query_current`, `sqc`, `searchQueryCurrent`

     Current query phase operations, such as `0`. 
`search.query_time`, `sqti`, `searchQueryTime`

     Time spent in query phase, such as `43ms`. 
`search.query_total`, `sqto`, `searchQueryTotal`

     Number of query operations, such as `9`. 
`search.scroll_current`, `scc`, `searchScrollCurrent`

     Open scroll contexts, such as `2`. 
`search.scroll_time`, `scti`, `searchScrollTime`

     Time scroll contexts held open, such as `2m`. 
`search.scroll_total`, `scto`, `searchScrollTotal`

     Completed scroll contexts, such as `1`. 
`segments.count`, `sc`, `segmentsCount`

     Number of segments, such as `4`. 
`segments.memory`, `sm`, `segmentsMemory`

     Memory used by segments, such as `1.4kb`. 
`segments.index_writer_memory`, `siwm`, `segmentsIndexWriterMemory`

     Memory used by index writer, such as `18mb`. 
`segments.version_map_memory`, `svmm`, `segmentsVersionMapMemory`

     Memory used by version map, such as `1.0kb`. 
`segments.fixed_bitset_memory`, `sfbm`, `fixedBitsetMemory`

     Memory used by fixed bit sets for nested object field types and type filters for types referred in [`join`](parent-join.html "Join field type") fields, such as `1.0kb`. 
`seq_no.global_checkpoint`, `sqg`, `globalCheckpoint`

     Global checkpoint. 
`seq_no.local_checkpoint`, `sql`, `localCheckpoint`

     Local checkpoint. 
`seq_no.max`, `sqm`, `maxSeqNo`

     Maximum sequence number. 
`suggest.current`, `suc`, `suggestCurrent`

     Number of current suggest operations, such as `0`. 
`suggest.time`, `suti`, `suggestTime`

     Time spent in suggest, such as `0`. 
`suggest.total`, `suto`, `suggestTotal`

     Number of suggest operations, such as `0`. 
`sync_id`

     Sync ID of the shard. 
`unassigned.at`, `ua`

     Time at which the shard became unassigned in [Coordinated Universal Time (UTC)](https://en.wikipedia.org/wiki/List_of_UTC_time_offsets). 
`unassigned.details`, `ud`

     Details about why the shard became unassigned. This does not explain why the shard is currently unassigned. To understand why a shard is not assigned, use the [Cluster allocation explain](cluster-allocation-explain.html "Cluster allocation explain API") API. 
`unassigned.for`, `uf`

     Time at which the shard was requested to be unassigned in [Coordinated Universal Time (UTC)](https://en.wikipedia.org/wiki/List_of_UTC_time_offsets). 

"未分配的原因"，"您的"

    

指示上次更改此未分配分片的状态的原因。这并不能解释为什么分片当前未分配。要了解为什么未分配分片，请使用集群分配解释 API。返回的值包括：

* "ALLOCATION_FAILED"：由于分片分配失败而未分配。  * "CLUSTER_RECOVERED"：由于完整集群恢复而未分配。  * "DANGLING_INDEX_IMPORTED"：由于导入悬空索引而未分配。  * "EXISTING_INDEX_RESTORED"：由于恢复到封闭索引而未分配。  * "FORCED_EMPTY_PRIMARY"：分片的分配上次修改方法是使用集群重新路由 API 强制使用空主数据库。  * "INDEX_CLOSED"：未分配，因为索引已关闭。  * "INDEX_CREATED"：由于 API 创建索引而未分配。  * "INDEX_REOPENED"：由于打开已关闭的索引而未分配。  * "MANUAL_ALLOCATION"：分片的分配上次由集群重新路由 API 修改。  * "NEW_INDEX_RESTORED"：由于还原到新索引而未分配。  * "NODE_LEFT"：由于托管它的节点离开集群而未分配。  * "NODE_RESTARTING"：与"NODE_LEFT"类似，不同之处在于节点已注册为使用节点关闭 API 重新启动。  * "PRIMARY_FAILED"：分片正在初始化为副本，但主分片在初始化完成之前失败。  * "REALLOCATED_REPLICA"：确定更好的副本位置，并导致取消现有副本分配。  * "重新初始化"：当分片从启动返回到初始化时。  * "REPLICA_ADDED"：由于显式添加副本而未分配。  * "REROUTE_CANCELLED"：由于显式取消重新路由命令而未分配。

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

#### 具有单个数据流或索引的示例

    
    
    response = client.cat.shards
    puts response
    
    
    GET _cat/shards

API 返回以下响应：

    
    
    my-index-000001 0 p STARTED 3014 31.1mb 192.168.56.10 H5dfFeA

#### 通配符模式示例

如果您的集群有许多分片，您可以在 '' path 参数中使用通配符模式<target>来限制 API 请求。

以下请求返回以"my-index-"开头的任何数据流或索引的信息。

    
    
    response = client.cat.shards(
      index: 'my-index-*'
    )
    puts response
    
    
    GET _cat/shards/my-index-*

API 返回以下响应：

    
    
    my-index-000001 0 p STARTED 3014 31.1mb 192.168.56.10 H5dfFeA

#### 具有重新定位分片的示例

    
    
    response = client.cat.shards
    puts response
    
    
    GET _cat/shards

API 返回以下响应：

    
    
    my-index-000001 0 p RELOCATING 3014 31.1mb 192.168.56.10 H5dfFeA -> -> 192.168.56.30 bGG90GE

"状态"列中的"重新定位"值表示索引分片正在重新定位。

#### 分片状态示例

在分片可供使用之前，它会经历"正在初始化"状态。您可以使用 cat 分片 API 查看哪些分片正在初始化。

    
    
    response = client.cat.shards
    puts response
    
    
    GET _cat/shards

API 返回以下响应：

    
    
    my-index-000001 0 p STARTED      3014 31.1mb 192.168.56.10 H5dfFeA
    my-index-000001 0 r INITIALIZING    0 14.3mb 192.168.56.30 bGG90GE

#### 未分配分片原因的示例

以下请求返回"unassigned.reason"列，该列指示分片未分配的原因。

    
    
    response = client.cat.shards(
      h: 'index,shard,prirep,state,unassigned.reason'
    )
    puts response
    
    
    GET _cat/shards?h=index,shard,prirep,state,unassigned.reason

API 返回以下响应：

    
    
    my-index-000001 0 p STARTED    3014 31.1mb 192.168.56.10 H5dfFeA
    my-index-000001 0 r STARTED    3014 31.1mb 192.168.56.30 bGG90GE
    my-index-000001 0 r STARTED    3014 31.1mb 192.168.56.20 I8hydUG
    my-index-000001 0 r UNASSIGNED ALLOCATION_FAILED

[« cat segments API](cat-segments.md) [cat snapshots API »](cat-
snapshots.md)
