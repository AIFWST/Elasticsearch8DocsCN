

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat data frame analytics API](cat-dfanalytics.md) [cat fielddata API
»](cat-fielddata.md)

## cat datafeedsAPI

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取数据馈送统计信息 API。

返回有关数据馈送的配置和使用情况信息。

###Request

'GET /_cat/ml/datafeeds/<feed_id>'

'GET /_cat/ml/datafeeds'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"monitor_ml"、"监控"、"manage_ml"或"管理"集群权限才能使用此 API。请参阅安全特权和机器学习安全特权。

###Description

数据馈送从 Elasticsearch 检索数据，以便通过异常检测作业进行分析。有关详细信息，请参阅数据馈送。

此 API 最多返回 10，000 个作业。

### 路径参数

`<feed_id>`

     (Optional, string) A numerical character string that uniquely identifies the datafeed. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的数据馈送。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回一个空的"数据馈送"数组，当存在部分匹配时返回结果子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

"assignment_explanation"、"ae"

     For started datafeeds only, contains messages relating to the selection of a node. 
`buckets.count`, `bc`, `bucketsCount`

     (Default) The number of buckets processed. 
`id`

     (Default) A numerical character string that uniquely identifies the datafeed. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 
`node.address`, `na`, `nodeAddress`

    

节点的网络地址。

仅对于已启动的数据馈送，此信息与启动数据馈送的节点有关。

'node.ephemeral_id'， 'ne'， 'nodeEphemeralId'

    

节点的临时 ID。

仅对于已启动的数据馈送，此信息与启动数据馈送的节点有关。

'node.id'， 'ni'， 'nodeId'

    

节点的唯一标识符。

仅对于已启动的数据馈送，此信息与启动数据馈送的节点有关。

"node.name"、"nn"、"节点名称"

    

节点名称。

仅对于已启动的数据馈送，此信息与启动数据馈送的节点有关。

'search.bucket_avg'， 'sba'， 'searchBucketAvg'

     The average search time per bucket, in milliseconds. 
`search.count`, `sc`, `searchCount`

     (Default) The number of searches run by the datafeed. 
`search.exp_avg_hour`, `seah`, `searchExpAvgHour`

     The exponential average search time per hour, in milliseconds. 
`search.time`, `st`, `searchTime`

     The total time the datafeed spent searching, in milliseconds. 
`state`, `s`

    

(默认)数据馈送的状态，可以是以下值之一：

* "正在启动"：已请求启动数据馈送，但尚未启动。  * "已启动"：数据馈送正在主动接收数据。  * "停止"：已请求数据馈送正常停止，并正在完成其最终操作。  * "停止"：数据馈送已停止，在重新启动之前不会接收数据。

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    response = client.cat.ml_datafeeds(
      v: true
    )
    puts response
    
    
    GET _cat/ml/datafeeds?v=true
    
    
    id                              state buckets.count search.count
    datafeed-high_sum_total_sales stopped 743          7
    datafeed-low_request_rate     stopped 1457         3
    datafeed-response_code_rates  stopped 1460         18
    datafeed-url_scanning         stopped 1460         18

[« cat data frame analytics API](cat-dfanalytics.md) [cat fielddata API
»](cat-fielddata.md)
