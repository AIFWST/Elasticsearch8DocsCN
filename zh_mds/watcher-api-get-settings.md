

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Update Watcher index settings](watcher-api-update-settings.md) [Start
watch service API »](watcher-api-start.md)

## 获取观察程序索引设置

此 API 允许用户检索观察程序内部索引 ('.watches') 的用户可配置设置。将仅显示索引设置的子集(用户可配置的索引设置)。这包括：

* "index.auto_expand_replicas" * "index.number_of_replicas"

检索观察程序设置的示例：

    
    
    response = client.watcher.get_settings
    puts response
    
    
    GET /_watcher/settings

可以使用更新观察程序索引设置 API 修改可配置设置。

[« Update Watcher index settings](watcher-api-update-settings.md) [Start
watch service API »](watcher-api-start.md)
