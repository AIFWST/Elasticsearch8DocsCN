

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Node lifecycle APIs](node-lifecycle-api.md)

[« Get shutdown API](get-shutdown.md) [Reload search analyzers API
»](indices-reload-analyzers.md)

## 删除关机接口

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

取消关闭准备或清除关闭请求，以便节点可以恢复正常操作。

###Request

"删除_nodes/<node-id>/关闭"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。  * 如果启用了操作员权限功能，您必须是操作员才能使用此 API。

###Description

使节点能够在放置关闭请求后恢复正常操作。当节点重新加入群集或节点永久离开群集时，必须显式清除关闭请求。关闭请求永远不会被 Elasticsearch 自动删除。

### 路径参数

`<node-id>`

     (Optional, string) The ID of a node that you prepared for shut down. 

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
        reason: 'Demonstrating how the node shutdown API works'
      }
    )
    puts response
    
    
    PUT /_nodes/USpTGYaBSIKbgSUJR2Z9lg/shutdown
    {
      "type": "restart",
      "reason": "Demonstrating how the node shutdown API works"
    }

重新启动后取消关机准备或清除关机请求：

    
    
    response = client.shutdown.delete_node(
      node_id: 'USpTGYaBSIKbgSUJR2Z9lg'
    )
    puts response
    
    
    DELETE /_nodes/USpTGYaBSIKbgSUJR2Z9lg/shutdown

这将返回以下响应：

    
    
    {
        "acknowledged": true
    }

[« Get shutdown API](get-shutdown.md) [Reload search analyzers API
»](indices-reload-analyzers.md)
