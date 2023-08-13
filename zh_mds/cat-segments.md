

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat repositories API](cat-repositories.md) [cat shards API »](cat-
shards.md)

## 猫段API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用索引段 API。

返回有关索引分片中 Lucene 段的低级别信息，类似于索引段 API。

对于数据流，API 返回有关流的支持索引的信息。

###Request

'获取/_cat/段/<target>"

"获取/_cat/段"

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
`ip`

     (Default) IP address of the segment's shard, such as `127.0.1.1`. 
`segment`

     (Default) Name of the segment, such as `_0`. The segment name is derived from the segment generation and used internally to create file names in the directory of the shard. 
`generation`

     (Default) Generation number, such as `0`. Elasticsearch increments this generation number for each segment written. Elasticsearch then uses this number to derive the segment name. 
`docs.count`

     (Default) The number of documents as reported by Lucene. This excludes deleted documents and counts any [nested documents](nested.html "Nested field type") separately from their parents. It also excludes documents which were indexed recently and do not yet belong to a segment. 
`docs.deleted`

     (Default) The number of deleted documents as reported by Lucene, which may be higher or lower than the number of delete operations you have performed. This number excludes deletes that were performed recently and do not yet belong to a segment. Deleted documents are cleaned up by the [automatic merge process](index-modules-merge.html "Merge") if it makes sense to do so. Also, Elasticsearch creates extra deleted documents to internally track the recent history of operations on a shard. 
`size`

     (Default) Disk space used by the segment, such as `50kb`. 
`size.memory`

    

(默认)存储在内存中的段数据字节，用于高效搜索，例如"1264"。

值"-1"表示 Elasticsearch 无法计算此数字。

`committed`

    

(默认)如果为"true"，则段将同步到磁盘。同步的分段可以在硬重启后幸存下来。

如果为"false"，则来自未提交段的数据也存储在事务日志中，以便 Elasticsearch 能够在下一次启动时重放更改。

`searchable`

    

(默认)如果为"true"，则细分受众群是可搜索的。

如果为"false"，则段很可能已写入磁盘，但需要刷新才能搜索。

`version`

     (Default) Version of Lucene used to write the segment. 
`compound`

     (Default) If `true`, the segment is stored in a compound file. This means Lucene merged all files from the segment in a single file to save file descriptors. 
`id`

     ID of the node, such as `k0zy`. 

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    response = client.cat.segments(
      v: true
    )
    puts response
    
    
    GET /_cat/segments?v=true

API 返回以下响应：

    
    
    index shard prirep ip        segment generation docs.count docs.deleted size size.memory committed searchable version compound
    test  0     p      127.0.0.1 _0               0          1            0  3kb           0 false     true       9.7.0   true
    test1 0     p      127.0.0.1 _0               0          1            0  3kb           0 false     true       9.7.0   true

[« cat repositories API](cat-repositories.md) [cat shards API »](cat-
shards.md)
