

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher actions](actions.md)

[« Adding conditions to Watcher actions](action-conditions.md) [Watcher
webhook action »](actions-webhook.md)

## 观察者电子邮件操作

使用"电子邮件"操作发送电子邮件通知。要发送电子邮件，您必须在"elasticsearch.yml"中配置至少一个电子邮件帐户。

电子邮件通知可以是纯文本或使用 HTML 设置样式。您可以使用模板包含来自监视执行有效负载的信息，并将整个监视有效负载附加到消息中。

有关支持的属性，请参阅电子邮件操作属性。电子邮件操作定义中缺少的任何属性都将在电子邮件帐户配置中查找。必须在电子邮件操作定义或帐户的"email_defaults"中设置必需的属性。

### 配置电子邮件操作

您可以在"操作"数组中配置电子邮件操作。特定于操作的属性使用"电子邮件"关键字指定。

例如，以下电子邮件操作使用模板在电子邮件正文中包含来自监视有效负载的数据：

    
    
    "actions" : {
      "send_email" : { __"email" : { __"to" : "username@example.org", __"subject" : "Watcher Notification", __"body" : "{{ctx.payload.hits.total}} error logs found" __}
      }
    }

__

|

操作的 ID。   ---|---    __

|

操作类型设置为"电子邮件"。   __

|

要将电子邮件发送到的一个或多个地址。必须在操作定义或电子邮件帐户配置中指定。   __

|

电子邮件的主题可以包含静态文本和 Mustache 模板。   __

|

电子邮件正文可以包含静态文本和 Mustache 模板。必须在操作定义或电子邮件帐户配置中指定。   ### 配置电子邮件附件编辑

您可以将任何 HTTP 服务中的执行上下文有效负载或数据附加到电子邮件通知。您可以配置的附件数量没有限制。

要配置附件，请指定附件的名称和附件类型："数据"、"http"或"报告"。"数据"附件类型将执行上下文有效负载附加到电子邮件。"http"附件类型使您能够发出 HTTP 请求并将响应附加到电子邮件。配置"http"附件类型时，必须指定请求 URL。"报告"附件类型是一种特殊类型，包括来自 kibana 的 PDFrender 仪表板。如果仪表板渲染完成，此类型会持续轮询 kibanaapp，从而防止长时间运行的 HTTP连接，这些连接可能会被两者之间的防火墙或负载均衡器杀死。

    
    
    "actions" : {
      "email_admin" : {
        "email": {
          "to": "John Doe <john.doe@example.com>",
          "attachments" : {
            "my_image.png" : { __"http" : { __"content_type" : "image/png",
                "request" : {
                  "url": "http://example.org/foo/my-image.png" __}
              }
            },
            "dashboard.pdf" : {
              "reporting" : {
                "url": "http://example.org:5601/api/reporting/generate/dashboard/Error-Monitoring"
              }
            },
            "data.yml" : {
              "data" : {
                "format" : "yaml" __}
            }
          }
        }
      }
    }

__

|

附件的 ID，用作电子邮件附件中的文件名。   ---|---    __

|

附件的类型及其特定配置。   __

|

要从中检索附件的 URL。   __

|

如果未指定格式，则数据附件默认为 JSON。   **表 82.'http' 附件类型属性**

姓名 |描述 ---|--- 'content_type'

|

设置电子邮件附件的内容类型。默认情况下，内容类型是从 HTTP 服务发送的响应中提取的。您可以显式指定内容类型，以确保在电子邮件中正确设置类型，以防响应未指定内容类型或指定不正确。自选。   "内联"

|

配置为附件以"内联"处置发送。这允许在HTML正文中使用嵌入的图像，这些图像在某些电子邮件客户端中显示。自选。默认为"假"。   "请求"

|

包含 HTTP 请求属性。至少必须指定"url"属性来配置主机和服务终结点的路径。有关 HTTP 请求属性的完整列表，请参阅 Webhookaction 属性。必填。   **表 83."数据"附件类型属性**

姓名 |描述 ---|--- "格式"

|

附加监视数据，等效于在监视配置中指定"attach_data"。可能的值是"json"或"yaml"。如果未指定，则默认为"json"。   **表 84."报告"附件类型属性**

姓名 |描述 ---|--- 'url'

|

用于触发"内联"仪表板创建的 URL

|

配置为附件以"内联"处置发送。这允许在HTML正文中使用嵌入的图像，这些图像在某些电子邮件客户端中显示。自选。默认为"假"。   "重试"

|

报告附件类型尝试定期轮询以接收创建的 PDF。这将配置重试次数。默认为"40"。设置"xpack.notification.reporting.retries"可以全局配置以更改默认值。   "间隔"

|

在两次轮询尝试之间等待的时间。默认为"15s"(这意味着，默认情况下，观察程序尝试下载仪表板 10 分钟，40 次 15 秒)。设置"xpack.notification.reporting.interval"可以全局配置以更改默认值。   '请求.auth'

|

