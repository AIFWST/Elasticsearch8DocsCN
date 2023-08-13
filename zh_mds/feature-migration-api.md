

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Migration APIs](migration-api.md)

[« Deprecation info APIs](migration-api-deprecation.md) [Node lifecycle APIs
»](node-lifecycle-api.md)

## 功能迁移接口

这些 API 专为 Kibana 的升级助手间接使用而设计。我们强烈建议您使用升级助手从 7.17 升级到 8.9.0。有关升级说明，请参阅升级到 Elastic8.9.0。

版本升级有时需要更改功能在系统索引中存储配置信息和数据的方式。通过功能迁移 API，您可以查看哪些功能需要更改、启动自动迁移过程并检查迁移状态。

在迁移过程中，某些功能可能暂时不可用。

###Request

"获取/_migration/system_features"

"发布/_migration/system_features"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

###Description

向"_migration/system_features"终结点提交 GET 请求，以查看需要迁移的功能以及正在进行的任何迁移的状态。

向端点提交 POST 请求以启动迁移过程。

###Examples

当您向"_migration/system_features"端点提交 GET 请求时，响应会指示需要迁移的任何功能的状态。

    
    
    response = client.migration.get_feature_upgrade_status
    puts response
    
    
    GET /_migration/system_features

示例响应：

    
    
    {
      "features" : [
        {
          "feature_name" : "async_search",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "enrich",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "ent_search",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "fleet",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "geoip",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "kibana",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "logstash_management",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "machine_learning",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "searchable_snapshots",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "security",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "synonyms",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "tasks",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "transform",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        },
        {
          "feature_name" : "watcher",
          "minimum_index_version" : "{version}",
          "migration_status" : "NO_MIGRATION_NEEDED",
          "indices" : [ ]
        }
      ],
      "migration_status" : "NO_MIGRATION_NEEDED"
    }

当您向"_migration/system_features"端点提交 POST 请求以启动迁移过程时，响应会指示将迁移哪些功能。

    
    
    response = client.migration.post_feature_upgrade
    puts response
    
    
    POST /_migration/system_features

示例响应：

    
    
    {
      "accepted" : true,
      "features" : [
        {
          "feature_name" : "security" __}
      ]
    }

__

|

Elasticsearch 安全性将在集群升级之前迁移。   ---|--- 后续 GET 请求将返回迁移过程的状态。

[« Deprecation info APIs](migration-api-deprecation.md) [Node lifecycle APIs
»](node-lifecycle-api.md)
