

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Data stream APIs](data-stream-apis.md)

[« Data stream stats API](data-stream-stats-api.md) [Modify data streams API
»](modify-data-streams-api.md)

## 提升数据流API

提升数据流 API 的目的是将 CCR 复制的数据流转换为常规数据流。

通过 CCR 自动跟随，可以将来自远程集群的数据流复制到本地集群。这些数据流无法在本地群集中滚动更新。仅当上游数据流滚动更新时，这些复制的数据流也会滚动。如果远程集群不再可用，可以将本地集群中的数据流提升为非常规数据流，从而允许这些数据流在本地集群中滚动。

    
    
    response = client.indices.promote_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
    
    POST /_data_stream/_promote/my-data-stream

###Request

"发布/_data_stream/_promote/<data-stream>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_follow_index"集群权限才能使用此 API。

### 路径参数

`<data-stream>`

     (Required, string) The name of the data stream to promote. 

[« Data stream stats API](data-stream-stats-api.md) [Modify data streams API
»](modify-data-streams-api.md)
