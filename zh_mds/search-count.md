

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Multi search API](search-multi-search.md) [Validate API »](search-
validate.md)

## 计数接口

获取搜索查询的匹配项数。

    
    
    response = client.count(
      index: 'my-index-000001',
      q: 'user:kimchy'
    )
    puts response
    
    
    GET /my-index-000001/_count?q=user:kimchy

在正文中发送的查询必须嵌套在"查询"键中，与搜索 API 的工作方式相同。

###Request

"获取/<target>/_count"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。

###Description

计数 API 允许您执行查询并获取该查询的匹配项数。可以使用简单查询字符串作为参数来提供查询，也可以使用请求正文中定义的查询 DSL 来提供查询。

计数 API 支持多目标语法。您可以跨多个数据流和索引运行单个计数 API 搜索。

该操作跨所有分片广播。对于每个分片 id 组，将针对它选择并执行副本。这意味着副本提高了计数的可伸缩性。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to search. Supports wildcards (`*`). To search all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

`analyzer`

    

(可选，字符串)用于查询字符串的分析器。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`analyze_wildcard`

    

(可选，布尔值)如果为"true"，则分析通配符和前缀查询。默认为"假"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`default_operator`

    

(可选，字符串)查询字符串查询的默认运算符：AND 或 OR。默认为"或"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`df`

    

(可选，字符串)用作默认值的字段，其中查询字符串中未提供字段前缀。

仅当指定了"q"查询字符串参数时，才能使用此参数。

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

`ignore_throttled`

     (Optional, Boolean) If `true`, concrete, expanded or aliased indices are ignored when frozen. Defaults to `true`. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`lenient`

    

(可选，布尔值)如果为"true"，则将忽略查询字符串中基于格式的查询失败(例如向数值字段提供文本)。默认为"假"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`min_score`

     (Optional, float) Sets the minimum `_score` value that documents must have to be included in the result. 
`preference`

     (Optional, string) Specifies the node or shard the operation should be performed on. Random by default. 
`q`

     (Optional, string) Query in the Lucene query string syntax. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`terminate_after`

    

(可选，整数)每个分片要收集的最大文档数。如果查询达到此限制，Elasticsearch 会提前终止查询。Elasticsearch 在排序之前收集文档。

请谨慎使用。Elasticsearch 将此参数应用于处理请求的每个分片。如果可能，让 Elasticsearch 自动执行提前终止。避免为跨多个数据层使用支持索引的数据流为目标的请求指定此参数。

### 请求正文

`query`

     (Optional, [query object](query-dsl.html "Query DSL")) Defines the search definition using the [Query DSL](query-dsl.html "Query DSL"). 

###Examples

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        "user.id": 'kimchy'
      }
    )
    puts response
    
    response = client.count(
      index: 'my-index-000001',
      q: 'user:kimchy'
    )
    puts response
    
    response = client.count(
      index: 'my-index-000001',
      body: {
        query: {
          term: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_doc/1?refresh
    {
      "user.id": "kimchy"
    }
    
    GET /my-index-000001/_count?q=user:kimchy
    
    GET /my-index-000001/_count
    {
      "query" : {
        "term" : { "user.id" : "kimchy" }
      }
    }

上面的两个示例都做同样的事情：计算"my-index-000001"中"user.id"为"kimchy"的文档数量。API 返回以下响应：

    
    
    {
      "count": 1,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      }
    }

查询是可选的，如果未提供，它将使用"match_all"来计算所有文档。

[« Multi search API](search-multi-search.md) [Validate API »](search-
validate.md)
