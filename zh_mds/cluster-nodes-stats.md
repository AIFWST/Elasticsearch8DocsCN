

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Nodes reload secure settings API](cluster-nodes-reload-secure-
settings.md) [Cluster Info API »](cluster-info.md)

## 节点统计接口

返回群集节点统计信息。

###Request

"获取/_nodes/统计"

'获取/_nodes/<node_id>/统计"

'获取/_nodes/统计/<metric>'

'获取/_nodes/<node_id>/统计/<metric>'

'获取/_nodes/统计/<metric>/<index_metric>"

'获取 /_nodes/<node_id>/stats/<metric>/<index_metric>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

您可以使用群集节点统计信息 API 检索群集中节点的统计信息。

此处介绍了所有节点选择性选项。

默认情况下，将返回所有统计信息。您可以使用指标限制返回的信息。

### 路径参数

`<metric>`

    

(可选，字符串)将返回的信息限制为特定指标。以下选项的逗号分隔列表：

`adaptive_selection`

     Statistics about [adaptive replica selection](search-shard-routing.html#search-adaptive-replica "Adaptive replica selection"). 
`breaker`

     Statistics about the field data circuit breaker. 
`discovery`

     Statistics about the discovery. 
`fs`

     File system information, data path, free disk space, read/write stats. 
`http`

     HTTP connection information. 
`indexing_pressure`

     Statistics about the node's indexing load and related rejections. 
`indices`

     Indices stats about size, document count, indexing and deletion times, search times, field cache size, merges and flushes. 
`ingest`

     Statistics about ingest preprocessing. 
`jvm`

     JVM stats, memory pool information, garbage collection, buffer pools, number of loaded/unloaded classes. 
`os`

     Operating system stats, load average, mem, swap. 
`process`

     Process statistics, memory consumption, cpu usage, open file descriptors. 
`repositories`

     Statistics about snapshot repositories. 
`thread_pool`

     Statistics about each thread pool, including current size, queue and rejected tasks. 
`transport`

     Transport statistics about sent and received bytes in cluster communication. 

`<index_metric>`

    

(可选，字符串)将返回的"索引"指标信息限制为特定的索引指标。仅当指定了"索引"(或"全部")指标时，才能使用它。支持的指标包括：

* "批量" * "完成" * "文档" * "字段数据" * "刷新" * "获取" * "索引" * "映射" * "合并" * "query_cache" * "恢复" * "刷新" * "request_cache" * "搜索" * "细分" * "shard_stats" * "存储" * "转写" * "更暖"

`<node_id>`

     (Optional, string) Comma-separated list of node IDs or names used to limit returned information. 

### 查询参数

`completion_fields`

     (Optional, string) Comma-separated list or wildcard expressions of fields to include in `fielddata` and `suggest` statistics. 
`fielddata_fields`

     (Optional, string) Comma-separated list or wildcard expressions of fields to include in `fielddata` statistics. 
`fields`

    

(可选，字符串)要包含在统计信息中的字段的逗号分隔列表或通配符表达式。

用作默认列表，除非在"completion_fields"或"fielddata_fields"参数中提供了特定的字段列表。

`groups`

     (Optional, string) Comma-separated list of search groups to include in the `search` statistics. 
`level`

    

(可选，字符串)指示统计信息是在集群、索引还是分片级别聚合。

有效值为：

* "集群" * "索引" * "分片"

`types`

     (Optional, string) A comma-separated list of document types for the `indexing` index metric. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`include_segment_file_sizes`

     (Optional, Boolean) If `true`, the call reports the aggregated disk usage of each one of the Lucene index files (only applies if segment stats are requested). Defaults to `false`. 
`include_unloaded_segments`

     (Optional, Boolean) If `true`, the response includes information from segments that are **not** loaded into memory. Defaults to `false`. 

### 响应正文

`_nodes`

    

(对象)包含有关请求选择的节点数的统计信息。

"_nodes"的属性

`total`

     (integer) Total number of nodes selected by the request. 
`successful`

     (integer) Number of nodes that responded successfully to the request. 
`failed`

     (integer) Number of nodes that rejected the request or failed to respond. If this value is not `0`, a reason for the rejection or failure is included in the response. 

`cluster_name`

     (string) Name of the cluster. Based on the [Cluster name setting](important-settings.html#cluster-name "Cluster name setting") setting. 
`nodes`

    

(对象)包含请求选择的节点的统计信息。

"节点"的属性

`<node_id>`

    

(对象)包含节点的统计信息。

""的属性<node_id>

`timestamp`

     (integer) Time the node stats were collected for this response. Recorded in milliseconds since the [Unix Epoch](https://en.wikipedia.org/wiki/Unix_time). 
`name`

     (string) Human-readable identifier for the node. Based on the [Node name setting](important-settings.html#node-name "Node name setting") setting. 
`transport_address`

     (string) Host and port for the [transport layer](modules-network.html#transport-settings "Advanced transport settings"), used for internal communication between nodes in a cluster. 
`host`

     (string) Network host for the node, based on the [Network host setting](important-settings.html#network.host "Network host setting") setting. 
`ip`

     (string) IP address and port for the node. 
`roles`

     (array of strings) Roles assigned to the node. See [Node](modules-node.html "Node"). 
`attributes`

     (object) Contains a list of attributes for the node. 

`indices`

    

(对象)包含有关分配了分片的索引的统计信息。

"指数"的属性

`docs`

    

(对象)包含有关分配给节点的所有主分片的文档的统计信息。

"文档"的属性

`count`

     (integer) The number of documents as reported by Lucene. This excludes deleted documents and counts any [nested documents](nested.html "Nested field type") separately from their parents. It also excludes documents which were indexed recently and do not yet belong to a segment. 
`deleted`

     (integer) The number of deleted documents as reported by Lucene, which may be higher or lower than the number of delete operations you have performed. This number excludes deletes that were performed recently and do not yet belong to a segment. Deleted documents are cleaned up by the [automatic merge process](index-modules-merge.html "Merge") if it makes sense to do so. Also, Elasticsearch creates extra deleted documents to internally track the recent history of operations on a shard. 

`store`

    

(对象)包含有关分配给节点的分片大小的统计信息。

"商店"的属性

`size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total size of all shards assigned to the node. 
`size_in_bytes`

     (integer) Total size, in bytes, of all shards assigned to the node. 
`total_data_set_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total data set size of all shards assigned to the node. This includes the size of shards not stored fully on the node, such as the cache for [partially mounted indices](searchable-snapshots.html#partially-mounted). 
`total_data_set_size_in_bytes`

     (integer) Total data set size, in bytes, of all shards assigned to the node. This includes the size of shards not stored fully on the node, such as the cache for [partially mounted indices](searchable-snapshots.html#partially-mounted). 
`reserved`

     ([byte value](api-conventions.html#byte-units "Byte size units")) A prediction of how much larger the shard stores on this node will eventually grow due to ongoing peer recoveries, restoring snapshots, and similar activities. A value of `-1b` indicates that this is not available. 
`reserved_in_bytes`

     (integer) A prediction, in bytes, of how much larger the shard stores on this node will eventually grow due to ongoing peer recoveries, restoring snapshots, and similar activities. A value of `-1` indicates that this is not available. 

`indexing`

    

(对象)包含有关节点索引操作的统计信息。

"索引"的属性

`index_total`

     (integer) Total number of indexing operations. 
`index_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent performing indexing operations. 
`index_time_in_millis`

     (integer) Total time in milliseconds spent performing indexing operations. 
`index_current`

     (integer) Number of indexing operations currently running. 
`index_failed`

     (integer) Number of failed indexing operations. 
`delete_total`

     (integer) Total number of deletion operations. 
`delete_time`

     ([time value](api-conventions.html#time-units "Time units")) Time spent performing deletion operations. 
`delete_time_in_millis`

     (integer) Time in milliseconds spent performing deletion operations. 
`delete_current`

     (integer) Number of deletion operations currently running. 
`noop_update_total`

     (integer) Total number of noop operations. 
`is_throttled`

     (Boolean) Number of times operations were throttled. 
`throttle_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent throttling operations. 
`throttle_time_in_millis`

     (integer) Total time in milliseconds spent throttling operations. 
`write_load`

     (double) Average number of write threads used while indexing documents. 

`get`

    

(对象)包含有关节点的获取操作的统计信息。

"获取"的属性

`total`

     (integer) Total number of get operations. 
`getTime`

     ([time value](api-conventions.html#time-units "Time units")) Time spent performing get operations. 
`time_in_millis`

     (integer) Time in milliseconds spent performing get operations. 
`exists_total`

     (integer) Total number of successful get operations. 
`exists_time`

     ([time value](api-conventions.html#time-units "Time units")) Time spent performing successful get operations. 
`exists_time_in_millis`

     (integer) Time in milliseconds spent performing successful get operations. 
`missing_total`

     (integer) Total number of failed get operations. 
`missing_time`

     ([time value](api-conventions.html#time-units "Time units")) Time spent performing failed get operations. 
`missing_time_in_millis`

     (integer) Time in milliseconds spent performing failed get operations. 
`current`

     (integer) Number of get operations currently running. 

`search`

    

(对象)包含有关节点搜索操作的统计信息。

"搜索"的属性

`open_contexts`

     (integer) Number of open search contexts. 
`query_total`

     (integer) Total number of query operations. 
`query_time`

     ([time value](api-conventions.html#time-units "Time units")) Time spent performing query operations. 
`query_time_in_millis`

     (integer) Time in milliseconds spent performing query operations. 
`query_current`

     (integer) Number of query operations currently running. 
`fetch_total`

     (integer) Total number of fetch operations. 
`fetch_time`

     ([time value](api-conventions.html#time-units "Time units")) Time spent performing fetch operations. 
`fetch_time_in_millis`

     (integer) Time in milliseconds spent performing fetch operations. 
`fetch_current`

     (integer) Number of fetch operations currently running. 
`scroll_total`

     (integer) Total number of scroll operations. 
`scroll_time`

     ([time value](api-conventions.html#time-units "Time units")) Time spent performing scroll operations. 
`scroll_time_in_millis`

     (integer) Time in milliseconds spent performing scroll operations. 
`scroll_current`

     (integer) Number of scroll operations currently running. 
`suggest_total`

     (integer) Total number of suggest operations. 
`suggest_time`

     ([time value](api-conventions.html#time-units "Time units")) Time spent performing suggest operations. 
`suggest_time_in_millis`

     (integer) Time in milliseconds spent performing suggest operations. 
`suggest_current`

     (integer) Number of suggest operations currently running. 

`merges`

    

(对象)包含有关节点合并操作的统计信息。

"合并"的属性

`current`

     (integer) Number of merge operations currently running. 
`current_docs`

     (integer) Number of document merges currently running. 
`current_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory used performing current document merges. 
`current_size_in_bytes`

     (integer) Memory, in bytes, used performing current document merges. 
`total`

     (integer) Total number of merge operations. 
`total_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent performing merge operations. 
`total_time_in_millis`

     (integer) Total time in milliseconds spent performing merge operations. 
`total_docs`

     (integer) Total number of merged documents. 
`total_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total size of document merges. 
`total_size_in_bytes`

     (integer) Total size of document merges in bytes. 
`total_stopped_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent stopping merge operations. 
`total_stopped_time_in_millis`

     (integer) Total time in milliseconds spent stopping merge operations. 
`total_throttled_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent throttling merge operations. 
`total_throttled_time_in_millis`

     (integer) Total time in milliseconds spent throttling merge operations. 
`total_auto_throttle`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Size of automatically throttled merge operations. 
`total_auto_throttle_in_bytes`

     (integer) Size, in bytes, of automatically throttled merge operations. 

`refresh`

    

(对象)包含有关节点刷新操作的统计信息。

"刷新"的属性

`total`

     (integer) Total number of refresh operations. 
`total_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent performing refresh operations. 
`total_time_in_millis`

     (integer) Total time in milliseconds spent performing refresh operations. 
`external_total`

     (integer) Total number of external refresh operations. 
`external_total_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent performing external operations. 
`external_total_time_in_millis`

     (integer) Total time in milliseconds spent performing external operations. 
`listeners`

     (integer) Number of refresh listeners. 

`flush`

    

(对象)包含有关节点刷新操作的统计信息。

"同花顺"的属性

`total`

     (integer) Number of flush operations. 
`periodic`

     (integer) Number of flush periodic operations. 
`total_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent performing flush operations. 
`total_time_in_millis`

     (integer) Total time in milliseconds spent performing flush operations. 

`warmer`

    

(对象)包含有关节点的索引预热操作的统计信息。

"温暖"的特性

`current`

     (integer) Number of active index warmers. 
`total`

     (integer) Total number of index warmers. 
`total_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent performing index warming operations. 
`total_time_in_millis`

     (integer) Total time in milliseconds spent performing index warming operations. 

`query_cache`

    

(对象)包含有关分配给节点的所有分片的查询缓存的统计信息。

"query_cache"的属性

`memory_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for the query cache across all shards assigned to the node. 
`memory_size_in_bytes`

     (integer) Total amount of memory, in bytes, used for the query cache across all shards assigned to the node. 
`total_count`

     (integer) Total count of hits, misses, and cached queries in the query cache. 
`hit_count`

     (integer) Number of query cache hits. 
`miss_count`

     (integer) Number of query cache misses. 
`cache_size`

     (integer) Current number of cached queries. 
`cache_count`

     (integer) Total number of all queries that have been cached. 
`evictions`

     (integer) Number of query cache evictions. 

`fielddata`

    

(对象)包含有关分配给节点的所有分片的字段数据缓存的统计信息。

"字段数据"的属性

`memory_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for the field data cache across all shards assigned to the node. 
`memory_size_in_bytes`

     (integer) Total amount of memory, in bytes, used for the field data cache across all shards assigned to the node. 
`evictions`

     (integer) Number of fielddata evictions. 

`completion`

    

(对象)包含有关分配给节点的所有分片的完成情况的统计信息。

"完成"的属性

`size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for completion across all shards assigned to the node. 
`size_in_bytes`

     (integer) Total amount of memory, in bytes, used for completion across all shards assigned to the node. 

`segments`

    

(对象)包含有关分配给节点的所有分片的段的统计信息。

"段"的属性

`count`

     (integer) Number of segments. 
`memory`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for segments across all shards assigned to the node. 
`memory_in_bytes`

     (integer) Total amount of memory, in bytes, used for segments across all shards assigned to the node. 
`terms_memory`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for terms across all shards assigned to the node. 
`terms_memory_in_bytes`

     (integer) Total amount of memory, in bytes, used for terms across all shards assigned to the node. 
`stored_fields_memory`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for stored fields across all shards assigned to the node. 
`stored_fields_memory_in_bytes`

     (integer) Total amount of memory, in bytes, used for stored fields across all shards assigned to the node. 
`term_vectors_memory`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for term vectors across all shards assigned to the node. 
`term_vectors_memory_in_bytes`

     (integer) Total amount of memory, in bytes, used for term vectors across all shards assigned to the node. 
`norms_memory`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for normalization factors across all shards assigned to the node. 
`norms_memory_in_bytes`

     (integer) Total amount of memory, in bytes, used for normalization factors across all shards assigned to the node. 
`points_memory`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for points across all shards assigned to the node. 
`points_memory_in_bytes`

     (integer) Total amount of memory, in bytes, used for points across all shards assigned to the node. 
`doc_values_memory`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for doc values across all shards assigned to the node. 
`doc_values_memory_in_bytes`

     (integer) Total amount of memory, in bytes, used for doc values across all shards assigned to the node. 
`index_writer_memory`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used by all index writers across all shards assigned to the node. 
`index_writer_memory_in_bytes`

     (integer) Total amount of memory, in bytes, used by all index writers across all shards assigned to the node. 
`version_map_memory`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory used by all version maps across all shards assigned to the node. 
`version_map_memory_in_bytes`

     (integer) Total amount of memory, in bytes, used by all version maps across all shards assigned to the node. 
`fixed_bit_set`

    

(字节值)分配给节点的所有分片中的固定位集使用的总内存量。

固定位集用于嵌套对象字段类型和联接字段的类型筛选器。

`fixed_bit_set_memory_in_bytes`

    

(整数)分配给节点的所有分片上的固定位集使用的内存总量(以字节为单位)。

固定位集用于嵌套对象字段类型和联接字段的类型筛选器。

`max_unsafe_auto_id_timestamp`

     (integer) Time of the most recently retried indexing request. Recorded in milliseconds since the [Unix Epoch](https://en.wikipedia.org/wiki/Unix_time). 
`file_sizes`

    

(对象)包含有关段文件大小的统计信息。

"file_sizes"的属性

`size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Size of the segment file. 
`size_in_bytes`

     (integer) Size, in bytes, of the segment file. 
`description`

     (string) Description of the segment file. 

`translog`

    

(对象)包含有关节点的事务日志操作的统计信息。

"Translog"的属性

`operations`

     (integer) Number of transaction log operations. 
`size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Size of the transaction log. 
`size_in_bytes`

     (integer) Size, in bytes, of the transaction log. 
`uncommitted_operations`

     (integer) Number of uncommitted transaction log operations. 
`uncommitted_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Size of uncommitted transaction log operations. 
`uncommitted_size_in_bytes`

     (integer) Size, in bytes, of uncommitted transaction log operations. 
`earliest_last_modified_age`

     (integer) Earliest last modified age for the transaction log. 

`request_cache`

    

(对象)包含有关分配给节点的所有分片的请求缓存的统计信息。

"request_cache"的属性

`memory_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory used by the request cache. 
`memory_size_in_bytes`

     (integer) Memory, in bytes, used by the request cache. 
`evictions`

     (integer) Number of request cache operations. 
`hit_count`

     (integer) Number of request cache hits. 
`miss_count`

     (integer) Number of request cache misses. 

`recovery`

    

(对象)包含有关节点恢复操作的统计信息。

"恢复"的属性

`current_as_source`

     (integer) Number of recoveries that used an index shard as a source. 
`current_as_target`

     (integer) Number of recoveries that used an index shard as a target. 
`throttle_time`

     ([time value](api-conventions.html#time-units "Time units")) Time by which recovery operations were delayed due to throttling. 
`throttle_time_in_millis`

     (integer) Time in milliseconds recovery operations were delayed due to throttling. 

`shard_stats`

    

(对象)包含有关分配给节点的所有分片的统计信息。

"shard_stats"的属性

`total_count`

     (integer) The total number of shards assigned to the node. 

`mappings`

    

(对象)包含有关节点映射的统计信息。对于"分片"级别，这不会显示，因为映射可以在节点上的索引分片之间共享。

"映射"的属性

`total_count`

     (integer) Number of mappings, including [runtime](runtime.html "Runtime fields") and [object](object.html "Object field type") fields. 
`total_estimated_overhead`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Estimated heap overhead of mappings on this node, which allows for 1kiB of heap for every mapped field. 
`total_estimated_overhead_in_bytes`

     (integer) Estimated heap overhead, in bytes, of mappings on this node, which allows for 1kiB of heap for every mapped field. 

`os`

    

(对象)包含有关节点操作系统的统计信息。

"os"的属性

`timestamp`

     (integer) Last time the operating system statistics were refreshed. Recorded in milliseconds since the [Unix Epoch](https://en.wikipedia.org/wiki/Unix_time). 
`cpu`

    

(对象)包含有关节点的 CPU 使用率的统计信息。

"中央处理器"的属性

`percent`

     (integer) Recent CPU usage for the whole system, or `-1` if not supported. 
`load_average`

    

(对象)包含有关系统上负载平均值的统计信息。

"load_average"的属性

`1m`

     (float) One-minute load average on the system (field is not present if one-minute load average is not available). 
`5m`

     (float) Five-minute load average on the system (field is not present if five-minute load average is not available). 
`15m`

     (float) Fifteen-minute load average on the system (field is not present if fifteen-minute load average is not available). 

`mem`

    

(对象)包含有关节点内存使用情况的统计信息。

"mem"的属性

`total`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of physical memory. 
`total_in_bytes`

     (integer) Total amount of physical memory in bytes. 
`adjusted_total`

     ([byte value](api-conventions.html#byte-units "Byte size units")) If the amount of physical memory has been overridden using the `es.total_memory_bytes` system property then this reports the overridden value. Otherwise it reports the same value as `total`. 
`adjusted_total_in_bytes`

     (integer) If the amount of physical memory has been overridden using the `es.total_memory_bytes` system property then this reports the overridden value in bytes. Otherwise it reports the same value as `total_in_bytes`. 
`free`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of free physical memory. 
`free_in_bytes`

     (integer) Amount of free physical memory in bytes. 
`used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of used physical memory. 
`used_in_bytes`

     (integer) Amount of used physical memory in bytes. 
`free_percent`

     (integer) Percentage of free memory. 
`used_percent`

     (integer) Percentage of used memory. 

`swap`

    

(对象)包含有关节点交换空间的统计信息。

"交换"的属性

`total`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of swap space. 
`total_in_bytes`

     (integer) Total amount of swap space in bytes. 
`free`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of free swap space. 
`free_in_bytes`

     (integer) Amount of free swap space in bytes. 
`used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of used swap space. 
`used_in_bytes`

     (integer) Amount of used swap space in bytes. 

"cgroup"(仅限 Linux)

    

(对象)包含节点的 cgroup 统计信息。

为了使 cgroup 统计信息可见，必须将 cgroups 编译到内核中，必须配置"cpu"和"cpuacct"cgroup 子系统，并且统计信息必须可从"/sys/fs/cgroup/cpu"和"/sys/fs/cgroup/cpuacct"读取。

"cgroup"的属性

'cpuacct' (仅限 Linux)

    

(对象)包含有关节点的"cpuacct"控制组的统计信息。

"cpuacct"的属性

"control_group"(仅限 Linux)

     (string) The `cpuacct` control group to which the Elasticsearch process belongs. 
`usage_nanos` (Linux only)

     (integer) The total CPU time (in nanoseconds) consumed by all tasks in the same cgroup as the Elasticsearch process. 

"cpu"(仅限 Linux)

    

(对象)包含有关节点的"cpu"控制组的统计信息。

"中央处理器"的属性

"control_group"(仅限 Linux)

     (string) The `cpu` control group to which the Elasticsearch process belongs. 
`cfs_period_micros` (Linux only)

     (integer) The period of time (in microseconds) for how regularly all tasks in the same cgroup as the Elasticsearch process should have their access to CPU resources reallocated. 
`cfs_quota_micros` (Linux only)

     (integer) The total amount of time (in microseconds) for which all tasks in the same cgroup as the Elasticsearch process can run during one period `cfs_period_micros`. 
`stat` (Linux only)

    

(对象)包含节点的 CPU 统计信息。

"统计"的属性

"number_of_elapsed_periods"(仅限 Linux)

     (integer) The number of reporting periods (as specified by `cfs_period_micros`) that have elapsed. 
`number_of_times_throttled` (Linux only)

     (integer) The number of times all tasks in the same cgroup as the Elasticsearch process have been throttled. 
`time_throttled_nanos` (Linux only)

     (integer) The total amount of time (in nanoseconds) for which all tasks in the same cgroup as the Elasticsearch process have been throttled. 

"内存"(仅限 Linux)

    

(对象)包含有关节点的"内存"控制组的统计信息。

"记忆"的属性

"control_group"(仅限 Linux)

     (string) The `memory` control group to which the Elasticsearch process belongs. 
`limit_in_bytes` (Linux only)

     (string) The maximum amount of user memory (including file cache) allowed for all tasks in the same cgroup as the Elasticsearch process. This value can be too big to store in a `long`, so is returned as a string so that the value returned can exactly match what the underlying operating system interface returns. Any value that is too large to parse into a `long` almost certainly means no limit has been set for the cgroup. 
`usage_in_bytes` (Linux only)

     (string) The total current memory usage by processes in the cgroup (in bytes) by all tasks in the same cgroup as the Elasticsearch process. This value is stored as a string for consistency with `limit_in_bytes`. 

`process`

    

(对象)包含节点的进程统计信息。

"过程"的属性

`timestamp`

     (integer) Last time the statistics were refreshed. Recorded in milliseconds since the [Unix Epoch](https://en.wikipedia.org/wiki/Unix_time). 
`open_file_descriptors`

     (integer) Number of opened file descriptors associated with the current or `-1` if not supported. 
`max_file_descriptors`

     (integer) Maximum number of file descriptors allowed on the system, or `-1` if not supported. 
`cpu`

    

(对象)包含节点的 CPU 统计信息。

"中央处理器"的属性

`percent`

     (integer) CPU usage in percent, or `-1` if not known at the time the stats are computed. 
`total`

     ([time value](api-conventions.html#time-units "Time units")) CPU time used by the process on which the Java virtual machine is running. 
`total_in_millis`

     (integer) CPU time (in milliseconds) used by the process on which the Java virtual machine is running, or `-1` if not supported. 

`mem`

    

(对象)包含节点的虚拟内存统计信息。

"mem"的属性

`total_virtual`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Size of virtual memory that is guaranteed to be available to the running process. 
`total_virtual_in_bytes`

     (integer) Size in bytes of virtual memory that is guaranteed to be available to the running process. 

`jvm`

    

(对象)包含节点的 Java 虚拟机 (JVM) 统计信息。

"jvm"的属性

`timestamp`

     (integer) Last time JVM statistics were refreshed. 
`uptime`

     ([time value](api-conventions.html#time-units "Time units")) Human-readable JVM uptime. Only returned if the [`human`](common-options.html#_human_readable_output "Human readable output") query parameter is `true`. 
`uptime_in_millis`

     (integer) JVM uptime in milliseconds. 
`mem`

    

(对象)包含节点的 JVM 内存使用情况统计信息。

"mem"的属性

`heap_used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory currently in use by the heap. 
`heap_used_in_bytes`

     (integer) Memory, in bytes, currently in use by the heap. 
`heap_used_percent`

     (integer) Percentage of memory currently in use by the heap. 
`heap_committed`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of memory available for use by the heap. 
`heap_committed_in_bytes`

     (integer) Amount of memory, in bytes, available for use by the heap. 
`heap_max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Maximum amount of memory available for use by the heap. 
`heap_max_in_bytes`

     (integer) Maximum amount of memory, in bytes, available for use by the heap. 
`non_heap_used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Non-heap memory used. 
`non_heap_used_in_bytes`

     (integer) Non-heap memory used, in bytes. 
`non_heap_committed`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of non-heap memory available. 
`non_heap_committed_in_bytes`

     (integer) Amount of non-heap memory available, in bytes. 
`pools`

    

(对象)包含有关节点的堆内存使用情况的统计信息。

"池"的属性

`young`

    

(对象)包含有关节点的年轻一代堆的内存使用情况的统计信息。

"年轻"的性质

`used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory used by the young generation heap. 
`used_in_bytes`

     (integer) Memory, in bytes, used by the young generation heap. 
`max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Maximum amount of memory available for use by the young generation heap. 
`max_in_bytes`

     (integer) Maximum amount of memory, in bytes, available for use by the young generation heap. 
`peak_used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Largest amount of memory historically used by the young generation heap. 
`peak_used_in_bytes`

     (integer) Largest amount of memory, in bytes, historically used by the young generation heap. 
`peak_max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Largest amount of memory historically used by the young generation heap. 
`peak_max_in_bytes`

     (integer) Largest amount of memory, in bytes, historically used by the young generation heap. 

`survivor`

    

(对象)包含有关节点的幸存者空间的内存使用情况的统计信息。

"幸存者"的属性

`used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory used by the survivor space. 
`used_in_bytes`

     (integer) Memory, in bytes, used by the survivor space. 
`max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Maximum amount of memory available for use by the survivor space. 
`max_in_bytes`

     (integer) Maximum amount of memory, in bytes, available for use by the survivor space. 
`peak_used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Largest amount of memory historically used by the survivor space. 
`peak_used_in_bytes`

     (integer) Largest amount of memory, in bytes, historically used by the survivor space. 
`peak_max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Largest amount of memory historically used by the survivor space. 
`peak_max_in_bytes`

     (integer) Largest amount of memory, in bytes, historically used by the survivor space. 

`old`

    

(对象)包含有关节点的旧代堆的内存使用情况的统计信息。

"旧"的属性

`used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory used by the old generation heap. 
`used_in_bytes`

     (integer) Memory, in bytes, used by the old generation heap. 
`max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Maximum amount of memory available for use by the old generation heap. 
`max_in_bytes`

     (integer) Maximum amount of memory, in bytes, available for use by the old generation heap. 
`peak_used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Largest amount of memory historically used by the old generation heap. 
`peak_used_in_bytes`

     (integer) Largest amount of memory, in bytes, historically used by the old generation heap. 
`peak_max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Highest memory limit historically available for use by the old generation heap. 
`peak_max_in_bytes`

     (integer) Highest memory limit, in bytes, historically available for use by the old generation heap. 

`threads`

    

(对象)包含有关节点的 JVM 线程使用情况的统计信息。

"线程"的属性

`count`

     (integer) Number of active threads in use by JVM. 
`peak_count`

     (integer) Highest number of threads used by JVM. 

`gc`

    

(对象)包含有关节点的 JVM 垃圾回收器的统计信息。

"gc"的属性

`collectors`

    

(对象)包含有关节点的 JVM 垃圾回收器的统计信息。

"收集器"的属性

`young`

    

(对象)包含有关收集节点年轻一代对象的 JVM 垃圾回收器的统计信息。

"年轻"的性质

`collection_count`

     (integer) Number of JVM garbage collectors that collect young generation objects. 
`collection_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent by JVM collecting young generation objects. 
`collection_time_in_millis`

     (integer) Total time in milliseconds spent by JVM collecting young generation objects. 

`old`

    

(对象)包含有关收集节点旧代对象的 JVM 垃圾回收器的统计信息。

"旧"的属性

`collection_count`

     (integer) Number of JVM garbage collectors that collect old generation objects. 
`collection_time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent by JVM collecting old generation objects. 
`collection_time_in_millis`

     (integer) Total time in milliseconds spent by JVM collecting old generation objects. 

`buffer_pools`

    

(对象)包含有关节点的 JVM 缓冲池的统计信息。

"buffer_pools"的属性

`mapped`

    

(对象)包含有关节点的映射 JVM 缓冲池的统计信息。

"映射"的属性

`count`

     (integer) Number of mapped buffer pools. 
`used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Size of mapped buffer pools. 
`used_in_bytes`

     (integer) Size, in bytes, of mapped buffer pools. 
`total_capacity`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total capacity of mapped buffer pools. 
`total_capacity_in_bytes`

     (integer) Total capacity, in bytes, of mapped buffer pools. 

`direct`

    

(对象)包含有关节点的直接 JVM 缓冲池的统计信息。

"直接"的属性

`count`

     (integer) Number of direct buffer pools. 
`used`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Size of direct buffer pools. 
`used_in_bytes`

     (integer) Size, in bytes, of direct buffer pools. 
`total_capacity`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total capacity of direct buffer pools. 
`total_capacity_in_bytes`

     (integer) Total capacity, in bytes, of direct buffer pools. 

`classes`

    

(对象)包含有关 JVM 为节点装入的类的统计信息。

"类"的属性

`current_loaded_count`

     (integer) Number of classes currently loaded by JVM. 
`total_loaded_count`

     (integer) Total number of classes loaded since the JVM started. 
`total_unloaded_count`

     (integer) Total number of classes unloaded since the JVM started. 

`repositories`

    

(对象)有关快照存储库的统计信息。

"存储库"的属性

`<repository_name>`

    

(对象)包含节点的存储库限制统计信息。

""的属性<repository_name>

`total_read_throttled_time_nanos`

     (integer) Total number of nanos which node had to wait during recovery. 
`total_write_throttled_time_nanos`

     (integer) Total number of nanos which node had to wait during snapshotting. 

`thread_pool`

    

(对象)包含节点的线程池统计信息

"thread_pool"的属性

`<thread_pool_name>`

    

(对象)包含有关节点的线程池的统计信息。

""的属性<thread_pool_name>

`threads`

     (integer) Number of threads in the thread pool. 
`queue`

     (integer) Number of tasks in queue for the thread pool. 
`active`

     (integer) Number of active threads in the thread pool. 
`rejected`

     (integer) Number of tasks rejected by the thread pool executor. 
`largest`

     (integer) Highest number of active threads in the thread pool. 
`completed`

     (integer) Number of tasks completed by the thread pool executor. 

`fs`

    

(对象)包含节点的文件存储统计信息。

"fs"的属性

`timestamp`

     (integer) Last time the file stores statistics were refreshed. Recorded in milliseconds since the [Unix Epoch](https://en.wikipedia.org/wiki/Unix_time). 
`total`

    

(对象)包含节点的所有文件存储的统计信息。

"总计"的属性

`total`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total size of all file stores. 
`total_in_bytes`

     (integer) Total size (in bytes) of all file stores. 
`free`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total unallocated disk space in all file stores. 
`free_in_bytes`

     (integer) Total number of unallocated bytes in all file stores. 
`available`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total disk space available to this Java virtual machine on all file stores. Depending on OS or process level restrictions, this might appear less than `free`. This is the actual amount of free disk space the Elasticsearch node can utilise. 
`available_in_bytes`

     (integer) Total number of bytes available to this Java virtual machine on all file stores. Depending on OS or process level restrictions, this might appear less than `free_in_bytes`. This is the actual amount of free disk space the Elasticsearch node can utilise. 

`data`

    

(对象数组)所有文件存储的列表。

"数据"的属性

`path`

     (string) Path to the file store. 
`mount`

     (string) Mount point of the file store (ex: /dev/sda2). 
`type`

     (string) Type of the file store (ex: ext4). 
`total`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total size of the file store. 
`total_in_bytes`

     (integer) Total size (in bytes) of the file store. 
`free`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of unallocated disk space in the file store. 
`free_in_bytes`

     (integer) Total number of unallocated bytes in the file store. 
`available`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of disk space available to this Java virtual machine on this file store. 
`available_in_bytes`

     (integer) Total number of bytes available to this Java virtual machine on this file store. 

"io_stats"(仅限 Linux)

    

(对象)包含节点的 I/O 统计信息。

"io_stats"的属性

"设备"(仅限 Linux)

    

(阵列)支持 Elasticsearchdata 路径的每个设备的磁盘指标数组。定期探测这些磁盘指标，并计算上次探测和当前探测之间的平均值。

"设备"的属性

"device_name"(仅限 Linux)

     (string) The Linux device name. 
`operations` (Linux only)

     (integer) The total number of read and write operations for the device completed since starting Elasticsearch. 
`read_operations` (Linux only)

     (integer) The total number of read operations for the device completed since starting Elasticsearch. 
`write_operations` (Linux only)

     (integer) The total number of write operations for the device completed since starting Elasticsearch. 
`read_kilobytes` (Linux only)

     (integer) The total number of kilobytes read for the device since starting Elasticsearch. 
`write_kilobytes` (Linux only)

     (integer) The total number of kilobytes written for the device since starting Elasticsearch. 
`io_time_in_millis` (Linux only)

     (integer) The total time in milliseconds spent performing I/O operations for the device since starting Elasticsearch. 

"total"(仅限 Linux)

    

(对象)支持弹性搜索数据路径的所有设备的磁盘指标总和。

"总计"的属性

"操作"(仅限 Linux)

     (integer) The total number of read and write operations across all devices used by Elasticsearch completed since starting Elasticsearch. 
`read_operations` (Linux only)

     (integer) The total number of read operations for across all devices used by Elasticsearch completed since starting Elasticsearch. 
`write_operations` (Linux only)

     (integer) The total number of write operations across all devices used by Elasticsearch completed since starting Elasticsearch. 
`read_kilobytes` (Linux only)

     (integer) The total number of kilobytes read across all devices used by Elasticsearch since starting Elasticsearch. 
`write_kilobytes` (Linux only)

     (integer) The total number of kilobytes written across all devices used by Elasticsearch since starting Elasticsearch. 
`io_time_in_millis` (Linux only)

     (integer) The total time in milliseconds spent performing I/O operations across all devices used by Elasticsearch since starting Elasticsearch. 

`transport`

    

(对象)包含节点的传输统计信息。

"运输"的属性

`server_open`

     (integer) Current number of inbound TCP connections used for internal communication between nodes. 
`total_outbound_connections`

     (integer) The cumulative number of outbound transport connections that this node has opened since it started. Each transport connection may comprise multiple TCP connections but is only counted once in this statistic. Transport connections are typically [long-lived](modules-network.html#long-lived-connections "Long-lived idle connections") so this statistic should remain constant in a stable cluster. 
`rx_count`

     (integer) Total number of RX (receive) packets received by the node during internal cluster communication. 
`rx_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Size of RX packets received by the node during internal cluster communication. 
`rx_size_in_bytes`

     (integer) Size, in bytes, of RX packets received by the node during internal cluster communication. 
`tx_count`

     (integer) Total number of TX (transmit) packets sent by the node during internal cluster communication. 
`tx_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Size of TX packets sent by the node during internal cluster communication. 
`tx_size_in_bytes`

     (integer) Size, in bytes, of TX packets sent by the node during internal cluster communication. 
`inbound_handling_time_histogram`

    

(阵列)在传输线程上处理每个入站消息所花费的时间分布，表示为直方图。

"inbound_handling_time_histogram"的属性

`ge`

     (string) The inclusive lower bound of the bucket as a human-readable string. May be omitted on the first bucket if this bucket has no lower bound. 
`ge_millis`

     (integer) The inclusive lower bound of the bucket in milliseconds. May be omitted on the first bucket if this bucket has no lower bound. 
`lt`

     (string) The exclusive upper bound of the bucket as a human-readable string. May be omitted on the last bucket if this bucket has no upper bound. 
`lt_millis`

     (integer) The exclusive upper bound of the bucket in milliseconds. May be omitted on the last bucket if this bucket has no upper bound. 
`count`

     (integer) The number of times a transport thread took a period of time within the bounds of this bucket to handle an inbound message. 

`outbound_handling_time_histogram`

    

(阵列)在传输线程上发送每个出站传输消息所花费的时间分布，以直方图表示。

"outbound_handling_time_histogram"的属性

`ge`

     (string) The inclusive lower bound of the bucket as a human-readable string. May be omitted on the first bucket if this bucket has no lower bound. 
`ge_millis`

     (integer) The inclusive lower bound of the bucket in milliseconds. May be omitted on the first bucket if this bucket has no lower bound. 
`lt`

     (string) The exclusive upper bound of the bucket as a human-readable string. May be omitted on the last bucket if this bucket has no upper bound. 
`lt_millis`

     (integer) The exclusive upper bound of the bucket in milliseconds. May be omitted on the last bucket if this bucket has no upper bound. 
`count`

     (integer) The number of times a transport thread took a period of time within the bounds of this bucket to send a transport message. 

`actions`

    

(对象)此节点处理的传输流量的逐个操作细分，显示流量总量以及传入请求和传出响应的消息大小直方图。

"actions.*.requests"和"actions.*.responses"的属性

`count`

     (integer) The total number of requests received, or responses sent, for the current action. 
`total_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The total size (as a human-readable string) of all requests received, or responses sent, for the current action. 
`total_size_in_bytes`

     (integer) The total size in bytes of all requests received, or responses sent, for the current action. 
`histogram`

    

(阵列)针对当前操作收到的请求或发送的响应大小的分布细分。

"直方图"的属性

`ge`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The inclusive lower bound of the bucket as a human-readable string. May be omitted on the first bucket if this bucket has no lower bound. 
`ge_bytes`

     (integer) The inclusive lower bound of the bucket in bytes. May be omitted on the first bucket if this bucket has no lower bound. 
`lt`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The exclusive upper bound of the bucket as a human-readable string. May be omitted on the last bucket if this bucket has no upper bound. 
`lt_bytes`

     (integer) The exclusive upper bound of the bucket in bytes. May be omitted on the last bucket if this bucket has no upper bound. 
`count`

     (integer) The number of times a request was received, or a response sent, with a size within the bounds of this bucket. 

`http`

    

(对象)包含节点的 http 统计信息。

"http"的属性

`current_open`

     (integer) Current number of open HTTP connections for the node. 
`total_opened`

     (integer) Total number of HTTP connections opened for the node. 
`clients`

    

(对象数组)有关当前和最近关闭的 HTTP 客户端连接的信息。关闭时间超过 thehttp.client_stats.closed_channels.max_age 设置的客户端将不在此处显示。

"客户端"的属性

`id`

     (integer) Unique ID for the HTTP client. 
`agent`

     (string) Reported agent for the HTTP client. If unavailable, this property is not included in the response. 
`local_address`

     (string) Local address for the HTTP connection. 
`remote_address`

     (string) Remote address for the HTTP connection. 
`last_uri`

     (string) The URI of the client's most recent request. 
`x_forwarded_for`

     (string) Value from the client's `x-forwarded-for` HTTP header. If unavailable, this property is not included in the response. 
`x_opaque_id`

     (string) Value from the client's `x-opaque-id` HTTP header. If unavailable, this property is not included in the response. 
`opened_time_millis`

     (integer) Time at which the client opened the connection. 
`closed_time_millis`

     (integer) Time at which the client closed the connection if the connection is closed. 
`last_request_time_millis`

     (integer) Time of the most recent request from this client. 
`request_count`

     (integer) Number of requests from this client. 
`request_size_bytes`

     (integer) Cumulative size in bytes of all requests from this client. 

`breakers`

    

(对象)包含节点的断路器统计信息。

"断路器"的属性

`<circuit_breaker_name>`

    

(对象)包含断路器的统计信息。

""的属性<circuit_breaker_name>

`limit_size_in_bytes`

     (integer) Memory limit, in bytes, for the circuit breaker. 
`limit_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory limit for the circuit breaker. 
`estimated_size_in_bytes`

     (integer) Estimated memory used, in bytes, for the operation. 
`estimated_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Estimated memory used for the operation. 
`overhead`

     (float) A constant that all estimates for the circuit breaker are multiplied with to calculate a final estimate. 
`tripped`

     (integer) Total number of times the circuit breaker has been triggered and prevented an out of memory error. 

`script`

    

(对象)包含节点的脚本统计信息。

"脚本"的属性

`compilations`

     (integer) Total number of inline script compilations performed by the node. 
`compilations_history`

     (object) Contains this recent history of script compilations 

"compilations_history"的属性

`5m`

     (long) The number of script compilations in the last five minutes. 
`15m`

     (long) The number of script compilations in the last fifteen minutes. 
`24h`

     (long) The number of script compilations in the last twenty-four hours. 

`cache_evictions`

     (integer) Total number of times the script cache has evicted old data. 
`cache_evictions_history`

     (object) Contains this recent history of script cache evictions 

"cache_evictions"的属性

`5m`

     (long) The number of script cache evictions in the last five minutes. 
`15m`

     (long) The number of script cache evictions in the last fifteen minutes. 
`24h`

     (long) The number of script cache evictions in the last twenty-four hours. 

`compilation_limit_triggered`

     (integer) Total number of times the [script compilation](circuit-breaker.html#script-compilation-circuit-breaker "Script compilation circuit breaker") circuit breaker has limited inline script compilations. 

`discovery`

    

(对象)包含节点的节点发现统计信息。

"发现"的属性

`cluster_state_queue`

    

(对象)包含节点的群集状态队列的统计信息。

"cluster_state_queue"的属性

`total`

     (integer) Total number of cluster states in queue. 
`pending`

     (integer) Number of pending cluster states in queue. 
`committed`

     (integer) Number of committed cluster states in queue. 

`published_cluster_states`

    

(对象)包含节点的已发布群集状态的统计信息。

"published_cluster_states"的属性

`full_states`

     (integer) Number of published cluster states. 
`incompatible_diffs`

     (integer) Number of incompatible differences between published cluster states. 
`compatible_diffs`

     (integer) Number of compatible differences between published cluster states. 

`cluster_state_update`

    

(对象)包含有关节点是选定主节点时各种活动在群集状态更新期间所花费的时间的低级统计信息。如果节点不符合主节点条件，则省略。在此对象中，名称以"_time"结尾的每个字段也表示为名称以"_time_millis"结尾的字段中的原始毫秒数。仅当使用"？human=true"查询参数请求时，才会返回带有"_time"后缀的人类可读字段。

"cluster_state_update"的属性

`unchanged`

    

(对象)包含有关未更改群集状态的群集状态更新尝试的统计信息。

"不变"的属性

`count`

     (long) The number of cluster state update attempts that did not change the cluster state since the node started. 
`computation_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent computing no-op cluster state updates since the node started. 
`notification_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent notifying listeners of a no-op cluster state update since the node started. 

`success`

    

(对象)包含有关成功更改群集状态的群集状态更新尝试的统计信息。

"成功"的属性

`count`

     (long) The number of cluster state update attempts that successfully changed the cluster state since the node started. 
`computation_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent computing cluster state updates that were ultimately successful since the node started. 
`publication_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent publishing cluster state updates which ultimately succeeded, which includes everything from the start of the publication (i.e. just after the computation of the new cluster state) until the publication has finished and the master node is ready to start processing the next state update. This includes the time measured by `context_construction_time`, `commit_time`, `completion_time` and `master_apply_time`. 
`context_construction_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent constructing a _publication context_ since the node started for publications that ultimately succeeded. This statistic includes the time spent computing the difference between the current and new cluster state preparing a serialized representation of this difference. 
`commit_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent waiting for a successful cluster state update to _commit_ , which measures the time from the start of each publication until a majority of the master-eligible nodes have written the state to disk and confirmed the write to the elected master. 
`completion_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent waiting for a successful cluster state update to _complete_ , which measures the time from the start of each publication until all the other nodes have notified the elected master that they have applied the cluster state. 
`master_apply_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent successfully applying cluster state updates on the elected master since the node started. 
`notification_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent notifying listeners of a successful cluster state update since the node started. 

`failure`

    

(对象)包含有关未成功更改集群状态的集群状态更新尝试的统计信息，通常是因为新的主节点在完成之前退出。

"失败"的属性

`count`

     (long) The number of cluster state update attempts that failed to change the cluster state since the node started. 
`computation_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent computing cluster state updates that were ultimately unsuccessful since the node started. 
`publication_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent publishing cluster state updates which ultimately failed, which includes everything from the start of the publication (i.e. just after the computation of the new cluster state) until the publication has finished and the master node is ready to start processing the next state update. This includes the time measured by `context_construction_time`, `commit_time`, `completion_time` and `master_apply_time`. 
`context_construction_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent constructing a _publication context_ since the node started for publications that ultimately failed. This statistic includes the time spent computing the difference between the current and new cluster state preparing a serialized representation of this difference. 
`commit_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent waiting for an unsuccessful cluster state update to _commit_ , which measures the time from the start of each publication until a majority of the master-eligible nodes have written the state to disk and confirmed the write to the elected master. 
`completion_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent waiting for an unsuccessful cluster state update to _complete_ , which measures the time from the start of each publication until all the other nodes have notified the elected master that they have applied the cluster state. 
`master_apply_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent unsuccessfully applying cluster state updates on the elected master since the node started. 
`notification_time`

     ([time value](api-conventions.html#time-units "Time units")) The cumulative amount of time spent notifying listeners of a failed cluster state update since the node started. 

`ingest`

    

(对象)包含节点的引入统计信息。

"摄取"的属性

`total`

    

(对象)包含有关节点的摄取操作的统计信息。

"总计"的属性

`count`

     (integer) Total number of documents ingested during the lifetime of this node. 
`time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent preprocessing ingest documents during the lifetime of this node. 
`time_in_millis`

     (integer) Total time, in milliseconds, spent preprocessing ingest documents during the lifetime of this node. 
`current`

     (integer) Total number of documents currently being ingested. 
`failed`

     (integer) Total number of failed ingest operations during the lifetime of this node. 

`pipelines`

    

(对象)包含有关节点引入管道的统计信息。

"管道"的属性

`<pipeline_id>`

    

(对象)包含有关引入管道的统计信息。

""的属性<pipeline_id>

`count`

     (integer) Number of documents preprocessed by the ingest pipeline. 
`time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent preprocessing documents in the ingest pipeline. 
`time_in_millis`

     (integer) Total time, in milliseconds, spent preprocessing documents in the ingest pipeline. 
`failed`

     (integer) Total number of failed operations for the ingest pipeline. 
`processors`

    

(对象数组)包含最摄取管道的摄取处理器的统计信息。

"处理器"的属性

`<processor>`

    

(对象)包含引入处理器的统计信息。

""的属性<processor>

`count`

     (integer) Number of documents transformed by the processor. 
`time`

     ([time value](api-conventions.html#time-units "Time units")) Time spent by the processor transforming documents. 
`time_in_millis`

     (integer) Time, in milliseconds, spent by the processor transforming documents. 
`current`

     (integer) Number of documents currently being transformed by the processor. 
`failed`

     (integer) Number of failed operations for the processor. 

`indexing_pressure`

    

(对象)包含节点的索引压力统计信息。

"indexing_pressure"的属性

`memory`

    

(对象)包含索引加载的内存消耗统计信息。

""的属性<memory>

`current`

    

(对象)包含当前索引负载的统计信息。

""的属性<current>

`combined_coordinating_and_primary`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the coordinating or primary stage. This value is not the sum of coordinating and primary as a node can reuse the coordinating memory if the primary stage is executed locally. 
`combined_coordinating_and_primary_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the coordinating or primary stage. This value is not the sum of coordinating and primary as a node can reuse the coordinating memory if the primary stage is executed locally. 
`coordinating`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the coordinating stage. 
`coordinating_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the coordinating stage. 
`primary`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the primary stage. 
`primary_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the primary stage. 
`replica`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the replica stage. 
`replica_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the replica stage. 
`all`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the coordinating, primary, or replica stage. 
`all_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the coordinating, primary, or replica stage. 

`total`

    

(对象)包含自节点启动以来累积索引负载的统计信息。

""的属性<total>

`combined_coordinating_and_primary`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the coordinating or primary stage. This value is not the sum of coordinating and primary as a node can reuse the coordinating memory if the primary stage is executed locally. 
`combined_coordinating_and_primary_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the coordinating or primary stage. This value is not the sum of coordinating and primary as a node can reuse the coordinating memory if the primary stage is executed locally. 
`coordinating`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the coordinating stage. 
`coordinating_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the coordinating stage. 
`primary`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the primary stage. 
`primary_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the primary stage. 
`replica`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the replica stage. 
`replica_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the replica stage. 
`all`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Memory consumed by indexing requests in the coordinating, primary, or replica stage. 
`all_in_bytes`

     (integer) Memory consumed, in bytes, by indexing requests in the coordinating, primary, or replica stage. 
`coordinating_rejections`

     (integer) Number of indexing requests rejected in the coordinating stage. 
`primary_rejections`

     (integer) Number of indexing requests rejected in the primary stage. 
`replica_rejections`

     (integer) Number of indexing requests rejected in the replica stage. 

`limit`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Configured memory limit for the indexing requests. Replica requests have an automatic limit that is 1.5x this value. 
`limit_in_bytes`

     (integer) Configured memory limit, in bytes, for the indexing requests. Replica requests have an automatic limit that is 1.5x this value. 

`adaptive_selection`

    

(对象)包含节点的自适应选择统计信息。

"adaptive_selection"的属性

`outgoing_searches`

     (integer) The number of outstanding search requests from the node these stats are for to the keyed node. 
`avg_queue_size`

     (integer) The exponentially weighted moving average queue size of search requests on the keyed node. 
`avg_service_time`

     ([time value](api-conventions.html#time-units "Time units")) The exponentially weighted moving average service time of search requests on the keyed node. 
`avg_service_time_ns`

     (integer) The exponentially weighted moving average service time, in nanoseconds, of search requests on the keyed node. 
`avg_response_time`

     ([time value](api-conventions.html#time-units "Time units")) The exponentially weighted moving average response time of search requests on the keyed node. 
`avg_response_time_ns`

     (integer) The exponentially weighted moving average response time, in nanoseconds, of search requests on the keyed node. 
`rank`

     (string) The rank of this node; used for shard selection when routing search requests. 

###Examples

    
    
    response = client.nodes.stats(
      metric: 'indices'
    )
    puts response
    
    response = client.nodes.stats(
      metric: 'os,process'
    )
    puts response
    
    response = client.nodes.stats(
      node_id: '10.0.0.1',
      metric: 'process'
    )
    puts response
    
    
    # return just indices
    GET /_nodes/stats/indices
    
    # return just os and process
    GET /_nodes/stats/os,process
    
    # return just process for node with IP address 10.0.0.1
    GET /_nodes/10.0.0.1/stats/process

所有统计数据都可以通过"/_nodes/stats/_all"或"/_nodes/stats？metric=_all"明确请求。

您可以在"节点"、"索引"或"分片"级别获取有关索引统计信息的信息。

    
    
    response = client.nodes.stats(
      metric: 'indices',
      index_metric: 'fielddata',
      fields: 'field1,field2'
    )
    puts response
    
    response = client.nodes.stats(
      metric: 'indices',
      index_metric: 'fielddata',
      level: 'indices',
      fields: 'field1,field2'
    )
    puts response
    
    response = client.nodes.stats(
      metric: 'indices',
      index_metric: 'fielddata',
      level: 'shards',
      fields: 'field1,field2'
    )
    puts response
    
    response = client.nodes.stats(
      metric: 'indices',
      index_metric: 'fielddata',
      fields: 'field*'
    )
    puts response
    
    
    # Fielddata summarized by node
    GET /_nodes/stats/indices/fielddata?fields=field1,field2
    
    # Fielddata summarized by node and index
    GET /_nodes/stats/indices/fielddata?level=indices&fields=field1,field2
    
    # Fielddata summarized by node, index, and shard
    GET /_nodes/stats/indices/fielddata?level=shards&fields=field1,field2
    
    # You can use wildcards for field names
    GET /_nodes/stats/indices/fielddata?fields=field*

您可以获取有关在此节点上执行的搜索的搜索组的统计信息。

    
    
    response = client.nodes.stats(
      groups: '_all'
    )
    puts response
    
    response = client.nodes.stats(
      metric: 'indices',
      groups: 'foo,bar'
    )
    puts response
    
    
    # All groups with all stats
    GET /_nodes/stats?groups=_all
    
    # Some groups from just the indices stats
    GET /_nodes/stats/indices?groups=foo,bar

#### 仅检索引入统计信息

要仅返回与摄取相关的节点统计信息，请将 '' <metric>pathparameter 设置为 'ingest' 并使用 'filter_path' 查询参数。

    
    
    response = client.nodes.stats(
      metric: 'ingest',
      filter_path: 'nodes.*.ingest'
    )
    puts response
    
    
    GET /_nodes/stats/ingest?filter_path=nodes.*.ingest

您可以使用"指标"和"filter_path"查询参数来获取相同的响应。

    
    
    response = client.nodes.stats(
      metric: 'ingest',
      filter_path: 'nodes.*.ingest'
    )
    puts response
    
    
    GET /_nodes/stats?metric=ingest&filter_path=nodes.*.ingest

要进一步细化响应，请更改"filter_path"值。例如，以下请求仅返回引入管道统计信息。

    
    
    response = client.nodes.stats(
      metric: 'ingest',
      filter_path: 'nodes.*.ingest.pipelines'
    )
    puts response
    
    
    GET /_nodes/stats?metric=ingest&filter_path=nodes.*.ingest.pipelines

[« Nodes reload secure settings API](cluster-nodes-reload-secure-
settings.md) [Cluster Info API »](cluster-info.md)
