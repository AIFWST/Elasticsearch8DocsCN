

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md) ›[Migrating to 8.0](migrating-8.0.md)

[« Java time migration guide](migrate-to-java-time.md) [Release notes »](es-
release-notes.md)

## 瞬态设置迁移指南

不再建议使用瞬态群集设置。您可以使用瞬态设置对集群进行临时配置更改。但是，群集重新启动或群集不稳定可能会意外清除这些设置，从而导致可能不需要的群集配置。

若要避免此风险，请重置已在群集上配置的任何瞬态设置。将要保留的任何瞬态设置转换为持久设置，该设置在群集重启和群集不稳定后持续存在。还应更新任何自定义工作流和应用程序以使用持久性设置而不是瞬态设置。

某些 Elastic 产品在执行特定操作时可能会使用瞬态设置。仅重置您、您的用户或您的自定义工作流和应用程序配置的瞬态设置。

要重置和转换瞬态设置：

1. 使用群集获取设置 API 获取任何已配置的瞬态设置的列表。           响应 = client.cluster.get_settings( flat_settings：真，filter_path："瞬态") 将响应 GET _cluster/设置？flat_settings=真&filter_path=瞬态

API 在"瞬态"对象中返回瞬态设置。如果此对象为空，则您的集群没有瞬态设置，您可以跳过其余步骤。

    
        {
      "persistent": { ... },
      "transient": {
        "cluster.indices.close.enable": "false",
        "indices.recovery.max_bytes_per_sec": "50mb"
      }
    }

2. 将要转换为群集更新设置 API 请求的"持久"对象的任何设置复制。在同一请求中，通过为任何瞬态设置分配"null"值来重置它们。           响应 = client.cluster.put_settings( body： { 持久： { "cluster.indices.close.enable"： false， "indices.recovery.max_bytes_per_sec"： '50MB' }， 瞬态： { "*"： nil } } ) put response PUT _cluster/settings { "persistent"： { "cluster.indices.close.enable"： false， "indices.recovery.max_bytes_per_sec"： "50MB" }， "transient"： { "*"： null } }

3. 使用群集获取设置 API 确认群集没有剩余的瞬态设置。           响应 = client.cluster.get_settings( flat_settings： true ) 放置响应 GET _cluster/settings？flat_settings=true

如果"瞬态"对象为空，则您的集群没有瞬态设置。

    
        {
      "persistent": {
        "cluster.indices.close.enable": "false",
        "indices.recovery.max_bytes_per_sec": "50mb",
        ...
      },
      "transient": {
      }
    }

[« Java time migration guide](migrate-to-java-time.md) [Release notes »](es-
release-notes.md)
