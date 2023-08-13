

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[EQL APIs](eql-apis.md)

[« Get async EQL search API](get-async-eql-search-api.md) [Features APIs
»](features-apis.md)

## 获取异步 EQL 状态API

返回异步 EQL 搜索或存储的同步 EQL 搜索的当前状态，但不返回结果。这是一个比获取异步 EQL 搜索 API 更轻量级的 API，因为它不返回搜索结果，只报告状态。

如果启用了 Elasticsearch 安全功能，则对 getasync eql status API 的访问仅限于monitoring_user角色。

    
    
    response = client.eql.get_status(
      id: 'FkpMRkJGS1gzVDRlM3g4ZzMyRGlLbkEaTXlJZHdNT09TU2VTZVBoNDM3cFZMUToxMDM='
    )
    puts response
    
    
    GET /_eql/search/status/FkpMRkJGS1gzVDRlM3g4ZzMyRGlLbkEaTXlJZHdNT09TU2VTZVBoNDM3cFZMUToxMDM=

###Request

'GET /_eql/search/status/<search_id>'

### 路径参数

`<search_id>`

    

(必需，字符串)搜索的标识符。

异步搜索的 EQL 搜索 API 响应中提供了搜索 ID。如果请求的"keep_on_completion"参数为"true"，则还会提供搜索 ID。

### 响应正文

`id`

     (string) Identifier for the search. 
`is_running`

     (boolean) If `true`, the search request is still executing. If `false`, the search is completed. 
`is_partial`

     (boolean) If `true`, the response does not contain complete search results. This could be because either the search is still running (`is_running` status is `false`), or because it is already completed (`is_running` status is `true`) and results are partial due to failures or timeouts. 
`start_time_in_millis`

     (Long) For a running search shows a timestamp when the eql search started, in milliseconds since the Unix epoch. 
`expiration_time_in_millis`

     (long) Shows a timestamp when the eql search will be expired, in milliseconds since the Unix epoch. When this time is reached, the search and its results are deleted, even if the search is still ongoing. 
`completion_status`

     (Integer) For a completed search shows the http status code of the completed search. 

###Examples

    
    
    response = client.eql.get_status(
      id: 'FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=',
      keep_alive: '5d'
    )
    puts response
    
    
    GET /_eql/search/status/FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=?keep_alive=5d

如果搜索仍在运行，则状态响应具有以下形式：

    
    
    {
      "id" : "FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=",
      "is_running" : true,
      "is_partial" : true,
      "start_time_in_millis" : 1611690235000,
      "expiration_time_in_millis" : 1611690295000
    
    }

如果搜索完成，则状态响应没有"start_time_in_millis"，但有一个附加的"completion_status"字段，显示已完成的 eql 搜索的状态代码：

    
    
    {
      "id" : "FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=",
      "is_running" : false,
      "is_partial" : false,
      "expiration_time_in_millis" : 1611690295000,
      "completion_status" : 200 __}

__

|

指示 eql 搜索已成功完成 ---|--- « 获取异步 EQL 搜索 API 功能 API»