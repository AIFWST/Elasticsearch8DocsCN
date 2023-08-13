

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Licensing APIs](licensing-apis.md)

[« Start trial API](start-trial.md) [Start basic API »](start-basic.md)

## 获取基本状态API

此 API 使您能够检查基本许可证的状态。

####Request

"获取/_license/basic_status"

####Description

要启动基本许可证，您当前不得拥有基本许可证。

有关不同类型的许可证的详细信息，请参阅 seehttps://www.elastic.co/subscriptions。

###Authorization

您必须具有"监视"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

####Examples

以下示例检查您是否有资格启动基本：

    
    
    response = client.license.get_basic_status
    puts response
    
    
    GET /_license/basic_status

示例响应：

    
    
    {
      "eligible_to_start_basic": true
    }

[« Start trial API](start-trial.md) [Start basic API »](start-basic.md)
