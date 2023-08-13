

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Cluster stats API](cluster-stats.md) [Nodes feature usage API »](cluster-
nodes-usage.md)

## 集群更新设置接口

配置动态群集设置。

###Request

"放置/_cluster/设置"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

###Description

您可以使用群集更新设置 API 在正在运行的群集上配置和更新动态设置。您还可以使用"elasticsearch.yml"在未启动或关闭的节点上本地配置动态设置。

使用群集更新设置 API 进行的更新可以是 _persistent_ (适用于群集重新启动)或 _transient_ (在群集重新启动后重置)。您还可以通过使用 API 为其分配"null"值来重置瞬态或持久性设置。

如果使用多种方法配置相同的设置，则 Elasticsearch 将按以下优先级顺序应用这些设置：

1. 瞬态设置 2.持久设置 3."弹性搜索.yml"设置 4.默认设置值

例如，您可以应用瞬态设置来覆盖持久性设置或"弹性搜索.yml"设置。但是，对"elasticsearch.yml"设置的更改不会覆盖定义的瞬态或持久性设置。

如果使用 Elasticsearch Service，请使用用户设置功能配置所有集群设置。此方法允许 Elasticsearch Service 自动拒绝可能破坏集群的不安全设置。

如果您在自己的硬件上运行 Elasticsearch，请使用集群更新设置 API 来配置动态集群设置。仅对静态集群设置和节点设置使用"elasticsearch.yml"。API 不需要重启，并确保设置的值在所有节点上都相同。

不再建议使用瞬态群集设置。请改用持久群集设置。如果群集变得不稳定，则暂时性设置可能会意外清除，从而导致可能不需要的群集配置。请参阅瞬态设置迁移指南。

### 查询参数

`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`include_defaults`

     (Optional, Boolean) If `true`, returns all default cluster settings. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

持久更新的示例：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "indices.recovery.max_bytes_per_sec": '50mb'
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent" : {
        "indices.recovery.max_bytes_per_sec" : "50mb"
      }
    }

瞬态更新的示例：

不再建议使用瞬态群集设置。请改用持久群集设置。如果群集变得不稳定，则暂时性设置可能会意外清除，从而导致可能不需要的群集配置。请参阅瞬态设置迁移指南。

    
    
    response = client.cluster.put_settings(
      flat_settings: true,
      body: {
        transient: {
          "indices.recovery.max_bytes_per_sec": '20mb'
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings?flat_settings=true
    {
      "transient" : {
        "indices.recovery.max_bytes_per_sec" : "20mb"
      }
    }

对更新的响应返回更改的设置，如对暂时性示例的以下响应所示：

    
    
    {
      ...
      "persistent" : { },
      "transient" : {
        "indices.recovery.max_bytes_per_sec" : "20mb"
      }
    }

此示例重置一个设置：

    
    
    response = client.cluster.put_settings(
      body: {
        transient: {
          "indices.recovery.max_bytes_per_sec": nil
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "transient" : {
        "indices.recovery.max_bytes_per_sec" : null
      }
    }

响应不包括已重置的设置：

    
    
    {
      ...
      "persistent" : {},
      "transient" : {}
    }

您还可以使用通配符重置设置。例如，要重置所有动态"索引.恢复"设置：

    
    
    response = client.cluster.put_settings(
      body: {
        transient: {
          "indices.recovery.*": nil
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "transient" : {
        "indices.recovery.*" : null
      }
    }

[« Cluster stats API](cluster-stats.md) [Nodes feature usage API »](cluster-
nodes-usage.md)
