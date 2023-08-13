

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« Compact and aligned text (CAT) APIs](cat.md) [cat allocation API »](cat-
allocation.md)

## 猫别名API

cat API 仅供人类使用命令行或 Kibana 控制台使用。它们_不是_供应用程序使用。对于应用程序使用，请使用别名 API。

检索群集的索引别名，包括筛选器和路由信息。API 不返回数据流别名。

###Request

"获取_cat/别名/<alias>"

"获取_cat/别名"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对检索到的任何别名具有"view_index_metadata"或"管理"索引权限。

### 路径参数

`<alias>`

     (Optional, string) Comma-separated list of aliases to retrieve. Supports wildcards (`*`). To retrieve all aliases, omit this parameter or use `*` or `_all`. 

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
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

    
    
    response = client.cat.aliases(
      v: true
    )
    puts response
    
    
    GET _cat/aliases?v=true

API 返回以下响应：

    
    
    alias  index filter routing.index routing.search is_write_index
    alias1 test1 -      -            -              -
    alias2 test1 *      -            -              -
    alias3 test1 -      1            1              -
    alias4 test1 -      2            1,2            -

此响应显示"alias2"已配置过滤器，并在"alias3"和"alias4"中配置了特定的路由配置。

如果您只想获取有关特定别名的信息，则可以将逗号分隔格式的别名指定为 URL 参数，例如，/_cat/aliases/alias1，alias2。

[« Compact and aligned text (CAT) APIs](cat.md) [cat allocation API »](cat-
allocation.md)
