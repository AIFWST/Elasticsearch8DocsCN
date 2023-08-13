

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Delete alias API](indices-delete-alias.md) [Delete index template API
»](indices-delete-template.md)

## 删除索引接口

删除一个或多个索引。

    
    
    response = client.indices.delete(
      index: 'my-index-000001'
    )
    puts response
    
    
    DELETE /my-index-000001

###Request

"删除/<index>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标索引具有"delete_index"或"管理"索引权限。

###Description

删除索引会删除其文档、分片和元数据。它不会删除相关的 Kibana 组件，例如数据视图、可视化效果或仪表板。

您无法删除数据流的当前写入索引。要删除索引，必须滚动访问数据流，以便创建新的写入索引。然后，可以使用删除索引 API 删除以前的写入索引。

### 路径参数

`<index>`

    

(必需，字符串)要删除的索引的逗号分隔列表。不能指定索引别名。

默认情况下，此参数不支持通配符 ('*') 或 '_all'。要使用通配符或"_all"，请将"action.destructive_requires_name"群集设置设置为"false"。

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

默认为"打开，关闭"。

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Delete alias API](indices-delete-alias.md) [Delete index template API
»](indices-delete-template.md)
