

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Diagnose unassigned shards](diagnose-unassigned-shards.md) [Allow
Elasticsearch to allocate the data in the system »](allow-all-cluster-
allocation.md)

## 向系统添加缺失层

Elasticsearch 部署中的索引分配可以在数据层上分配。

为了允许分配索引，请按照以下步骤将索引期望在其上分配的数据层添加到部署中：

弹性搜索服务 自我管理

为了分配分片，我们需要在部署中启用新层。

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 确定索引期望分配的层级。检索"index.routing.allocation.include._tier_preference"设置的配置值：响应 = client.indices.get_settings(索引："my-index-000001"，名称："index.routing.allocation.include._tier_preference"，flat_settings：true ) 将响应 GET /my-index-000001/_settings/index.routing.allocation.include._tier_preference？flat_settings

响应将如下所示：

    
        {
      "my-index-000001": {
        "settings": {
          "index.routing.allocation.include._tier_preference": "data_warm,data_hot" __}
      }
    }

__

|

表示允许分配此索引的数据层节点角色的逗号分隔列表，列表中的第一个角色是具有较高优先级的角色，即索引的目标层。例如，在本例中，TheTier 首选项为 'data_warm，data_hot'，因此索引以 'warm'tier 为目标，并且在 Elasticsearchcluster 中需要更多具有 'data_warm' 角色的节点。   ---|--- 5.打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到**管理此部署**。  6. 在右侧，单击以展开"**管理**"下拉按钮，然后从选项列表中选择"**编辑部署**"。  7. 在"**编辑**"页上，单击"**\+ 添加容量**"，以确定需要在部署中启用的层。为新层选择所需的大小和可用性区域。  8. 导航到页面底部，然后单击"**保存**"按钮。

为了分配分片，您可以向Elasticsearch集群添加更多节点，并将索引的目标层节点角色分配给新节点。

若要确定索引需要哪个层进行分配，请使用获取索引设置 API 检索"index.routing.allocation.include._tier_preference"设置的配置值：

    
    
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

表示允许分配此索引的数据层节点角色的逗号分隔列表，列表中的第一个角色是具有较高优先级的角色，即索引的目标层。例如，在本例中，TheTier 首选项为 'data_warm，data_hot'，因此索引以 'warm'tier 为目标，并且在 Elasticsearchcluster 中需要更多具有 'data_warm' 角色的节点。   ---|--- « 诊断未分配的分片 允许弹性搜索以分配系统中的数据 »