

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Point in time API](point-in-time-api.md) [Reciprocal rank fusion
»](rrf.md)

## kNN 搜索API

### 在 8.4.0 中已弃用。

kNN 搜索 API 已替换为搜索 API 中的"knn"选项。

执行 k 最近邻 (kNN) 搜索并返回匹配的文档。

    
    
    GET my-index/_knn_search
    {
      "knn": {
        "field": "image_vector",
        "query_vector": [0.3, 0.1, 1.2],
        "k": 10,
        "num_candidates": 100
      },
      "_source": ["name", "file_type"]
    }

###Request

"获取<target>/_knn_search"

"发布<target>/_knn_search"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。

###Description

kNN 搜索 API 对"dense_vector"字段执行 k 最近邻 (kNN) 搜索。给定一个查询向量，它找到 _k_ 最接近的向量，并将这些文档作为搜索命中返回。

Elasticsearch使用HNSW算法来支持高效的kNN搜索。与大多数 kNN 算法一样，HNSW 是一种近似方法，它牺牲了结果的准确性以提高搜索速度。这意味着返回的结果并不总是真正的 _k_ 最近邻。

kNN 搜索 API 支持使用过滤器限制搜索。搜索将返回与筛选器查询匹配的顶部"k"文档。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to search. Supports wildcards (`*`). To search all data streams and indices, use `*` or `_all`. 

### 查询参数

`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 

### 请求正文

`filter`

     (Optional, [Query DSL object](query-dsl.html "Query DSL")) Query to filter the documents that can match. The kNN search will return the top `k` documents that also match this filter. The value can be a single query or a list of queries. If `filter` is not provided, all documents are allowed to match. 
`knn`

    

(必填，对象)定义要运行的 kNN 查询。

"knn"对象的属性

`field`

     (Required, string) The name of the vector field to search against. Must be a [`dense_vector` field with indexing enabled](dense-vector.html#index-vectors-knn-search "Index vectors for kNN search"). 
`k`

     (Required, integer) Number of nearest neighbors to return as top hits. This value must be less than `num_candidates`. 
`num_candidates`

     (Required, integer) The number of nearest neighbor candidates to consider per shard. Cannot exceed 10,000. Elasticsearch collects `num_candidates` results from each shard, then merges them to find the top `k` results. Increasing `num_candidates` tends to improve the accuracy of the final `k` results. 
`query_vector`

     (Required, array of floats) Query vector. Must have the same number of dimensions as the vector field you are searching against. 

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

`stored_fields`

    

(可选，字符串)要作为命中的一部分返回的存储字段的逗号分隔列表。如果未指定任何字段，则响应中不包含任何存储的字段。请参阅存储字段。

如果指定此选项，则"_source"参数默认为"false"。您可以传递"_source：true"以返回搜索响应中的源字段和存储字段。

### 响应正文

kNN 搜索响应与搜索 API 响应具有完全相同的结构。但是，某些部分具有特定于 kNN 搜索的含义：

* 文档"_score"由查询和文档向量之间的相似性决定。参见"相似性"。  * "hits.total"对象包含考虑的最近邻候选者的总数，即"num_candidates * num_shards"。"hits.total.relation"将始终为"eq"，表示一个确切的值。

[« Point in time API](point-in-time-api.md) [Reciprocal rank fusion
»](rrf.md)
