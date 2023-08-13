

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get application privileges API](security-api-get-privileges.md) [Get role
mappings API »](security-api-get-role-mapping.md)

## 获取内置权限API

检索此版本的 Elasticsearch 中可用的集群权限和索引权限列表。

###Request

'获取/_security/特权/_builtin"

###Prerequisites

* 要使用此 API，您必须具有"read_security"群集权限(或更大的权限，例如"manage_security"或"全部")。

###Description

此 API 检索正在查询的 Elasticsearch 版本中可用的集群和索引权限名称集。

要检查用户是否具有特定权限，请使用具有权限 API。

### 响应正文

响应是一个具有两个字段的对象：

`cluster`

     (array of string) The list of [cluster privileges](security-privileges.html#privileges-list-cluster "Cluster privileges") that are understood by this version of Elasticsearch. 
`index`

     (array of string) The list of [index privileges](security-privileges.html#privileges-list-indices "Indices privileges") that are understood by this version of Elasticsearch. 

###Examples

以下示例检索所有内置权限的名称：

    
    
    GET /_security/privilege/_builtin

成功的调用会返回具有"集群"和"索引"字段的对象。

    
    
    {
      "cluster" : [
        "all",
        "cancel_task",
        "create_snapshot",
        "delegate_pki",
        "grant_api_key",
        "manage",
        "manage_api_key",
        "manage_autoscaling",
        "manage_behavioral_analytics",
        "manage_ccr",
        "manage_data_frame_transforms",
        "manage_enrich",
        "manage_ilm",
        "manage_index_templates",
        "manage_ingest_pipelines",
        "manage_logstash_pipelines",
        "manage_ml",
        "manage_oidc",
        "manage_own_api_key",
        "manage_pipeline",
        "manage_rollup",
        "manage_saml",
        "manage_search_application",
        "manage_security",
        "manage_service_account",
        "manage_slm",
        "manage_token",
        "manage_transform",
        "manage_user_profile",
        "manage_watcher",
        "monitor",
        "monitor_data_frame_transforms",
        "monitor_ml",
        "monitor_rollup",
        "monitor_snapshot",
        "monitor_text_structure",
        "monitor_transform",
        "monitor_watcher",
        "none",
        "post_behavioral_analytics_event",
        "read_ccr",
        "read_ilm",
        "read_pipeline",
        "read_security",
        "read_slm",
        "transport_client"
      ],
      "index" : [
        "all",
        "auto_configure",
        "create",
        "create_doc",
        "create_index",
        "delete",
        "delete_index",
        "index",
        "maintenance",
        "manage",
        "manage_follow_index",
        "manage_ilm",
        "manage_leader_index",
        "monitor",
        "none",
        "read",
        "read_cross_cluster",
        "view_index_metadata",
        "write"
      ]
    }

[« Get application privileges API](security-api-get-privileges.md) [Get role
mappings API »](security-api-get-role-mapping.md)
