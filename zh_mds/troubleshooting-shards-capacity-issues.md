

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Troubleshooting searches](troubleshooting-searches.md) [REST APIs
»](rest-apis.md)

## 排查分片容量运行状况问题

Elasticsearch使用"cluster.max_shards_per_node"和"cluster.max_shards_per_node.frozen"设置来限制每个节点的最大分片数。集群的当前分片容量可在运行状况 API 分片容量部分中找到。

### 集群即将达到数据节点配置的最大分片数。

"cluster.max_shards_per_node"集群设置限制集群的最大开放分片数，仅计算不属于冻结层的数据节点。

此症状表示应采取措施，否则可能会阻止创建新索引或升级群集。

如果您确信更改不会破坏集群的稳定性，则可以使用集群更新设置 API 暂时提高限制：

弹性搜索服务 自我管理

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 根据分片容量指标检查集群的当前状态：响应 = client.health_report(功能："shards_capacity")将响应 GET _health_report/shards_capacity

响应将如下所示：

    
        {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "yellow",
          "symptom": "Cluster is close to reaching the configured maximum number of shards for data nodes.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000, __"current_used_shards": 988 __},
            "frozen": {
              "max_shards_in_cluster": 3000,
              "current_used_shards": 0
            }
          },
          "impacts": [
            ...
          ],
          "diagnosis": [
            ...
        }
      }
    }

__

|

设置 'cluster.max_shards_per_node' 的当前值 ---|--- __

|

集群中的当前开放分片数 5.使用适当的值更新"cluster.max_shards_per_node"设置：响应 = client.cluster.put_settings( body： { persistent： { "cluster.max_shards_per_node"： 1200 } } ) put response PUT _cluster/settings { "persistent" ： { "cluster.max_shards_per_node"： 1200 } }

这种增加应该只是暂时的。作为长期解决方案，我们建议您将节点添加到分片数据层，或者减少不属于冻结层的节点上的集群分片计数。

6. 要验证更改是否已解决问题，您可以通过检查运行状况 API 的"数据"部分来获取"shards_capacity"指示器的当前状态：响应 = client.health_report(功能："shards_capacity")将响应 GET _health_report/shards_capacity

响应将如下所示：

    
        {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "green",
          "symptom": "The cluster has enough room to add new shards.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000
            },
            "frozen": {
              "max_shards_in_cluster": 3000
            }
          }
        }
      }
    }

7. 当长期解决方案到位时，我们建议您重置"集群.max_分片_每个节点"限制。           响应 = client.cluster.put_settings( body： { 持久： { "cluster.max_shards_per_node"： nil } } ) put response PUT _cluster/settings { "persistent" ： { "cluster.max_shards_per_node"： null } }

根据分片容量指示器检查集群的当前状态：

    
    
    response = client.health_report(
      feature: 'shards_capacity'
    )
    puts response
    
    
    GET _health_report/shards_capacity

响应将如下所示：

    
    
    {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "yellow",
          "symptom": "Cluster is close to reaching the configured maximum number of shards for data nodes.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000, __"current_used_shards": 988 __},
            "frozen": {
              "max_shards_in_cluster": 3000
            }
          },
          "impacts": [
            ...
          ],
          "diagnosis": [
            ...
        }
      }
    }

__

|

设置 'cluster.max_shards_per_node' 的当前值 ---|--- __

|

集群中当前打开的分片数 使用"集群设置 API"，更新"集群.max_分片_每个节点"设置：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.max_shards_per_node": 1200
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node": 1200
      }
    }

这种增加应该只是暂时的。作为长期解决方案，我们建议您将节点添加到分片数据层，或者减少不属于冻结层的节点上的集群分片计数。要验证更改是否已解决问题，您可以通过检查运行状况 API 的"数据"部分来获取"shards_capacity"指示器的当前状态：

    
    
    response = client.health_report(
      feature: 'shards_capacity'
    )
    puts response
    
    
    GET _health_report/shards_capacity

响应将如下所示：

    
    
    {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "green",
          "symptom": "The cluster has enough room to add new shards.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1200
            },
            "frozen": {
              "max_shards_in_cluster": 3000
            }
          }
        }
      }
    }

当长期解决方案到位时，我们建议您重置"cluster.max_shards_per_node"限制。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.max_shards_per_node": nil
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node": null
      }
    }

