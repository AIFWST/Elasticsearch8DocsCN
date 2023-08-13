

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Create or update watch API](watcher-api-put-watch.md) [Get Watcher index
settings »](watcher-api-get-settings.md)

## 更新观察程序索引设置

此 API 允许用户修改观察程序内部索引(".watches")的设置。修改后仅允许设置的子集。这包括：

* "index.auto_expand_replicas" * "index.number_of_replicas"

修改观察程序设置的示例：

    
    
    PUT /_watcher/watch/test_watch
    {
      "trigger": {
        "schedule": {
          "hourly": {
            "minute": [ 0, 5 ]
            }
          }
      },
      "input": {
        "simple": {
          "payload": {
            "send": "yes"
          }
        }
      },
      "condition": {
        "always": {}
      }
    }
    
    
    response = client.watcher.update_settings(
      body: {
        "index.auto_expand_replicas": '0-4'
      }
    )
    puts response
    
    
    PUT /_watcher/settings
    {
      "index.auto_expand_replicas": "0-4"
    }

可以使用获取观察程序索引设置 API 检索可配置设置。

[« Create or update watch API](watcher-api-put-watch.md) [Get Watcher index
settings »](watcher-api-get-settings.md)
