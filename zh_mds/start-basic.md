

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Licensing APIs](licensing-apis.md)

[« Get basic status API](get-basic-status.md) [Update license API »](update-
license.md)

## 启动基本接口

此 API 启动无限期基本许可证。

####Request

"发布/_license/start_basic"

####Description

"启动基本"API 使您能够启动无限期的基本许可证，该许可证可以访问所有基本功能。但是，如果基本许可证不支持当前许可证提供的所有功能，则会在响应中通知您。然后，您必须重新提交 API请求，并将"确认"参数设置为"true"。

要检查基本许可证的状态，请使用以下 API：获取基本状态。

有关不同类型的许可证的详细信息，请参阅 seehttps://www.elastic.co/subscriptions。

###Authorization

您必须具有"管理"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

####Examples

如果您当前没有许可证，以下示例将启动基本许可证：

    
    
    response = client.license.post_start_basic
    puts response
    
    
    POST /_license/start_basic

示例响应：

    
    
    {
      "basic_was_started": true,
      "acknowledged": true
    }

如果您当前拥有的功能多于基本许可证的许可证，以下示例将启动基本许可证。当您丢失功能时，必须传递确认参数：

    
    
    response = client.license.post_start_basic(
      acknowledge: true
    )
    puts response
    
    
    POST /_license/start_basic?acknowledge=true

示例响应：

    
    
    {
      "basic_was_started": true,
      "acknowledged": true
    }

[« Get basic status API](get-basic-status.md) [Update license API »](update-
license.md)