### 集群即将达到配置的最大冻结节点分片数。

"cluster.max_shards_per_node.frozen"集群设置限制了集群的最大开放分片数，仅计算属于冻结层的数据节点。

此症状表示应采取措施，否则可能会阻止创建新索引或升级群集。

如果您确信更改不会破坏集群的稳定性，则可以使用集群更新设置 API 暂时提高限制：

弹性搜索服务 自我管理

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 根据分片容量指标检查集群的当前状态：响应 = client.health_report(功能："shards_capacity")将响应 GET _health_report/shards_capacity

响应将如下所示：

    
        {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "yellow",
          "symptom": "Cluster is close to reaching the configured maximum number of shards for frozen nodes.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000
            },
            "frozen": {
              "max_shards_in_cluster": 3000, __"current_used_shards": 2998 __}
          },
          "impacts": [
            ...
          ],
          "diagnosis": [
            ...
        }
      }
    }

__

|

设置 'cluster.max_shards_per_node.frozen' 的当前值 ---|--- __

|

集群中冻结节点使用的当前开放分片数 5.更新 'cluster.max_shards_per_node.frozen' 设置： response = client.cluster.put_settings( body： { persistent： { "cluster.max_shards_per_node.frozen"： 3200 } } ) put response PUT _cluster/settings { "persistent" ： { "cluster.max_shards_per_node.frozen"： 3200 } }

这种增加应该只是暂时的。作为长期解决方案，我们建议您将节点添加到分片数据层，或减少属于冻结层的节点上的集群分片计数。

6. 要验证更改是否已解决问题，您可以通过检查运行状况 API 的"数据"部分来获取"shards_capacity"指示器的当前状态：响应 = client.health_report(功能："shards_capacity")将响应 GET _health_report/shards_capacity

响应将如下所示：

    
        {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "green",
          "symptom": "The cluster has enough room to add new shards.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000
            },
            "frozen": {
              "max_shards_in_cluster": 3200
            }
          }
        }
      }
    }

7. 当长期解决方案到位时，我们建议您重置"cluster.max_shards_per_node.frozen"限制。           响应 = client.cluster.put_settings( body： { persistent： { "cluster.max_shards_per_node.frozen"： nil } } ) put response PUT _cluster/settings { "persistent" ： { "cluster.max_shards_per_node.frozen"： null } }

根据分片容量指示器检查集群的当前状态：

    
    
    response = client.health_report(
      feature: 'shards_capacity'
    )
    puts response
    
    
    GET _health_report/shards_capacity
    
    
    {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "yellow",
          "symptom": "Cluster is close to reaching the configured maximum number of shards for frozen nodes.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000
            },
            "frozen": {
              "max_shards_in_cluster": 3000, __"current_used_shards": 2998 __}
          },
          "impacts": [
            ...
          ],
          "diagnosis": [
            ...
        }
      }
    }

__

|

设置"cluster.max_shards_per_node.frozen"的当前值。   ---|---    __

|

集群中冻结节点使用的当前开放分片数。   使用"集群设置 API"，更新"cluster.max_shards_per_node.frozen"设置：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.max_shards_per_node.frozen": 3200
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node.frozen": 3200
      }
    }

这种增加应该只是暂时的。作为长期解决方案，我们建议您将节点添加到分片数据层，或减少属于冻结层的节点上的集群分片计数。要验证更改是否已解决问题，您可以通过检查 healthAPI 的"数据"部分来获取"shards_capacity"指示器的当前状态：

    
    
    response = client.health_report(
      feature: 'shards_capacity'
    )
    puts response
    
    
    GET _health_report/shards_capacity

响应将如下所示：

    
    
    {
      "cluster_name": "...",
      "indicators": {
        "shards_capacity": {
          "status": "green",
          "symptom": "The cluster has enough room to add new shards.",
          "details": {
            "data": {
              "max_shards_in_cluster": 1000
            },
            "frozen": {
              "max_shards_in_cluster": 3200
            }
          }
        }
      }
    }

当长期解决方案到位时，我们建议您重置"cluster.max_shards_per_node.frozen"限制。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.max_shards_per_node.frozen": nil
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node.frozen": null
      }
    }

[« Troubleshooting searches](troubleshooting-searches.md) [REST APIs
»](rest-apis.md)
