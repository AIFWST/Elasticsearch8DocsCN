

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Index APIs](indices.md) [Aliases API »](indices-aliases.md)

## 别名存在API

检查别名是否存在。

    
    
    response = client.indices.exists_alias(
      name: 'my-alias'
    )
    puts response
    
    
    HEAD _alias/my-alias

###Request

"头_alias/<alias>"

"头<target>/_alias/<alias>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须具有别名的"view_index_metadata"或"管理"索引权限。如果指定目标，则还必须具有目标的"view_index_metadata"或"管理"索引权限。

### 路径参数

`<alias>`

     (Optional, string) Comma-separated list of aliases to check. Supports wildcards (`*`). 
`<target>`

     (Optional, string) Comma-separated list of data streams or indices used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

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

默认为"全部"。

`ignore_unavailable`

     (Optional, Boolean) If `false`, requests that include a missing data stream or index in the `<target>` return an error. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 

### 响应码

`200`

     All specified aliases exist. 
`404`

     One or more of the specified aliases don't exist. 

[« Index APIs](indices.md) [Aliases API »](indices-aliases.md)
