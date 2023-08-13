

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Autoscaling APIs](autoscaling-apis.md)

[« Get autoscaling capacity API](autoscaling-get-autoscaling-capacity.md)
[Get autoscaling policy API »](autoscaling-get-autoscaling-policy.md)

## 删除自动伸缩策略接口

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

删除自动缩放策略。

###Request

    
    
    DELETE /_autoscaling/policy/<name>

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_autoscaling"集群权限才能使用此 API。  * 如果启用了操作员权限功能，则只有操作员用户才能使用此 API。

###Description

此 API 删除具有提供的名称的自动缩放策略。

###Examples

此示例删除名为"my_autoscaling_policy"的自动缩放策略。

    
    
    response = client.autoscaling.delete_autoscaling_policy(
      name: 'my_autoscaling_policy'
    )
    puts response
    
    
    DELETE /_autoscaling/policy/my_autoscaling_policy

API 返回以下结果：

    
    
    {
      "acknowledged": true
    }

此示例删除所有自动缩放策略。

    
    
    response = client.autoscaling.delete_autoscaling_policy(
      name: '*'
    )
    puts response
    
    
    DELETE /_autoscaling/policy/*

API 返回以下结果：

    
    
    {
      "acknowledged": true
    }

[« Get autoscaling capacity API](autoscaling-get-autoscaling-capacity.md)
[Get autoscaling policy API »](autoscaling-get-autoscaling-policy.md)
