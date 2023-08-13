

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Cluster Info API](cluster-info.md) [Remote cluster info API »](cluster-
remote-info.md)

## 待处理集群任务API

返回尚未执行的群集级更改。

###Request

"获取/_cluster/pending_tasks"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

挂起的集群任务 API 返回尚未执行的任何集群级更改(例如创建索引、更新映射、分配或失败分片)的列表。

此 API 返回群集状态的任何挂起更新的列表。这些与任务管理 API 报告的任务不同，后者包括定期任务和用户启动的任务，例如节点统计信息、搜索查询或创建索引请求。但是，如果用户启动的任务(如创建索引命令)导致群集状态更新，则任务 API 和挂起的群集任务 API 可能会报告此任务的活动。

### 路径参数

`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 响应正文

`tasks`

     (object) A list of pending tasks. 
`insert_order`

     (integer) The number that represents when the task has been inserted into the task queue. 
`priority`

     (string) The priority of the pending task. The valid priorities in descending priority order are: `IMMEDIATE` > `URGENT` > `HIGH` > `NORMAL` > `LOW` > `LANGUID`. 
`source`

     (string) A general description of the cluster task that may include a reason and origin. 
`executing`

     (boolean) True or false, indicating whether the pending tasks is currently getting executed or not. 
`time_in_queue_millis`

     (integer) The time expressed in milliseconds since the task is waiting for being performed. 
`time_in_queue`

     (string) The time since the task is waiting for being performed. 

###Examples

通常，请求将返回一个空列表，因为集群级别的更改很快。但是，如果有任务排队，响应将如下所示：

    
    
    {
       "tasks": [
          {
             "insert_order": 101,
             "priority": "URGENT",
             "source": "create-index [foo_9], cause [api]",
             "executing" : true,
             "time_in_queue_millis": 86,
             "time_in_queue": "86ms"
          },
          {
             "insert_order": 46,
             "priority": "HIGH",
             "source": "shard-started ([foo_2][1], node[tMTocMvQQgGCkj7QDHl3OA], [P], s[INITIALIZING]), reason [after recovery from shard_store]",
             "executing" : false,
             "time_in_queue_millis": 842,
             "time_in_queue": "842ms"
          },
          {
             "insert_order": 45,
             "priority": "HIGH",
             "source": "shard-started ([foo_2][0], node[tMTocMvQQgGCkj7QDHl3OA], [P], s[INITIALIZING]), reason [after recovery from shard_store]",
             "executing" : false,
             "time_in_queue_millis": 858,
             "time_in_queue": "858ms"
          }
      ]
    }

[« Cluster Info API](cluster-info.md) [Remote cluster info API »](cluster-
remote-info.md)
