

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Autoscaling APIs](autoscaling-apis.md)

[« Autoscaling APIs](autoscaling-apis.md) [Get autoscaling capacity API
»](autoscaling-get-autoscaling-capacity.md)

## 创建或更新自动缩放策略API

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

创建或更新自动缩放策略。

###Request

    
    
    PUT /_autoscaling/policy/<name>
    {
      "roles": [],
      "deciders": {
        "fixed": {
        }
      }
    }

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_autoscaling"集群权限才能使用此 API。  * 如果启用了操作员权限功能，则只有操作员用户才能使用此 API。

###Description

此 API 使用提供的名称放置自动缩放策略。有关可用的决策程序，请参阅自动缩放决策程序。

###Examples

此示例使用固定的自动缩放决策程序放置名为"my_autoscaling_policy"的自动缩放策略，应用于(仅)具有"data_hot"角色的节点集。

    
    
    PUT /_autoscaling/policy/my_autoscaling_policy
    {
      "roles" : [ "data_hot" ],
      "deciders": {
        "fixed": {
        }
      }
    }

API 返回以下结果：

    
    
    {
      "acknowledged": true
    }

[« Autoscaling APIs](autoscaling-apis.md) [Get autoscaling capacity API
»](autoscaling-get-autoscaling-capacity.md)
