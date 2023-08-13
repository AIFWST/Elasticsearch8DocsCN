

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Analyze API](indices-analyze.md) [Clear cache API »](indices-
clearcache.md)

## 分析索引盘使用情况API

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

分析索引或数据流的每个字段的磁盘使用情况。此 API 可能不支持在以前的 Elasticsearch 版本中创建的索引。小索引的结果可能不准确，因为 API 可能无法分析索引的某些部分。

    
    
    response = client.indices.disk_usage(
      index: 'my-index-000001',
      run_expensive_tasks: true
    )
    puts response
    
    
    POST /my-index-000001/_disk_usage?run_expensive_tasks=true

###Request

"发布/<target>/_disk_usage"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标索引、数据流或别名具有"管理"索引权限。

### 路径参数

`<target>`

     (Required, string) Comma-separated list of data streams, indices, and aliases used to limit the request. It's recommended to execute this API with a single index (or the latest backing index of a data stream) as the API consumes resources significantly. 

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

`flush`

     (Optional, Boolean) If `true`, the API performs a flush before analysis. If `false`, the response may not include uncommitted data. Defaults to `true`. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`run_expensive_tasks`

     (Required, Boolean) Analyzing field disk usage is resource-intensive. To use the API, this parameter must be set to `true`. Defaults to `false`. 
`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

###Examples

    
    
    response = client.indices.disk_usage(
      index: 'my-index-000001',
      run_expensive_tasks: true
    )
    puts response
    
    
    POST /my-index-000001/_disk_usage?run_expensive_tasks=true

该 API 返回：

    
    
    {
        "_shards": {
            "total": 1,
            "successful": 1,
            "failed": 0
        },
        "my-index-000001": {
            "store_size": "929mb", __"store_size_in_bytes": 974192723,
            "all_fields": {
                "total": "928.9mb", __"total_in_bytes": 973977084,
                "inverted_index": {
                    "total": "107.8mb",
                    "total_in_bytes": 113128526
                },
                "stored_fields": "623.5mb",
                "stored_fields_in_bytes": 653819143,
                "doc_values": "125.7mb",
                "doc_values_in_bytes": 131885142,
                "points": "59.9mb",
                "points_in_bytes": 62885773,
                "norms": "2.3kb",
                "norms_in_bytes": 2356,
                "term_vectors": "2.2kb",
                "term_vectors_in_bytes": 2310,
                "knn_vectors": "0b",
                "knn_vectors_in_bytes": 0
            },
            "fields": {
                "_id": {
                    "total": "49.3mb",
                    "total_in_bytes": 51709993,
                    "inverted_index": {
                        "total": "29.7mb",
                        "total_in_bytes": 31172745
                    },
                    "stored_fields": "19.5mb", __"stored_fields_in_bytes": 20537248,
                    "doc_values": "0b",
                    "doc_values_in_bytes": 0,
                    "points": "0b",
                    "points_in_bytes": 0,
                    "norms": "0b",
                    "norms_in_bytes": 0,
                    "term_vectors": "0b",
                    "term_vectors_in_bytes": 0,
                    "knn_vectors": "0b",
                    "knn_vectors_in_bytes": 0
                },
                "_primary_term": {...},
                "_seq_no": {...},
                "_version": {...},
                "_source": {
                    "total": "603.9mb",
                    "total_in_bytes": 633281895,
                    "inverted_index": {...},
                    "stored_fields": "603.9mb", __"stored_fields_in_bytes": 633281895,
                    "doc_values": "0b",
                    "doc_values_in_bytes": 0,
                    "points": "0b",
                    "points_in_bytes": 0,
                    "norms": "0b",
                    "norms_in_bytes": 0,
                    "term_vectors": "0b",
                    "term_vectors_in_bytes": 0,
                    "knn_vectors": "0b",
                    "knn_vectors_in_bytes": 0
                },
                "context": {
                    "total": "28.6mb",
                    "total_in_bytes": 30060405,
                    "inverted_index": {
                        "total": "22mb",
                        "total_in_bytes": 23090908
                    },
                    "stored_fields": "0b",
                    "stored_fields_in_bytes": 0,
                    "doc_values": "0b",
                    "doc_values_in_bytes": 0,
                    "points": "0b",
                    "points_in_bytes": 0,
                    "norms": "2.3kb",
                    "norms_in_bytes": 2356,
                    "term_vectors": "2.2kb",
                    "term_vectors_in_bytes": 2310,
                    "knn_vectors": "0b",
                    "knn_vectors_in_bytes": 0
                },
                "context.keyword": {...},
                "message": {...},
                "message.keyword": {...}
            }
        }
    }

__

|

仅分析索引分片的存储大小。   ---|---    __

|

索引的分析分片的字段总大小。此总数通常小于 <1> 中指定的索引大小，因为某些小的元数据文件将被忽略，并且 API 可能不会扫描数据文件的某些部分。   __

|

"_id"字段的存储大小 __

|

"_source"字段的存储大小。由于存储字段以压缩格式存储在一起，因此存储字段的估计大小是尽力而为，并且可能不准确。"_id"字段的存储大小可能被低估，而"_source"字段被高估。   « 分析 API 清除缓存 API »