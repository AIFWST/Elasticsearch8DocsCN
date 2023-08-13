

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[SQL APIs](sql-apis.md)

[« Get async SQL search API](get-async-sql-search-api.md) [SQL search API
»](sql-search-api.md)

## 获取异步 SQL 搜索状态API

返回异步 SQL 搜索或存储的同步 SQL 搜索的当前状态。

    
    
    response = client.sql.get_async_status(
      id: 'FmdMX2pIang3UWhLRU5QS0lqdlppYncaMUpYQ05oSkpTc3kwZ21EdC1tbFJXQToxOTI=',
      format: 'json'
    )
    puts response
    
    
    GET _sql/async/status/FmdMX2pIang3UWhLRU5QS0lqdlppYncaMUpYQ05oSkpTc3kwZ21EdC1tbFJXQToxOTI=?format=json

###Request

'获取_sql/异步/状态/<search_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"集群权限才能使用此 API。

####Limitations

请参阅_SQL Limitations_。

### 路径参数

`<search_id>`

     (Required, string) Identifier for the search. 

### 响应正文

`id`

     (string) Identifier for the search. 
`is_running`

     (Boolean) If `true`, the search is still running. If `false`, the search has finished. 
`is_partial`

     (Boolean) If `true`, the response does not contain complete search results. If `is_partial` is `true` and `is_running` is `true`, the search is still running. If `is_partial` is `true` but `is_running` is `false`, the results are partial due to a failure or timeout. 
`start_time_in_millis`

     (integer) Timestamp, in milliseconds since the Unix epoch, when the search started. The API only returns this property for running searches. 
`expiration_time_in_millis`

     (integer) Timestamp, in milliseconds since the Unix epoch, when Elasticsearch will delete the search and its results, even if the search is still running. 
`completion_status`

     (integer) HTTP status code for the search. The API only returns this property for completed searches. 

[« Get async SQL search API](get-async-sql-search-api.md) [SQL search API
»](sql-search-api.md)
