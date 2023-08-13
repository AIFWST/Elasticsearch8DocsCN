

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[EQL APIs](eql-apis.md)

[« EQL search API](eql-search-api.md) [Get async EQL status API »](get-
async-eql-status-api.md)

## 获取异步 EQL 搜索API

返回异步 EQL 搜索或存储的同步 EQL 搜索的当前状态和可用结果。

    
    
    response = client.eql.get(
      id: 'FkpMRkJGS1gzVDRlM3g4ZzMyRGlLbkEaTXlJZHdNT09TU2VTZVBoNDM3cFZMUToxMDM='
    )
    puts response
    
    
    GET /_eql/search/FkpMRkJGS1gzVDRlM3g4ZzMyRGlLbkEaTXlJZHdNT09TU2VTZVBoNDM3cFZMUToxMDM=

###Request

'获取/_eql/搜索/<search_id>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则只有首次提交 EQL 搜索的用户才能使用此 API 检索搜索。  * 请参阅必填字段。

####Limitations

请参阅 EQL 限制。

### 路径参数

`<search_id>`

    

(必需，字符串)搜索的标识符。

异步搜索的 EQL 搜索 API 响应中提供了搜索 ID。如果请求的"keep_on_completion"参数为"true"，则还会提供搜索 ID。

### 查询参数

`keep_alive`

    

(可选，时间值)搜索及其结果在群集上的存储周期。默认为搜索的 EQL 搜索 API 请求设置的"keep_alive"值。

如果指定，此参数将为搜索设置一个新的"keep_alive"周期，从执行 get 异步 EQL 搜索 API 请求时开始。此新周期将覆盖 EQL 搜索 API 请求中指定的时间段。

当此期限到期时，搜索及其结果将被删除，即使搜索正在进行中也是如此。

`wait_for_completion_timeout`

    

(可选，时间值)等待请求完成的超时持续时间。默认为无超时，表示请求等待完整的搜索结果。

如果指定了该参数，且在此期间请求完成，则返回完整的搜索结果。

如果请求在此期间未完成，则响应将返回"true"值"is_partial"，并且没有搜索结果。

### 响应正文

异步 EQL 搜索 API 返回与 EQL 搜索 API 相同的响应正文。请参阅 EQL 搜索 API 的响应正文参数。

[« EQL search API](eql-search-api.md) [Get async EQL status API »](get-
async-eql-status-api.md)
