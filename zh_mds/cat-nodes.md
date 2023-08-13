

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat nodeattrs API](cat-nodeattrs.md) [cat pending tasks API »](cat-
pending-tasks.md)

## 猫节点接口

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用节点信息 API。

返回有关群集节点的信息。

###Request

"获取/_cat/节点"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

### 查询参数

`bytes`

     (Optional, [byte size units](api-conventions.html#byte-units "Byte size units")) Unit used to display byte values. 
`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`full_id`

     (Optional, Boolean) If `true`, return the full node ID. If `false`, return the shortened node ID. Defaults to `false`. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将按下面列出的顺序返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

"知识产权"、"我"

     (Default) IP address, such as `127.0.1.1`. 
`heap.percent`, `hp`, `heapPercent`

     (Default) Maximum configured heap, such as `7`. 
`heap.max`, `hm`, `heapMax`

     (Default) Total heap, such as `4gb`. 
`ram.percent`, `rp`, `ramPercent`

     (Default) Used total memory percentage, such as `47`. 
`file_desc.percent`, `fdp`, `fileDescriptorPercent`

     (Default) Used file descriptors percentage, such as `1`. 
`node.role`, `r`, `role`, `nodeRole`

    

(默认)节点的角色。返回的值包括"c"(冷节点)、"d"(数据节点)、"f"(冻结节点)、"h"(热节点)、"i"(采集节点)、"l"(机器学习节点)、"m"(符合主节点条件的节点)、"r"(远程群集客户端节点)、"s"(内容节点)、"t"(转换节点)、"v"(仅投票节点)、"w"(暖节点)和"-"(仅限协调节点)。

例如，"dim"表示符合主节点条件的数据和采集节点。参见节点。

"主"、"米"

     (Default) Indicates whether the node is the elected master node. Returned values include `*` (elected master) and `-` (not elected master). 
`name`, `n`

     (Default) Node name, such as `I8hydUG`. 
`id`, `nodeId`

     ID of the node, such as `k0zy`. 
`pid`, `p`

     Process ID, such as `13061`. 
`port`, `po`

     Bound transport port, such as `9300`. 
`http_address`, `http`

     Bound http address, such as `127.0.0.1:9200`. 
`version`, `v`

     Elasticsearch version, such as 8.9.0. 
`build`, `b`

     Elasticsearch build hash, such as `5c03844`. 
`jdk`, `j`

     Java version, such as `1.8.0`. 
`disk.total`, `dt`, `diskTotal`

     Total disk space, such as `458.3gb`. 
`disk.used`, `du`, `diskUsed`

     Used disk space, such as `259.8gb`. 
`disk.avail`, `d`, `disk`, `diskAvail`

     Available disk space, such as `198.4gb`. 
`disk.used_percent`, `dup`, `diskUsedPercent`

     Used disk space percentage, such as `47`. 
`heap.current`, `hc`, `heapCurrent`

     Used heap, such as `311.2mb`. 
`ram.current`,`rc`, `ramCurrent`

     Used total memory, such as `513.4mb`. 
`ram.max`, `rm`, `ramMax`

     Total memory, such as `2.9gb`. 
`file_desc.current`, `fdc`, `fileDescriptorCurrent`

     Used file descriptors, such as `123`. 
`file_desc.max`, `fdm`, `fileDescriptorMax`

     Maximum number of file descriptors, such as `1024`. 
`cpu`

     Recent system CPU usage as percent, such as `12`. 
`load_1m`, `l`

     Most recent load average, such as `0.22`. 
`load_5m`, `l`

     Load average for the last five minutes, such as `0.78`. 
`load_15m`, `l`

     Load average for the last fifteen minutes, such as `1.24`. 
`uptime`, `u`

     Node uptime, such as `17.3m`. 
`completion.size`, `cs`, `completionSize`

     Size of completion, such as `0b`. 
`fielddata.memory_size`, `fm`, `fielddataMemory`

     Used fielddata cache memory, such as `0b`. 
`fielddata.evictions`, `fe`, `fielddataEvictions`

     Fielddata cache evictions, such as `0`. 
`query_cache.memory_size`, `qcm`, `queryCacheMemory`

     Used query cache memory, such as `0b`. 
`query_cache.evictions`, `qce`, `queryCacheEvictions`

     Query cache evictions, such as `0`. 
`query_cache.hit_count`, `qchc`, `queryCacheHitCount`

     Query cache hit count, such as `0`. 
`query_cache.miss_count`, `qcmc`, `queryCacheMissCount`

     Query cache miss count, such as `0`. 
`request_cache.memory_size`, `rcm`, `requestCacheMemory`

     Used request cache memory, such as `0b`. 
`request_cache.evictions`, `rce`, `requestCacheEvictions`

     Request cache evictions, such as `0`. 
`request_cache.hit_count`, `rchc`, `requestCacheHitCount`

     Request cache hit count, such as `0`. 
`request_cache.miss_count`, `rcmc`, `requestCacheMissCount`

     Request cache miss count, such as `0`. 
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
`refresh.total`, `rto`, `refreshTotal`

     Number of refreshes, such as `16`. 
`refresh.time`, `rti`, `refreshTime`

     Time spent in refreshes, such as `91ms`. 
`script.compilations`, `scrcc`, `scriptCompilations`

     Total script compilations, such as `17`. 
`script.cache_evictions`, `scrce`, `scriptCacheEvictions`

     Total compiled scripts evicted from cache, such as `6`. 
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
`suggest.current`, `suc`, `suggestCurrent`

     Number of current suggest operations, such as `0`. 
`suggest.time`, `suti`, `suggestTime`

     Time spent in suggest, such as `0`. 
`suggest.total`, `suto`, `suggestTotal`

     Number of suggest operations, such as `0`. 
`shard_stats.total_count`, `sstc`, `shardStatsTotalCount`

     Number of shards assigned. 
`mappings.total_count`, `mtc`, `mappingsTotalCount`

     Number of mappings, including [runtime](runtime.html "Runtime fields") and [object](object.html "Object field type") fields. 
`mappings.total_estimated_overhead_in_bytes`, `mteo`,
`mappingsTotalEstimatedOverheadInBytes`

     Estimated heap overhead, in bytes, of mappings on this node, which allows for 1KiB of heap for every mapped field. 

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
`include_unloaded_segments`

     (Optional, Boolean) If `true`, the response includes information from segments that are **not** loaded into memory. Defaults to `false`. 

###Examples

#### 默认列的示例

    
    
    response = client.cat.nodes(
      v: true
    )
    puts response
    
    
    GET /_cat/nodes?v=true

API 返回以下响应：

    
    
    ip        heap.percent ram.percent cpu load_1m load_5m load_15m node.role master name
    127.0.0.1           65          99  42    3.07                  dim       *      mJw06l1

"ip"、"heap.percent"、"ram.percent"、"cpu"和"load_*"列提供每个节点的 IP 地址和性能信息。

"node.role"、"master"和"name"列提供了对监控整个集群(尤其是大型集群)有用的信息。

#### 显式列的示例

以下 API 请求返回"id"、"ip"、"端口"、"v"(版本)和"m"(主)列。

    
    
    response = client.cat.nodes(
      v: true,
      h: 'id,ip,port,v,m'
    )
    puts response
    
    
    GET /_cat/nodes?v=true&h=id,ip,port,v,m

API 返回以下响应：

    
    
    id   ip        port  v         m
    veJR 127.0.0.1 59938 8.9.0 *

[« cat nodeattrs API](cat-nodeattrs.md) [cat pending tasks API »](cat-
pending-tasks.md)
