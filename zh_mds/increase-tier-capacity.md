

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Indices mix index allocation filters with data tiers node roles to move
through data tiers](troubleshoot-migrate-to-tiers.md) [Total number of
shards for an index on a single node exceeded »](increase-shard-limit.md)

## 没有足够的节点来分配所有分片副本

在不同节点上分发数据副本(索引分片副本)可以并行处理请求，从而加快搜索查询速度。这可以通过将副本分片的数量增加到最大值(节点总数减去 1)来实现，这也可用于防止硬件故障。如果索引具有首选层，则 Elasticsearch 将仅将该索引的数据副本放在目标层中的节点上。

如果遇到警告，没有足够的节点来分配所有分片副本，您可以通过向集群添加更多节点(如果正在使用层，则为层)或减少"index.number_of_replicas"索引设置来影响此行为。

为了解决此问题，请按照以下步骤操作：

弹性搜索服务 自我管理

分配副本分片的一种方法是添加可用区。这将增加 Elasticsearch 集群中的数据节点数量，以便可以分配副本分片。这可以通过编辑部署来完成。但首先，您需要发现索引的目标分配层。使用 Kibana 执行此操作。

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

若要检查索引面向哪个层进行分配，请使用获取索引设置 API 检索"index.routing.allocation.include._tier_preference"设置的配置值：

    
    
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

表示允许分配此索引的数据层节点角色的逗号分隔列表，列表中的第一个角色是具有较高优先级的角色，即索引的目标层。例如，在本例中，TheTier 首选项为 'data_warm，data_hot'，因此索引以 'warm'tier 为目标，并且在 Elasticsearchcluster 中需要更多具有 'data_warm' 角色的节点。   ---|--- 现在您已经知道了该层，您希望增加该层中的节点数，以便可以分配副本。为此，您可以增加每个区域的大小以增加已在使用的可用区中的节点数，也可以增加可用区的数量。返回到部署的登录页面，方法是单击屏幕左上角的三个水平条，然后选择"**管理此部署**"。在该页上，单击"**管理**"按钮，然后选择"**编辑部署**"。请注意，您必须登录到<https://cloud.elastic.co/>才能执行此操作。在 Elasticsearch 部分中，找到无法分配副本分片的层。

!木花控制台

* 选项 1：增加每个区域的大小

    * Look at the values in the **Size per zone** drop down. One node is created in each zone for every 64 GB of RAM you select here. If you currently have 64 GB RAM or less selected, you have one node in each zone. If you select 128 GB RAM, you will get 2 nodes per zone. If you select 192 GB RAM, you will get 3 nodes per zone, and so on. If the value is less than the maximum possible, you can choose a higher value for that tier to add more nodes. 

* 选项 2：增加可用区的数量

    * Find the **Availability zones** selection. If it is less than 3, you can select a higher number of availability zones for that tier. 

如果无法增加每个区域的大小或可用性区域的数量，则可以减少索引数据的副本数。我们将通过检查"index.number_of_replicas"索引设置索引设置并减小配置的值来实现此目的。

1. 如上所述访问 Kibana。  2. 检查"index.number_of_replicas"索引设置。           响应 = client.indices.get_settings( 索引： 'my-index-000001'， name： 'index.number_of_replicas' ) 放置响应 GET /my-index-000001/_settings/index.number_of_replicas

响应将如下所示：

    
        {
      "my-index-000001" : {
        "settings" : {
          "index" : {
            "number_of_replicas" : "2" __}
        }
      }
    }

__

|

表示索引 ---|--- 3 所需的副本分片数的当前配置值。使用"_cat/节点"API 查找目标层中的节点数：响应 = client.cat.nodes( h： 'node.role' ) 将响应 GET /_cat/nodes？h=node.role

响应将如下所示，每个节点包含一行：

    
        himrst
    mv
    himrst

您可以计算包含代表目标层的字母的行，以了解您有多少节点。有关详细信息，请参阅查询参数。上面的示例有两行包含"h"，因此热层中有两个节点。

4. 减小此索引所需的副本分片总数的值。由于副本分片不能与主分片位于同一节点上以实现高可用性，因此新值需要小于或等于上述节点数减 1。由于上面的示例在热层中找到了 2 个节点，因此"index.number_of_replicas"的最大值为 1。           响应 = client.indices.put_settings( index： 'my-index-000001'， body： { index： { number_of_replicas： 1 } } ) put response PUT /my-index-000001/_settings { "index" ： { "number_of_replicas" ： 1 __} }

__

|

"index.number_of_replicas"索引配置的新值从以前的值"2"减少到"1"。它可以设置为低至 0，但为可搜索快照索引以外的索引将其配置为 0 可能会导致节点重新启动期间暂时可用性丢失，或者在数据损坏的情况下永久丢失数据。   ---|---   

为了分配副本分片，您可以向 Elasticsearch 集群添加更多节点，并将索引的目标层节点角色分配给新节点。

若要检查索引面向哪个层进行分配，请使用获取索引设置 API 检索"index.routing.allocation.include._tier_preference"设置的配置值：

    
    
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

表示允许分配此索引的数据层节点角色的逗号分隔列表，列表中的第一个角色是具有较高优先级的角色，即索引的目标层。例如，在本例中，TheTier 首选项为 'data_warm，data_hot'，因此索引以 'warm'tier 为目标，并且在 Elasticsearchcluster 中需要更多具有 'data_warm' 角色的节点。   ---|--- 或者，如果不需要向 Elasticsearch 集群添加更多节点，请检查"index.number_of_replicas"索引设置并减小配置的值：

1. 检查具有未分配副本分片的索引的"index.number_of_replicas"索引设置：响应 = client.indices.get_settings(索引："my-index-000001"，名称："index.number_of_replicas")将响应 GET /my-index-000001/_settings/index.number_of_replicas

响应将如下所示：

    
        {
      "my-index-000001" : {
        "settings" : {
          "index" : {
            "number_of_replicas" : "2" __}
        }
      }
    }

__

|

表示索引 ---|--- 2 所需的副本分片数的当前配置值。使用"_cat/节点"API 查找目标层中的节点数：响应 = client.cat.nodes( h： 'node.role' ) 将响应 GET /_cat/nodes？h=node.role

响应将如下所示，每个节点包含一行：

    
        himrst
    mv
    himrst

您可以计算包含代表目标层的字母的行，以了解您有多少节点。有关详细信息，请参阅查询参数。上面的示例有两行包含"h"，因此热层中有两个节点。

3. 减小此索引所需的副本分片总数的值。由于副本分片不能与主分片位于同一节点上以实现高可用性，因此新值需要小于或等于上述节点数减 1。由于上面的示例在热层中找到了 2 个节点，因此"index.number_of_replicas"的最大值为 1。           响应 = client.indices.put_settings( index： 'my-index-000001'， body： { index： { number_of_replicas： 1 } } ) put response PUT /my-index-000001/_settings { "index" ： { "number_of_replicas" ： 1 __} }

__

|

"index.number_of_replicas"索引配置的新值从以前的值"2"减少到"1"。它可以设置为低至 0，但为可搜索快照索引以外的索引将其配置为 0 可能会导致节点重新启动期间暂时可用性丢失，或者在数据损坏的情况下永久丢失数据。   ---|---   

[« Indices mix index allocation filters with data tiers node roles to move
through data tiers](troubleshoot-migrate-to-tiers.md) [Total number of
shards for an index on a single node exceeded »](increase-shard-limit.md)
