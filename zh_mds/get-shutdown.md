

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Node lifecycle APIs](node-lifecycle-api.md)

[« Put shutdown API](put-shutdown.md) [Delete shutdown API »](delete-
shutdown.md)

## 获取关机接口

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

检索准备关闭的节点的状态。

###Request

"获取_nodes/关机"

"获取_nodes/<node-id>/关闭"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。  * 如果启用了操作员权限功能，您必须是操作员才能使用此 API。

###Description

指示节点是否已准备好关闭，或者关闭准备工作是否仍在进行中或已停止。返回关机过程每个部分的状态信息。用于在调用放置关闭后监视关闭过程。

### 路径参数

`<node-id>`

     (Optional, string) The ID of a node that is being prepared for shutdown. If no ID is specified, returns the status of all nodes being prepared for shutdown. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

准备要重新启动的节点：

    
    
    response = client.shutdown.put_node(
      node_id: 'USpTGYaBSIKbgSUJR2Z9lg',
      body: {
        type: 'restart',
        reason: 'Demonstrating how the node shutdown API works',
        allocation_delay: '10m'
      }
    )
    puts response
    
    
    PUT /_nodes/USpTGYaBSIKbgSUJR2Z9lg/shutdown
    {
      "type": "restart",
      "reason": "Demonstrating how the node shutdown API works",
      "allocation_delay": "10m"
    }

获取关机准备的状态：

    
    
    response = client.shutdown.get_node(
      node_id: 'USpTGYaBSIKbgSUJR2Z9lg'
    )
    puts response
    
    
    GET /_nodes/USpTGYaBSIKbgSUJR2Z9lg/shutdown

响应显示有关关闭准备的信息，包括分片迁移、任务迁移和插件清理的状态：

    
    
    {
        "nodes": [
            {
                "node_id": "USpTGYaBSIKbgSUJR2Z9lg",
                "type": "RESTART",
                "reason": "Demonstrating how the node shutdown API works",
                "shutdown_startedmillis": 1624406108685,
                "allocation_delay": "10m",
                "status": "COMPLETE",
                "shard_migration": {
                    "status": "COMPLETE",
                    "shard_migrations_remaining": 0,
                    "explanation": "no shard relocation is necessary for a node restart"
                },
                "persistent_tasks": {
                    "status": "COMPLETE"
                },
                "plugins": {
                    "status": "COMPLETE"
                }
            }
        ]
    }

[« Put shutdown API](put-shutdown.md) [Delete shutdown API »](delete-
shutdown.md)
