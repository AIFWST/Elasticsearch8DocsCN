

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Stop index lifecycle management API](ilm-stop.md) [Ingest APIs »](ingest-
apis.md)

## 迁移到数据层路由API

将索引、ILM 策略以及旧版、可组合模板和组件模板从使用自定义节点属性和基于属性的分配筛选器切换到使用数据层，并选择性地删除一个旧索引模板。使用节点角色使 ILM 能够在数据层之间自动移动索引。

可以手动执行从自定义节点属性迁移路由的操作，如将索引分配筛选器迁移到节点角色页面中所述。

此 API 提供了一种自动执行迁移指南中列出的四个手动步骤中的三个的方法：

1. 停止在新索引上设置自定义热属性 2.从现有 ILM 策略中删除自定义分配设置 3.将现有索引中的自定义分配设置替换为相应的层首选项

###Request

"发布/_ilm/migrate_to_data_tiers"

API 接受允许您指定以下内容的可选正文：

* 要删除的旧索引模板名称。默认为无。  * 用于索引和 ILM 策略分配筛选的自定义节点属性的名称。默认为"数据"。

###Prerequisites

* 在执行迁移之前，必须停止 ILM。使用停止 ILM API 停止 ILM 并获取状态 API 以等待，直到报告的操作模式为"已停止"。

### 查询参数

`dry_run`

     (Optional, Boolean) If `true`, simulates the migration from node attributes based allocation filters to data tiers, but does not perform the migration. This provides a way to retrieve the indices and ILM policies that need to be migrated. Defaults to `false`. 

在模拟迁移时(即"dry_run"为"真")，不需要停止 ILM。

###Examples

以下示例将索引、ILM 策略、旧模板、可组合模板和组件模板从定义自定义分配筛选中迁移出来，并使用"custom_attribute_name"节点属性定义自定义分配筛选，并删除名称为"全局模板"的旧模板(如果系统中存在)。

    
    
    POST /_ilm/migrate_to_data_tiers
    {
      "legacy_template_to_delete": "global-template",
      "node_attribute": "custom_attribute_name"
    }

如果请求成功，将收到如下响应：

    
    
    {
      "dry_run": false,
      "removed_legacy_template":"global-template", __"migrated_ilm_policies":["policy_with_allocate_action"], __"migrated_indices":["warm-index-to-migrate-000001"], __"migrated_legacy_templates":["a-legacy-template"], __"migrated_composable_templates":["a-composable-template"], __"migrated_component_templates":["a-component-template"] __}

__

|

显示已删除的旧索引模板的名称。如果未删除旧索引模板，则会丢失此模板。   ---|---    __

|

已更新的 ILM 策略。   __

|

已迁移到层首选项路由的索引。   __

|

已更新为不包含所提供数据属性的自定义路由设置的旧索引模板。   __

|

已更新为不包含所提供数据属性的自定义路由设置的可组合索引模板。   __

|

已更新为不包含所提供数据属性的自定义工艺路线设置的组件模板。   « 停止索引生命周期管理 API 摄取 API »