

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Not enough nodes to allocate all shard replicas](increase-tier-
capacity.md) [Total number of shards per node has been reached »](increase-
cluster-shard-limit.md)

## 单个节点上索引的分片总数超出

Elasticsearch 尝试通过在集群中的节点之间分配数据(索引分片)来利用所有可用资源。

用户可能希望通过将索引设置配置为自定义值来影响此数据分布theindex.routing.allocation.total_shards_per_node(例如，在高流量索引的情况下为"1")。限制索引在一个节点上可以位于多少个分片的各种配置可能会导致分片未分配，因为集群没有足够的节点来满足索引配置。

为了解决此问题，请按照以下步骤操作：

弹性搜索服务 自我管理

为了分配分片，我们需要增加可以在节点上并置的分片数量。我们将通过检查"index.routing.allocation.total_shards_per_node"索引设置的配置并增加未分配分片的索引的配置值来实现此目的。

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 检查具有未分配分片的索引的"index.routing.allocation.total_shards_per_node"索引设置：响应 = client.indices.get_settings(索引："my-index-000001"，名称："index.routing.allocation.total_shards_per_node"，flat_settings：true ) 将响应 GET /my-index-000001/_settings/index.routing.allocation.total_shards_per_node？flat_settings

响应将如下所示：

    
        {
      "my-index-000001": {
        "settings": {
          "index.routing.allocation.total_shards_per_node": "1" __}
      }
    }

__

|

表示可以驻留在"my-index-000001"索引的一个节点上的分片总数的当前配置值。   ---|--- 5.将可在一个节点上分配的分片总数的值增加到更高的值：响应 = client.indices.put_settings( 索引： 'my-index-000001'， body： { index： { "routing.allocation.total_shards_per_node"： '2' } } ) put 响应 PUT /my-index-000001/_settings { "index" ： { "routing.allocation.total_shards_per_node" ： "2" __} }

__

|

"my-index-000001"索引的"total_shards_per_node"配置的新值从以前的值"1"增加到"2"。"total_shards_per_node"配置也可以设置为"-1"，这表示同一索引的分片数量可以驻留在一个节点上没有上限。   ---|---   

为了分配分片，您可以向Elasticsearch集群添加更多节点，并将索引的目标层节点角色分配给新节点。

若要检查哪个层是分配的索引目标，请使用获取索引设置 API 检索"index.routing.allocation.include._tier_preference"设置的配置值：

    
    
    response = client.indices.get_settings(
      index: 'my-index-000001',
      name: 'index.routing.allocation.include._tier_preference',
      flat_settings: true
    )
    puts response
    
    
    GET /my-index-000001/_settings/index.routing.allocation.include._tier_preference?flat_settings

响应将如下所示：

    
    
    {
      "my-index-000001": {
        "settings": {
          "index.routing.allocation.include._tier_preference": "data_warm,data_hot" __}
      }
    }

__

|

表示允许分配此索引的数据层节点角色的逗号分隔列表，列表中的第一个角色是具有较高优先级的角色，即索引的目标层。例如，在本例中，TheTier 首选项为 'data_warm，data_hot'，因此索引以 'warm'tier 为目标，并且在 Elasticsearchcluster 中需要更多具有 'data_warm' 角色的节点。   ---|--- 或者，如果不需要向 Elasticsearch 集群添加更多节点，则检查"index.routing.allocation.total_shards_per_node"索引设置的配置并增加配置的值将允许在同一节点上分配更多分片。

1. 检查具有未分配分片的索引的"index.routing.allocation.total_shards_per_node"索引设置：响应 = client.indices.get_settings(索引："my-index-000001"，名称："index.routing.allocation.total_shards_per_node"，flat_settings：true ) 将响应 GET /my-index-000001/_settings/index.routing.allocation.total_shards_per_node？flat_settings

响应将如下所示：

    
        {
      "my-index-000001": {
        "settings": {
          "index.routing.allocation.total_shards_per_node": "1" __}
      }
    }

__

|

表示可以驻留在"my-index-000001"索引的一个节点上的分片总数的当前配置值。   ---|--- 2.增加可以在一个节点上分配的分片总数或将值重置为无界 ('-1')： 响应 = client.indices.put_settings( 索引： 'my-index-000001'， body： { index： { "routing.allocation.total_shards_per_node"： -1 } } } ) put 响应 PUT /my-index-000001/_settings { "index" ： { "routing.allocation.total_shards_per_node" ： -1 } }

[« Not enough nodes to allocate all shard replicas](increase-tier-
capacity.md) [Total number of shards per node has been reached »](increase-
cluster-shard-limit.md)
