

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Index shard stores API](indices-shards-stores.md) [Index template exists
API »](indices-template-exists-v1.md)

## 索引统计信息API

返回一个或多个索引的统计信息。对于数据流，API 检索流的支持索引的统计信息。

    
    
    response = client.indices.stats(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_stats

###Request

'获取 /<target>/_stats<index-metric>/'

"获取/<target>/_stats"

"获取/_stats"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"监控"或"管理"索引权限。

###Description

使用索引统计信息 API 获取一个或多个数据流和索引的高级聚合和统计信息。

默认情况下，返回的统计信息是索引级别的，具有"主要"和"总计"聚合。"主分片"仅是主分片的值，"总计"是主分片和副本分片的累积值。

要获取分片级统计信息，请将"level"参数设置为"分片"。

移动到另一个节点时，将清除分片的分片级统计信息。尽管分片不再是节点的一部分，但该节点会保留分片参与的任何节点级统计信息。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 
`<index-metric>`

    

(可选，字符串)用于限制请求的指标的逗号分隔列表。支持的指标包括：

`_all`

     Return all statistics. 
`completion`

     [Completion suggester](search-suggesters.html#completion-suggester "Completion Suggester") statistics. 
`docs`

     Number of documents and deleted docs, which have not yet merged out. [Index refreshes](indices-refresh.html "Refresh API") can affect this statistic. 
`fielddata`

     [Fielddata](text.html#fielddata-mapping-param "fielddata mapping parameter") statistics. 
`flush`

     [Flush](indices-flush.html "Flush API") statistics. 
`get`

     Get statistics, including missing stats. 
`indexing`

     [Indexing](docs-index_.html "Index API") statistics. 
`merge`

     [Merge](index-modules-merge.html "Merge") statistics. 
`query_cache`

     [Query cache](query-cache.html "Node query cache settings") statistics. 
`refresh`

     [Refresh](indices-refresh.html "Refresh API") statistics. 
`request_cache`

     [Shard request cache](shard-request-cache.html "Shard request cache settings") statistics. 
`search`

     Search statistics including suggest statistics. You can include statistics for custom groups by adding an extra `groups` parameter (search operations can be associated with one or more groups). The `groups` parameter accepts a comma separated list of group names. Use `_all` to return statistics for all groups. 
`segments`

    

所有开放段的内存使用。

如果"include_segment_file_sizes"参数为"true"，则此指标包括每个 Lucene 索引文件的聚合磁盘使用情况。

`store`

     Size of the index in [byte units](api-conventions.html#byte-units "Byte size units"). 
`translog`

     [Translog](index-modules-translog.html "Translog") statistics. 

### 查询参数

`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的索引类型。如果请求可以以数据流为目标，则此参数确定通配符表达式是否与隐藏的数据流匹配。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open, non-hidden indices. Also matches any non-hidden data stream. 
`closed`

     Match closed, non-hidden indices. Also matches any non-hidden data stream. Data streams cannot be closed. 
`hidden`

     Match hidden data streams and hidden indices. Must be combined with `open`, `closed`, or both. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

`fields`

    

(可选，字符串)要包含在统计信息中的字段的逗号分隔列表或通配符表达式。

用作默认列表，除非在"completion_fields"或"fielddata_fields"参数中提供了特定的字段列表。

`completion_fields`

     (Optional, string) Comma-separated list or wildcard expressions of fields to include in `fielddata` and `suggest` statistics. 
`fielddata_fields`

     (Optional, string) Comma-separated list or wildcard expressions of fields to include in `fielddata` statistics. 
`forbid_closed_indices`

     (Optional, Boolean) If `true`, statistics are **not** collected from closed indices. Defaults to `true`. 
`groups`

     (Optional, string) Comma-separated list of search groups to include in the `search` statistics. 
`level`

    

(可选，字符串)指示统计信息是在集群、索引还是分片级别聚合。

有效值为：

* "集群" * "索引" * "分片"

`include_segment_file_sizes`

     (Optional, Boolean) If `true`, the call reports the aggregated disk usage of each one of the Lucene index files (only applies if segment stats are requested). Defaults to `false`. 
`include_unloaded_segments`

     (Optional, Boolean) If `true`, the response includes information from segments that are **not** loaded into memory. Defaults to `false`. 

###Examples

#### 获取多个数据流和索引的统计信息

    
    
    response = client.indices.stats(
      index: 'index1,index2'
    )
    puts response
    
    
    GET /index1,index2/_stats

#### 获取集群中所有数据流和索引的统计信息

    
    
    response = client.indices.stats
    puts response
    
    
    GET /_stats

#### 获取特定统计信息

以下请求仅返回所有索引的"合并"和"刷新"统计信息。

    
    
    response = client.indices.stats(
      metric: 'merge,refresh'
    )
    puts response
    
    
    GET /_stats/merge,refresh

#### 获取特定搜索组的统计信息

以下请求仅返回"group1"和"group2"搜索组的搜索统计信息。

    
    
    response = client.indices.stats(
      metric: 'search',
      groups: 'group1,group2'
    )
    puts response
    
    
    GET /_stats/search?groups=group1,group2

[« Index shard stores API](indices-shards-stores.md) [Index template exists
API »](indices-template-exists-v1.md)
