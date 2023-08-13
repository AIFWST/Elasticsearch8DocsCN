

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Get watch API](watcher-api-get-watch.md) [Query watches API »](watcher-
api-query-watches.md)

## 获取观察者统计信息API

检索当前观察程序指标。

###Request

"获取_watcher/统计数据"

"获取_watcher/统计数据/<metric>"

###Prerequisites

* 您必须具有"manage_watcher"或"monitor_watcher"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

### 路径参数

`emit_stacktraces`

     (Optional, Boolean) Defines whether stack traces are generated for each watch that is running. The default value is `false`. 
`<metric>`

    

(可选，枚举)定义响应中包含哪些其他指标。

`current_watches`

     Includes the current executing watches in the response. 
`queued_watches`

     Includes the watches queued for execution in the response. 
`_all`

     Includes all metrics in the response. 

### 响应正文

此 API 始终返回基本指标。您可以使用"指标"参数检索更多指标。

`current_watches`

    

(列表)通过"当前正在执行的监视"指标，可以深入了解观察程序当前正在执行的监视。其他信息是共享当前正在执行的每个监视。此信息包括"watch_id"、其执行开始的时间和当前执行阶段。

    
    
    To include this metric, the `metric` option should be set to `current_watches`
    or `_all`. In addition you can also specify the `emit_stacktraces=true`
    parameter, which adds stack traces for each watch that is being executed. These
    stack traces can give you more insight into an execution of a watch.

`queued_watches`

    

(列表)观察程序调节监视的执行，使其执行不会对节点及其资源造成太大压力。如果同时触发的监视过多，并且没有足够的容量来执行所有监视，则某些监视将排队，等待当前正在执行的监视完成其执行。"排队监视"指标可深入了解这些排队监视。

    
    
    To include this metric, the `metric` option should include `queued_watches` or
    `_all`.

###Examples

以下示例调用"统计信息"API 来检索基本指标：

    
    
    response = client.watcher.stats
    puts response
    
    
    GET _watcher/stats

成功的调用会返回类似于以下示例的 JSON 结构：

    
    
    {
       "watcher_state": "started",  __"watch_count": 1, __"execution_thread_pool": {
          "size": 1000, __"max_size": 1 __}
    }

__

|

观察程序的当前状态，可以是"已启动"、"正在启动"或"已停止"。   ---|---    __

|

当前注册的手表数量。   __

|

已触发且当前排队等待执行的监视数。   __

|

执行线程池的最大大小，指示并发执行监视的最大数量。   以下示例将"metric"选项指定为查询字符串参数，并将包括基本指标和有关当前执行监视的指标：

    
    
    response = client.watcher.stats(
      metric: 'current_watches'
    )
    puts response
    
    
    GET _watcher/stats?metric=current_watches

以下示例将"指标"选项指定为 url 路径的一部分：

    
    
    response = client.watcher.stats(
      metric: 'current_watches'
    )
    puts response
    
    
    GET _watcher/stats/current_watches

以下代码片段显示了捕获执行中的监视的成功 JSON 响应的示例：

    
    
    {
       "watcher_state": "started",
       "watch_count": 2,
       "execution_thread_pool": {
          "queue_size": 1000,
          "max_size": 20
       },
       "current_watches": [ __{
             "watch_id": "slow_condition", __"watch_record_id": "slow_condition_3-2015-05-13T07:42:32.179Z", __"triggered_time": "2015-05-12T11:53:51.800Z", __"execution_time": "2015-05-13T07:42:32.179Z", __"execution_phase": "condition" __}
       ]
    }

__

|

观察程序当前正在执行的所有监视的列表。当当前没有监视正在执行时，将返回一个空数组。捕获的监视按执行时间降序排序。因此，运行时间最长的手表始终位于顶部。   ---|---    __

|

正在执行的监视的 ID。   __

|

监视记录的 ID。   __

|

手表由触发引擎触发的时间。   __

|

手表的执行时间。这是在执行输入之前。   __

|

当前监视执行阶段。可以是"输入"、"条件"、"操作"、"awaits_execution"、"已启动"、"watch_transform"、"中止"、"已完成"。   以下示例指定"queued_watches"指标选项，并包括基本指标和排队的监视：

    
    
    response = client.watcher.stats(
      metric: 'queued_watches'
    )
    puts response
    
    
    GET _watcher/stats/queued_watches

捕获正在执行的监视的成功 JSON 响应示例：

    
    
    {
       "watcher_state": "started",
       "watch_count": 10,
       "execution_thread_pool": {
          "queue_size": 1000,
          "max_size": 20
       },
       "queued_watches": [ __{
                "watch_id": "slow_condition4", __"watch_record_id": "slow_condition4_223-2015-05-21T11:59:59.811Z", __"triggered_time": "2015-05-21T11:59:59.811Z", __"execution_time": "2015-05-21T11:59:59.811Z" __},
          ...
       ]
    }

__

|

当前排队等待执行的所有监视的列表。当没有监视排队时，将返回一个空数组。   ---|---    __

|

排队等待执行的监视的 ID。   __

|

监视记录的 ID。   __

|

手表由触发引擎触发的时间。   __

|

手表进入排队状态的时间。   « 获取手表 API 查询手表 API »