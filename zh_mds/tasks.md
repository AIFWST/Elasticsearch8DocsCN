

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Remote cluster info API](cluster-remote-info.md) [Voting configuration
exclusions API »](voting-config-exclusions.md)

## 任务管理接口

任务管理 API 是新的，仍应被视为测试版功能。API 可能会以不向后兼容的方式更改。有关功能状态，请参阅 #51628。

返回有关群集中当前执行的任务的信息。

###Request

"获取/_tasks/<task_id>"

"获取/_tasks"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

任务管理 API 返回有关当前在群集中的一个或多个节点上执行的任务的信息。

### 路径参数

`<task_id>`

     (Optional, string) ID of the task to return (`node_id:task_number`). 

### 查询参数

`actions`

    

(可选，字符串)用于限制请求的操作的逗号分隔列表或通配符表达式。

省略此参数以返回所有操作。

`detailed`

     (Optional, Boolean) If `true`, the response includes detailed information about shard recoveries. Defaults to `false`. 
`group_by`

    

(可选，字符串)用于对响应中的任务进行分组的键。

可能的值为：

`nodes`

     (Default) Node ID 
`parents`

     Parent task ID 
`none`

     Do not group tasks. 

`nodes`

     (Optional, string) Comma-separated list of node IDs or names used to limit returned information. 
`parent_task_id`

    

(可选，字符串)用于限制返回信息的父任务 ID。

要返回所有任务，请省略此参数或使用值"-1"。

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`wait_for_completion`

     (Optional, Boolean) If `true`, the request blocks until all found tasks are complete. Defaults to `false`. 

### 响应码

"404"(缺少资源)

     If `<task_id>` is specified but not found, this code indicates that there are no resources that match the request. 

###Examples

    
    
    response = client.tasks.list
    puts response
    
    response = client.tasks.list(
      nodes: 'nodeId1,nodeId2'
    )
    puts response
    
    response = client.tasks.list(
      nodes: 'nodeId1,nodeId2',
      actions: 'cluster:*'
    )
    puts response
    
    
    GET _tasks __GET _tasks?nodes=nodeId1,nodeId2 __GET _tasks?nodes=nodeId1,nodeId2 &actions=cluster:* __

__

|

检索群集中所有节点上当前运行的所有任务。   ---|---    __

|

检索在节点"nodeId1"和"nodeId2"上运行的所有任务。有关如何选择单个节点的详细信息，请参阅 NodeSpecification。   __

|

检索在节点"nodeId1"和"nodeId2"上运行的所有与群集相关的任务。   API 返回以下结果：

    
    
    {
      "nodes" : {
        "oTUltX4IQMOUUVeiohTt8A" : {
          "name" : "H5dfFeA",
          "transport_address" : "127.0.0.1:9300",
          "host" : "127.0.0.1",
          "ip" : "127.0.0.1:9300",
          "tasks" : {
            "oTUltX4IQMOUUVeiohTt8A:124" : {
              "node" : "oTUltX4IQMOUUVeiohTt8A",
              "id" : 124,
              "type" : "direct",
              "action" : "cluster:monitor/tasks/lists[n]",
              "start_time_in_millis" : 1458585884904,
              "running_time_in_nanos" : 47402,
              "cancellable" : false,
              "parent_task_id" : "oTUltX4IQMOUUVeiohTt8A:123"
            },
            "oTUltX4IQMOUUVeiohTt8A:123" : {
              "node" : "oTUltX4IQMOUUVeiohTt8A",
              "id" : 123,
              "type" : "transport",
              "action" : "cluster:monitor/tasks/lists",
              "start_time_in_millis" : 1458585884904,
              "running_time_in_nanos" : 236042,
              "cancellable" : false
            }
          }
        }
      }
    }

#### 从特定任务中检索信息

还可以检索特定任务的信息。以下示例检索有关任务'oTUltX4IQMOUUVeiohTt8A：124'的信息：

    
    
    response = client.tasks.get(
      task_id: 'oTUltX4IQMOUUVeiohTt8A:124'
    )
    puts response
    
    
    GET _tasks/oTUltX4IQMOUUVeiohTt8A:124

如果未找到任务，API 将返回 404。

检索特定任务的所有子任务：

    
    
    response = client.tasks.list(
      parent_task_id: 'oTUltX4IQMOUUVeiohTt8A:123'
    )
    puts response
    
    
    GET _tasks?parent_task_id=oTUltX4IQMOUUVeiohTt8A:123

如果未找到父级，API 不会返回 404。

#### 获取有关任务的详细信息

您还可以使用"详细"请求参数来获取有关正在运行的任务的更多信息。这对于区分任务很有用，但执行成本更高。例如，使用"详细"请求参数获取所有搜索：

    
    
    response = client.tasks.list(
      actions: '*search',
      detailed: true
    )
    puts response
    
    
    GET _tasks?actions=*search&detailed

API 返回以下结果：

    
    
    {
      "nodes" : {
        "oTUltX4IQMOUUVeiohTt8A" : {
          "name" : "H5dfFeA",
          "transport_address" : "127.0.0.1:9300",
          "host" : "127.0.0.1",
          "ip" : "127.0.0.1:9300",
          "tasks" : {
            "oTUltX4IQMOUUVeiohTt8A:464" : {
              "node" : "oTUltX4IQMOUUVeiohTt8A",
              "id" : 464,
              "type" : "transport",
              "action" : "indices:data/read/search",
              "description" : "indices[test], types[test], search_type[QUERY_THEN_FETCH], source[{\"query\":...}]",
              "start_time_in_millis" : 1483478610008,
              "running_time_in_nanos" : 13991383,
              "cancellable" : true,
              "cancelled" : false
            }
          }
        }
      }
    }

