

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher actions](actions.md)

[« Watcher logging Action](actions-logging.md) [Watcher PagerDuty action
»](actions-pagerduty.md)

## 观察者松弛动作

使用"松弛"操作向 Slack 团队的频道或用户发送消息。要发送 Slack 消息，您需要在"elasticsearch.yml"中配置至少一个 Slack 帐户。

### 配置松弛操作

您可以在"操作"数组中配置 Slack 操作。特定于操作的属性是使用"slack"关键字指定的。

以下代码片段显示了一个简单的松弛操作定义：

    
    
    "actions" : {
      "notify-slack" : {
        "transform" : { ... },
        "throttle_period" : "5m",
        "slack" : {
          "message" : {
            "to" : [ "#admins", "@chief-admin" ], __"text" : "Encountered  {{ctx.payload.hits.total}} errors in the last 5 minutes (facepalm)" __}
        }
      }
    }

__

|

要向其发送消息的频道和用户。   ---|---    __

|

消息的内容。   ### 使用附件格式化松弛消息编辑

除了发送简单的基于文本的消息外，您还可以使用 Slack 附件机制来发送格式化的消息。观察程序利用 Slack 附件，使您能够从执行上下文有效负载动态填充模板化消息。

以下代码片段显示了标准邮件附件：

    
    
    "actions" : {
      "notify-slack" : {
        "throttle_period" : "5m",
        "slack" : {
          "account" : "team1",
          "message" : {
            "from" : "watcher",
            "to" : [ "#admins", "@chief-admin" ],
            "text" : "System X Monitoring",
            "attachments" : [
              {
                "title" : "Errors Found",
                "text" : "Encountered  {{ctx.payload.hits.total}} errors in the last 5 minutes (facepalm)",
                "color" : "danger"
              }
            ]
          }
        }
      }
    }

要定义从有效负载动态填充的附件模板，请在监视操作中指定"dynamic_attachments"。例如，动态附件可以引用有效负载中的直方图存储桶，并为每个存储桶构建一个附件。

在以下示例中，监视输入使用日期直方图聚合和 Slack 操作执行搜索：

1. 将有效负载转换为一个列表，其中列表中的每个项目都包含月份、该月的用户计数以及表示与该计数关联的情绪(危险或错误)的颜色。  2. 定义一个附件模板，该模板引用转换生成的列表中的项。

    
    
    "input" : {
      "search" : {
        "request" : {
          "body" : {
            "aggs" : {
              "users_per_month" : {
                "date_histogram" : {
                  "field" : "@timestamp",
                  "interval" : "month"
                }
              }
            }
          }
        }
      }
    },
    ...
    "actions" : {
      "notify-slack" : {
        "throttle_period" : "5m",
        "transform" : {
          "script" : {
            "source" : "['items': ctx.payload.aggregations.users_per_month.buckets.collect(bucket -> ['count': bucket.doc_count, 'name': bucket.key_as_string, 'color': bucket.doc_count < 100 ? 'danger' : 'good'])]",
            "lang" : "painless"
          }
        },
        "slack" : {
          "account" : "team1",
          "message" : {
            "from" : "watcher",
            "to" : [ "#admins", "@chief-admin" ],
            "text" : "System X Monitoring",
            "dynamic_attachments" : {
              "list_path" : "ctx.payload.items" __"attachment_template" : {
                "title" : "{{month}}", __"text" : "Users Count: {{count}}",
                "color" : "{{color}}"
              }
            }
          }
        }
      }
    }

__

|

操作的转换生成的列表。   ---|---    __

|

参数占位符引用转换生成的列表中的每个项中的属性。   ### 松弛动作属性编辑

姓名 |必填 |描述 ---|---|--- 'message.from'

|

no

|

要在 Slack 消息中显示的发件人姓名。覆盖传入网络钩子的配置名称。   "message.to"

|

yes

|

要向其发送消息的频道和用户。频道名称必须以"#"开头，用户名必须以"@"开头。接受字符串值或字符串值数组。   '消息图标'

|

no

|

要在 Slack 消息中显示的图标。覆盖传入 Webhook 的已配置图标。接受图像的公共 URL。   "消息.文本"

|

yes

|

消息内容。   "邮件附件"

|

no

|

松弛邮件附件。邮件附件使您能够创建格式更丰富的邮件。Slackattachments 文档中定义的指定数组。   "message.dynamic_attachments"

|

no

|

Slack 消息附件，可根据当前监视有效负载动态填充。有关更多信息，请参阅使用附件格式化 Slack 邮件。   'proxy.host'

|

no

|

要使用的代理主机(仅与"proxy.port"结合使用)"proxy.port"

|

no

|

要使用的代理端口(仅与"proxy.host"结合使用) ### 配置 SlackAccountsedit

您可以在"elasticsearch.yml"的"xpack.notification.slack"命名空间中配置 Watcher 可用于与 Slack 通信的帐户。

您需要一个具有传入Webhooks功能的Slack应用程序来配置Slack帐户。使用生成的 webhook URL 在 Elasticsearch 中设置您的 Slack 帐户。

要配置 Slack 帐户，您至少需要在 Elasticsearch 密钥库中指定帐户名和 webhook URL(请参阅安全设置)：

    
    
    bin/elasticsearch-keystore add xpack.notification.slack.account.monitoring.secure_url

你不能再使用"elasticsearch.yml"设置来配置Slack帐户。请改用 Elasticsearch 的安全密钥库方法。

您可以指定 Slack 通知属性的默认值：

    
    
    xpack.notification.slack:
      account:
        monitoring:
          message_defaults:
            from: x-pack
            to: notifications
            icon: http://example.com/images/watcher-icon.jpg
            attachment:
              fallback: "X-Pack Notification"
              color: "#36a64f"
              title: "X-Pack Notification"
              title_link: "https://www.elastic.co/guide/en/x-pack/current/index.html"
              text: "One of your watches generated this notification."
              mrkdwn_in: "pretext, text"

要通知多个频道，请在 Slack 中为每个频道创建一个 webhook URL，并在 Elasticsearch 中为多个 Slack 帐户创建一个(每个 webhook URL 一个)。

如果配置多个 Slack 帐户，则需要配置默认帐户，或者在"Slack"操作中指定应发送通知的帐户。

    
    
    xpack.notification.slack:
      default_account: team1
      account:
        team1:
          ...
        team2:
          ...

[« Watcher logging Action](actions-logging.md) [Watcher PagerDuty action
»](actions-pagerduty.md)
