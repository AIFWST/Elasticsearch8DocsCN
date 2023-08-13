

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher actions](actions.md)

[« Watcher email action](actions-email.md) [Watcher index action »](actions-
index.md)

## 观察者网络钩子操作

使用"webhook"操作将请求发送到任何 Web 服务。webhookaction 支持 HTTP 和 HTTPS 连接。有关支持的属性，请参阅 Webhook 操作属性。

### 配置 Webhookaction

您可以在"操作"数组中配置 Webhook 操作。特定于操作的属性是使用"webhook"关键字指定的。

以下代码片段显示了一个简单的 Webhook 操作定义：

    
    
    "actions" : {
      "my_webhook" : { __"transform" : { ... }, __"throttle_period" : "5m", __"webhook" : {
          "method" : "POST", __"host" : "mylisteningserver", __"port" : 9200, __"path": "/{{ctx.watch_id}}", __"body" : "{{ctx.watch_id}}:{{ctx.payload.hits.total}}" __}
      }
    }

__

|

操作的 id ---|--- __

|

一个可选的转换，用于在执行"webhook"操作之前转换有效负载 __

|

操作的可选限制周期(在本例中为 5 分钟)__

|

连接到主机时要使用的 HTTP 方法 __

|

要连接到的主机 __

|

要连接到的端口 __

|

要在 HTTP 请求中使用的路径 (URI) __

|

要随请求一起发送的正文 在向受保护的 Web 服务发送请求时，可以使用基本身份验证。例如，以下"webhook"操作会在 GitHub 中创建新问题：

    
    
    "actions" : {
      "create_github_issue" : {
        "transform": {
          "script": "return ['title':'Found errors in \\'contact.html\\'', 'body' : 'Found ' + ctx.payload.hits.total + ' errors in the last 5 minutes', 'assignee' : 'web-admin', 'labels' : ['bug','sev2']]"
        },
        "webhook" : {
          "method" : "POST",
          "url" : "https://api.github.com/repos/<owner>/<repo>/issues",
          "body": "{{#toJson}}ctx.payload{{/toJson}}",
          "auth" : {
            "basic" : {
              "username" : "<username>", __"password" : " <password>"
            }
          }
        }
      }
    }

__

|

创建问题的用户的用户名和密码 ---|--- 默认情况下，用户名和密码都以纯文本形式存储在".watches"索引中。启用 Elasticsearch 安全功能后，观察器可以在存储密码之前对其进行加密。

在向启用了 Elasticsearch 安全功能的集群提交请求时，您还可以使用基于 PKI 的身份验证。使用基于 PKI 的身份验证而不是 HTTP 基本身份验证时，无需在手表本身中存储任何身份验证信息。要使用基于 PKI 的身份验证，请在"elasticsearch.yml"中为 Watcher 配置 SSL 密钥设置。

### 查询参数

您可以使用"params"字段指定要随请求一起发送的查询参数。此字段仅保存一个对象，其中键用作参数名称，值用作参数值：

    
    
    "actions" : {
      "my_webhook" : {
        "webhook" : {
          "method" : "POST",
          "host" : "mylisteningserver",
          "port" : 9200,
          "path": "/alert",
          "params" : {
            "watch_id" : "{{ctx.watch_id}}" __}
        }
      }
    }

__

|

参数值可以包含模板化字符串。   ---|--- ### 自定义请求标头编辑

您可以使用"标头"字段指定要与请求一起发送的请求标头。此字段仅保存一个对象，其中键用作标头名称，值用作标头值：

    
    
    "actions" : {
      "my_webhook" : {
        "webhook" : {
          "method" : "POST",
          "host" : "mylisteningserver",
          "port" : 9200,
          "path": "/alert/{{ctx.watch_id}}",
          "headers" : {
            "Content-Type" : "application/yaml" __},
          "body" : "count: {{ctx.payload.hits.total}}"
        }
      }
    }

__

|

标头值可以包含模板化字符串。   ---|--- ### Webhook actionattributesedit

姓名 |必填 |默认 |描述 ---|---|---|--- 'scheme'

|

no

|

http

|

连接方案。有效值为："http"或"https"。   "主机"

|

yes

|

-

|

要连接到的主机。   "端口"

|

yes

|

-

|

HTTP 服务正在侦听的端口。   "路径"

|

no

|

-

|

网址路径。路径可以是静态文本或包含胡须模板。URL 查询字符串参数必须通过"request.params"属性指定。   "方法"

|

no

|

get

|

HTTP 方法。有效值为："头"、"获取"、"发布"、"放置"和"删除"。   "标题"

|

no

|

-

|

HTTP 请求标头。标头值可以是静态文本或包含胡须模板。   "参数"

|

no

|

-

|

网址查询字符串参数。参数值可以是静态文本，也可以包含 Mustache 模板。   "身份验证"

|

no

|

-

|

与身份验证相关的 HTTP 标头。目前仅支持基本身份验证。   "身体"

|

no

|

-

|

HTTP 请求正文。正文可以是静态文本或包含胡子模板。如果未指定，则发送空正文。   'proxy.host'

|

no

|

-

|

连接到主机时要使用的代理主机。   'proxy.port'

|

no

|

-

|

连接到主机时要使用的代理端口。   "connection_timeout"

|

no

|

10s

|

设置 http 连接的超时。如果无法在此时间内设置连接，则操作将超时并失败。   "read_timeout"

|

no

|

10s

|

从 http 连接读取数据的超时。如果在此时间内未收到响应，则操作将超时并失败。   "网址"

|

no

|

-

|

用于将请求方案、主机、端口和路径指定为单个字符串的快捷方式。例如，"http://example.org/foo/my-service"。   « 观察者电子邮件操作 观察程序索引操作 »