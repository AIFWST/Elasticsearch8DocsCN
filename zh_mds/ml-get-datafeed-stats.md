

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get datafeeds API](ml-get-datafeed.md) [Get influencers API »](ml-get-
influencer.md)

## 获取数据馈送统计信息API

检索数据馈送的使用信息。

###Request

"获取_ml/数据馈送/<feed_id>/_stats"

'获取_ml/数据馈送/<feed_id>，<feed_id>/_stats"

"获取_ml/数据馈送/_stats"

"获取_ml/数据馈送/_all/_stats"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

如果数据馈送停止，您收到的唯一信息是"datafeed_id"和"状态"。

此 API 最多返回 10，000 个数据馈送。

### 路径参数

`<feed_id>`

    

(可选，字符串)数据馈送的标识符。它可以是数据馈送标识符或通配符表达式。

您可以使用逗号分隔的数据馈送列表或通配符表达式在单个 API 请求中获取多个数据馈送的统计信息。您可以通过使用"_all"、指定"*"作为数据馈送标识符或省略标识符来获取所有数据馈送的统计信息。

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的数据馈送。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回一个空的"数据馈送"数组，当存在部分匹配时返回结果子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

### 响应正文

API 返回数据馈送计数对象的数组。所有这些属性都是信息性的;您无法更新其值。

`assignment_explanation`

     (string) For started datafeeds only, contains messages relating to the selection of a node. 
`datafeed_id`

     (string) A numerical character string that uniquely identifies the datafeed. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 
`node`

    

(对象)仅对于已启动的数据馈送，此信息与启动数据馈送的节点有关。

Details

`attributes`

     (object) Lists node attributes such as `ml.machine_memory` or `ml.max_open_jobs` settings. 
`ephemeral_id`

     (string) The ephemeral ID of the node. 
`id`

     (string) The unique identifier of the node. 
`name`

     (string) The node name. For example, `0-o0tOo`. 
`transport_address`

     (string) The host and port where transport HTTP connections are accepted. 

`running_state`

    

(对象)包含此数据馈送的运行状态的对象。仅当数据馈送启动时，才会提供它。

Details

`real_time_configured`

     (boolean) Indicates if the datafeed is "real-time"; meaning that the datafeed has no configured `end` time. 
`real_time_running`

     (boolean) Indicates whether the datafeed has finished running on the available past data. For datafeeds without a configured `end` time, this means that the datafeed is now running on "real-time" data. 
`search_interval`

    

(可选，对象)提供数据馈送搜索的最新时间间隔。

Details

`start_ms`

     The start time as an epoch in milliseconds. 
`end_ms`

     The end time as an epoch in milliseconds. 

`state`

    

(字符串)数据馈送的状态，可以是以下值之一：

* "正在启动"：已请求启动数据馈送，但尚未启动。  * "已启动"：数据馈送正在主动接收数据。  * "停止"：已请求数据馈送正常停止，并正在完成其最终操作。  * "停止"：数据馈送已停止，在重新启动之前不会接收数据。

`timing_stats`

    

(对象)一个对象，提供有关此数据馈送的计时方面的统计信息。

Details

`average_search_time_per_bucket_ms`

     (double) The average search time per bucket, in milliseconds. 
`bucket_count`

     (long) The number of buckets processed. 
`exponential_average_search_time_per_hour_ms`

     (double) The exponential average search time per hour, in milliseconds. 
`job_id`

     Identifier for the anomaly detection job. 
`search_count`

     The number of searches run by the datafeed. 
`total_search_time_ms`

     The total time the datafeed spent searching, in milliseconds. 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

    
    
    response = client.ml.get_datafeed_stats(
      datafeed_id: 'datafeed-high_sum_total_sales'
    )
    puts response
    
    
    GET _ml/datafeeds/datafeed-high_sum_total_sales/_stats

API 返回以下结果：

    
    
    {
      "count" : 1,
      "datafeeds" : [
        {
          "datafeed_id" : "datafeed-high_sum_total_sales",
          "state" : "started",
          "node" : {
            "id" : "7bmMXyWCRs-TuPfGJJ_yMw",
            "name" : "node-0",
            "ephemeral_id" : "hoXMLZB0RWKfR9UPPUCxXX",
            "transport_address" : "127.0.0.1:9300",
            "attributes" : {
              "ml.machine_memory" : "17179869184",
              "ml.max_open_jobs" : "512"
            }
          },
          "assignment_explanation" : "",
          "timing_stats" : {
            "job_id" : "high_sum_total_sales",
            "search_count" : 7,
            "bucket_count" : 743,
            "total_search_time_ms" : 134.0,
            "average_search_time_per_bucket_ms" : 0.180349932705249,
            "exponential_average_search_time_per_hour_ms" : 11.514712961628677
          }
        }
      ]
    }

[« Get datafeeds API](ml-get-datafeed.md) [Get influencers API »](ml-get-
influencer.md)
