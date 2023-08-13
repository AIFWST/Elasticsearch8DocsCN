

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Data stream APIs](data-stream-apis.md)

[« Migrate to data stream API](indices-migrate-to-data-stream.md) [Promote
data stream API »](promote-data-stream-api.md)

## 数据流统计接口

检索一个或多个数据流的统计信息。

    
    
    response = client.indices.data_streams_stats(
      name: 'my-data-stream'
    )
    puts response
    
    
    GET /_data_stream/my-data-stream/_stats

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对数据流具有"监控"或"管理"索引权限。

###Request

"获取/_data_stream/<data-stream>/_stats"

### 路径参数

`<data-stream>`

    

(可选，字符串)用于限制请求的数据流的逗号分隔列表。支持通配符表达式 ('*')。

要定位集群中的所有数据流，请省略此参数或使用"*"。

### 查询参数

`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的数据流类型。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

"全部"、"隐藏"

     Match any data stream, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`, `closed`

     Matches any non-hidden data stream. Data streams cannot be closed. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

`human`

     (Optional, Boolean) If `true`, the response includes statistics in human-readable [byte values](api-conventions.html#byte-units "Byte size units"). Defaults to `false`. 

### 响应正文

`_shards`

    

(对象)包含有关尝试执行请求的分片的信息。

"_shards"的属性

`total`

     (integer) Total number of shards that attempted to execute the request. 
`successful`

     (integer) Number of shards that successfully executed the request. 
`failed`

     (integer) Number of shards that failed to execute the request. 

`data_stream_count`

     (integer) Total number of selected data streams. 
`backing_indices`

     (integer) Total number of backing indices for the selected data streams. 
`total_store_sizes`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total size of all shards for the selected data streams. This property is included only if the `human` query parameter is `true`. 
`total_store_size_bytes`

     (integer) Total size, in bytes, of all shards for the selected data streams. 
`data_streams`

    

(对象数组)包含所选数据流的统计信息。

"data_streams"中对象的属性

`data_stream`

     (string) Name of the data stream. 
`backing_indices`

     (integer) Current number of backing indices for the data stream. 
`store_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total size of all shards for the data stream's backing indices. This parameter is only returned if the `human` query parameter is `true`. 
`store_size_bytes`

     (integer) Total size, in bytes, of all shards for the data stream's backing indices. 
`maximum_timestamp`

    

(整数)数据流的最高"@timestamp"值，自 Unix 纪元以来转换为毫秒。

此时间戳是尽力而为提供的。如果满足以下一个或多个条件，则数据流可能包含高于此值的"@timestamp"值：

* 流包含封闭的支持索引。  * 较低世代的后备指数包含较高的"@timestamp"值。

###Examples

    
    
    response = client.indices.data_streams_stats(
      name: 'my-data-stream*',
      human: true
    )
    puts response
    
    
    GET /_data_stream/my-data-stream*/_stats?human=true

API 返回以下响应。

    
    
    {
      "_shards": {
        "total": 10,
        "successful": 5,
        "failed": 0
      },
      "data_stream_count": 2,
      "backing_indices": 5,
      "total_store_size": "7kb",
      "total_store_size_bytes": 7268,
      "data_streams": [
        {
          "data_stream": "my-data-stream",
          "backing_indices": 3,
          "store_size": "3.7kb",
          "store_size_bytes": 3772,
          "maximum_timestamp": 1607512028000
        },
        {
          "data_stream": "my-data-stream-two",
          "backing_indices": 2,
          "store_size": "3.4kb",
          "store_size_bytes": 3496,
          "maximum_timestamp": 1607425567000
        }
      ]
    }

[« Migrate to data stream API](indices-migrate-to-data-stream.md) [Promote
data stream API »](promote-data-stream-api.md)
