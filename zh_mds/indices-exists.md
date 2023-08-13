

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Delete index template API](indices-delete-template-v1.md) [Field usage
stats API »](field-usage-stats.md)

## 存在API

检查数据流、索引或别名是否存在。

    
    
    response = client.indices.exists(
      index: 'my-data-stream'
    )
    puts response
    
    
    HEAD my-data-stream

###Request

"头<target>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有目标的"view_index_metadata"或"管理"索引权限。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases. Supports wildcards (`*`). 

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

`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`include_defaults`

     (Optional, Boolean) If `true`, return all default settings in the response. Defaults to `false`. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 

### 响应码

`200`

     All targets exist. 
`404`

     One or more specified targets do not exist. 

[« Delete index template API](indices-delete-template-v1.md) [Field usage
stats API »](field-usage-stats.md)
