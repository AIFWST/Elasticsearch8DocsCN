

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Search template API](search-template-api.md) [Render search template API
»](render-search-template-api.md)

## 多搜索模板API

使用单个请求运行多个模板化搜索。

    
    
    response = client.msearch_template(
      index: 'my-index',
      body: [
        {},
        {
          id: 'my-search-template',
          params: {
            query_string: 'hello world',
            from: 0,
            size: 10
          }
        },
        {},
        {
          id: 'my-other-search-template',
          params: {
            query_type: 'match_all'
          }
        }
      ]
    )
    puts response
    
    
    GET my-index/_msearch/template
    { }
    { "id": "my-search-template", "params": { "query_string": "hello world", "from": 0, "size": 10 }}
    { }
    { "id": "my-other-search-template", "params": { "query_type": "match_all" }}

###Request

"获取<target>/_msearch/模板"

"获取_msearch/模板"

"发布<target>/_msearch/模板"

"发布_msearch/模板"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。有关跨集群搜索，请参阅配置具有安全性的远程集群。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to search. Supports wildcards (`*`). To search all data streams and indices, omit this parameter or use `*`. 

### 查询参数

`ccs_minimize_roundtrips`

     (Optional, Boolean) If `true`, network round-trips are minimized for cross-cluster search requests. Defaults to `true`. 
`max_concurrent_searches`

     (Optional, integer) Maximum number of concurrent searches the API can run. Defaults to `max(1, (# of [data nodes](modules-node.html#data-node "Data node") * min([search thread pool size](modules-threadpool.html#search-threadpool), 10)))`. 
`rest_total_hits_as_int`

     (Optional, Boolean) If `true`, the response returns `hits.total` as an integer. If false, it returns `hits.total` as an object. Defaults to `false`. 
`search_type`

    

(可选，字符串)搜索操作的类型。可用选项：

* "query_then_fetch" * "dfs_query_then_fetch"

`typed_keys`

     (Optional, Boolean) If `true`, the response prefixes aggregation and suggester names with their respective types. Defaults to `false`. 

### 请求正文

请求正文必须是以下格式的换行符分隔的 JSON (NDJSON)：

    
    
    <header>\n
    <body>\n
    <header>\n
    <body>\n

每个 '' <header>和 '<body>' 对代表一个搜索请求。

"<header>"支持与多搜索 API 的""相同的参数<header>。"<body>"支持与搜索模板 API 的请求正文相同的参数。

`<header>`

    

(必填，对象)用于限制或更改搜索的参数。

此对象对于每个搜索正文都是必需的，但可以是空 ('{}') 或空行。

"<header>"对象的属性

`allow_no_indices`

    

(可选，布尔值)如果为"true"，则在通配符表达式或"_all"值仅检索缺失或关闭的索引时，请求不会返回错误。

此参数也适用于指向缺失或索引的别名。

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

     (Optional, Boolean) If `true`, documents from missing or closed indices are not included in the response. Defaults to `false`. 
`index`

    

(可选，字符串或字符串数组)要搜索的数据流、索引和别名。支持通配符 ("*")。将多个目标指定为一个数组。

如果未指定此参数，则使用<target>""请求路径参数作为回退。

`preference`

     (Optional, string) Node or shard used to perform the search. Random by default. 
`request_cache`

     (Optional, Boolean) If `true`, the request cache can be used for this search. Defaults to index-level settings. See [Shard request cache settings](shard-request-cache.html "Shard request cache settings"). 
`routing`

     (Optional, string) Custom [routing value](mapping-routing-field.html "_routing field") used to route search operations to a specific shard. 
`search_type`

    

(可选，字符串)指示在对返回的文档进行评分时是否应使用全局术语和文档频率。

选项包括：

`query_then_fetch`

     (default) Documents are scored using local term and document frequencies for the shard. This is usually faster but less accurate. 
`dfs_query_then_fetch`

     Documents are scored using global term and document frequencies across all shards. This is usually slower but more accurate. 

`<body>`

    

(请求、对象)搜索的参数。

`explain`

     (Optional, Boolean) If `true`, returns detailed information about score calculation as part of each hit. Defaults to `false`. 
`id`

     (Required*, string) ID of the search template to use. If no `source` is specified, this parameter is required. 
`params`

     (Optional, object) Key-value pairs used to replace Mustache variables in the template. The key is the variable name. The value is the variable value. 
`profile`

     (Optional, Boolean) If `true`, the query execution is profiled. Defaults to `false`. 
`source`

    

(必填*，对象)内联搜索模板。支持与搜索 API 的请求正文相同的参数。还支持胡子变量。

如果未指定"id"，则此参数是必需的。

### 响应码

仅当请求本身失败时，API 才会返回"400"状态代码。如果请求中的一个或多个搜索失败，API 将返回一个"200"状态代码，其中包含响应中每个失败搜索的"error"对象。

### 响应正文

`responses`

    

(对象数组)每个搜索的结果，按提交的顺序返回。每个对象使用与搜索 API 的响应相同的属性。

如果搜索失败，响应将包含包含错误消息的"错误"对象。

### 卷曲请求

如果向"curl"提供文本文件或文本输入，请使用"--data-binary"标志而不是"-d"来保留换行符。

    
    
    $ cat requests
    { "index": "my-index" }
    { "id": "my-search-template", "params": { "query_string": "hello world", "from": 0, "size": 10 }}
    { "index": "my-other-index" }
    { "id": "my-other-search-template", "params": { "query_type": "match_all" }}
    
    $ curl -H "Content-Type: application/x-ndjson" -XGET localhost:9200/_msearch/template --data-binary "@requests"; echo

[« Search template API](search-template-api.md) [Render search template API
»](render-search-template-api.md)
