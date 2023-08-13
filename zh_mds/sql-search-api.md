

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[SQL APIs](sql-apis.md)

[« Get async SQL search status API](get-async-sql-search-status-api.md) [SQL
translate API »](sql-translate-api.md)

## SQL 搜索接口

返回 SQL 搜索的结果。

    
    
    POST _sql?format=txt
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC LIMIT 5"
    }

###Request

"_sql"

"发布_sql"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对搜索的数据流、索引或别名具有"读取"索引权限。

####Limitations

请参阅_SQL Limitations_。

### 查询参数

`delimiter`

     (Optional, string) Separator for CSV results. Defaults to `,`. The API only supports this parameter for CSV responses. 
`format`

    

(可选，字符串)响应的格式。有关有效值，请参阅响应数据格式。

您还可以使用"接受"HTTP 标头指定格式。如果同时指定此参数和"接受"HTTP 标头，则此参数优先。

### 请求正文

`allow_partial_search_results`

     (Optional, Boolean) If `true`, returns partial results if there are shard request timeouts or [shard failures](docs-replication.html#shard-failures "Shard failures"). If `false`, returns an error with no partial results. Defaults to `false`. 
`catalog`

    

(可选，字符串)查询的默认目录(群集)。如果未指定，则查询仅对本地群集中的数据执行。

preview] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。 请参阅 [跨集群搜索。

`columnar`

     (Optional, Boolean) If `true`, returns results in a columnar format. Defaults to `false`. The API only supports this parameter for CBOR, JSON, SMILE, and YAML responses. See [Columnar results](sql-rest-columnar.html "Columnar results"). 
`cursor`

     (Optional, string) [Cursor](sql-pagination.html "Paginating through a large response") used to retrieve a set of paginated results. If you specify a `cursor`, the API only uses the `columnar` and `time_zone` request body parameters. It ignores other request body parameters. 

`fetch_size`

     (Optional, integer) Maximum number of rows to return in the response. Defaults to `1000`. 

`field_multi_value_leniency`

     (Optional, Boolean) If `false`, the API returns an error for fields containing [array values](array.html "Arrays"). If `true`, the API returns the first value from the array with no guarantee of consistent results. Defaults to `false`. 
`filter`

     (Optional, object) [Query DSL](query-dsl.html "Query DSL") used to filter documents for the SQL search. See [Filtering using Elasticsearch Query DSL](sql-rest-filtering.html "Filtering using Elasticsearch Query DSL"). 
`index_include_frozen`

     (Optional, Boolean) If `true`, the search can run on frozen indices. Defaults to `false`. 
`keep_alive`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Retention period for an [async](sql-async.html "Run an async SQL search") or [saved synchronous search](sql-async.html#sql-store-searches "Store synchronous SQL searches"). Defaults to `5d` (five days). 
`keep_on_completion`

     (Optional, Boolean) If `true`, Elasticsearch [stores synchronous searches](sql-async.html#sql-store-searches "Store synchronous SQL searches") if you also specify the `wait_for_completion_timeout` parameter. If `false`, Elasticsearch only stores [async searches](sql-async.html "Run an async SQL search") that don't finish before the `wait_for_completion_timeout`. Defaults to `false`. 
`page_timeout`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Minimum retention period for the scroll cursor. After this time period, a [pagination request](sql-pagination.html "Paginating through a large response") might fail because the scroll cursor is no longer available. Subsequent scroll requests prolong the lifetime of the scroll cursor by the duration of `page_timeout` in the scroll request. Defaults to `45s` (45 seconds). 
`params`

     (Optional, array) Values for parameters in the `query`. For syntax, see [Passing parameters to a query](sql-rest-params.html "Passing parameters to a query"). 
`query`

     (Required, object) SQL query to run. For syntax, see [_SQL Language_](sql-spec.html "SQL Language"). 
`request_timeout`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Timeout before the request fails. Defaults to `90s` (90 seconds). 
`runtime_mappings`

    

(可选，对象的对象)在搜索请求中定义一个或多个运行时字段。这些字段优先于具有相同名称的映射字段。

"runtime_mappings"对象的属性

`<field-name>`

    

(必填，对象)运行时字段的配置。键是字段名称。

""的属性<field-name>

`type`

    

(必需，字符串)字段类型，可以是以下任何一种：

* "布尔值" * "复合" * "日期" * "双精度" * "geo_point" * "IP" * "关键字" * "长" * "查找"

`script`

    

(可选，字符串)查询时执行的无痛脚本。该脚本可以访问文档的整个上下文，包括原始"_source"和任何映射字段及其值。

此脚本必须包含"emit"以返回计算值。例如：

    
    
    "script": "emit(doc['@timestamp'].value.dayOfWeekEnum.toString())"

`time_zone`

     (Optional, string) ISO-8601 time zone ID for the search. Several [SQL date/time functions](sql-functions-datetime.html "Date/Time and Interval Functions and Operators") use this time zone. Defaults to `Z` (UTC). 
`wait_for_completion_timeout`

    

(可选，时间值)期间等待完整结果。默认为无超时，表示请求等待完整的搜索结果。如果搜索未在此时间段内完成，则搜索将变为异步。

若要保存同步搜索，必须指定此参数和"keep_on_completion"参数。

### 响应正文

SQL 搜索 API 支持多种响应格式。大多数响应格式使用表格布局。JSON 响应包含以下属性：

`id`

     (string) Identifier for the search. This value is only returned for [async](sql-async.html "Run an async SQL search") and [saved synchronous searches](sql-async.html#sql-store-searches "Store synchronous SQL searches"). For CSV, TSV, and TXT responses, this value is returned in the `Async-ID` HTTP header. 
`is_running`

     (Boolean) If `true`, the search is still running. If `false`, the search has finished. This value is only returned for [async](sql-async.html "Run an async SQL search") and [saved synchronous searches](sql-async.html#sql-store-searches "Store synchronous SQL searches"). For CSV, TSV, and TXT responses, this value is returned in the `Async-partial` HTTP header. 
`is_partial`

    

(布尔值)如果为"true"，则响应不包含完整的搜索结果。如果"is_partial"为"true"，is_running"为"true"，则搜索仍在运行。如果"is_partial"为"真"，但"is_running"为"假"，则由于失败或超时，结果是部分的。

仅对异步和保存的同步搜索返回此值。对于 CSV、TSV 和 TXT 响应，此值在"异步部分"HTTP 标头中返回。

`rows`

     (array of arrays) Values for the search results. 
`columns`

    

(对象数组)搜索结果的列标题。每个对象都是一列。

"列"对象的属性

`name`

     (string) Name of the column. 
`type`

     (string) Data type for the column. 

`cursor`

     (string) [Cursor](sql-pagination.html "Paginating through a large response") for the next set of paginated results. For CSV, TSV, and TXT responses, this value is returned in the `Cursor` HTTP header. 

[« Get async SQL search status API](get-async-sql-search-status-api.md) [SQL
translate API »](sql-translate-api.md)
