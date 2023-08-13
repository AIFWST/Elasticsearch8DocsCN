

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Cluster state API](cluster-state.md) [Cluster update settings API
»](cluster-update-settings.md)

## 集群统计接口

返回群集统计信息。

###Request

"获取/_cluster/统计数据"

'获取/_cluster/统计/节点/<node_filter>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

集群统计信息 API 允许从集群宽视角检索统计信息。API 返回基本索引指标(分片数量、存储大小、内存使用情况)以及有关构成集群的当前节点的信息(数量、角色、操作系统、jvm 版本、内存使用情况、CPU 和已安装的插件)。

### 路径参数

`<node_filter>`

     (Optional, string) Comma-separated list of [node filters](cluster.html#cluster-nodes "Node specification") used to limit returned information. Defaults to all nodes in the cluster. 

### 查询参数

`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for each node to respond. If a node does not respond before its timeout expires, the response does not include its stats. However, timed out nodes are included in the response's `_nodes.failed` property. Defaults to no timeout. 

### 响应正文

`_nodes`

    

(对象)包含有关请求的节点筛选器选择的节点数的统计信息。

"_nodes"的属性

`total`

     (integer) Total number of nodes selected by the request. 
`successful`

     (integer) Number of nodes that responded successfully to the request. 
`failed`

     (integer) Number of nodes that rejected the request or failed to respond. If this value is not `0`, a reason for the rejection or failure is included in the response. 

`cluster_name`

     (string) Name of the cluster, based on the [Cluster name setting](important-settings.html#cluster-name "Cluster name setting") setting. 
`cluster_uuid`

     (string) Unique identifier for the cluster. 
`timestamp`

     (integer) [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time), in milliseconds, of the last time the cluster statistics were refreshed. 
`status`

    

(字符串)集群的运行状况，基于其主分片和副本分片的状态。状态为：

* "绿色"：分配所有分片。  * 'yellow'：已分配所有主分片，但未分配一个或多个副本分片。如果群集中的某个节点发生故障，则在修复该节点之前，某些数据可能不可用。  * "red"：一个或多个主分片未分配，因此某些数据不可用。在分配主分片时，这可能会在集群启动期间短暂发生。

请参阅群集运行状况。

`indices`

    

(对象)包含有关将分片分配给选定节点的索引的统计信息。

"指数"的属性

`count`

     (integer) Total number of indices with shards assigned to selected nodes. 
`shards`

    

(对象)包含有关分配给所选节点的分片的统计信息。

"分片"的属性

`total`

     (integer) Total number of shards assigned to selected nodes. 
`primaries`

     (integer) Number of primary shards assigned to selected nodes. 
`replication`

     (float) Ratio of replica shards to primary shards across all selected nodes. 
`index`

    

(对象)包含有关分配给所选节点的分片的统计信息。

"索引"的属性

`shards`

    

(对象)包含有关分配给选定节点的分片数量的统计信息。

"分片"的属性

`min`

     (integer) Minimum number of shards in an index, counting only shards assigned to selected nodes. 
`max`

     (integer) Maximum number of shards in an index, counting only shards assigned to selected nodes. 
`avg`

     (float) Mean number of shards in an index, counting only shards assigned to selected nodes. 

`primaries`

    

(对象)包含有关分配给所选节点的主分片数量的统计信息。

"原色"的属性

`min`

     (integer) Minimum number of primary shards in an index, counting only shards assigned to selected nodes. 
`max`

     (integer) Maximum number of primary shards in an index, counting only shards assigned to selected nodes. 
`avg`

     (float) Mean number of primary shards in an index, counting only shards assigned to selected nodes. 

`replication`

    

(对象)包含有关分配给所选节点的复制分片数的统计信息。

"复制"的属性

`min`

     (float) Minimum replication factor in an index, counting only shards assigned to selected nodes. 
`max`

     (float) Maximum replication factor in an index, counting only shards assigned to selected nodes. 
`avg`

     (float) Mean replication factor in an index, counting only shards assigned to selected nodes. 

`docs`

    

(对象)包含选定节点中文档的计数。

"文档"的属性

`count`

    

(整数)分配给所选节点的所有主分片中未删除的文档总数。

此数字基于 Lucene 段中的文档，可能包括嵌套字段中的文档。

`deleted`

    

(整数)分配给选定节点的所有主分片中的已删除文档总数。

此数字基于 Lucene 段中的文档。Elasticsearch 在合并段时回收已删除的 Lucene 文档的磁盘空间。

`store`

    

(对象)包含有关分配给选定节点的分片大小的统计信息。

"商店"的属性

`size`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total size of all shards assigned to selected nodes. 
`size_in_bytes`

     (integer) Total size, in bytes, of all shards assigned to selected nodes. 
`total_data_set_size`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total data set size of all shards assigned to selected nodes. This includes the size of shards not stored fully on the nodes, such as the cache for [partially mounted indices](searchable-snapshots.html#partially-mounted). 
`total_data_set_size_in_bytes`

     (integer) Total data set size, in bytes, of all shards assigned to selected nodes. This includes the size of shards not stored fully on the nodes, such as the cache for [partially mounted indices](searchable-snapshots.html#partially-mounted). 
`reserved`

     ([byte value](api-conventions.html#byte-units "Byte size units")) A prediction of how much larger the shard stores will eventually grow due to ongoing peer recoveries, restoring snapshots, and similar activities. 
`reserved_in_bytes`

     (integer) A prediction, in bytes, of how much larger the shard stores will eventually grow due to ongoing peer recoveries, restoring snapshots, and similar activities. 

`fielddata`

    

(对象)包含有关所选节点的字段数据缓存的统计信息。

"字段数据"的属性

`memory_size`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for the field data cache across all shards assigned to selected nodes. 
`memory_size_in_bytes`

     (integer) Total amount, in bytes, of memory used for the field data cache across all shards assigned to selected nodes. 
`evictions`

     (integer) Total number of evictions from the field data cache across all shards assigned to selected nodes. 
`global_ordinals.build_time`

     ([time unit](api-conventions.html#time-units "Time units")) The total time spent building global ordinals for all fields. 
`global_ordinals.build_time_in_millis`

     (integer) The total time, in milliseconds, spent building global ordinals for all fields. 
`global_ordinals.fields.[field-name].build_time`

     ([time unit](api-conventions.html#time-units "Time units")) The total time spent building global ordinals for field with specified name. 
`global_ordinals.fields.[field-name].build_time_in_millis`

     (integer) The total time, in milliseconds, spent building global ordinals for field with specified name. 
`global_ordinals.fields.[field-name].shard_max_value_count`

     (long) The total time spent building global ordinals for field with specified name. 

`query_cache`

    

(对象)包含有关所选节点的查询缓存的统计信息。

"query_cache"的属性

`memory_size`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for the query cache across all shards assigned to selected nodes. 
`memory_size_in_bytes`

     (integer) Total amount, in bytes, of memory used for the query cache across all shards assigned to selected nodes. 
`total_count`

     (integer) Total count of hits and misses in the query cache across all shards assigned to selected nodes. 
`hit_count`

     (integer) Total count of query cache hits across all shards assigned to selected nodes. 
`miss_count`

     (integer) Total count of query cache misses across all shards assigned to selected nodes. 
`cache_size`

     (integer) Total number of entries currently in the query cache across all shards assigned to selected nodes. 
`cache_count`

     (integer) Total number of entries added to the query cache across all shards assigned to selected nodes. This number includes current and evicted entries. 
`evictions`

     (integer) Total number of query cache evictions across all shards assigned to selected nodes. 

`completion`

    

(对象)包含有关选定节点中用于完成的内存的统计信息。

"完成"的属性

`size`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for completion across all shards assigned to selected nodes. 
`size_in_bytes`

     (integer) Total amount, in bytes, of memory used for completion across all shards assigned to selected nodes. 

`segments`

    

(对象)包含有关选定节点中段的统计信息。

"段"的属性

`count`

     (integer) Total number of segments across all shards assigned to selected nodes. 
`memory`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for segments across all shards assigned to selected nodes. 
`memory_in_bytes`

     (integer) Total amount, in bytes, of memory used for segments across all shards assigned to selected nodes. 
`terms_memory`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for terms across all shards assigned to selected nodes. 
`terms_memory_in_bytes`

     (integer) Total amount, in bytes, of memory used for terms across all shards assigned to selected nodes. 
`stored_fields_memory`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for stored fields across all shards assigned to selected nodes. 
`stored_fields_memory_in_bytes`

     (integer) Total amount, in bytes, of memory used for stored fields across all shards assigned to selected nodes. 
`term_vectors_memory`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for term vectors across all shards assigned to selected nodes. 
`term_vectors_memory_in_bytes`

     (integer) Total amount, in bytes, of memory used for term vectors across all shards assigned to selected nodes. 
`norms_memory`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for normalization factors across all shards assigned to selected nodes. 
`norms_memory_in_bytes`

     (integer) Total amount, in bytes, of memory used for normalization factors across all shards assigned to selected nodes. 
`points_memory`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for points across all shards assigned to selected nodes. 
`points_memory_in_bytes`

     (integer) Total amount, in bytes, of memory used for points across all shards assigned to selected nodes. 
`doc_values_memory`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used for doc values across all shards assigned to selected nodes. 
`doc_values_memory_in_bytes`

     (integer) Total amount, in bytes, of memory used for doc values across all shards assigned to selected nodes. 
`index_writer_memory`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used by all index writers across all shards assigned to selected nodes. 
`index_writer_memory_in_bytes`

     (integer) Total amount, in bytes, of memory used by all index writers across all shards assigned to selected nodes. 
`version_map_memory`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of memory used by all version maps across all shards assigned to selected nodes. 
`version_map_memory_in_bytes`

     (integer) Total amount, in bytes, of memory used by all version maps across all shards assigned to selected nodes. 
`fixed_bit_set`

    

(字节单位)分配给所选节点的所有分片中的固定位集使用的总内存量。

固定位集用于嵌套对象字段类型和联接字段的类型筛选器。

`fixed_bit_set_memory_in_bytes`

     (integer) Total amount of memory, in bytes, used by fixed bit sets across all shards assigned to selected nodes. 
`max_unsafe_auto_id_timestamp`

     (integer) [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time), in milliseconds, of the most recently retried indexing request. 
`file_sizes`

    

(对象)此对象不由群集统计信息 API 填充。

要获取有关分段文件的信息，请使用节点统计信息 API。

`mappings`

    

(对象)包含有关所选节点的字段映射的统计信息。

"映射"的属性

`total_field_count`

     (integer) Total number of fields in all non-system indices. 
`total_deduplicated_field_count`

     (integer) Total number of fields in all non-system indices, accounting for mapping deduplication. 
`total_deduplicated_mapping_size`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total size of all mappings after deduplication and compression. 
`total_deduplicated_mapping_size_in_bytes`

     (integer) Total size of all mappings, in bytes, after deduplication and compression. 
`field_types`

    

(对象数组)包含有关所选节点中使用的字段数据类型的统计信息。

"field_types"对象的属性

`name`

     (string) Field data type used in selected nodes. 
`count`

     (integer) Number of fields mapped to the field data type in selected nodes. 
`index_count`

     (integer) Number of indices containing a mapping of the field data type in selected nodes. 
`indexed_vector_count`

     (integer) For dense_vector field types, number of indexed vector types in selected nodes. 
`indexed_vector_dim_min`

     (integer) For dense_vector field types, the minimum dimension of all indexed vector types in selected nodes. 
`indexed_vector_dim_max`

     (integer) For dense_vector field types, the maximum dimension of all indexed vector types in selected nodes. 
`script_count`

     (integer) Number of fields that declare a script. 
`lang`

     (array of strings) Script languages used for the optional scripts 
`lines_max`

     (integer) Maximum number of lines for a single field script 
`lines_total`

     (integer) Total number of lines for the scripts 
`chars_max`

     (integer) Maximum number of characters for a single field script 
`chars_total`

     (integer) Total number of characters for the scripts 
`source_max`

     (integer) Maximum number of accesses to _source for a single field script 
`source_total`

     (integer) Total number of accesses to _source for the scripts 
`doc_max`

     (integer) Maximum number of accesses to doc_values for a single field script 
`doc_total`

     (integer) Total number of accesses to doc_values for the scripts 

`runtime_field_types`

    

(对象数组)包含有关选定节点中使用的运行时字段数据类型的统计信息。

"runtime_field_types"对象的属性

`name`

     (string) Field data type used in selected nodes. 
`count`

     (integer) Number of runtime fields mapped to the field data type in selected nodes. 
`index_count`

     (integer) Number of indices containing a mapping of the runtime field data type in selected nodes. 
`scriptless_count`

     (integer) Number of runtime fields that don't declare a script. 
`shadowed_count`

     (integer) Number of runtime fields that shadow an indexed field. 
`lang`

     (array of strings) Script languages used for the runtime fields scripts 
`lines_max`

     (integer) Maximum number of lines for a single runtime field script 
`lines_total`

     (integer) Total number of lines for the scripts that define the current runtime field data type 
`chars_max`

     (integer) Maximum number of characters for a single runtime field script 
`chars_total`

     (integer) Total number of characters for the scripts that define the current runtime field data type 
`source_max`

     (integer) Maximum number of accesses to _source for a single runtime field script 
`source_total`

     (integer) Total number of accesses to _source for the scripts that define the current runtime field data type 
`doc_max`

     (integer) Maximum number of accesses to doc_values for a single runtime field script 
`doc_total`

     (integer) Total number of accesses to doc_values for the scripts that define the current runtime field data type 

`analysis`

    

(对象)包含有关选定节点中使用的分析器和分析器组件的统计信息。

"分析"的属性

`char_filter_types`

    

(对象数组)包含有关所选节点中使用的字符筛选器类型的统计信息。

"char_filter_types"对象的属性

`name`

     (string) Character filter type used in selected nodes. 
`count`

     (integer) Number of analyzers or normalizers using the character filter type in selected nodes. 
`index_count`

     (integer) Number of indices the character filter type in selected nodes. 

`tokenizer_types`

    

(对象数组)包含有关所选节点中使用的分词器类型的统计信息。

"tokenizer_types"对象的属性

`name`

     (string) Tokenizer type used in selected nodes. 
`count`

     (integer) Number of analyzers or normalizers using the tokenizer type in selected nodes. 
`index_count`

     (integer) Number of indices using the tokenizer type in selected nodes. 

`filter_types`

    

(对象数组)包含有关所选节点中使用的令牌筛选器类型的统计信息。

"filter_types"对象的属性

`name`

     (string) Token filter type used in selected nodes. 
`count`

     (integer) Number of analyzers or normalizers using the token filter type in selected nodes. 
`index_count`

     (integer) Number of indices using the token filter type in selected nodes. 

`analyzer_types`

    

(对象数组)包含有关所选节点中使用的分析器类型的统计信息。

"analyzer_types"对象的属性

`name`

     (string) Analyzer type used in selected nodes. 
`count`

     (integer) Occurrences of the analyzer type in selected nodes. 
`index_count`

     (integer) Number of indices using the analyzer type in selected nodes. 

`built_in_char_filters`

    

(对象数组)包含有关未选定节点使用的内置字符筛选器的统计信息。

"built_in_char_filters"对象的属性

`name`

     (string) Built-in character filter used in selected nodes. 
`count`

     (integer) Number of analyzers or normalizers using the built-in character filter in selected nodes. 
`index_count`

     (integer) Number of indices using the built-in character filter in selected nodes. 

`built_in_tokenizers`

    

(对象数组)包含有关选定节点中使用的内置分词器的统计信息。

"built_in_tokenizers"对象的属性

`name`

     (string) Built-in tokenizer used in selected nodes. 
`count`

     (integer) Number of analyzers or normalizers using the built-in tokenizer in selected nodes. 
`index_count`

     (integer) Number of indices using the built-in tokenizer in selected nodes. 

`built_in_filters`

    

(对象数组)包含有关选定节点中使用的内置令牌筛选器的统计信息。

"built_in_filters"对象的属性

`name`

     (string) Built-in token filter used in selected nodes. 
`count`

     (integer) Number of analyzers or normalizers using the built-in token filter in selected nodes. 
`index_count`

     (integer) Number of indices using the built-in token filter in selected nodes. 

`built_in_analyzers`

    

(对象数组)包含有关所选节点中使用的内置分析器的统计信息。

"built_in_analyzers"对象的属性

`name`

     (string) Built-in analyzer used in selected nodes. 
`count`

     (integer) Occurrences of the built-in analyzer in selected nodes. 
`index_count`

     (integer) Number of indices using the built-in analyzer in selected nodes. 

`search`

    

(对象)包含有关提交到在搜索执行期间充当协调器的选定节点的搜索请求的使用情况统计信息。搜索请求在成功解析时进行跟踪，无论其结果如何：解析后产生错误的请求会影响使用情况统计信息，以及不访问任何数据的请求。

"搜索"对象的属性

`total`

     (integer) Total number of incoming search requests. Search requests that don't specify a request body are not counted. 
`queries`

     (object) Query types used in selected nodes. For each query, name and number of times it's been used within the `query` or `post_filter` section is reported. Queries are counted once per search request, meaning that if the same query type is used multiple times in the same search request, its counter will be incremented by 1 rather than by the number of times it's been used in that individual search request. 
`sections`

     (object) Search sections used in selected nodes. For each section, name and number of times it's been used is reported. 

`nodes`

    

(对象)包含有关请求的节点筛选器选择的节点的统计信息。

"节点"的属性

`count`

    

(对象)包含由请求的节点筛选器选择的节点的计数。

"计数"的属性

`total`

     (integer) Total number of selected nodes. 
`coordinating_only`

     (integer) Number of selected nodes without a [role](modules-node.html "Node"). These nodes are considered [coordinating only](modules-node.html#coordinating-only-node "Coordinating only node") nodes. 
`<role>`

     (integer) Number of selected nodes with the role. For a list of roles, see [Node](modules-node.html "Node"). 

`versions`

     (array of strings) Array of Elasticsearch versions used on selected nodes. 
`os`

    

(对象)包含有关选定节点使用的操作系统的统计信息。

"os"的属性

`available_processors`

     (integer) Number of processors available to JVM across all selected nodes. 
`allocated_processors`

    

(整数)用于计算所有选定节点的线程池大小的处理器数。

可以使用节点的"处理器"设置设置此数字，默认为操作系统报告的处理器数量。在这两种情况下，此数字都不会大于"32"。

`names`

    

(对象数组)包含有关所选节点使用的操作系统的统计信息。

"名称"的属性

`name`

     (string) Name of an operating system used by one or more selected nodes. 
`count`

     (string) Number of selected nodes using the operating system. 

`pretty_names`

    

(对象数组)包含有关所选节点使用的操作系统的统计信息。

"pretty_names"的属性

`pretty_name`

     (string) Human-readable name of an operating system used by one or more selected nodes. 
`count`

     (string) Number of selected nodes using the operating system. 

`architectures`

    

(对象数组)包含有关所选节点使用的处理器体系结构(例如，x86_64 或 aarch64)的统计信息。

"架构"的属性

`arch`

     (string) Name of an architecture used by one or more selected nodes. 
`count`

     (string) Number of selected nodes using the architecture. 

`mem`

    

(对象)包含有关所选节点使用的内存的统计信息。

"mem"的属性

`total`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total amount of physical memory across all selected nodes. 
`total_in_bytes`

     (integer) Total amount, in bytes, of physical memory across all selected nodes. 
`adjusted_total`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of memory across all selected nodes, but using the value specified using the `es.total_memory_bytes` system property instead of measured total memory for those nodes where that system property was set. 
`adjusted_total_in_bytes`

     (integer) Total amount, in bytes, of memory across all selected nodes, but using the value specified using the `es.total_memory_bytes` system property instead of measured total memory for those nodes where that system property was set. 
`free`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Amount of free physical memory across all selected nodes. 
`free_in_bytes`

     (integer) Amount, in bytes, of free physical memory across all selected nodes. 
`used`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Amount of physical memory in use across all selected nodes. 
`used_in_bytes`

     (integer) Amount, in bytes, of physical memory in use across all selected nodes. 
`free_percent`

     (integer) Percentage of free physical memory across all selected nodes. 
`used_percent`

     (integer) Percentage of physical memory in use across all selected nodes. 

`process`

    

(对象)包含有关所选节点使用的进程的统计信息。

"过程"的属性

`cpu`

    

(对象)包含有关所选节点使用的 CPU 的统计信息。

"中央处理器"的属性

`percent`

     (integer) Percentage of CPU used across all selected nodes. Returns `-1` if not supported. 

`open_file_descriptors`

    

(对象)包含有关选定节点中打开的文件描述符的统计信息。

"open_file_descriptors"的属性

`min`

     (integer) Minimum number of concurrently open file descriptors across all selected nodes. Returns `-1` if not supported. 
`max`

     (integer) Maximum number of concurrently open file descriptors allowed across all selected nodes. Returns `-1` if not supported. 
`avg`

     (integer) Average number of concurrently open file descriptors. Returns `-1` if not supported. 

`jvm`

    

(对象)包含有关选定节点使用的 Java 虚拟机 (JVM) 的统计信息。

"jvm"的属性

`max_uptime`

     ([time unit](api-conventions.html#time-units "Time units")) Uptime duration since JVM last started. 
`max_uptime_in_millis`

     (integer) Uptime duration, in milliseconds, since JVM last started. 
`versions`

    

(对象数组)包含有关选定节点使用的 JVM 版本的统计信息。

"版本"的属性

`version`

     (string) Version of JVM used by one or more selected nodes. 
`vm_name`

     (string) Name of the JVM. 
`vm_version`

    

(字符串)JVM 的完整版本号。

完整版本号包括一个加号 ('+')，后跟内部版本号。

`vm_vendor`

     (string) Vendor of the JVM. 
`bundled_jdk`

     (Boolean) Always `true`. All distributions come with a bundled Java Development Kit (JDK). 
`using_bundled_jdk`

     (Boolean) If `true`, a bundled JDK is in use by JVM. 
`count`

     (integer) Total number of selected nodes using JVM. 

`mem`

    

(对象)包含有关所选节点使用的内存的统计信息。

"mem"的属性

`heap_used`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Memory currently in use by the heap across all selected nodes. 
`heap_used_in_bytes`

     (integer) Memory, in bytes, currently in use by the heap across all selected nodes. 
`heap_max`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Maximum amount of memory, in bytes, available for use by the heap across all selected nodes. 
`heap_max_in_bytes`

     (integer) Maximum amount of memory, in bytes, available for use by the heap across all selected nodes. 

`threads`

     (integer) Number of active threads in use by JVM across all selected nodes. 

`fs`

    

(对象)包含有关选定节点的文件存储的统计信息。

"fs"的属性

`total`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Total size of all file stores across all selected nodes. 
`total_in_bytes`

     (integer) Total size, in bytes, of all file stores across all selected nodes. 
`free`

     ([byte units](api-conventions.html#byte-units "Byte size units")) Amount of unallocated disk space in file stores across all selected nodes. 
`free_in_bytes`

     (integer) Total number of unallocated bytes in file stores across all selected nodes. 
`available`

    

(字节单位)跨所有选定节点的文件存储中 JVM 可用的磁盘空间总量。

根据操作系统或进程级别的限制，此数量可能小于"nodes.fs.free"。这是所选 Elasticsearch 节点可以使用的实际可用磁盘空间量。

`available_in_bytes`

    

(整数)跨所有选定节点的文件存储中可供 JVM 使用的总字节数。

根据操作系统或进程级别的限制，此数字可能小于"nodes.fs.free_in_byes"。这是所选 Elasticsearch 节点可以使用的实际可用磁盘空间量。

`plugins`

    

(对象数组)包含有关所选节点安装的插件和模块的统计信息。

如果未安装插件或模块，则此数组为空。

"插件"的属性

`<plugin>`

    

(对象)包含有关已安装插件或模块的统计信息。

""的属性<plugin>

`name`

     (string) Name of the Elasticsearch plugin. 
`version`

     (string) Elasticsearch version for which the plugin was built. 
`elasticsearch_version`

     (string) Elasticsearch version for which the plugin was built. 
`java_version`

     (string) Java version for which the plugin was built. 
`description`

     (string) Short description of the plugin. 
`classname`

     (string) Class name used as the plugin's entry point. 
`extended_plugins`

    

(字符串数组)此插件通过 Java 服务提供程序接口 (SPI) 扩展的一系列其他插件。

如果此插件未扩展其他插件，则此数组为空。

`has_native_controller`

     (Boolean) If `true`, the plugin has a native controller process. 

`network_types`

    

(对象)包含有关所选节点使用的传输和 HTTP 网络的统计信息。

"network_types"的属性

`transport_types`

    

(对象)包含有关所选节点使用的传输网络类型的统计信息。

"transport_types"的属性

`<transport_type>`

     (integer) Number of selected nodes using the transport type. 

`http_types`

    

(对象)包含有关选定节点使用的 HTTP 网络类型的统计信息。

"http_types"的属性

`<http_type>`

     (integer) Number of selected nodes using the HTTP type. 

`discovery_types`

    

(对象)包含有关所选节点使用的发现类型的统计信息。

"discovery_types"的属性

`<discovery_type>`

     (integer) Number of selected nodes using the [discovery type](discovery-hosts-providers.html "Discovery") to find other nodes. 

`packaging_types`

    

(对象数组)包含有关安装在选定节点上的 Elasticsearch 发行版的统计信息。

"packaging_types"的属性

`flavor`

     (string) Type of Elasticsearch distribution. This is always `default`. 
`type`

     (string) File type, such as `tar` or `zip`, used for the distribution package. 
`count`

     (integer) Number of selected nodes using the distribution flavor and file type. 

`snapshots`

    

(对象)包含有关群集中快照活动的统计信息。

"快照"的属性

`current_counts`

    

(对象)包含报告群集中各种正在进行的快照活动数量的统计信息。

"current_counts"的属性

`snapshots`

     (integer) The total number of snapshots and clones currently being created by the cluster. 
`shard_snapshots`

     (integer) The total number of outstanding shard snapshots in the cluster. 
`snapshot_deletions`

     (integer) The total number of snapshot deletion operations that the cluster is currently running. 
`concurrent_operations`

     (integer) The total number of snapshot operations that the cluster is currently running concurrently. This is the total of the `snapshots` and `snapshot_deletions` entries, and is limited by [the `snapshot.max_concurrent_operations` setting](snapshot-settings.html#snapshot-max-concurrent-ops). 
`cleanups`

     (integer) The total number of repository cleanup operations that the cluster is currently running. These operations do not count towards the total number of concurrent operations. 

`repositories`

    

(对象)包含报告快照活动进度的统计信息，这些活动按存储库细分。此对象包含每个存储库在群集中注册的一个条目。

"存储库"的属性

`current_counts`

    

(对象)包含报告此存储库的各种正在进行的快照活动数量的统计信息。

"current_counts"的属性

`snapshots`

     (integer) The total number of ongoing snapshots in this repository. 
`clones`

     (integer) The total number of ongoing snapshot clones in this repository. 
`finalizations`

     (integer) The total number of this repository's ongoing snapshots and clone operations which are mostly complete except for their last "finalization" step. 
`deletions`

     (integer) The total number of ongoing snapshot deletion operations in this repository. 
`snapshot_deletions`

     (integer) The total number of snapshots that are currently being deleted from this repository. 
`active_deletions`

     (integer) The total number of ongoing snapshot deletion operations which are currently active in this repository. Snapshot deletions do not run concurrently with other snapshot operations, so this may be `0` if any pending deletes are waiting for other operations to finish. 
`shards`

    

(对象)包含报告存储库正在进行的快照活动的分片级进度的统计信息。请注意，这些统计信息仅与正在进行的快照相关。

"分片"的属性

`total`

     (integer) The total number of shard snapshots currently tracked by this repository. This statistic only counts shards in ongoing snapshots, so it will drop when a snapshot completes and will be `0` if there are no ongoing snapshots. 
`complete`

     (integer) The total number of tracked shard snapshots which have completed in this repository. This statistic only counts shards in ongoing snapshots, so it will drop when a snapshot completes and will be `0` if there are no ongoing snapshots. 
`incomplete`

     (integer) The total number of tracked shard snapshots which have not completed in this repository. This is the difference between the `total` and `complete` values. 
`states`

     (object) The total number of shard snapshots in each of the named states in this repository. These states are an implementation detail of the snapshotting process which may change between versions. They are included here for expert users, but should otherwise be ignored. 

`oldest_start_time`

     (string) The start time of the oldest running snapshot in this repository. 
`oldest_start_time_in_millis`

     (integer) The start time of the oldest running snapshot in this repository, represented as milliseconds since the Unix epoch. 

###Examples

    
    
    response = client.cluster.stats(
      human: true,
      pretty: true
    )
    puts response
    
    
    GET /_cluster/stats?human&pretty

API 返回以下响应：

    
    
    {
       "_nodes" : {
          "total" : 1,
          "successful" : 1,
          "failed" : 0
       },
       "cluster_uuid": "YjAvIhsCQ9CbjWZb2qJw3Q",
       "cluster_name": "elasticsearch",
       "timestamp": 1459427693515,
       "status": "green",
       "indices": {
          "count": 1,
          "shards": {
             "total": 5,
             "primaries": 5,
             "replication": 0,
             "index": {
                "shards": {
                   "min": 5,
                   "max": 5,
                   "avg": 5
                },
                "primaries": {
                   "min": 5,
                   "max": 5,
                   "avg": 5
                },
                "replication": {
                   "min": 0,
                   "max": 0,
                   "avg": 0
                }
             }
          },
          "docs": {
             "count": 10,
             "deleted": 0
          },
          "store": {
             "size": "16.2kb",
             "size_in_bytes": 16684,
             "total_data_set_size": "16.2kb",
             "total_data_set_size_in_bytes": 16684,
             "reserved": "0b",
             "reserved_in_bytes": 0
          },
          "search": {
              ...
          },
          "fielddata": {
             "memory_size": "0b",
             "memory_size_in_bytes": 0,
             "evictions": 0,
             "global_ordinals": {
                "build_time" : "0s",
                "build_time_in_millis" : 0
             }
          },
          "query_cache": {
             "memory_size": "0b",
             "memory_size_in_bytes": 0,
             "total_count": 0,
             "hit_count": 0,
             "miss_count": 0,
             "cache_size": 0,
             "cache_count": 0,
             "evictions": 0
          },
          "completion": {
             "size": "0b",
             "size_in_bytes": 0
          },
          "segments": {
             "count": 4,
             "memory": "8.6kb",
             "memory_in_bytes": 0,
             "terms_memory": "0b",
             "terms_memory_in_bytes": 0,
             "stored_fields_memory": "0b",
             "stored_fields_memory_in_bytes": 0,
             "term_vectors_memory": "0b",
             "term_vectors_memory_in_bytes": 0,
             "norms_memory": "0b",
             "norms_memory_in_bytes": 0,
             "points_memory" : "0b",
             "points_memory_in_bytes" : 0,
             "doc_values_memory": "0b",
             "doc_values_memory_in_bytes": 0,
             "index_writer_memory": "0b",
             "index_writer_memory_in_bytes": 0,
             "version_map_memory": "0b",
             "version_map_memory_in_bytes": 0,
             "fixed_bit_set": "0b",
             "fixed_bit_set_memory_in_bytes": 0,
             "max_unsafe_auto_id_timestamp" : -9223372036854775808,
             "file_sizes": {}
          },
          "mappings": {
            "total_field_count": 0,
            "total_deduplicated_field_count": 0,
            "total_deduplicated_mapping_size": "0b",
            "total_deduplicated_mapping_size_in_bytes": 0,
            "field_types": [],
            "runtime_field_types": []
          },
          "analysis": {
            "char_filter_types": [],
            "tokenizer_types": [],
            "filter_types": [],
            "analyzer_types": [],
            "built_in_char_filters": [],
            "built_in_tokenizers": [],
            "built_in_filters": [],
            "built_in_analyzers": []
          },
          "versions": [
            {
              "version": "8.0.0",
              "index_count": 1,
              "primary_shard_count": 1,
              "total_primary_size": "7.4kb",
              "total_primary_bytes": 7632
            }
          ]
       },
       "nodes": {
          "count": {
             "total": 1,
             "data": 1,
             "coordinating_only": 0,
             "master": 1,
             "ingest": 1,
             "voting_only": 0
          },
          "versions": [
             "8.9.0"
          ],
          "os": {
             "available_processors": 8,
             "allocated_processors": 8,
             "names": [
                {
                   "name": "Mac OS X",
                   "count": 1
                }
             ],
             "pretty_names": [
                {
                   "pretty_name": "Mac OS X",
                   "count": 1
                }
             ],
             "architectures": [
                {
                   "arch": "x86_64",
                   "count": 1
                }
             ],
             "mem" : {
                "total" : "16gb",
                "total_in_bytes" : 17179869184,
                "adjusted_total" : "16gb",
                "adjusted_total_in_bytes" : 17179869184,
                "free" : "78.1mb",
                "free_in_bytes" : 81960960,
                "used" : "15.9gb",
                "used_in_bytes" : 17097908224,
                "free_percent" : 0,
                "used_percent" : 100
             }
          },
          "process": {
             "cpu": {
                "percent": 9
             },
             "open_file_descriptors": {
                "min": 268,
                "max": 268,
                "avg": 268
             }
          },
          "jvm": {
             "max_uptime": "13.7s",
             "max_uptime_in_millis": 13737,
             "versions": [
                {
                   "version": "12",
                   "vm_name": "OpenJDK 64-Bit Server VM",
                   "vm_version": "12+33",
                   "vm_vendor": "Oracle Corporation",
                   "bundled_jdk": true,
                   "using_bundled_jdk": true,
                   "count": 1
                }
             ],
             "mem": {
                "heap_used": "57.5mb",
                "heap_used_in_bytes": 60312664,
                "heap_max": "989.8mb",
                "heap_max_in_bytes": 1037959168
             },
             "threads": 90
          },
          "fs": {
             "total": "200.6gb",
             "total_in_bytes": 215429193728,
             "free": "32.6gb",
             "free_in_bytes": 35064553472,
             "available": "32.4gb",
             "available_in_bytes": 34802409472
          },
          "plugins": [
            {
              "name": "analysis-icu",
              "version": "8.9.0",
              "description": "The ICU Analysis plugin integrates Lucene ICU module into elasticsearch, adding ICU relates analysis components.",
              "classname": "org.elasticsearch.plugin.analysis.icu.AnalysisICUPlugin",
              "has_native_controller": false
            },
            ...
          ],
          "ingest": {
            "number_of_pipelines" : 1,
            "processor_stats": {
              ...
            }
          },
          "indexing_pressure": {
            "memory": {
                "current": {
                     "combined_coordinating_and_primary": "0b",
                     "combined_coordinating_and_primary_in_bytes": 0,
                     "coordinating": "0b",
                     "coordinating_in_bytes": 0,
                     "primary": "0b",
                     "primary_in_bytes": 0,
                     "replica": "0b",
                     "replica_in_bytes": 0,
                     "all": "0b",
                     "all_in_bytes": 0
                },
                "total": {
                    "combined_coordinating_and_primary": "0b",
                    "combined_coordinating_and_primary_in_bytes": 0,
                    "coordinating": "0b",
                    "coordinating_in_bytes": 0,
                    "primary": "0b",
                    "primary_in_bytes": 0,
                    "replica": "0b",
                    "replica_in_bytes": 0,
                    "all": "0b",
                    "all_in_bytes": 0,
                    "coordinating_rejections": 0,
                    "primary_rejections": 0,
                    "replica_rejections": 0
                },
                "limit" : "0b",
                "limit_in_bytes": 0
            }
          },
          "network_types": {
            ...
          },
          "discovery_types": {
            ...
          },
          "packaging_types": [
            {
              ...
            }
          ]
       },
       "snapshots": {
         ...
       }
    }

可以使用节点筛选器将此 API 限制为节点的子集：

    
    
    response = client.cluster.stats(
      node_id: 'node1,node*,master:false'
    )
    puts response
    
    
    GET /_cluster/stats/nodes/node1,node*,master:false

[« Cluster state API](cluster-state.md) [Cluster update settings API
»](cluster-update-settings.md)
