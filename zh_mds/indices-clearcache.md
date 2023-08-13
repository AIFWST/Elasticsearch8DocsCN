

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Analyze index disk usage API](indices-disk-usage.md) [Clone index API
»](indices-clone-index.md)

## 清除缓存接口

清除一个或多个索引的缓存。对于数据流，API 会清除流的支持索引的缓存。

    
    
    response = client.indices.clear_cache(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_cache/clear

###Request

"发布/<target>/_cache/清除"

"发布/_cache/清除"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"管理"索引权限。

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

`fielddata`

    

(可选，布尔值)如果为"true"，则清除字段缓存。

使用"字段"参数仅清除特定字段的缓存。

`fields`

    

(可选，字符串)用于限制"字段数据"参数的字段名称的逗号分隔列表。

默认为所有字段。

此参数不支持对象或字段别名。

`index`

     (Optional, string) Comma-separated list of index names used to limit the request. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`query`

     (Optional, Boolean) If `true`, clears the query cache. 
`request`

     (Optional, Boolean) If `true`, clears the request cache. 

###Examples

#### 清除特定缓存

默认情况下，清除缓存 API 会清除所有缓存。通过将以下查询参数设置为"true"，只能清除特定缓存：

* "字段数据" * "查询" * "请求"

    
    
    response = client.indices.clear_cache(
      index: 'my-index-000001',
      fielddata: true
    )
    puts response
    
    response = client.indices.clear_cache(
      index: 'my-index-000001',
      query: true
    )
    puts response
    
    response = client.indices.clear_cache(
      index: 'my-index-000001',
      request: true
    )
    puts response
    
    
    POST /my-index-000001/_cache/clear?fielddata=true  __POST /my-index-000001/_cache/clear?query=true __POST /my-index-000001/_cache/clear?request=true __

__

|

仅清除字段缓存 ---|--- __

|

仅清除查询缓存 __

|

仅清除请求缓存 #### 清除特定字段的缓存编辑

要仅清除特定字段的缓存，请使用"字段"查询参数。

    
    
    response = client.indices.clear_cache(
      index: 'my-index-000001',
      fields: 'foo,bar'
    )
    puts response
    
    
    POST /my-index-000001/_cache/clear?fields=foo,bar   __

__

|

清除"foo"和"bar"字段的缓存 ---|--- #### 清除多个数据流和索引编辑的缓存

    
    
    response = client.indices.clear_cache(
      index: 'my-index-000001,my-index-000002'
    )
    puts response
    
    
    POST /my-index-000001,my-index-000002/_cache/clear

#### 清除所有数据流和索引的缓存

    
    
    response = client.indices.clear_cache
    puts response
    
    
    POST /_cache/clear

[« Analyze index disk usage API](indices-disk-usage.md) [Clone index API
»](indices-clone-index.md)
