

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Cluster get settings API](cluster-get-settings.md) [Health API »](health-
api.md)

## 集群健康接口

返回群集的运行状况。

###Request

'获取/_cluster/健康/<target>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

群集运行状况 API 返回有关群集运行状况的简单状态。您还可以使用 API 仅获取指定数据流和索引的运行状况。对于数据流，API 检索流的支持索引的运行状况。

群集运行状况为："绿色"、"黄色"或"红色"。在分片级别，"红色"状态表示集群中未分配特定分片，"黄色"表示已分配主分片但未分配副本，"绿色"表示已分配所有分片。索引级别状态由最差分片状态控制。集群状态由最差索引状态控制。

API 的主要优点之一是能够等到群集达到某个高水位线运行状况级别。例如，以下内容将等待 50 秒，以使集群达到"黄色"级别(如果在 50 秒之前达到"绿色"或"黄色"状态，它将在此时返回)：

    
    
    $response = $client->cluster()->health();
    
    
    resp = client.cluster.health(wait_for_status="yellow", timeout="50s")
    print(resp)
    
    
    response = client.cluster.health(
      wait_for_status: 'yellow',
      timeout: '50s'
    )
    puts response
    
    
    res, err := es.Cluster.Health(
    	es.Cluster.Health.WithTimeout(time.Duration(50000000000)),
    	es.Cluster.Health.WithWaitForStatus("yellow"),
    )
    fmt.Println(res, err)
    
    
    const response = await client.cluster.health({
      wait_for_status: 'yellow',
      timeout: '50s'
    })
    console.log(response)
    
    
    GET /_cluster/health?wait_for_status=yellow&timeout=50s

### 路径参数

`<target>`

    

(可选，字符串)用于限制请求的数据流、索引和索引别名的逗号分隔列表。支持通配符表达式 ('*')。

要定位集群中的所有数据流和索引，请省略此参数或使用"_all"或"*"。

### 查询参数

`level`

     (Optional, string) Can be one of `cluster`, `indices` or `shards`. Controls the details level of the health information returned. Defaults to `cluster`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`wait_for_active_shards`

     (Optional, string) A number controlling to how many active shards to wait for, `all` to wait for all shards in the cluster to be active, or `0` to not wait. Defaults to `0`. 
`wait_for_events`

     (Optional, string) Can be one of `immediate`, `urgent`, `high`, `normal`, `low`, `languid`. Wait until all currently queued events with the given priority are processed. 
`wait_for_no_initializing_shards`

     (Optional, Boolean) A boolean value which controls whether to wait (until the timeout provided) for the cluster to have no shard initializations. Defaults to false, which means it will not wait for initializing shards. 
`wait_for_no_relocating_shards`

     (Optional, Boolean) A boolean value which controls whether to wait (until the timeout provided) for the cluster to have no shard relocations. Defaults to false, which means it will not wait for relocating shards. 
`wait_for_nodes`

     (Optional, string) The request waits until the specified number `N` of nodes is available. It also accepts `>=N`, `<=N`, `>N` and `<N`. Alternatively, it is possible to use `ge(N)`, `le(N)`, `gt(N)` and `lt(N)` notation. 
`wait_for_status`

     (Optional, string) One of `green`, `yellow` or `red`. Will wait (until the timeout provided) until the status of the cluster changes to the one provided or better, i.e. `green` > `yellow` > `red`. By default, will not wait for any status. 

### 响应正文

`cluster_name`

     (string) The name of the cluster. 
`status`

    

(字符串)集群的运行状况，基于其主分片和副本分片的状态。状态为：

* "绿色"：分配所有分片。  * 'yellow'：已分配所有主分片，但未分配一个或多个副本分片。如果群集中的某个节点发生故障，则在修复该节点之前，某些数据可能不可用。  * "red"：一个或多个主分片未分配，因此某些数据不可用。在分配主分片时，这可能会在集群启动期间短暂发生。

`timed_out`

     (Boolean) If `false` the response returned within the period of time that is specified by the `timeout` parameter (`30s` by default). 
`number_of_nodes`

     (integer) The number of nodes within the cluster. 
`number_of_data_nodes`

     (integer) The number of nodes that are dedicated data nodes. 
`active_primary_shards`

     (integer) The number of active primary shards. 
`active_shards`

     (integer) The total number of active primary and replica shards. 
`relocating_shards`

     (integer) The number of shards that are under relocation. 
`initializing_shards`

     (integer) The number of shards that are under initialization. 
`unassigned_shards`

     (integer) The number of shards that are not allocated. 
`delayed_unassigned_shards`

     (integer) The number of shards whose allocation has been delayed by the timeout settings. 
`number_of_pending_tasks`

     (integer) The number of cluster-level changes that have not yet been executed. 
`number_of_in_flight_fetch`

     (integer) The number of unfinished fetches. 
`task_max_waiting_in_queue_millis`

     (integer) The time expressed in milliseconds since the earliest initiated task is waiting for being performed. 
`active_shards_percent_as_number`

     (float) The ratio of active shards in the cluster expressed as a percentage. 

###Examples

    
    
    $response = $client->cluster()->health();
    
    
    resp = client.cluster.health()
    print(resp)
    
    
    response = client.cluster.health
    puts response
    
    
    res, err := es.Cluster.Health()
    fmt.Println(res, err)
    
    
    const response = await client.cluster.health()
    console.log(response)
    
    
    GET _cluster/health

如果安静的单节点集群具有具有一个分片和一个副本的单个索引，则 API 将返回以下响应：

    
    
    {
      "cluster_name" : "testcluster",
      "status" : "yellow",
      "timed_out" : false,
      "number_of_nodes" : 1,
      "number_of_data_nodes" : 1,
      "active_primary_shards" : 1,
      "active_shards" : 1,
      "relocating_shards" : 0,
      "initializing_shards" : 0,
      "unassigned_shards" : 1,
      "delayed_unassigned_shards": 0,
      "number_of_pending_tasks" : 0,
      "number_of_in_flight_fetch": 0,
      "task_max_waiting_in_queue_millis": 0,
      "active_shards_percent_as_number": 50.0
    }

以下是在"分片"级别获取集群运行状况的示例：

    
    
    response = client.cluster.health(
      index: 'my-index-000001',
      level: 'shards'
    )
    puts response
    
    
    GET /_cluster/health/my-index-000001?level=shards

[« Cluster get settings API](cluster-get-settings.md) [Health API »](health-
api.md)
