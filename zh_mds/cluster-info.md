

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Nodes stats API](cluster-nodes-stats.md) [Pending cluster tasks API
»](cluster-pending.md)

## 集群信息接口

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

返回群集信息。

###Request

"获取/_info/<target>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

您可以使用群集信息 API 检索群集的信息。

### 路径参数

`<target>`

    

(字符串)限制返回到特定"目标"的信息。以下选项的逗号分隔列表：

`_all`

     All the information available. Can not be mixed with other targets. 
`http`

     HTTP connection information. 
`ingest`

     Ingest information. 
`thread_pool`

     Statistics about each thread pool, including current size, queue size and rejected tasks. 
`script`

     Contains script statistics of the cluster. 

### 响应正文

`cluster_name`

     (string) Name of the cluster. Based on the [Cluster name setting](important-settings.html#cluster-name "Cluster name setting") setting. 

`http`

    

(对象)包含群集的 http 信息。

"http"的属性

`current_open`

     (integer) Current number of open HTTP connections for the cluster. 
`total_opened`

     (integer) Total number of HTTP connections opened for the cluster. 
`clients`

    

(对象数组)有关当前和最近关闭的 HTTP 客户端连接的信息。关闭时间超过 thehttp.client_stats.closed_channels.max_age 设置的客户端将不在此处显示。

"客户端"的属性

`id`

     (integer) Unique ID for the HTTP client. 
`agent`

     (string) Reported agent for the HTTP client. If unavailable, this property is not included in the response. 
`local_address`

     (string) Local address for the HTTP connection. 
`remote_address`

     (string) Remote address for the HTTP connection. 
`last_uri`

     (string) The URI of the client's most recent request. 
`x_forwarded_for`

     (string) Value from the client's `x-forwarded-for` HTTP header. If unavailable, this property is not included in the response. 
`x_opaque_id`

     (string) Value from the client's `x-opaque-id` HTTP header. If unavailable, this property is not included in the response. 
`opened_time_millis`

     (integer) Time at which the client opened the connection. 
`closed_time_millis`

     (integer) Time at which the client closed the connection if the connection is closed. 
`last_request_time_millis`

     (integer) Time of the most recent request from this client. 
`request_count`

     (integer) Number of requests from this client. 
`request_size_bytes`

     (integer) Cumulative size in bytes of all requests from this client. 

`ingest`

    

(对象)包含群集的引入信息。

"摄取"的属性

`total`

    

(对象)包含有关群集的引入操作的信息。

"总计"的属性

`count`

     (integer) Total number of documents ingested across the cluster. 
`time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent preprocessing ingest documents across the cluster. 
`time_in_millis`

     (integer) Total time, in milliseconds, spent preprocessing ingest documents across the cluster. 
`current`

     (integer) Total number of documents currently being ingested. 
`failed`

     (integer) Total number of failed ingest operations across the cluster. 

`pipelines`

    

(对象)包含有关群集的引入管道的信息。

"管道"的属性

`<pipeline_id>`

    

(对象)包含有关引入管道的信息。

""的属性<pipeline_id>

`count`

     (integer) Number of documents preprocessed by the ingest pipeline. 
`time`

     ([time value](api-conventions.html#time-units "Time units")) Total time spent preprocessing documents in the ingest pipeline. 
`time_in_millis`

     (integer) Total time, in milliseconds, spent preprocessing documents in the ingest pipeline. 
`failed`

     (integer) Total number of failed operations for the ingest pipeline. 
`processors`

    

(对象数组)包含有关引入管道的引入处理器的信息。

"处理器"的属性

`<processor>`

    

(对象)包含引入处理器的信息。

""的属性<processor>

`count`

     (integer) Number of documents transformed by the processor. 
`time`

     ([time value](api-conventions.html#time-units "Time units")) Time spent by the processor transforming documents. 
`time_in_millis`

     (integer) Time, in milliseconds, spent by the processor transforming documents. 
`current`

     (integer) Number of documents currently being transformed by the processor. 
`failed`

     (integer) Number of failed operations for the processor. 

`thread_pool`

    

(对象)包含有关群集的线程池的信息。

"thread_pool"的属性

`<thread_pool_name>`

    

(对象)包含有关名称为 '' 的群集的线程池的信息<thread_pool_name>。

""的属性<thread_pool_name>

`threads`

     (integer) Number of threads in the thread pool. 
`queue`

     (integer) Number of tasks in queue for the thread pool. 
`active`

     (integer) Number of active threads in the thread pool. 
`rejected`

     (integer) Number of tasks rejected by the thread pool executor. 
`largest`

     (integer) Highest number of active threads in the thread pool. 
`completed`

     (integer) Number of tasks completed by the thread pool executor. 

`script`

    

(对象)包含群集的脚本统计信息。

"脚本"的属性

`compilations`

     (integer) Total number of inline script compilations performed by the cluster. 
`compilations_history`

     (object) Contains the recent history of script compilations. 

"compilations_history"的属性

`5m`

     (long) The number of script compilations in the last five minutes. 
`15m`

     (long) The number of script compilations in the last fifteen minutes. 
`24h`

     (long) The number of script compilations in the last twenty-four hours. 

`cache_evictions`

     (integer) Total number of times the script cache has evicted old data. 
`cache_evictions_history`

     (object) Contains the recent history of script cache evictions. 

"cache_evictions"的属性

`5m`

     (long) The number of script cache evictions in the last five minutes. 
`15m`

     (long) The number of script cache evictions in the last fifteen minutes. 
`24h`

     (long) The number of script cache evictions in the last twenty-four hours. 

`compilation_limit_triggered`

     (integer) Total number of times the [script compilation](circuit-breaker.html#script-compilation-circuit-breaker "Script compilation circuit breaker") circuit breaker has limited inline script compilations. 

###Examples

    
    
    # returns all stats info of the cluster
    GET /_info/_all
    
    # returns the http info of the cluster
    GET /_info/http
    
    # returns the http info of the cluster
    GET /_info/ingest
    
    # returns the thread_pool info of the cluster
    GET /_info/thread_pool
    
    # returns the script info of the cluster
    GET /_info/script
    
    # returns the http and ingest info of the cluster
    GET /_info/http,ingest

[« Nodes stats API](cluster-nodes-stats.md) [Pending cluster tasks API
»](cluster-pending.md)
