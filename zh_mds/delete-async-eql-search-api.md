

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[EQL APIs](eql-apis.md)

[« EQL APIs](eql-apis.md) [EQL search API »](eql-search-api.md)

## 删除异步 EQL 搜索API

删除异步 EQL 搜索或存储的同步 EQL 搜索。API 还会删除搜索结果。

    
    
    response = client.eql.delete(
      id: 'FkpMRkJGS1gzVDRlM3g4ZzMyRGlLbkEaTXlJZHdNT09TU2VTZVBoNDM3cFZMUToxMDM='
    )
    puts response
    
    
    DELETE /_eql/search/FkpMRkJGS1gzVDRlM3g4ZzMyRGlLbkEaTXlJZHdNT09TU2VTZVBoNDM3cFZMUToxMDM=

###Request

"删除/_eql/搜索/<search_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则只有以下用户可以使用此 API 删除搜索：

    * Users with the `cancel_task` [cluster privilege](security-privileges.html#privileges-list-cluster "Cluster privileges")
    * The user who first submitted the search 

* 请参阅必填字段。

####Limitations

请参阅 EQL 限制。

### 路径参数

`<search_id>`

    

(必需，字符串)要删除的搜索的标识符。

异步搜索的 EQL 搜索 API 响应中提供了搜索 ID。如果请求的"keep_on_completion"参数为"true"，则还会提供搜索 ID。

[« EQL APIs](eql-apis.md) [EQL search API »](eql-search-api.md)
