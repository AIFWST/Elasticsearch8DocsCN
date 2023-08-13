

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Licensing APIs](licensing-apis.md)

[« Get license API](get-license.md) [Start trial API »](start-trial.md)

## 获取试用状态API

使您能够检查试用状态。

####Request

"获取/_license/trial_status"

####Description

如果您想尝试所有订阅功能，可以开始 30 天试用。

仅当您的集群尚未激活当前主要产品版本的试用版时，才允许您启动试用版。例如，如果您已经激活了 v6.0 的试用版，则在 v7.0 之前无法启动新的试用版。但是，您可以请求延长试用期 athttps://www.elastic.co/trialextension。

有关功能和订阅的详细信息，请参阅 seehttps://www.elastic.co/subscriptions。

###Authorization

您必须具有"监视"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

####Examples

以下示例检查您是否有资格开始试用：

    
    
    response = client.license.get_trial_status
    puts response
    
    
    GET /_license/trial_status

示例响应：

    
    
    {
      "eligible_to_start_trial": true
    }

[« Get license API](get-license.md) [Start trial API »](start-trial.md)