新的"description"字段包含人类可读的文本，用于标识任务正在执行的特定请求，例如标识由搜索任务执行的搜索请求，如上例所示。其他类型的任务有不同的描述，例如具有源和目标的"_reindex"或仅具有请求数和目标索引的"_bulk"。许多请求只有空的描述，因为有关请求的更多详细信息不容易获得，或者对识别请求特别有用。

带有"详细"的"_tasks"请求也可能返回"状态"。这是任务内部状态的报告。因此，其格式因任务而异。虽然我们试图保持特定任务的"状态"在不同版本之间保持一致，但这并不总是可能的，因为我们有时会更改实现。在这种情况下，我们可能会从特定请求的"状态"中删除字段，因此您对状态所做的任何解析都可能在次要版本中中断。

#### 等待完成

任务 API 还可用于等待特定任务的完成。以下调用将阻塞 10 秒或直到 id'oTUltX4IQMOUUVeiohTt8A：12345' 的任务完成。

    
    
    response = client.tasks.get(
      task_id: 'oTUltX4IQMOUUVeiohTt8A:12345',
      wait_for_completion: true,
      timeout: '10s'
    )
    puts response
    
    
    GET _tasks/oTUltX4IQMOUUVeiohTt8A:12345?wait_for_completion=true&timeout=10s

您还可以等待某些操作类型的所有任务完成。此命令将等待所有"重新索引"任务完成：

    
    
    response = client.tasks.list(
      actions: '*reindex',
      wait_for_completion: true,
      timeout: '10s'
    )
    puts response
    
    
    GET _tasks?actions=*reindex&wait_for_completion=true&timeout=10s

#### 任务取消

如果长时间运行的任务支持取消，则可以使用取消任务 API 取消该任务。以下示例取消任务'oTUltX4IQMOUUVeiohTt8A：12345'：

    
    
    response = client.tasks.cancel(
      task_id: 'oTUltX4IQMOUUVeiohTt8A:12345'
    )
    puts response
    
    
    POST _tasks/oTUltX4IQMOUUVeiohTt8A:12345/_cancel

任务取消命令支持与列表任务命令相同的任务选择参数，因此可以同时取消多个任务。例如，以下命令将取消在节点"nodeId1"和"nodeId2"上运行的所有重新索引任务。

    
    
    response = client.tasks.cancel(
      nodes: 'nodeId1,nodeId2',
      actions: '*reindex'
    )
    puts response
    
    
    POST _tasks/_cancel?nodes=nodeId1,nodeId2&actions=*reindex

任务在取消后可能会继续运行一段时间，因为它可能无法立即安全地停止其当前活动，或者因为 Elasticsearch 必须先完成其他任务的工作，然后才能处理取消。列出任务 API 将继续列出这些已取消的任务，直到它们完成。对列表任务 API 的响应中的"已取消"标志表示取消命令已处理，任务将尽快停止。要排查取消任务未及时完成的原因，请使用带有"详细"参数的列表任务 API 来标识系统正在运行的其他任务，并使用节点热线程 API 获取有关系统正在执行的工作的详细信息，而不是完成已取消的任务。

#### 任务分组

任务 API 命令返回的任务列表可以按节点(默认)或使用"group_by"参数按父任务分组。以下命令会将分组更改为父任务：

    
    
    response = client.tasks.list(
      group_by: 'parents'
    )
    puts response
    
    
    GET _tasks?group_by=parents

可以通过将"none"指定为"group_by"参数来禁用分组：

    
    
    response = client.tasks.list(
      group_by: 'none'
    )
    puts response
    
    
    GET _tasks?group_by=none

#### 识别正在运行的任务

在HTTP请求头上提供的"X-Opaque-Id"头将在响应中以及任务信息中的"头"字段中作为头返回。这允许跟踪某些调用，或将某些任务与启动它们的客户端相关联：

    
    
    curl -i -H "X-Opaque-Id: 123456" "http://localhost:9200/_tasks?group_by=parents"

API 返回以下结果：

    
    
    HTTP/1.1 200 OK
    X-Opaque-Id: 123456 __content-type: application/json; charset=UTF-8
    content-length: 831
    
    {
      "tasks" : {
        "u5lcZHqcQhu-rUoFaqDphA:45" : {
          "node" : "u5lcZHqcQhu-rUoFaqDphA",
          "id" : 45,
          "type" : "transport",
          "action" : "cluster:monitor/tasks/lists",
          "start_time_in_millis" : 1513823752749,
          "running_time_in_nanos" : 293139,
          "cancellable" : false,
          "headers" : {
            "X-Opaque-Id" : "123456" __},
          "children" : [
            {
              "node" : "u5lcZHqcQhu-rUoFaqDphA",
              "id" : 46,
              "type" : "direct",
              "action" : "cluster:monitor/tasks/lists[n]",
              "start_time_in_millis" : 1513823752750,
              "running_time_in_nanos" : 92133,
              "cancellable" : false,
              "parent_task_id" : "u5lcZHqcQhu-rUoFaqDphA:45",
              "headers" : {
                "X-Opaque-Id" : "123456" __}
            }
          ]
        }
      }
    }

__

|

id 作为响应标头的一部分 ---|--- __

|

由 REST 请求启动的任务的 id __

|

由 REST 请求启动的任务的子任务 « 远程群集信息 API 投票配置排除项 API »