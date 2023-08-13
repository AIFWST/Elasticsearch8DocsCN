

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Field usage stats API](field-usage-stats.md) [Force merge API »](indices-
forcemerge.md)

## 刷新接口

刷新一个或多个数据流或索引。

    
    
    response = client.indices.flush(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_flush

###Request

"发布/<target>/_flush"

"获取/<target>/_flush"

"发布/_flush"

"获取/_flush"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"维护"或"管理"索引权限。

###Description

刷新数据流或索引是确保当前仅存储在事务日志中的任何数据也永久存储在 Lucene 索引中的过程。重新启动时，Elasticsearch 会将事务日志中任何未刷新的操作重放到 Lucene 索引，以使其恢复到重新启动前的状态。Elasticsearch 根据需要自动触发刷新，使用启发式方法在未刷新的事务日志的大小与执行每次刷新的成本之间进行权衡。

刷新每个操作后，它就会永久存储在 Luceneindex 中。这可能意味着无需在事务日志中维护它的其他副本。事务日志由多个文件组成，称为 _generation_，一旦不再需要任何生成文件，Elasticsearch 就会将其删除，从而释放磁盘空间。

也可以使用 flushAPI 在一个或多个索引上触发刷新，尽管用户很少需要直接调用此 API。如果您在索引某些文档后调用刷新 API，则成功的响应表示 Elasticsearch 已刷新在调用刷新 API 之前已编制索引的所有文档。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to flush. Supports wildcards (`*`). To flush all data streams and indices, omit this parameter or use `*` or `_all`. 

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

`force`

    

(可选，布尔值)如果为"true"，则请求会强制刷新，即使没有要提交到索引的更改。默认为"真"。

可以使用此参数递增事务日志的生成号。

此参数被视为内部参数。

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`wait_if_ongoing`

    

(可选，布尔值)如果为"true"，则刷新操作将阻止，直到在另一个刷新操作正在运行时执行。

如果为"false"，则当您在另一个刷新操作运行时请求刷新时，Elasticsearch 将返回错误。

默认为"真"。

###Examples

#### 刷新特定数据流或索引

    
    
    response = client.indices.flush(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_flush

#### 刷新多个数据流和索引

    
    
    response = client.indices.flush(
      index: 'my-index-000001,my-index-000002'
    )
    puts response
    
    
    POST /my-index-000001,my-index-000002/_flush

#### 刷新集群中的所有数据流和索引

    
    
    response = client.indices.flush
    puts response
    
    
    POST /_flush

[« Field usage stats API](field-usage-stats.md) [Force merge API »](indices-
forcemerge.md)
