

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Suggesters](search-suggesters.md) [Count API »](search-count.md)

## 多搜索接口

使用单个 API 请求执行多个搜索。

    
    
    response = client.msearch(
      index: 'my-index-000001',
      body: [
        {},
        {
          query: {
            match: {
              message: 'this is a test'
            }
          }
        },
        {
          index: 'my-index-000002'
        },
        {
          query: {
            match_all: {}
          }
        }
      ]
    )
    puts response
    
    
    GET my-index-000001/_msearch
    { }
    {"query" : {"match" : { "message": "this is a test"}}}
    {"index": "my-index-000002"}
    {"query" : {"match_all" : {}}}

###Request

"获取/<target>/_msearch"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。有关跨集群搜索，请参阅配置具有安全性的远程集群。

###Description

多搜索 API 从单个 API 请求执行多个搜索。请求的格式类似于批量 API 格式，并使用换行分隔的 JSON (NDJSON) 格式。

结构如下：

    
    
    header\n
    body\n
    header\n
    body\n

此结构经过专门优化，可在特定搜索最终重定向到另一个节点时减少解析。

数据的最后一行必须以换行符"\n"结尾。每个换行符前面可以带有回车符"\r"。向此端点发送请求时，"内容类型"标头应设置为"application/x-ndjson"。

### 路径参数

`<target>`

    

(可选，字符串)要搜索的数据流、索引和别名的逗号分隔列表。

如果请求正文中的搜索未指定"索引"目标，则此列表充当回退。

支持通配符 ('*') 表达式。要搜索集群中的所有数据流和索引，请省略此参数或使用"_all"或"*"。

### 查询参数

`allow_no_indices`

     (Optional, Boolean) If `false`, the request returns an error if any wildcard expression, [index alias](aliases.html "Aliases"), or `_all` value targets only missing or closed indices. This behavior applies even if the request targets other open indices. For example, a request targeting `foo*,bar*` returns an error if an index starts with `foo` but no index starts with `bar`. 
