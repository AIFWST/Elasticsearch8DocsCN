

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Nodes feature usage API](cluster-nodes-usage.md) [Nodes info API
»](cluster-nodes-info.md)

## 节点热线程API

返回群集中每个选定节点上的热线程。

###Request

"获取/_nodes/hot_threads"

"获取/_nodes/<node_id>/hot_threads"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

此 API 生成群集中每个选定节点上的热线程的细分。输出为纯文本，其中包含每个节点的热门线程的细分。

### 路径参数

`<node_id>`

     (Optional, string) Comma-separated list of node IDs or names used to limit returned information. 

### 查询参数

`ignore_idle_threads`

     (Optional, Boolean) If true, known idle threads (e.g. waiting in a socket select, or to get a task from an empty queue) are filtered out. Defaults to true. 
`interval`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The interval to do the second sampling of threads. Defaults to `500ms`. 
`snapshots`

     (Optional, integer) Number of samples of thread stacktrace. Defaults to `10`. 
`threads`

     (Optional, integer) Specifies the number of hot threads to provide information for. Defaults to `3`. If you are using this API for troubleshooting, set this parameter to a large number (e.g. `9999`) to get information about all the threads in the system. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`type`

     (Optional, string) The type to sample. Available options are `block`, `cpu`, and `wait`. Defaults to `cpu`. 

###Examples

    
    
    response = client.nodes.hot_threads
    puts response
    
    response = client.nodes.hot_threads(
      node_id: 'nodeId1,nodeId2'
    )
    puts response
    
    
    GET /_nodes/hot_threads
    GET /_nodes/nodeId1,nodeId2/hot_threads

[« Nodes feature usage API](cluster-nodes-usage.md) [Nodes info API
»](cluster-nodes-info.md)
