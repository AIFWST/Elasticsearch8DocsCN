

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Search APIs](search.md) [Async search »](async-search.md)

## 搜索接口

返回与请求中定义的查询匹配的搜索命中。

    
    
    response = client.search(
      index: 'my-index-000001'
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("my-index-000001"),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /my-index-000001/_search

###Request

"获取/<target>/_search"

"获取/_search"

"发布/<target>/_search"

"发布/_search"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。对于跨集群搜索，请参阅配置跨集群搜索的权限。

要在时间点 (PIT) 中搜索别名，您必须对别名的数据流或索引具有"读取"索引权限。

###Description

允许您执行搜索查询并获取与查询匹配的搜索命中。您可以使用"q"查询字符串参数或请求正文提供搜索查询。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to search. Supports wildcards (`*`). To search all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

可以使用查询参数或请求正文参数指定此 API 的多个选项。如果同时指定了这两个参数，则仅使用查询参数。

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

`allow_partial_search_results`

    

(可选，布尔值)如果为 'true'，则在存在分片请求超时或分片失败时返回部分结果。如果为"false"，则返回没有部分结果的错误。默认为"真"。

要覆盖此字段的默认值，请将"search.default_allow_partial_results"群集设置设置为"false"。

`analyzer`

    

(可选，字符串)用于查询字符串的分析器。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`analyze_wildcard`

    

(可选，布尔值)如果为"true"，则分析通配符和前缀查询。默认为"假"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`batched_reduce_size`

     (Optional, integer) The number of shard results that should be reduced at once on the coordinating node. This value should be used as a protection mechanism to reduce the memory overhead per search request if the potential number of shards in the request can be large. Defaults to `512`. 

`ccs_minimize_roundtrips`

     (Optional, Boolean) If `true`, network round-trips between the coordinating node and the remote clusters are minimized when executing cross-cluster search (CCS) requests. See [How cross-cluster search handles network delays](modules-cross-cluster-search.html#ccs-network-delays "How cross-cluster search handles network delays"). Defaults to `true`. 
`default_operator`

    

(可选，字符串)查询字符串查询的默认运算符：AND 或 OR。默认为"或"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`df`

    

(可选，字符串)用作默认值的字段，其中查询字符串中未提供字段前缀。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`docvalue_fields`

     (Optional, string) A comma-separated list of fields to return as the docvalue representation of a field for each hit. See [Doc value fields](search-fields.html#docvalue-fields "Doc value fields"). 
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

`explain`

     (Optional, Boolean) If `true`, returns detailed information about score computation as part of a hit. Defaults to `false`. 

`from`

    

(可选，整数)起始文档偏移量。需要为非负数并默认为"0"。

默认情况下，您不能使用"发件人"和"大小"参数翻阅超过 10，000 次点击。要翻阅更多点击，请使用"search_after"参数。

`ignore_throttled`

     (Optional, Boolean) If `true`, concrete, expanded or aliased indices will be ignored when frozen. Defaults to `true`. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`lenient`

    

(可选，布尔值)如果为"true"，则将忽略查询字符串中基于格式的查询失败(例如向数值字段提供文本)。默认为"假"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`max_concurrent_shard_requests`

     (Optional, integer) Defines the number of concurrent shard requests per node this search executes concurrently. This value should be used to limit the impact of the search on the cluster in order to limit the number of concurrent shard requests. Defaults to `5`. 
`pre_filter_shard_size`

    

(可选，整数)定义一个阈值，该阈值在搜索请求扩展到超过阈值的分片数时，强制实施预筛选往返以基于查询重写预筛选搜索分片。此过滤器往返可以显着限制分片的数量，例如，如果分片无法根据其重写方法匹配任何文档，即。如果日期筛选器必须匹配，但分片边界和查询不相交。如果未指定，则在满足以下任何条件时执行预过滤器阶段：

* 请求针对多个"128"分片。  * 请求以一个或多个只读索引为目标。  * 查询的主要排序以索引字段为目标。

`preference`

    

(可选，字符串)用于搜索的节点和分片。默认情况下，Elasticsearch 使用自适应副本选择从符合条件的节点和分片中进行选择，并考虑分配感知。

"首选项"的有效值

`_only_local`

     Run the search only on shards on the local node. 
`_local`

     If possible, run the search on shards on the local node. If not, select shards using the default method. 
`_only_nodes:<node-id>,<node-id>`

     Run the search on only the specified nodes IDs. If suitable shards exist on more than one selected node, use shards on those nodes using the default method. If none of the specified nodes are available, select shards from any available node using the default method. 
`_prefer_nodes:<node-id>,<node-id>`

     If possible, run the search on the specified nodes IDs. If not, select shards using the default method. 
`_shards:<shard>,<shard>`

     Run the search only on the specified shards. You can combine this value with other `preference` values. However, the `_shards` value must come first. For example: `_shards:2,3|_local`. 
`<custom-string>`

     Any string that does not start with `_`. If the cluster state and selected shards do not change, searches using the same `<custom-string>` value are routed to the same shards in the same order. 

`q`

    

(可选，字符串)Lucene 查询字符串语法中的查询。

可以使用"q"参数运行查询参数搜索。查询参数搜索不支持完整的 Elasticsearch Query DSL，但便于测试。

"q"参数覆盖请求正文中的"查询"参数。如果同时指定了这两个参数，则不会返回与"query"请求正文参数匹配的文档。

`request_cache`

     (Optional, Boolean) If `true`, the caching of search results is enabled for requests where `size` is `0`. See [Shard request cache settings](shard-request-cache.html "Shard request cache settings"). Defaults to index level settings. 
`rest_total_hits_as_int`

     (Optional, Boolean) Indicates whether hits.total should be rendered as an integer or an object in the rest search response. Defaults to `false`. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 

`scroll`

    

(可选，时间值)句点保留用于滚动的搜索上下文。请参阅滚动搜索结果。

默认情况下，此值不能超过"1d"(24 小时)。您可以使用"search.max_keep_alive"群集级别设置更改此限制。

`search_type`

    

(可选，字符串)如何计算分布式术语频率以进行相关性评分。

"search_type"的有效值

`query_then_fetch`

     (Default) Distributed term frequencies are calculated locally for each shard running the search. We recommend this option for faster searches with potentially less accurate scoring. 

`dfs_query_then_fetch`

     Distributed term frequencies are calculated globally, using information gathered from all shards running the search. While this option increases the accuracy of scoring, it adds a round-trip to each shard, which can result in slower searches. 

`seq_no_primary_term`

     (Optional, Boolean) If `true`, returns sequence number and primary term of the last modification of each hit. See [Optimistic concurrency control](optimistic-concurrency-control.html "Optimistic concurrency control"). 

`size`

    

(可选，整数)定义要返回的命中数。默认为"10"。

默认情况下，您不能使用"发件人"和"大小"参数翻阅超过 10，000 次点击。要翻阅更多点击，请使用"search_after"参数。

`sort`

     (Optional, string) A comma-separated list of <field>:<direction> pairs. 

`_source`

    

(可选)指示为匹配文档返回哪些源字段。这些字段在搜索响应的"hits._source"属性中返回。默认为"真"。请参阅源代码过滤。

"_source"的有效值

`true`

     (Boolean) The entire document source is returned. 
`false`

     (Boolean) The document source is not returned. 
`<string>`

     (string) Comma-separated list of source fields to return. Wildcard (`*`) patterns are supported. 

`_source_excludes`

    

(可选，字符串)要从响应中排除的源字段的逗号分隔列表。

您还可以使用此参数从"_source_includes"查询参数中指定的子集中排除字段。

如果"_source"参数为"false"，则忽略此参数。

`_source_includes`

    

(可选，字符串)要包含在响应中的源字段的逗号分隔列表。

如果指定此参数，则仅返回这些源字段。您可以使用"_source_excludes"查询参数从此子集中排除字段。

如果"_source"参数为"false"，则忽略此参数。

`stats`

     (Optional, string) Specific `tag` of the request for logging and statistical purposes. 
`stored_fields`

    

(可选，字符串)要作为命中的一部分返回的存储字段的逗号分隔列表。如果未指定任何字段，则响应中不包含任何存储的字段。请参阅存储字段。

如果指定此字段，则"_source"参数默认为"false"。您可以传递"_source：true"以返回搜索响应中的源字段和存储字段。

`suggest_field`

     (Optional, string) Specifies which field to use for suggestions. 
`suggest_mode`

    

(可选，字符串)指定建议模式。默认为"缺失"。可用选项：

* "总是" * "缺失" * "流行"

仅当指定了"suggest_field"和"suggest_text"查询字符串参数时，才能使用此参数。

`suggest_size`

    

(可选，整数)建议返回的数量。

仅当指定了"suggest_field"和"suggest_text"查询字符串参数时，才能使用此参数。

`suggest_text`

    

(可选，字符串)应返回建议的源文本。

仅当指定了"suggest_field"查询字符串参数时，才能使用此参数。

`terminate_after`

    

(可选，整数)每个分片要收集的最大文档数。如果查询达到此限制，Elasticsearch 会提前终止查询。Elasticsearch 在排序之前收集文档。

请谨慎使用。Elasticsearch 将此参数应用于处理请求的每个分片。如果可能，让 Elasticsearch 自动执行提前终止。避免为跨多个数据层使用支持索引的数据流为目标的请求指定此参数。

默认为"0"，表示不会提前终止查询执行。

`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a response from each shard. If no response is received before the timeout expires, the request fails and returns an error. Defaults to no timeout. 
`track_scores`

     (Optional, Boolean) If `true`, calculate and return document scores, even if the scores are not used for sorting. Defaults to `false`. 
`track_total_hits`

    

(可选，整数或布尔值)与查询匹配的命中数准确计数。默认为"10000"。

如果为"true"，则以牺牲某些性能为代价返回确切的命中数。如果为"false"，则响应不包括与查询匹配的命中总数。

`typed_keys`

     (Optional, Boolean) If `true`, aggregation and suggester names are be prefixed by their respective types in the response. Defaults to `true`. 
`version`

     (Optional, Boolean) If `true`, returns document version as part of a hit. Defaults to `false`. 

### 请求正文

`docvalue_fields`

    

(可选，字符串和对象的数组)字段模式数组。请求返回与响应的"hits.fields"属性中的这些模式匹配的字段名称的值。

可以将数组中的项指定为字符串或对象。请参阅文档值字段。

"docvalue_fields"对象的属性

`field`

     (Required, string) Wildcard pattern. The request returns doc values for field names matching this pattern. 
`format`

    

(可选，字符串)返回文档值的格式。

对于日期字段，您可以指定日期日期"格式"。对于数值字段字段，您可以指定十进制格式模式。

对于其他字段数据类型，不支持此参数。

`fields`

    

(可选，字符串和对象的数组)字段模式数组。请求返回与响应的"hits.fields"属性中的这些模式匹配的字段名称的值。

可以将数组中的项指定为字符串或对象。请参阅"字段"选项。

"字段"对象的属性

`field`

     (Required, string) Field to return. Supports wildcards (`*`). 
`format`

    

(可选，字符串)日期和地理空间字段的格式。其他字段数据类型不支持此参数。

"日期"和"date_nanos"字段接受日期格式。"geo_point"和"geo_shape"字段接受：

"geojson"(默认)

     [GeoJSON](http://www.geojson.org)
`wkt`

     [Well Known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
`mvt(<spec>)`

    

二进制地图框矢量图块。API 将磁贴作为 base64 编码的字符串返回。""<spec>的格式为"//<zoom><x><y>"，带有两个可选的后缀："@<extent>"和/或"："<buffer>。例如，"2/0/1"或"2/0/1@4096：5"。

"MVT"参数

`<zoom>`

     (Required, integer) Zoom level for the tile. Accepts `0`-`29`. 
`<x>`

     (Required, integer) X coordinate for the tile. 
`<y>`

     (Required, integer) Y coordinate for the tile. 
`<extent>`

     (Optional, integer) Size, in pixels, of a side of the tile. Vector tiles are square with equal sides. Defaults to `4096`. 
`<buffer>`

     (Optional, integer) Size, in pixels, of a clipping buffer outside the tile. This allows renderers to avoid outline artifacts from geometries that extend past the extent of the tile. Defaults to `5`. 

`stored_fields`

    

(可选，字符串)要作为命中的一部分返回的存储字段的逗号分隔列表。如果未指定任何字段，则响应中不包含任何存储的字段。请参阅存储字段。

如果指定此选项，则"_source"参数默认为"false"。您可以传递"_source：true"以返回搜索响应中的源字段和存储字段。

`explain`

     (Optional, Boolean) If `true`, returns detailed information about score computation as part of a hit. Defaults to `false`. 
`from`

    

(可选，整数)起始文档偏移量。需要为非负数并默认为"0"。

默认情况下，您不能使用"发件人"和"大小"参数翻阅超过 10，000 次点击。要翻阅更多点击，请使用"search_after"参数。

`indices_boost`

    

(可选，对象数组)提升指定索引中文档的"_score"。

"indices_boost"对象的属性

'<index>： <boost-value>'

    

(必需，浮点数)"<index>"是索引或索引别名的名称。支持通配符 ('*') 表达式。

"<boost-value>"是分数乘以的因素。

提升值大于"1.0"会增加分数。介于"0"和"1.0"之间的提升值会降低分数。

`knn`

    

(可选，对象或对象数组)定义要运行的 kNN 查询。

"knn"对象的属性

`field`

     (Required, string) The name of the vector field to search against. Must be a [`dense_vector` field with indexing enabled](dense-vector.html#index-vectors-knn-search "Index vectors for kNN search"). 
`filter`

     (Optional, [Query DSL object](query-dsl.html "Query DSL")) Query to filter the documents that can match. The kNN search will return the top `k` documents that also match this filter. The value can be a single query or a list of queries. If `filter` is not provided, all documents are allowed to match. 
`k`

     (Required, integer) Number of nearest neighbors to return as top hits. This value must be less than `num_candidates`. 
`num_candidates`

     (Required, integer) The number of nearest neighbor candidates to consider per shard. Cannot exceed 10,000. Elasticsearch collects `num_candidates` results from each shard, then merges them to find the top `k` results. Increasing `num_candidates` tends to improve the accuracy of the final `k` results. 
`query_vector`

     (Optional, array of floats) Query vector. Must have the same number of dimensions as the vector field you are searching against. 
`query_vector_builder`

     (Optional, object) A configuration object indicating how to build a query_vector before executing the request. You must provide a `query_vector_builder` or `query_vector`, but not both. Refer to [Perform semantic search](knn-search.html#knn-semantic-search "Perform semantic search") to learn more. 
`similarity`

    

(可选，浮动)文档被视为匹配所需的最小相似性。计算的相似性值与所使用的原始"相似性"相关。不是文档分数。然后根据"相似性"对匹配的文档进行评分，并应用提供的"提升"。

"相似性"参数是直接向量相似性计算。

*"l2_norm"：也称为欧几里得，将包括矢量位于"暗淡"维度超球体内的文档，其半径为"相似性"，原点位于"query_vector"。  * '余弦' & 'dot_product'：仅返回余弦相似性或点积至少是提供的"相似性"的向量。

`min_score`

     (Optional, float) Minimum [`_score`](query-filter-context.html#relevance-scores "Relevance scores") for matching documents. Documents with a lower `_score` are not included in the search results. 

`pit`

    

(可选，对象)将搜索限制为时间点 (PIT)。如果提供"pit"，则无法<target>在请求路径中指定""。

"坑"的性质

`id`

     (Required*, string) ID for the PIT to search. If you provide a `pit` object, this parameter is required. 
`keep_alive`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Period of time used to extend the life of the PIT. 

`query`

     (Optional, [query object](query-dsl.html "Query DSL")) Defines the search definition using the [Query DSL](query-dsl.html "Query DSL"). 

`rank`

    

[预览] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。 此参数处于技术预览阶段，将来可能会更改。语法可能会在正式发布之前更改。

(可选，对象)定义一种方法，用于从查询、子搜索和/或 knnsearch 的组合中组合和排名结果集。至少需要 2 个结果集才能对指定源进行排名。

排名方法

`rrf`

     (Optional, object) Sets the ranking method to [reciprocal rank fusion (RRF)](rrf.html "Reciprocal rank fusion"). 

`runtime_mappings`

    

(可选，对象的对象)在搜索请求中定义一个或多个运行时字段。这些字段优先于具有相同名称的映射字段。

"runtime_mappings"对象的属性

`<field-name>`

    

(必填，对象)运行时字段的配置。键是字段名称。

""的属性<field-name>

`type`

    

(必需，字符串)字段类型，可以是以下任何一种：

* "布尔值" * "复合" * "日期" * "双精度" * "geo_point" * "IP" * "关键字" * "长" * "查找"

`script`

    

(可选，字符串)查询时执行的无痛脚本。该脚本可以访问文档的整个上下文，包括原始"_source"和任何映射字段及其值。

此脚本必须包含"emit"以返回计算值。例如：

    
    
    "script": "emit(doc['@timestamp'].value.dayOfWeekEnum.toString())"

`seq_no_primary_term`

     (Optional, Boolean) If `true`, returns sequence number and primary term of the last modification of each hit. See [Optimistic concurrency control](optimistic-concurrency-control.html "Optimistic concurrency control"). 
`size`

    

(可选，整数)要返回的命中数。需要为非负数，默认为"10"。

默认情况下，您不能使用"发件人"和"大小"参数翻阅超过 10，000 次点击。要翻阅更多点击，请使用"search_after"参数。

`_source`

    

(可选)指示为匹配文档返回哪些源字段。这些字段在搜索响应的"hits._source"属性中返回。默认为"真"。请参阅源代码过滤。

"_source"的有效值

`true`

     (Boolean) The entire document source is returned. 
`false`

     (Boolean) The document source is not returned. 
`<wildcard_pattern>`

     (string or array of strings) Wildcard (`*`) pattern or array of patterns containing source fields to return. 
`<object>`

    

(对象)包含要包括或排除的源字段列表的对象。

""的属性<object>

`excludes`

    

(字符串或字符串数组)通配符 ('*') 模式或模式数组包含要从响应中排除的源字段。

还可以使用此属性从"include"属性中指定的子集中排除字段。

`includes`

    

(字符串或字符串数组)通配符 ('*') 模式或模式数组包含要返回的源字段。

如果指定此属性，则仅返回这些源字段。您可以使用"excludes"属性从此子集中排除字段。

`stats`

     (Optional, array of strings) Stats groups to associate with the search. Each group maintains a statistics aggregation for its associated searches. You can retrieve these stats using the [indices stats API](indices-stats.html "Index stats API"). 

`sub_searches`

    

[预览] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。 此参数处于技术预览阶段，将来可能会更改。语法可能会在正式发布之前更改。

(可选，对象数组)一个"sub_search"对象的数组，其中每个"sub_search"都是独立计算的，它们的结果集稍后作为排名的一部分进行组合。每个"sub_search"对象都需要包含单个"查询"。"sub_searches"只允许与"rank"元素一起使用，不允许与顶级"查询"元素结合使用。

"sub_searches"作为搜索的一部分：

    
    
    {
      "sub_searches": [
        { "query": {...} },
        { "query": {...} }
      ]
      ...
    }

`terminate_after`

    

(可选，整数)每个分片要收集的最大文档数。如果查询达到此限制，Elasticsearch 会提前终止查询。Elasticsearch 在排序之前收集文档。

请谨慎使用。Elasticsearch 将此参数应用于处理请求的每个分片。如果可能，让 Elasticsearch 自动执行提前终止。避免为跨多个数据层使用支持索引的数据流为目标的请求指定此参数。

默认为"0"，表示不会提前终止查询执行。

`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a response from each shard. If no response is received before the timeout expires, the request fails and returns an error. Defaults to no timeout. 

`version`

     (Optional, Boolean) If `true`, returns document version as part of a hit. Defaults to `false`. 

### 响应正文

`_scroll_id`

    

(字符串)搜索及其搜索上下文的标识符。

您可以将此滚动 ID 与滚动 API 一起使用，以检索请求的下一批搜索结果。请参阅滚动搜索结果。

仅当在请求中指定了"scroll"查询参数时，才会返回此参数。

`took`

    

(整数)Elasticsearch 执行请求所花费的毫秒数。

此值是通过测量从协调节点上收到请求到协调节点准备好发送响应的时间之间经过的时间来计算的。

花费的时间包括：

* 协调节点和数据节点之间的通信时间 * 请求在"搜索"线程池中等待执行的时间 * 实际执行时间

花费的时间**不包括**包括：

* 将请求发送到 Elasticsearch 所需的时间 * 序列化 JSON 响应所需的时间 * 将响应发送到客户端所需的时间

`timed_out`

     (Boolean) If `true`, the request timed out before completion; returned results may be partial or empty. 

`_shards`

    

(对象)包含用于请求的分片计数。

"_shards"的属性

`total`

     (integer) Total number of shards that require querying, including unallocated shards. 
`successful`

     (integer) Number of shards that executed the request successfully. 
`skipped`

     (integer) Number of shards that skipped the request because a lightweight check helped realize that no documents could possibly match on this shard. This typically happens when a search request includes a range filter and the shard only has values that fall outside of that range. 
`failed`

     (integer) Number of shards that failed to execute the request. Note that shards that are not allocated will be considered neither successful nor failed. Having `failed+successful` less than `total` is thus an indication that some of the shards were not allocated. 

`hits`

    

(对象)包含返回的文档和元数据。

"命中"的属性

`total`

    

(对象)有关匹配文档数的元数据。

"总计"的属性

`value`

     (integer) Total number of matching documents. 
`relation`

    

(字符串)指示"value"参数中的匹配文档数是准确还是下限。

"关系"的价值：

`eq`

     Accurate 
`gte`

     Lower bound 

`max_score`

    

(浮点数)返回的最高文档"_score"。

对于不按"_score"排序的请求，此值为"null"。

`hits`

    

(对象数组)返回的文档对象的数组。

"命中"对象的属性

`_index`

     (string) Name of the index containing the returned document. 
`_id`

     (string) Unique identifier for the returned document. This ID is only unique within the returned index. 

`_score`

     (float) Positive 32-bit floating point number used to determine the relevance of the returned document. 

`_source`

    

(对象)在索引时为文档传递的原始 JSON 正文。

您可以使用"_source"参数从响应中排除此属性，或指定要返回的源字段。

`fields`

    

(对象)包含文档的字段值。必须在请求中使用以下一个或多个请求参数指定这些字段：

* "字段" * "docvalue_fields" * "script_fields" * "stored_fields"

仅当设置了一个或多个这些参数时，才会返回此属性。

"字段"的属性

`<field>`

     (array) Key is the field name. Value is the value for the field. 

###Examples

    
    
    response = client.search(
      index: 'my-index-000001',
      from: 40,
      size: 20,
      body: {
        query: {
          term: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?from=40&size=20
    {
      "query": {
        "term": {
          "user.id": "kimchy"
        }
      }
    }

API 返回以下响应：

    
    
    {
      "took": 5,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 20,
          "relation": "eq"
        },
        "max_score": 1.3862942,
        "hits": [
          {
            "_index": "my-index-000001",
            "_id": "0",
            "_score": 1.3862942,
            "_source": {
              "@timestamp": "2099-11-15T14:12:12",
              "http": {
                "request": {
                  "method": "get"
                },
                "response": {
                  "status_code": 200,
                  "bytes": 1070000
                },
                "version": "1.1"
              },
              "source": {
                "ip": "127.0.0.1"
              },
              "message": "GET /search HTTP/1.1 200 1070000",
              "user": {
                "id": "kimchy"
              }
            }
          },
          ...
        ]
      }
    }

[« Search APIs](search.md) [Async search »](async-search.md)
