

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[SQL APIs](sql-apis.md)

[« Delete async SQL search API](delete-async-sql-search-api.md) [Get async
SQL search status API »](get-async-sql-search-status-api.md)

## 获取异步 SQL 搜索API

返回异步 SQL 搜索或存储的同步 SQL 搜索的结果。

    
    
    response = client.sql.get_async(
      id: 'FmdMX2pIang3UWhLRU5QS0lqdlppYncaMUpYQ05oSkpTc3kwZ21EdC1tbFJXQToxOTI=',
      format: 'json'
    )
    puts response
    
    
    GET _sql/async/FmdMX2pIang3UWhLRU5QS0lqdlppYncaMUpYQ05oSkpTc3kwZ21EdC1tbFJXQToxOTI=?format=json

###Request

"获取_sql/异步/<search_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则只有首先提交 SQL 搜索的用户才能使用此 API 检索搜索。

####Limitations

请参阅_SQL Limitations_。

### 路径参数

`<search_id>`

     (Required, string) Identifier for the search. 

### 查询参数

`delimiter`

     (Optional, string) Separator for CSV results. Defaults to `,`. The API only supports this parameter for CSV responses. 
`format`

     (Required, string) Format for the response. You must specify a format using this parameter or the `Accept` HTTP header. If you specify both, the API uses this parameter. For valid values, see [Response Data Formats](sql-rest-format.html "Response Data Formats"). 
`keep_alive`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Retention period for the search and its results. Defaults to the `keep_alive` period for the original SQL search. 
`wait_for_completion_timeout`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Period to wait for complete results. Defaults to no timeout, meaning the request waits for complete search results. 

### 响应正文

获取异步 SQL 搜索 API 返回与 SQL 搜索 API 相同的响应正文。

[« Delete async SQL search API](delete-async-sql-search-api.md) [Get async
SQL search status API »](get-async-sql-search-status-api.md)
