

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Data stream APIs](data-stream-apis.md)

[« Create data stream API](indices-create-data-stream.md) [Get data stream
API »](indices-get-data-stream.md)

## 删除数据流接口

删除一个或多个数据流及其后备索引。请参阅删除数据流。

    
    
    response = client.indices.delete_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
    
    DELETE /_data_stream/my-data-stream

###Request

"删除/_data_stream/<data-stream>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对数据流具有"delete_index"或"管理"索引权限。

### 路径参数

`<data-stream>`

     (Required, string) Comma-separated list of data streams to delete. Wildcard (`*`) expressions are supported. 

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

[« Create data stream API](indices-create-data-stream.md) [Get data stream
API »](indices-get-data-stream.md)
