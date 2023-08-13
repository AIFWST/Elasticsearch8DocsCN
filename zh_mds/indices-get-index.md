

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Get field mapping API](indices-get-field-mapping.md) [Get index settings
API »](indices-get-settings.md)

## 获取索引接口

返回有关一个或多个索引的信息。对于数据流，API 返回有关流的支持索引的信息。

    
    
    response = client.indices.get(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001

###Request

'得到/<target>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"view_index_metadata"或"管理"索引权限。

### 路径参数

`<target>`

     (Required, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

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

`features`

     (Optional, string) Return information about specific index features. Supports comma- separated values. Valid values are `aliases`, `mappings`, and `settings`. Defaults to `aliases,mappings,settings`. 
`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`include_defaults`

     (Optional, Boolean) If `true`, return all default settings in the response. Defaults to `false`. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, requests that target a missing index return an error. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Get field mapping API](indices-get-field-mapping.md) [Get index settings
API »](indices-get-settings.md)
