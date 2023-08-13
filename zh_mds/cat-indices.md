

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat health API](cat-health.md) [cat master API »](cat-master.md)

## 猫指数API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取索引 API。

返回有关群集中索引的高级信息，包括数据流的支持索引。

###Request

'获取/_cat/索引/<target>'

'获取/_cat/索引'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。您还必须对检索到的任何数据流、索引或别名具有"监视"或"管理"索引权限。

###Description

使用 cat 索引 API 获取集群中每个索引的以下信息：

* 分片计数 * 文档计数 * 已删除文档计数 * 主存储大小 * 所有分片(包括分片副本)的总存储大小

这些指标直接从Lucene检索，Elasticsearch在内部使用它来支持索引和搜索。因此，所有文档计数都包括隐藏嵌套的文档。

要获得 Elasticsearch 文档的准确计数，请使用 cat count 或 count API。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`bytes`

     (Optional, [byte size units](api-conventions.html#byte-units "Byte size units")) Unit used to display byte values. 
`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`health`

    

(可选，字符串)用于限制返回索引的运行状况。有效值为：

* "绿色" * "黄色" * "红色"

默认情况下，响应包括任何运行状况的索引。

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`include_unloaded_segments`

     (Optional, Boolean) If `true`, the response includes information from segments that are **not** loaded into memory. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

"pri"(主分片)

     (Optional, Boolean) If `true`, the response only includes information from primary shards. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 
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

###Examples

    
    
    response = client.cat.indices(
      index: 'my-index-*',
      v: true,
      s: 'index'
    )
    puts response
    
    
    GET /_cat/indices/my-index-*?v=true&s=index

API 返回以下响应：

    
    
    health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    yellow open   my-index-000001  u8FNjxh8Rfy_awN11oDKYQ   1   1       1200            0     88.1kb         88.1kb
    green  open   my-index-000002  nYFWZEO7TUiOjLQXBaYJpA   1   0          0            0       260b           260b

[« cat health API](cat-health.md) [cat master API »](cat-master.md)
