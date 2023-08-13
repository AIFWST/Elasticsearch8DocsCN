

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Nodes info API](cluster-nodes-info.md) [Nodes reload secure settings API
»](cluster-nodes-reload-secure-settings.md)

## 预验证节点移除接口

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

预验证节点删除。

###Request

"发布/_internal/prevalidate_node_removal"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

此 API 检查尝试从群集中删除指定的节点是否可能成功。对于没有未分配分片的集群，删除任何节点都被认为是安全的，这意味着删除节点可能会成功。

如果集群具有"红色"集群运行状况，它会验证删除节点不会有删除未分配分片的最后一个剩余副本的风险。如果集群中有红色索引，API 会检查红色索引是否是可搜索快照索引，如果不是，它会向 API 调用中指定的每个节点发送请求，以验证这些节点是否可能包含不是可搜索快照索引的红色索引的本地分片副本。通过检查节点是否具有任何 redindex 分片的分片目录，在每个接收节点上处理此请求。

响应包括删除指定节点的总体安全性，以及每个节点的详细响应。响应的特定于节点的部分还包括有关删除该节点可能不成功的原因的更多详细信息。

请注意，只能使用其中一个查询参数("名称"、"ids"或"external_ids")来指定节点集。

请注意，如果一组节点的预验证结果返回"true"(i.e.it 可能会成功)，这并不意味着可以一次成功删除所有这些节点，而是删除每个单独的节点可能会成功。实际的节点删除可以通过节点生命周期 API 处理。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`names`

     (Optional, string) Comma-separated list of node names. 
`ids`

     (Optional, string) Comma-separated list of node IDs. 
`external_ids`

     (Optional, string) Comma-separated list of node external IDs. 

### 响应正文

`is_safe`

     (boolean) Whether the removal of all the provided nodes is safe or not. 
`message`

     (string) A message providing more detail on why the operation is considered safe or not. 
`nodes`

    

(对象)删除每个提供的节点的预验证结果。

"节点"的属性

`<node>`

    

(对象)包含有关特定节点的删除预验证的信息。

""的属性<node>

`id`

     (string) node ID 
`name`

     (string) node name 
`external_id`

     (string) node external ID 
`result`

    

(对象)包含节点的删除预验证结果。

"结果"的属性

`is_safe`

     (boolean) Whether the removal of the node is considered safe or not. 
`reason`

    

(字符串)一个字符串，指定预验证结果被视为安全与否的原因。它可以是以下值之一：

* "no_problems"：预验证未发现任何可能阻止节点安全删除的问题。  * 'no_red_shards_except_searchable_snapshots'：可以安全地删除节点，因为所有红色索引都是可搜索的快照索引，因此删除节点不会有从集群中删除该索引的最后一个副本的风险。  * "no_red_shards_on_node"：节点不包含红色不可搜索快照索引分片的任何副本。  * "red_shards_on_node"：节点可能包含一些不可搜索的快照红色索引的分片副本。节点上可能存在的分片列表在"消息"字段中指定。  * "unable_to_verify_red_shards"：联系节点失败或超时。"消息"字段中提供了更多详细信息。

`message`

     (Optional, string) Detailed information about the removal prevalidation result. 

###Examples

此示例验证删除节点"node1"和"node2"是否安全。响应指示删除"node1"是安全的，但删除"node2"可能不安全，因为它可能包含指定红色分片的副本。因此，删除两个节点的整体预验证将返回"false"。

    
    
    POST /_internal/prevalidate_node_removal?names=node1,node2

API 返回以下响应：

    
    
    {
      "is_safe": false,
      "message": "removal of the following nodes might not be safe: [node2-id]",
      "nodes": [
        {
          "id": "node1-id",
          "name" : "node1",
          "external_id" : "node1-externalId",
          "result" : {
            "is_safe": true,
            "reason": "no_red_shards_on_node",
            "message": ""
          }
        },
        {
          "id": "node2-id",
          "name" : "node2",
          "external_id" : "node2-externalId",
          "result" : {
            "is_safe": false,
            "reason": "red_shards_on_node",
            "message": "node contains copies of the following red shards: [[indexName][0]]"
          }
        }
      ]
    }

[« Nodes info API](cluster-nodes-info.md) [Nodes reload secure settings API
»](cluster-nodes-reload-secure-settings.md)
