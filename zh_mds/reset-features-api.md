

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Features APIs](features-apis.md)

[« Get Features API](get-features-api.md) [Fleet APIs »](fleet-apis.md)

## 重置功能接口

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

清除 Elasticsearchfeatures 存储在系统索引中的所有状态信息，包括安全和机器学习索引。

仅供开发和测试使用。不要重置生产群集上的功能。

    
    
    response = client.features.reset_features
    puts response
    
    
    POST /_features/_reset

###Request

"发布/_features/_reset"

###Description

通过重置所有 Elasticsearch 功能的功能状态，将集群返回到与新安装相同的状态。这将删除存储在系统索引中的所有状态信息。

如果所有功能的状态成功重置，则响应代码为"HTTP 200";如果存在成功和失败的混合状态，则响应代码为"HTTP 207";如果所有功能的重置操作失败，则响应代码为"HTTP 500"。

请注意，选择功能可能会提供重置特定系统索引的方法。使用此 API 可以重置 _all_ 功能，包括内置功能和作为插件实现的功能。

若要列出将受影响的功能，请使用获取功能 API。

您向其提交此请求的节点上安装的功能是将重置的功能。如果您对各个节点上安装了哪些插件有任何疑问，请在主节点上运行。

###Examples

示例响应：

    
    
    {
      "features" : [
        {
          "feature_name" : "security",
          "status" : "SUCCESS"
        },
        {
          "feature_name" : "tasks",
          "status" : "SUCCESS"
        }
      ]
    }

[« Get Features API](get-features-api.md) [Fleet APIs »](fleet-apis.md)
