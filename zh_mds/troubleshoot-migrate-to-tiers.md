

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Allow Elasticsearch to allocate the index](allow-all-index-allocation.md)
[Not enough nodes to allocate all shard replicas »](increase-tier-
capacity.md)

## 索引将索引分配筛选器与数据层节点角色混合在一起，以移动数据层

Elasticsearch 在 7.10 版本中将热-温-冷架构的实现标准化为数据层。某些索引和部署可能尚未完全过渡到数据层，并将实现热-温-冷体系结构的新方法与基于旧版的节点属性混合在一起。

这可能会导致未分配的分片或分片无法过渡到所需的层。

为了解决此问题，请按照以下步骤操作：

弹性搜索服务 自我管理

为了分配分片，我们需要调用迁移到数据层路由API，这将解决冲突的路由配置，以使用标准化数据层。这还可以根据需要通过迁移索引模板和 ILM 策略使系统经得起未来考验。

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 首先，让我们停止索引生命周期管理响应 = client.ilm.stop 放置响应 POST /_ilm/stop

响应将如下所示：

    
        {
      "acknowledged": true
    }

5. 等待索引生命周期管理停止。检查状态，直到它返回"已停止"，如下所示：响应 = client.ilm.get_status 放置响应 获取/_ilm/状态

当索引生命周期管理成功停止时，响应将如下所示：

    
        {
      "operation_mode": "STOPPED"
    }

6. 迁移到数据层响应 = client.ilm.migrate_to_data_tiers将响应 POST /_ilm/migrate_to_data_tiers

响应将如下所示：

    
        {
      "dry_run": false,
      "migrated_ilm_policies":["policy_with_allocate_action"], __"migrated_indices":["warm-index-to-migrate-000001"], __"migrated_legacy_templates":["a-legacy-template"], __"migrated_composable_templates":["a-composable-template"], __"migrated_component_templates":["a-component-template"] __}

__

|

已更新的 ILM 策略。   ---|---    __

|

已迁移到层首选项路由的索引。   __

|

已更新为不包含所提供数据属性的自定义路由设置的旧索引模板。   __

|

已更新为不包含所提供数据属性的自定义路由设置的可组合索引模板。   __

|

已更新为不包含所提供数据属性的自定义工艺路线设置的组件模板。     7. 重新启动索引生命周期管理响应 = client.ilm.start 放置响应 POST /_ilm/start

响应将如下所示：

    
        {
      "acknowledged": true
    }

为了分配分片，我们需要确保部署正在使用数据层节点角色，然后调用迁移到数据层路由 API，这将解决冲突的路由配置，以使用标准化数据层。如果需要，这也将通过迁移索引模板和 ILM 策略使系统经得起未来考验。

1. 如果您的部署尚未使用数据层，请将数据节点分配给相应的数据层。为每个数据节点配置适当的角色，以将其分配给一个或多个数据层："data_hot"、"data_content"、"data_warm"、"data_cold"或"data_frozen"。例如，以下设置将节点配置为热层和内容层中的纯数据节点。           node.roles [ data_hot， data_content ]

2. 停止索引生命周期管理响应 = client.ilm.stop 放置响应 POST /_ilm/stop

响应将如下所示：

    
        {
      "acknowledged": true
    }

3. 等待索引生命周期管理停止。检查状态，直到它返回"已停止"，如下所示：响应 = client.ilm.get_status 放置响应 获取/_ilm/状态

当索引生命周期管理成功停止时，响应将如下所示：

    
        {
      "operation_mode": "STOPPED"
    }

4. 迁移到数据层响应 = client.ilm.migrate_to_data_tiers将响应 POST /_ilm/migrate_to_data_tiers

响应将如下所示：

    
        {
      "dry_run": false,
      "migrated_ilm_policies":["policy_with_allocate_action"], __"migrated_indices":["warm-index-to-migrate-000001"], __"migrated_legacy_templates":["a-legacy-template"], __"migrated_composable_templates":["a-composable-template"], __"migrated_component_templates":["a-component-template"] __}

__

|

已更新的 ILM 策略。   ---|---    __

|

已迁移到层首选项路由的索引。   __

|

已更新为不包含所提供数据属性的自定义路由设置的旧索引模板。   __

|

已更新为不包含所提供数据属性的自定义路由设置的可组合索引模板。   __

|

已更新为不包含所提供数据属性的自定义工艺路线设置的组件模板。     5. 重新启动索引生命周期管理响应 = client.ilm.start 放置响应 POST /_ilm/start

响应将如下所示：

    
        {
      "acknowledged": true
    }

[« Allow Elasticsearch to allocate the index](allow-all-index-allocation.md)
[Not enough nodes to allocate all shard replicas »](increase-tier-
capacity.md)
