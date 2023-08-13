

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat templates API](cat-templates.md) [cat trained model API »](cat-
trained-model.md)

## 猫线程池API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用节点信息 API。

返回群集中每个节点的线程池统计信息。返回的信息包括所有内置线程池和自定义线程池。

###Request

"获取/_cat/thread_pool/<thread_pool>"

"获取/_cat/thread_pool"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

### 路径参数

`<thread_pool>`

     (Optional, string) Comma-separated list of thread pool names used to limit the request. Accepts wildcard expressions. 

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将按下面列出的顺序返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

`node_name`

     (Default) Node name, such as `I8hydUG`. 
`name`

     (Default) Name of the thread pool, such as `analyze` or `generic`. 
`active`, `a`

     (Default) Number of active threads in the current thread pool. 
`queue`,`q`

     (Default) Number of tasks in the queue for the current thread pool. 
`rejected`, `r`

     (Default) Number of tasks rejected by the thread pool executor. 
`completed`, `c`

     Number of tasks completed by the thread pool executor. 
`core`, `cr`

     Configured core number of active threads allowed in the current thread pool. 
`ephemeral_id`,`eid`

     Ephemeral node ID. 
`host`, `h`

     Hostname for the current node. 
`ip`, `i`

     IP address for the current node. 
`keep_alive`, `k`

     Configured keep alive time for threads. 
`largest`, `l`

     Highest number of active threads in the current thread pool. 
`max`, `mx`

     Configured maximum number of active threads allowed in the current thread pool. 
`node_id`, `id`

     ID of the node, such as `k0zy`. 
`pid`, `p`

     Process ID of the running node. 
`pool_size`, `psz`

     Number of threads in the current thread pool. 
`port`, `po`

     Bound transport port for the current node. 
`queue_size`, `qs`

     Maximum number of tasks permitted in the queue for the current thread pool. 
`size`, `sz`

     Configured fixed number of active threads allowed in the current thread pool. 
`type`, `t`

     Type of thread pool. Returned values are `fixed`, `fixed_auto_queue_size`, `direct`, or `scaling`. 

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

#### 默认列的示例

    
    
    response = client.cat.thread_pool
    puts response
    
    
    GET /_cat/thread_pool

API 返回以下响应：

    
    
    node-0 analyze             0 0 0
    ...
    node-0 fetch_shard_started 0 0 0
    node-0 fetch_shard_store   0 0 0
    node-0 flush               0 0 0
    ...
    node-0 write               0 0 0

#### 显式列的示例

以下 API 请求返回"id"、"名称"、"活动"、"已拒绝"和"已完成"列。该请求将返回的信息限制为"泛型"线程池。

    
    
    response = client.cat.thread_pool(
      thread_pool_patterns: 'generic',
      v: true,
      h: 'id,name,active,rejected,completed'
    )
    puts response
    
    
    GET /_cat/thread_pool/generic?v=true&h=id,name,active,rejected,completed

API 返回以下响应：

    
    
    id                     name    active rejected completed
    0EWUhXeBQtaVGlexUeVwMg generic      0        0        70

[« cat templates API](cat-templates.md) [cat trained model API »](cat-
trained-model.md)
