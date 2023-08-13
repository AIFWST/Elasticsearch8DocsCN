

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Node lifecycle APIs](node-lifecycle-api.md)

[« Node lifecycle APIs](node-lifecycle-api.md) [Get shutdown API »](get-
shutdown.md)

## 把关机接口

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

准备要关闭的节点。

###Request

"放_nodes/<node-id>/关机"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。  * 如果启用了操作员权限功能，您必须是操作员才能使用此 API。

###Description

根据需要将正在进行的任务和索引分片迁移到其他节点，以准备要重新启动或关闭并从群集中删除的阳极。这确保了 Elasticsearch 可以安全地停止，同时将对集群的干扰降至最低。

您必须指定关机类型："重新启动"、"删除"或"替换"。如果阳极已准备好关闭，则可以使用此 API 更改关闭类型。

此 API 不会终止 Elasticsearch 进程。监控节点关闭状态，以确定何时可以安全地停止 Elasticsearch。

### 路径参数

`<node-id>`

     (Required, string) The ID of the node you want to prepare for shutdown. If you specify a node that is offline, it will be prepared for shut down when it rejoins the cluster. 

此参数针对群集的活动节点进行**非**验证。这使您能够注册节点以在脱机时关闭。如果指定了无效的节点 ID，则不会引发错误。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`type`

     (Required, string) Valid values are `restart`, `remove`, or `replace`. Use `restart` when you need to temporarily shut down a node to perform an upgrade, make configuration changes, or perform other maintenance. Because the node is expected to rejoin the cluster, data is not migrated off of the node. Use `remove` when you need to permanently remove a node from the cluster. The node is not marked ready for shutdown until data is migrated off of the node. Use `replace` to do a 1:1 replacement of a node with another node. Certain allocation decisions will be ignored (such as disk watermarks) in the interest of true replacement of the source node with the target node. During a replace-type shutdown, rollover and index creation may result in unassigned shards, and shrink may fail until the replacement is complete. 
`reason`

     (Required, string) A human-readable reason that the node is being shut down. This field provides information for other cluster operators; it does not affect the shut down process. 
`allocation_delay`

     (Optional, string) Only valid if `type` is `restart`. Controls how long Elasticsearch will wait for the node to restart and join the cluster before reassigning its shards to other nodes. This works the same as [delaying allocation](delayed-allocation.html "Delaying allocation when a node leaves") with the `index.unassigned.node_left.delayed_timeout` setting. If you specify both a restart allocation delay and an index-level allocation delay, the longer of the two is used. 
`target_node_name`

     (Optional, string) Only valid if `type` is `replace`. Specifies the name of the node that is replacing the node being shut down. Shards from the shut down node are only allowed to be allocated to the target node, and no other data will be allocated to the target node. During relocation of data certain allocation rules are ignored, such as disk watermarks or user attribute filtering rules. 

###Examples

注册要关闭的节点：

    
    
    response = client.shutdown.put_node(
      node_id: 'USpTGYaBSIKbgSUJR2Z9lg',
      body: {
        type: 'restart',
        reason: 'Demonstrating how the node shutdown API works',
        allocation_delay: '20m'
      }
    )
    puts response
    
    
    PUT /_nodes/USpTGYaBSIKbgSUJR2Z9lg/shutdown
    {
      "type": "restart", __"reason": "Demonstrating how the node shutdown API works",
      "allocation_delay": "20m"
    }

__

|

准备要重新启动的节点。对将从群集中永久删除的节点使用"删除"。   ---|--- « 节点生命周期 API 获取关闭 API »