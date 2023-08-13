

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher actions](actions.md)

[« Watcher Slack Action](actions-slack.md) [Watcher Jira action »](actions-
jira.md)

## 观察者寻呼机职责操作

使用 PagerDuty 操作在 PagerDuty 中创建事件。要创建 PagerDuty 事件，您必须在 'elasticsearch.yml' 中配置至少一个 PagerDuty 帐户。

### 配置寻呼机操作

您可以在"操作"数组中配置寻呼机操作。特定于操作的属性是使用"pagerduty"关键字指定的。

以下代码片段显示了一个简单的 PagerDuty 操作定义：

    
    
    "actions" : {
      "notify-pagerduty" : {
        "transform" : { ... },
        "throttle_period" : "5m",
        "pagerduty" : {
          "description" : "Main system down, please check!" __}
      }
    }

__

|

消息说明 ---|--- ### 将元信息添加到寻呼机职责事件编辑

若要为 PagerDuty 事件提供更多上下文，可以将有效负载以及上下文数组附加到操作。

    
    
    "actions" : {
      "notify-pagerduty" : {
        "throttle_period" : "5m",
        "pagerduty" : {
          "account" : "team1",
          "description" : "Main system down, please check! Happened at {{ctx.execution_time}}",
          "attach_payload" : true,
          "client" : "/foo/bar/{{ctx.watch_id}}",
          "client_url" : "http://www.example.org/",
          "contexts" : [
            {
              "type": "link",
              "href": "http://acme.pagerduty.com"
            },{
              "type": "link",
              "href": "http://acme.pagerduty.com",
              "text": "View the incident on {{ctx.payload.link}}"
            }
          ]
        }
      }
    }

### 寻呼机操作属性

姓名 |必填 |描述 ---|---|--- '帐户'

|

no

|

要使用的帐户将回退到默认帐户。帐户需要"service_api_key"属性。   尽管下面的某些属性的名称与PagerDuty"Events API v1"参数名称匹配，但最终通过适当地翻译属性来使用"Events API v2"API。

**表 85.寻呼机事件触发事件属性**

姓名 |必填 |描述 ---|---|--- '描述'

|

yes

|

此事件"event_type"的快速描述

|

no

|

要发送的事件类型。必须是"触发"、"解决"或"确认"之一。默认为"触发器"。   "incident_key"

|

no

|

pagerduty 端的事件键，也用于重复数据消除，并允许解决或确认事件。   "客户端"

|

no

|

触发事件的客户端的名称，即"观察程序监视""client_url"

|

no

|

要访问以获取更多详细信息的客户端 URL。   "attach_payload"

|

no

|

如果设置为"true"，则有效负载将作为详细信息附加到 API 调用。默认为"假"。   "上下文"

|

no

|

对象数组，允许您提供其他链接或图像，以便为触发器提供更多上下文。   'proxy.host'

|

no

|

要使用的代理主机(仅与"proxy.port"结合使用)"proxy.port"

|

no

|

要使用的代理端口(仅与"proxy.host"结合使用) 您可以使用"xpack.notification.pagerduty.event_defaults.*"属性为整个服务的上述值配置默认值，也可以使用"xpack.notification.pagerduty.account.your_account_name.event_defaults.*"为每个帐户配置默认值

所有这些对象都有模板支持，因此您可以将上下文和有效负载中的数据用作所有字段的一部分。

**表 86.寻呼事件触发器上下文属性**

姓名 |必填 |描述 ---|---|--- 'type'

|

yes

|

"链接"或"图像"之一。   "唔"

|

yes/no

|

包含更多信息的链接。如果类型为"链接"，则必须存在，如果类型为"图像""src"，则必须存在可选

|

no

|

"图像"类型的 src 属性。   ### 配置寻呼机值班帐户编辑

您可以在"elasticsearch.yml"的"xpack.notification.pagerduty"命名空间中配置观察器用于与PagerDuty通信的帐户。

要配置寻呼机帐户，您需要要向其发送通知的寻呼机服务的 API 集成密钥。要获取密钥，请执行以下操作：

1. 以帐户管理员身份登录 pagerduty.com。  2. 转到**服务**，然后选择您要定位的寻呼机服务。  3. 单击**集成**选项卡，并添加**事件 API V2** 集成(如果尚不存在)。  4. 复制 API 集成密钥以供在下面使用。

要在密钥库中配置 PagerDuty 帐户，必须指定帐户名和集成密钥(请参阅安全设置)：

    
    
    bin/elasticsearch-keystore add xpack.notification.pagerduty.account.my_pagerduty_account.secure_service_api_key

### 在 7.0.0 中已弃用。

仍支持将服务 api 密钥存储在 YAML 文件中或通过群集更新设置，但应使用密钥库设置。

您还可以指定寻呼值班事件属性的默认值：。

    
    
    xpack.notification.pagerduty:
      account:
        my_pagerduty_account:
          event_defaults:
            description: "Watch notification"
            incident_key: "my_incident_key"
            client: "my_client"
            client_url: http://www.example.org
            event_type: trigger
            attach_payload: true

如果配置多个 PagerDuty 帐户，则需要设置默认帐户或在"pagerduty"操作中指定应使用哪个帐户发送事件。

    
    
    xpack.notification.pagerduty:
      default_account: team1
      account:
        team1:
          ...
        team2:
          ...

[« Watcher Slack Action](actions-slack.md) [Watcher Jira action »](actions-
jira.md)