请求"request.proxy"的其他身份验证配置

|

请求的其他代理配置 #### 将报告附加到电子邮件编辑

您可以在"电子邮件"操作中使用"报告"附件类型自动生成 Kibana 报告并通过电子邮件分发。

请参阅自动生成报告。

### 电子邮件操作属性

姓名 |必填 |默认 |描述 ---|---|---|--- '帐户'

|

no

|

默认帐户

|

用于发送电子邮件的电子邮件帐户。   "从"

|

no

|

-

|

发送电子邮件的电子邮件地址。"发件人"字段可以包含 Mustache 模板，只要它解析为有效的电子邮件地址即可。   "到"

|

yes

|

-

|

"收件人"收件人的电子邮件地址。"to"字段可以包含 Mustache 模板，只要它解析为有效的电子邮件地址即可。   "抄送"

|

no

|

-

|

"抄送"收件人的电子邮件地址。"cc"字段可以包含 Mustache 模板，只要它解析为有效的电子邮件地址即可。   "密件抄送"

|

no

|

-

|

"密件抄送"收件人的电子邮件地址。"密件抄送"字段可以包含 Mustache 模板，只要它解析为有效的电子邮件地址即可。   "reply_to"

|

no

|

-

|

将在邮件的"回复"标头上设置的电子邮件地址。"reply_to"字段可以包含胡子模板，只要它解析为有效的电子邮件地址即可。   "主题"

|

no

|

-

|

电子邮件的主题。主题可以是静态文本或包含胡须模板。   "身体"

|

no

|

-

|

电子邮件的正文。当此字段包含字符串时，它将默认为电子邮件的文本正文。设置为对象以指定文本或 html 正文或两者(使用以下字段)"body.text"

|

no

|

-

|

电子邮件的纯文本正文。正文可以是静态文本或包含胡须模板。   "身体.html"

|

no

|

-

|

电子邮件的 html 正文。正文可以是静态文本或包含胡须模板。此正文将被清理以删除脚本等危险内容。可以通过在"elasticsearch.yaml"中设置"xpack.notification.email.html.sanitization.enabled： false"来禁用此行为。   "优先级"

|

no

|

-

|

此电子邮件的优先级。有效值为："最低"、"低"、"正常"、"高"和"最高"。优先级可以包含 Mustache 模板，只要它解析为其中一个有效值即可。   "附件"

|

no

|

-

|

将监视有效负载("数据"附件)或从 HTTP 服务检索的文件("http"附件)附加到电子邮件。有关详细信息，请参阅配置电子邮件附件。   "attach_data"

|

no

|

false

|

指示是否应将监视执行数据附加到电子邮件中。可以指定布尔值或对象。如果"attach_data"设置为"true"，则数据将作为 YAML 文件附加。此属性已弃用，请使用"附件"属性添加"数据"附件以附加监视有效负载。   "attach_data.格式"

|

no

|

yaml

|

