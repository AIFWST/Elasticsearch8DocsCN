

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Exists API](indices-exists.md) [Flush API »](indices-flush.md)

## 字段使用情况统计信息API

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

返回索引的每个分片和字段的字段使用情况信息。当查询在群集上运行时，将自动捕获字段使用情况统计信息。访问给定字段的分片级搜索请求(即使在该请求期间多次访问)也计为一次使用。

    
    
    response = client.indices.field_usage_stats(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_field_usage_stats

###Request

'获取 /<index>/_field_usage_stats'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标索引或索引别名具有"管理"索引权限。

### 路径参数

`<index>`

     (Optional, string) Comma-separated list or wildcard expression of index names used to limit the request. 

### 查询参数

`allow_no_indices`

     (Optional, Boolean) If `false`, the request returns an error if any wildcard expression, [index alias](aliases.html "Aliases"), or `_all` value targets only missing or closed indices. This behavior applies even if the request targets other open indices. For example, a request targeting `foo*,bar*` returns an error if an index starts with `foo` but no index starts with `bar`. 
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

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`fields`

    

(可选，字符串)要包含在统计信息中的字段的逗号分隔列表或通配符表达式。

### 响应正文

响应正文报告支持索引中字段的数据结构的每个分片使用计数。给定的请求会将每个计数的最大值递增 1，即使该请求多次访问同一字段也是如此。

`any`

     (integer) Denotes any kind of use of the field (e.g. via the _inverted index_ , _stored fields_ , _doc values_ , etc.) such that any usage is counted once for a given search request. 
`inverted_index`

    

(对象)_inverted index_由"索引"映射参数启用，并通过为字段设置"index_options"进行配置。

"inverted_index"的属性：

`terms`

     (integer) Denotes the usages of _terms_ in the _inverted index_ , answering the question "Is this field's inverted index used?". 
`postings`

     (integer) Denotes the usage of the _posting list_ which contains the document ids for a given term. 
`proximity`

     (integer) Denotes any kind of usage of either _positions_ , _offsets_ or _payloads_ in the _inverted index_ such that any usage is counted once for a given search request. 
`positions`

     (integer) Denotes the usage of _position_ data (order of the term) in the _inverted index_. 
`term_frequencies`

     (integer) Denotes the usage of the _term frequencies_ in the _inverted index_ which are used to calculate scores. 
`offsets`

     (integer) Denotes the usage of the _offsets_ in the _inverted index_ which store the start and end character offsets of the terms. 
`payloads`

     (integer) Denotes the usage of _payloads_ in the _inverted index_ , e.g. via the [delimited payload token filter](analysis-delimited-payload-tokenfilter.html "Delimited payload token filter"), or by user-defined analysis components and plugins. 

`stored_fields`

     (integer) Denotes the usage of _stored fields_. These are enabled via the [`store`](mapping-store.html "store") mapping option, and accessed by specifying the [`stored_fields`](search-fields.html#stored-fields "Stored fields") query option. Note that the [`_source`](mapping-source-field.html "_source field") and [`_id`](mapping-id-field.html "_id field") fields are stored by default and their usage is counted here. 
`doc_values`

     (integer) Denotes the usage of _doc values_ , which are primarily used for sorting and aggregations. These are enabled via the [`doc_values`](doc-values.html "doc_values") mapping parameter. 
`points`

     (integer) Denotes the usage of the Lucene _PointValues_ which are the basis of most numeric _field data types_ , including [spacial data types](mapping-types.html#spatial_datatypes "Spatial data types"), [numbers](number.html "Numeric field types"), [dates](mapping-types.html#_core_datatypes "Common types"), and more. These are used by queries/aggregations for ranges, counts, bucketing, min/max, histograms, spacial, etc. 
`norms`

     (integer) Denotes the usage of [_norms_](norms.html "norms") which contain index-time boost values used for scoring. 
`term_vectors`

     (integer) Denotes the usage of [_term vectors_](term-vector.html "term_vector") which allow for a document's terms to be retrieved at search time. Usages include [highlighting](highlighting.html "Highlighting") and the [More Like This Query](query-dsl-mlt-query.html "More like this query"). 
`knn_vectors`

     (integer) Denotes the usage of the [_knn_vectors_](dense-vector.html "Dense vector field type") field type, primarily used for [k-nearest neighbor (kNN) search](knn-search.html "k-nearest neighbor \(kNN\) search"). 

###Examples

以下请求检索当前可用分片上索引"my-index-000001"的字段使用信息。

    
    
    response = client.indices.field_usage_stats(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_field_usage_stats

API 返回以下响应：

    
    
    {
        "_shards": {
            "total": 1,
            "successful": 1,
            "failed": 0
        },
        "my-index-000001": {
            "shards": [
                {
                    "tracking_id": "MpOl0QlTQ4SYYhEe6KgJoQ",
                    "tracking_started_at_millis": 1625558985010,
                    "routing": {
                        "state": "STARTED",
                        "primary": true,
                        "node": "gA6KeeVzQkGURFCUyV-e8Q",
                        "relocating_node": null
                    },
                    "stats" : {
                        "all_fields": { __"any": "6",
                            "inverted_index": {
                                "terms" : 1,
                                "postings" : 1,
                                "proximity" : 1,
                                "positions" : 0,
                                "term_frequencies" : 1,
                                "offsets" : 0,
                                "payloads" : 0
                            },
                            "stored_fields" : 2,
                            "doc_values" : 1,
                            "points" : 0,
                            "norms" : 1,
                            "term_vectors" : 0,
                            "knn_vectors" : 0
                        },
                        "fields": {
                            "_id": { __"any" : 1,
                                "inverted_index": {
                                    "terms" : 1,
                                    "postings" : 1,
                                    "proximity" : 1,
                                    "positions" : 0,
                                    "term_frequencies" : 1,
                                    "offsets" : 0,
                                    "payloads" : 0
                                },
                                "stored_fields" : 1,
                                "doc_values" : 0,
                                "points" : 0,
                                "norms" : 0,
                                "term_vectors" : 0,
                                "knn_vectors" : 0
                            },
                            "_source": {...},
                            "context": {...},
                            "message.keyword": {...}
                        }
                    }
                }
            ]
        }
    }

__

|

报告索引中所有字段的使用计数总和(在列出的分片上)。   ---|---    __

|

报告以下使用情况计数的字段名称(在列出的分片上)。   « 存在 API 刷新 API »