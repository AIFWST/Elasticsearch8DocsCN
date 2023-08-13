

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Data stream APIs](data-stream-apis.md)

[« Get data stream API](indices-get-data-stream.md) [Data stream stats API
»](data-stream-stats-api.md)

## 迁移到数据流API

将索引别名转换为数据流。

    
    
    POST /_data_stream/_migrate/my-logs

###Request

"发布/_data_stream/_migrate/<alias>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对索引别名具有"管理"索引权限。  * 启用了数据流的匹配索引模板。请参阅_Set数据stream_。

### 路径参数

`<alias>`

    

(必需，字符串)要转换为数据流的索引别名的名称。别名必须满足以下条件：

* 别名必须具有写入索引。  * 别名的所有索引都具有"日期"或"date_nanos"字段类型的"@timestamp"字段映射。  * 别名不得有任何过滤器。  * 别名不得使用自定义路由。

如果成功，请求将删除别名并创建具有相同名称的数据流。别名的索引成为流的隐藏支持索引。别名的写入索引将成为流的写入索引。

[« Get data stream API](indices-get-data-stream.md) [Data stream stats API
»](data-stream-stats-api.md)
