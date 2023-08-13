

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Licensing APIs](licensing-apis.md)

[« Get trial status API](get-trial-status.md) [Get basic status API »](get-
basic-status.md)

## 开始试用接口

开始 30 天试用。

####Request

"发布/_license/start_trial"

####Description

"开始试用"API 使您能够开始 30 天试用，从而可以访问所有订阅功能。

仅当您的集群尚未激活当前主要产品版本的试用版时，才允许您启动试用版。例如，如果您已经激活了 v6.0 的试用版，则在 v7.0 之前无法启动新的试用版。但是，您可以请求延长试用期 athttps://www.elastic.co/trialextension。

若要检查试用状态，请使用获取试用状态。

有关功能和订阅的详细信息，请参阅 seehttps://www.elastic.co/subscriptions。

###Authorization

您必须具有"管理"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

####Examples

以下示例开始 30 天试用。确认参数是必需的，因为您正在启动即将过期的许可证。

    
    
    response = client.license.post_start_trial(
      acknowledge: true
    )
    puts response
    
    
    POST /_license/start_trial?acknowledge=true

示例响应：

    
    
    {
      "trial_was_started": true,
      "acknowledged": true
    }

[« Get trial status API](get-trial-status.md) [Get basic status API »](get-
basic-status.md)
