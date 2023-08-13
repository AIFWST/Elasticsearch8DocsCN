

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher actions](actions.md)

[« Watcher PagerDuty action](actions-pagerduty.md) [Payload transforms
»](transform.md)

## 观察者吉拉行动

使用"jira"操作在 Atlassian 的 JiraSoftware 中创建问题。要创建问题，您需要在"elasticsearch.yml"中配置至少一个 Jira 帐户。

### 配置操作

您可以在"操作"数组中配置 Jira 操作。特定于操作的属性使用"jira"关键字指定。

以下代码片段显示了一个简单的 jira 操作定义：

    
    
    "actions" : {
      "create-jira-issue" : {
        "transform" : { ... },
        "throttle_period" : "5m",
        "jira" : {
          "account" : "integration-account", __"fields" : {
              "project" : {
                "key": "PROJ" __},
              "issuetype" : {
                "name": "Bug" __},
              "summary" : "Encountered {{ctx.payload.hits.total}} errors in the last 5 minutes", __"description" : "Encountered {{ctx.payload.hits.total}} errors in the last 5 minutes (facepalm)", __"labels" : ["auto"], __"priority" : {
                "name" : "High" __}
          }
        }
      }
    }

__

|

在"elasticsearch.yml"中配置的 Jira 帐户的名称。   ---|---    __

|

将在其中创建事务的 Jira 项目的密钥。   __

|

问题类型的名称。   __

|

Jira 问题的摘要。   __

|

Jira 事务的说明。   __

|

要应用于 Jira 事务的标签。   __

|

Jira 问题的优先级。   ### Jira 操作属性编辑

根据 Jira 项目的配置方式，事务可能具有许多不同的字段和值。因此，"jira"操作可以接受其"事务"字段中的任何类型的子字段。调用 Jira 的创建议题 API 时，将直接使用这些字段，允许使用任何类型的自定义字段。

在 Jira 中创建事务始终需要"项目.key"(或"project.id")、"issuetype.name"(或"issuetype.id")和"issue.summary"。

姓名 |必填 |描述 ---|---|--- '帐户'

|

no

|

用于发送消息的 Jira 帐户。   'proxy.host'

|

no

|

要使用的代理主机(仅与"proxy.port"结合使用)"proxy.port"

|

no

|

要使用的代理端口(仅与"proxy.host"结合使用)"fields.project.key"

|

yes

|

将在其中创建事务的 Jira 项目的密钥。如果项目的标识符已知，则可以将其替换为"issue.project.id"。   "fields.issuetype.name"

|

yes

|

标识问题类型的名称。Jira 提供默认问题类型，如"错误"、"任务"、"故事"、"新功能"等。如果类型的标识符已知，则可以将其替换为"issue.issuetype.id"。   "字段摘要"

|

yes

|

问题的摘要(或标题)。   "字段说明"

|

no

|

问题的描述。   "字段.标签"

|

no

|

要应用于 Jira 事务的标签。   "fields.priority.name"

|

no

|

Jira 问题的优先级。Jira 提供默认的"高"、"中"和"低"优先级。   "fields.assignee.name"

|

no

|

要向其分配问题的用户的名称。   "fields.reporter.name"

|

no

|

标识为问题报告者的用户的名称。默认为用户帐户。   "田野.环境"

|

no

|

与问题相关的环境的名称。   "fields.customfield_XXX"

|

no

|

问题的自定义字段 XXX(例如："customfield_10000"："09/Jun/81") ### 配置 Jiraaccountsedit

您可以在"elasticsearch.yml"的"xpack.notification.jira"命名空间中配置 Watcher 可用于与 Jira 通信的帐户。

观察程序支持 Jira 软件的基本身份验证。要配置 Jira帐户，您需要指定(请参阅安全设置)：

    
    
    bin/elasticsearch-keystore add xpack.notification.jira.account.monitoring.secure_url
    bin/elasticsearch-keystore add xpack.notification.jira.account.monitoring.secure_user
    bin/elasticsearch-keystore add xpack.notification.jira.account.monitoring.secure_password

在配置文件或群集设置中存储敏感数据("url"、"用户"和"密码")是不安全的，并且已被弃用。请使用Elasticsearch的安全密钥库方法。

为了避免凭据通过网络以明文形式传输，Watcher 将拒绝基于纯文本 HTTP 协议的"url"设置，如"http://internal-jira.elastic.co"。可以使用显式"allow_http"设置禁用此默认行为：

"url"字段还可以包含用于创建问题的路径。默认情况下，这是"/rest/api/2/issue"。如果也设置了此设置，请确保此路径是创建问题的终结点的完整路径。

    
    
    xpack.notification.jira:
      account:
        monitoring:
          allow_http: true

强烈建议仅将基本身份验证与安全的 HTTPS 协议一起使用。

您还可以指定 Jira 事务的默认值：

    
    
    xpack.notification.jira:
      account:
        monitoring:
          issue_defaults:
            project:
              key: proj
            issuetype:
              name: Bug
            summary: "X-Pack Issue"
            labels: ["auto"]

如果配置多个 Jira 账户，则需要配置默认账户或在"jira"操作中指定应发送通知的账户。

    
    
    xpack.notification.jira:
      default_account: team1
      account:
        team1:
          ...
        team2:
          ...

[« Watcher PagerDuty action](actions-pagerduty.md) [Payload transforms
»](transform.md)