当将"attach_data"指定为对象时，此字段控制附加数据的格式。支持的格式是"json"和"yaml"。此属性已弃用，请使用"附件"属性添加"数据"附件以附加监视有效负载。   电子邮件地址

     An email address can contain two possible parts--​the address itself and an optional personal name as described in [RFC 822](http://www.ietf.org/rfc/rfc822.txt). The address can be represented either as a string of the form `user@host.domain` or `Personal Name <user@host.domain>`. You can also specify an email address as an object that contains `name` and `address` fields. 

地址列表

     A list of addresses can be specified as a an array: `[ 'Personal Name <user1@host.domain>', 'user2@host.domain' ]`. 

### 配置电子邮件帐户

观察程序可以使用任何 SMTP 电子邮件服务发送电子邮件。电子邮件可以包含基本的 HTML 标记。您可以通过配置 HTML 清理选项来控制允许的标记组。

您可以配置观察程序可用于在"elasticsearch.yml"中的"xpack.notification.email"命名空间中发送电子邮件的帐户。指定 SMTP 用户的密码安全地存储在 Elasticsearchkeystore 中。

如果电子邮件帐户配置为需要双重验证，则需要生成并使用唯一的应用专用密码才能从 Watcher 发送电子邮件。如果使用主密码，身份验证将失败。

Watcher 提供了三个电子邮件配置文件来控制 MIME 邮件的结构："标准"(默认)、"gmail"和"outlook"。这些配置文件适应了各种电子邮件系统解释 MIME标准的方式的差异。如果您使用的是Gmail或Outlook，我们建议您使用相应的配置文件。如果您使用的是其他电子邮件系统，请使用"标准"配置文件。

有关配置观察程序以使用不同电子邮件系统的详细信息，请参阅：

* 从 Gmail 发送电子邮件 * 从 Outlook.com 发送电子邮件 * 从 Microsoft Exchange 发送电子邮件 * 从 Amazon SES(简单电子邮件服务)发送电子邮件")

如果配置多个电子邮件帐户，则必须配置默认帐户或在"电子邮件"操作中指定应使用哪个帐户发送电子邮件。

    
    
    xpack.notification.email:
      default_account: team1
      account:
        team1:
          ...
        team2:
          ...

##### 从 Gmail 发送电子邮件

使用以下电子邮件帐户设置从 Gmail SMTP 服务发送电子邮件：

    
    
    xpack.notification.email.account:
        gmail_account:
            profile: gmail
            smtp:
                auth: true
                starttls.enable: true
                host: smtp.gmail.com
                port: 587
                user: <username>

要存储帐户 SMTP 密码，请使用密钥库命令(请参阅安全设置)

    
    
    bin/elasticsearch-keystore add xpack.notification.email.account.gmail_account.smtp.secure_password

如果您收到身份验证错误，指示您需要在 Watcher 尝试发送电子邮件时继续从网络浏览器登录过程，则需要将 Gmail 配置为允许安全性较低的应用访问您的帐号。

如果为您的帐户启用了双重验证，则必须生成并使用唯一的应用专用密码才能从 Watcher 发送电子邮件。有关详细信息，请参阅使用应用密码登录。

##### 发送电子邮件 fromOutlook.com

使用以下电子邮件帐户设置从 SMTP 服务发送电子邮件操作 theOutlook.com：

    
    
    xpack.notification.email.account:
        outlook_account:
            profile: outlook
            smtp:
                auth: true
                starttls.enable: true
                host: smtp-mail.outlook.com
                port: 587
                user: <email.address>

要存储帐户 SMTP 密码，请使用密钥库命令(请参阅安全设置)

    
    
    bin/elasticsearch-keystore add xpack.notification.email.account.outlook_account.smtp.secure_password

发送电子邮件时，您必须提供发件人地址，可以是帐户配置中的默认地址，也可以是手表中电子邮件操作的一部分。

如果启用了两步验证，则需要使用唯一的应用专用密码。有关详细信息，请参阅应用密码和两步验证。

##### 从 Amazon SES (Simple EmailService) 发送电子邮件

使用以下电子邮件账户设置从 Amazon SimpleEmail Service (SES) SMTP 服务发送电子邮件：

    
    
    xpack.notification.email.account:
        ses_account:
            email_defaults:
                from: <email address of service account> __smtp:
                auth: true
                starttls.enable: true
                starttls.required: true
                host: email-smtp.us-east-1.amazonaws.com __port: 587
                user: <username>

__

|

在某些情况下，Amazon SES 会验证"email_defaults.from"，以确保它是有效的本地电子邮件账户。   ---|---    __

|

"smtp.host"因地区而异。   要存储帐户 SMTP 密码，请使用密钥库命令(请参阅安全设置)

    
    
    bin/elasticsearch-keystore add xpack.notification.email.account.ses_account.smtp.secure_password

您需要使用 Amazon SES SMTP 凭证通过 AmazonSES 发送电子邮件。有关更多信息，请参阅 获取您的 Amazon SES SMTPCredentials。您可能还需要验证您在 AWS 上的电子邮件地址或整个域。

##### 从微软交易所发送电子邮件

使用以下电子邮件帐户设置从 MicrosoftExchange 发送电子邮件操作：

    
    
    xpack.notification.email.account:
        exchange_account:
            profile: outlook
            email_defaults:
                from: <email address of service account> __smtp:
                auth: true
                starttls.enable: true
                host: <your exchange server>
                port: 587
                user: <email address of service account> __

__

|

某些组织将 Exchange 配置为验证"发件人"字段是否为有效的本地电子邮件帐户。   ---|---    __

|

许多组织支持使用您的电子邮件地址作为用户名，但是如果您收到与身份验证相关的失败，最好与系统管理员联系。   要存储帐户 SMTP 密码，请使用密钥库命令(请参阅安全设置)

    
    
    bin/elasticsearch-keystore add xpack.notification.email.account.exchange_account.smtp.secure_password

##### 配置 HTML 清理选项

"电子邮件"操作支持使用 HTML 正文发送邮件。但是，出于安全原因，Watchersanitize HTML。

您可以通过在"elasticsearch.yml"中配置"xpack.notification.email.html.sanitization.allow"和"xpack.notification.email.html.sanitization.disallow"设置来控制允许或不允许哪些HTML功能。您可以指定单个 HTML 元素和 HTML 功能组。默认情况下，Watcher 允许以下功能："body"、"head"、"_tables"、"_links"、"_blocks"、"_formatting"和"img：embedded"。

例如，以下设置允许 HTML 包含表和块元素，但不允许 '''<h4>、<h5>'' <h6>和 '' 标记。

    
    
    xpack.notification.email.html.sanitization:
        allow: _tables, _blocks
        disallow: h4, h5, h6

要完全禁用清理，请将以下设置添加到"elasticsearch.yml"：

    
    
    xpack.notification.email.html.sanitization.enabled: false

[« Adding conditions to Watcher actions](action-conditions.md) [Watcher
webhook action »](actions-webhook.md)
