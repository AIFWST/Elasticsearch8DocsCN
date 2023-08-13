

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Clear scroll API](clear-scroll-api.md) [Multi search template API
»](multi-search-template.md)

## 搜索模板接口

使用搜索模板运行搜索。

    
    
    response = client.search_template(
      index: 'my-index',
      body: {
        id: 'my-search-template',
        params: {
          query_string: 'hello world',
          from: 0,
          size: 10
        }
      }
    )
    puts response
    
    
    GET my-index/_search/template
    {
      "id": "my-search-template",
      "params": {
        "query_string": "hello world",
        "from": 0,
        "size": 10
      }
    }

###Request

"获取<target>/_search/模板"

"获取_search/模板"

"发布<target>/_search/模板"

"发布_search/模板"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。有关跨集群搜索，请参阅配置具有安全性的远程集群。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to search. Supports wildcards (`*`). To search all data streams and indices, omit this parameter or use `*`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

`ccs_minimize_roundtrips`

     (Optional, Boolean) If `true`, network round-trips are minimized for cross-cluster search requests. Defaults to `true`. 
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

`explain`

     (Optional, Boolean) If `true`, the response includes additional details about score computation as part of a hit. Defaults to `false`. 
`ignore_throttled`

     (Optional, Boolean) If `true`, specified concrete, expanded, or aliased indices are not included in the response when throttled. Defaults to `true`. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`preference`

     (Optional, string) Specifies the node or shard the operation should be performed on. Random by default. 
`rest_total_hits_as_int`

     (Optional, Boolean) If `true`, the response returns `hits.total` as an integer. If false, it returns `hits.total` as an object. Defaults to `false`. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`scroll`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies how long a consistent view of the index should be maintained for scrolled search. 
`search_type`

    

(可选，字符串)搜索操作的类型。可用选项：

* "query_then_fetch" * "dfs_query_then_fetch"

`typed_keys`

     (Optional, Boolean) If `true`, the response prefixes aggregation and suggester names with their respective types. Defaults to `false`. 

### 请求正文

`explain`

    

(可选，布尔值)如果为"true"，则返回有关分数计算的详细信息，作为每次命中的一部分。默认为"假"。

如果同时指定此参数和"解释"查询参数，则 API 仅使用查询参数。

`id`

     (Required*, string) ID of the search template to use. If no `source` is specified, this parameter is required. 
`params`

     (Optional, object) Key-value pairs used to replace Mustache variables in the template. The key is the variable name. The value is the variable value. 
`profile`

     (Optional, Boolean) If `true`, the query execution is profiled. Defaults to `false`. 
`source`

    

(必填*，对象)内联搜索模板。支持与搜索 API 的请求正文相同的参数。还支持胡子变量。

如果未指定"id"，则此参数是必需的。

[« Clear scroll API](clear-scroll-api.md) [Multi search template API
»](multi-search-template.md)
