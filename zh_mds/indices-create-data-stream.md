

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Data stream APIs](data-stream-apis.md)

[« Data stream APIs](data-stream-apis.md) [Delete data stream API
»](indices-delete-data-stream.md)

## 创建数据流接口

创建新的数据流。

    
    
    response = client.indices.create_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
    
    PUT /_data_stream/my-data-stream

###Request

"放/_data_stream/<data-stream>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须具有数据流的"create_index"或"管理"索引权限。  * 启用了数据流的匹配索引模板。请参阅_Set数据stream_。

### 路径参数

`<data-stream>`

    

(必需，字符串)要创建的数据流的名称。数据流名称必须满足以下条件：

* 仅限小写 * 不能包含"\"、"/"、"*"、"？"、"<"、">"、"|"、""、"#"、"："或空格字符 * 不能以"-"、"_"、"+"或".ds-"开头 * 不能是".."或"."。' * 不能超过 255 个字节。多字节字符计入此限制的速度更快。

[« Data stream APIs](data-stream-apis.md) [Delete data stream API
»](indices-delete-data-stream.md)