`ccs_minimize_roundtrips`

     (Optional, Boolean) If `true`, network roundtrips between the coordinating node and remote clusters are minimized for cross-cluster search requests. Defaults to `true`. See [How cross-cluster search handles network delays](modules-cross-cluster-search.html#ccs-network-delays "How cross-cluster search handles network delays"). 
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
`max_concurrent_searches`

     (Optional, integer) Maximum number of concurrent searches the multi search API can execute. Defaults to `max(1, (# of [data nodes](modules-node.html#data-node "Data node") * min([search thread pool size](modules-threadpool.html#search-threadpool), 10)))`. 
`max_concurrent_shard_requests`

    

(可选，整数)每个节点每个子搜索请求执行的最大并发分片请求数。默认为"5"。

您可以使用此参数来防止请求使集群过载。例如，默认请求命中集群中的所有数据流和索引。如果每个节点的分片数很高，这可能会导致分片请求被拒绝。

在某些情况下，并行性不是通过并发请求实现的。在这些情况下，此参数中的低值可能会导致性能不佳。例如，在预期并发搜索请求数非常少的环境中，此参数中的值越高可能会提高性能。

`pre_filter_shard_size`

    

(可选，整数)定义一个阈值，该阈值在搜索请求扩展到超过阈值的分片数时，强制实施预筛选往返以基于查询重写预筛选搜索分片。例如，如果分片无法根据其重写方法匹配任何文档，即如果日期过滤器是强制性的匹配，但分片边界和查询是不相交的，则此过滤器往返可以显着限制分片的数量。如果未指定，则在满足以下任一条件时执行预过滤阶段：

* 请求针对多个"128"分片。  * 请求以一个或多个只读索引为目标。  * 查询的主要排序以索引字段为目标。

`rest_total_hits_as_int`

     (Optional, Boolean) If `true`, `hits.total` are returned as an integer in the response. Defaults to `false`, which returns an object. 
`routing`

     (Optional, string) Custom [routing value](mapping-routing-field.html "_routing field") used to route search operations to a specific shard. 
`search_type`

    

(可选，字符串)指示在对返回的文档进行评分时是否应使用全局术语和文档频率。

选项包括：

`query_then_fetch`

     (default) Documents are scored using local term and document frequencies for the shard. This is usually faster but less accurate. 
`dfs_query_then_fetch`

     Documents are scored using global term and document frequencies across all shards. This is usually slower but more accurate. 

`typed_keys`

     (Optional, Boolean) Specifies whether aggregation and suggester names should be prefixed by their respective types in the response. 

### 请求正文

请求正文包含以换行符分隔的搜索""<header>和搜索"<body>"对象的列表。

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

    

(可选，对象)包含搜索请求的参数：

"<body>"对象的属性

`aggregations`

     (Optional, [aggregation object](search-aggregations.html "Aggregations")) Aggregations you wish to run during the search. See [Aggregations](search-aggregations.html "Aggregations"). 
`query`

     (Optional, [Query DSL object](query-dsl.html "Query DSL")) Query you wish to run during the search. Hits matching this query are returned in the response. 
`from`

     (Optional, integer) Starting offset for returned hits. Defaults to `0`. 
`size`

     (Optional, integer) Number of hits to return. Defaults to `10`. 

### 响应正文

`responses`

     (array) Includes the search response and status code for each search request matching its order in the original multi search request. If there was a complete failure for a specific search request, an object with `error` message and corresponding status code will be returned in place of the actual search response. 

###Examples

标头包括要搜索的数据流、索引和别名。标头还指示"search_type"、"首选项"和"路由"。正文包括典型的搜索正文请求(包括"查询"、"聚合"、"发件人"、"大小"等)。

    
    
    $ cat requests
    {"index" : "test"}
    {"query" : {"match_all" : {}}, "from" : 0, "size" : 10}
    {"index" : "test", "search_type" : "dfs_query_then_fetch"}
    {"query" : {"match_all" : {}}}
    {}
    {"query" : {"match_all" : {}}}
    
    {"query" : {"match_all" : {}}}
    {"search_type" : "dfs_query_then_fetch"}
    {"query" : {"match_all" : {}}}
    
    
    $ curl -H "Content-Type: application/x-ndjson" -XGET localhost:9200/_msearch --data-binary "@requests"; echo

请注意，上面包括一个空标头的示例(也可以只是没有任何内容)，它也受支持。

终端节点还允许您搜索请求路径中的数据流、索引和别名。在这种情况下，除非在标头的"index"参数中明确指定，否则它将用作默认目标。例如：

    
    
    response = client.msearch(
      index: 'my-index-000001',
      body: [
        {},
        {
          query: {
            match_all: {}
          },
          from: 0,
          size: 10
        },
        {},
        {
          query: {
            match_all: {}
          }
        },
        {
          index: 'my-index-000002'
        },
        {
          query: {
            match_all: {}
          }
        }
      ]
    )
    puts response
    
    
    GET my-index-000001/_msearch
    {}
    {"query" : {"match_all" : {}}, "from" : 0, "size" : 10}
    {}
    {"query" : {"match_all" : {}}}
    {"index" : "my-index-000002"}
    {"query" : {"match_all" : {}}}

上面将针对"my-index-000001"索引执行搜索，以查找未在请求正文中定义"索引"目标的所有请求。最后一次搜索将针对"my-index-000002"索引执行。

"search_type"可以以类似的方式设置，以全局应用于所有搜索请求。

###Security

请参阅基于 URL 的访问控制

### 部分响应

为了确保快速响应，如果一个或多个分片失败，多搜索 API 将使用部分结果进行响应。有关更多信息，请参阅分片失败。

### 搜索取消

可以使用标准任务取消机制取消多个搜索，并且当客户端关闭用于执行请求的 http 连接时，也会自动取消。HTTP 客户端发送请求在请求超时或中止时关闭连接，这一点至关重要。取消 msearch 请求也会取消所有相应的子搜索请求。

[« Suggesters](search-suggesters.md) [Count API »](search-count.md)
