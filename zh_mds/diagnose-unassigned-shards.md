

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Hot spotting](hotspotting.md) [Add a missing tier to the system »](add-
tier.md)

## 诊断未分配分片

分片可能未分配的原因有多种，从配置错误的分配设置到磁盘空间不足。

要诊断部署中未分配的分片，请使用以下步骤：

弹性搜索服务 自我管理

要诊断未分配的分片，请执行以下步骤：

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 使用 cat 分片 API 查看未分配的分片。           response = client.cat.shards( v： true， h： 'index，shard，prirep，state，node，unassigned.reason'， s： 'state' ) put response GET _cat/shards？v=true&h=index，shard，prirep，state，node，unassigned.reason&s=state

响应将如下所示：

    
        [
      {
        "index": "my-index-000001",
        "shard": "0",
        "prirep": "p",
        "state": "UNASSIGNED",
        "node": null,
        "unassigned.reason": "INDEX_CREATED"
      }
    ]

未分配的分片具有"未分配"的"状态"。对于主分片，"prirep"值为"p"，对于副本，值为"r"。

示例中的索引具有未分配的主分片。

5. 要了解未分配分片未分配的原因以及必须采取哪些操作才能允许 Elasticsearch 分配该分片，请使用集群分配说明 API。           响应 = client.cluster.allocation_explain( body： { index： 'my-index-000001'， shard： 0， primary： true } ) put response GET _cluster/allocation/explain { "index"： "my-index-000001"， __"shard"： 0， __"primary"： true __}

__

|

我们要诊断的索引。   ---|---    __

|

未分配的分片 ID。   __

|

指示我们正在诊断主分片。   响应将如下所示：

    
        {
      "index" : "my-index-000001",
      "shard" : 0,
      "primary" : true,
      "current_state" : "unassigned",                 __"unassigned_info" : {
        "reason" : "INDEX_CREATED", __"at" : "2022-01-04T18:08:16.600Z",
        "last_allocation_status" : "no"
      },
      "can_allocate" : "no", __"allocate_explanation" : "Elasticsearch isn't allowed to allocate this shard to any of the nodes in the cluster. Choose a node to which you expect this shard to be allocated, find this node in the node-by-node explanation, and address the reasons which prevent Elasticsearch from allocating this shard there.",
      "node_allocation_decisions" : [
        {
          "node_id" : "8qt2rY-pT6KNZB3-hGfLnw",
          "node_name" : "node-0",
          "transport_address" : "127.0.0.1:9401",
          "node_attributes" : {},
          "node_decision" : "no", __"weight_ranking" : 1,
          "deciders" : [
            {
              "decider" : "filter", __"decision" : "NO",
              "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"nonexistent_node\"]" __}
          ]
        }
      ]
    }

__

|

分片的当前状态。   ---|---    __

|

分片最初变得未分配的原因。   __

|

是否分配分片。   __

|

是否将分片分配给特定节点。   __

|

导致节点做出"否"决策的决策程序。   __

|

解释为什么决策程序返回"否"决策，并附有指向导致决策的设置的有用提示。     6. 本例中的解释表明索引分配配置不正确。若要查看分配设置，请使用获取索引设置和群集获取设置 API。           响应 = client.indices.get_settings( 索引： 'my-index-000001'， flat_settings： 真， include_defaults： 真 ) 放置响应 响应 = client.cluster.get_settings( flat_settings： 真， include_defaults： 真 ) 放置响应 获取 my-index-000001/_settings？flat_settings=true&include_defaults=true 获取_cluster/设置？flat_settings=true&include_defaults=true

7. 使用更新索引设置和群集更新设置 API 将设置更改为正确的值，以便分配索引。

有关修复未解决分片的最常见原因的更多指导，请按照本指南操作或联系 ElasticSupport。

要诊断未分配的分片，请执行以下步骤：

1. 使用 cat 分片 API 查看未分配的分片。           response = client.cat.shards( v： true， h： 'index，shard，prirep，state，node，unassigned.reason'， s： 'state' ) put response GET _cat/shards？v=true&h=index，shard，prirep，state，node，unassigned.reason&s=state

响应将如下所示：

    
        [
      {
        "index": "my-index-000001",
        "shard": "0",
        "prirep": "p",
        "state": "UNASSIGNED",
        "node": null,
        "unassigned.reason": "INDEX_CREATED"
      }
    ]

未分配的分片具有"未分配"的"状态"。对于主分片，"prirep"值为"p"，对于副本，值为"r"。

示例中的索引具有未分配的主分片。

2. 要了解未分配分片的原因以及必须采取哪些操作才能允许 Elasticsearch 分配该分片，请使用集群分配说明 API。           响应 = client.cluster.allocation_explain( body： { index： 'my-index-000001'， shard： 0， primary： true } ) put response GET _cluster/allocation/explain { "index"： "my-index-000001"， __"shard"： 0， __"primary"： true __}

__

|

我们要诊断的索引。   ---|---    __

|

未分配的分片 ID。   __

|

指示我们正在诊断主分片。   响应将如下所示：

    
        {
      "index" : "my-index-000001",
      "shard" : 0,
      "primary" : true,
      "current_state" : "unassigned",                 __"unassigned_info" : {
        "reason" : "INDEX_CREATED", __"at" : "2022-01-04T18:08:16.600Z",
        "last_allocation_status" : "no"
      },
      "can_allocate" : "no", __"allocate_explanation" : "Elasticsearch isn't allowed to allocate this shard to any of the nodes in the cluster. Choose a node to which you expect this shard to be allocated, find this node in the node-by-node explanation, and address the reasons which prevent Elasticsearch from allocating this shard there.",
      "node_allocation_decisions" : [
        {
          "node_id" : "8qt2rY-pT6KNZB3-hGfLnw",
          "node_name" : "node-0",
          "transport_address" : "127.0.0.1:9401",
          "node_attributes" : {},
          "node_decision" : "no", __"weight_ranking" : 1,
          "deciders" : [
            {
              "decider" : "filter", __"decision" : "NO",
              "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"nonexistent_node\"]" __}
          ]
        }
      ]
    }

__

|

分片的当前状态。   ---|---    __

|

分片最初变得未分配的原因。   __

|

是否分配分片。   __

|

是否将分片分配给特定节点。   __

|

导致节点做出"否"决策的决策程序。   __

|

解释为什么决策程序返回"否"决策，并附有指向导致决策的设置的有用提示。     3. 我们案例中的解释表明索引分配配置不正确。若要查看分配设置，请使用获取索引设置和群集获取设置 API。           响应 = client.indices.get_settings( 索引： 'my-index-000001'， flat_settings： 真， include_defaults： 真 ) 放置响应 响应 = client.cluster.get_settings( flat_settings： 真， include_defaults： 真 ) 放置响应 获取 my-index-000001/_settings？flat_settings=true&include_defaults=true 获取_cluster/设置？flat_settings=true&include_defaults=true

4. 使用更新索引设置和群集更新设置 API 将设置更改为正确的值，以便分配索引。

有关修复未确定分片的最常见原因的更多指导，请遵循本指南。

[« Hot spotting](hotspotting.md) [Add a missing tier to the system »](add-
tier.md)
