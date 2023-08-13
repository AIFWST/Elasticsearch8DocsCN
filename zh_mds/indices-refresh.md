

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Open index API](indices-open-close.md) [Resolve index API »](indices-
resolve-index-api.md)

## 刷新接口

刷新使最近对一个或多个索引执行的操作可供搜索。对于数据流，API 对流的支持索引运行刷新操作。有关刷新操作的详细信息，请参阅_Near实时search_。

    
    
    response = client.indices.refresh(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_refresh

###Request

"发布<target>/_refresh"

"获取<target>/_refresh"

"发布/_refresh"

"获取/_refresh"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"维护"或"管理"索引权限。

###Description

使用刷新 API 显式使自上次刷新以来对一个或多个索引执行的所有操作都可用于搜索。如果请求以数据流为目标，则会刷新流的支持索引。

默认情况下，Elasticsearch 每秒定期刷新索引，但仅限于在过去 30 秒内收到一个或更多搜索请求的索引。您可以使用"index.refresh_interval"设置更改此默认间隔。

刷新请求是同步的，并且在操作完成之前不会返回响应。

刷新会占用大量资源。为了确保良好的集群性能，我们建议等待 Elasticsearch 的定期刷新，而不是在可能的情况下执行显式刷新。

如果应用程序工作流为文档编制索引，然后运行搜索以检索索引文档，我们建议使用索引 API 的"refresh=wait_for"查询参数选项。此选项可确保索引操作在运行搜索之前等待定期刷新。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

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

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 

###Examples

#### 刷新多个数据流和索引

    
    
    response = client.indices.refresh(
      index: 'my-index-000001,my-index-000002'
    )
    puts response
    
    
    POST /my-index-000001,my-index-000002/_refresh

#### 刷新集群中的所有数据流和索引

    
    
    response = client.indices.refresh
    puts response
    
    
    POST /_refresh

[« Open index API](indices-open-close.md) [Resolve index API »](indices-
resolve-index-api.md)
