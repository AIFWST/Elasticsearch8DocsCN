

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher inputs](input.md)

[« Watcher search input](input-search.md) [Watcher chain input »](input-
chain.md)

## 观察程序 HTTPinput

使用"http"输入向 HTTP 终结点提交请求，并在触发监视时将响应加载到监视执行上下文中。有关所有受支持的属性，请参阅HTTP 输入属性。

使用"http"输入，您可以：

* 查询外部 Elasticsearch 集群。"http"输入提供了一种将搜索请求提交到运行观察程序的集群以外的集群的方法。当您运行专用的观察器集群或需要搜索运行不同 Elasticsearch 版本的集群时，这非常有用。  * 查询搜索 API 以外的弹性搜索 API。例如，您可能希望从节点统计信息、群集运行状况或群集状态 API 加载数据。  * 查询外部网络服务。"http"输入使你能够从公开 HTTP 终结点的任何服务加载数据。这在 Elasticsearch 集群和其他系统之间架起了一座桥梁。

### 查询外部弹性搜索集群

要查询外部 Elasticsearch 集群，请将集群的"host"和"port"属性以及索引的搜索端点指定为"路径"。如果省略搜索正文，请求将返回指定索引中的所有文档：

    
    
    "input" : {
      "http" : {
        "request" : {
          "host" : "example.com",
          "port" : 9200,
          "path" : "/idx/_search"
        }
      }
    }

您可以使用完整的 Elasticsearch Query DSL 来执行更复杂的搜索。例如，以下"http"输入检索"类别"字段中包含"事件"的所有文档：

    
    
    "input" : {
      "http" : {
        "request" : {
          "host" : "host.domain",
          "port" : 9200,
          "path" : "/idx/_search",
          "body" :  "{\"query\" :  {  \"match\" : { \"category\" : \"event\"}}}"
        }
      }
    }

### 调用 ElasticsearchAPI

要从其他 Elasticsearch API 加载数据，请将 API 端点指定为 'path' 属性。使用 'params' 属性指定查询字符串参数。例如，以下"http"输入调用集群统计 API 并启用"human"属性：

    
    
    "input" : {
      "http" : {
        "request" : {
          "host" : "host.domain",
          "port" : 9200,
          "path" : "/_cluster/stats",
          "params" : {
            "human" : "true" __}
        }
      }
    }

__

|

启用此属性将以人类可读的格式返回响应中的"字节"值。   ---|--- ### 调用外部 Web 服务编辑

您可以使用"http"输入从任何外部 Web 服务获取数据。"http"输入支持基本身份验证。例如，以下输入提供访问"myservice"的用户名和密码：

    
    
    "input" : {
      "http" : {
        "request" : {
          "host" : "host.domain",
          "port" : 9200,
          "path" : "/myservice",
          "auth" : {
            "basic" : {
              "username" : "user",
              "password" : "pass"
            }
          }
        }
      }
    }

您还可以通过"params"属性传入特定于服务的 API 密钥和其他信息。例如，以下"http"输入从OpenWeatherMap服务加载阿姆斯特丹的当前天气预报：

    
    
    "input" : {
      "http" : {
        "request" : {
          "url" : "http://api.openweathermap.org/data/2.5/weather",
          "params" : {
            "lat" : "52.374031",
            "lon" : "4.88969",
            "appid" : "<your openweathermap appid>"
          }
        }
      }
    }

#### 使用基于令牌的身份验证

您还可以使用"持有者令牌"而不是基本身份验证来调用 API。"request.headers"对象包含 HTTP 标头：

    
    
    "input" : {
      "http" : {
        "request" : {
          "url": "https://api.example.com/v1/something",
          "headers": {
            "authorization" : "Bearer ABCD1234...",
            "content-type": "application/json"
            # other headers params..
            },
          "connection_timeout": "30s"
        }
      }
    }

### 使用模板

"http"输入支持模板化。您可以在指定"路径"、"正文"、标头值和参数值时使用模板。

例如，以下代码片段使用模板来指定要查询的索引，并将结果限制为过去五分钟内添加的文档：

    
    
    "input" : {
      "http" : {
        "request" : {
          "host" : "host.domain",
          "port" : 9200,
          "path" : "/{{ctx.watch_id}}/_search",
          "body" : "{\"query\" : {\"range\": {\"@timestamp\" : {\"from\": \"{{ctx.trigger.triggered_time}}||-5m\",\"to\": \"{{ctx.trigger.triggered_time}}\"}}}}"
          }
        }
      }

### 访问 HTTP 响应

如果响应正文的格式为 JSON 或 YAML，则会对其进行分析并将其加载到执行上下文中。如果响应正文未采用 JSON 或 YAML 格式，则会将其加载到有效负载的"_value"字段中。

条件、转换和操作通过执行上下文访问响应数据。例如，如果响应包含"消息"对象，则可以使用"ctx.payload.message"访问消息数据。

此外，可以使用"ctx.payload._headers"字段访问响应中的所有标头，也可以使用"ctx.payload._status_code"访问响应的HTTP状态代码。

### HTTP 输入属性

姓名 |必填 |默认 |描述 ---|---|---|--- 'request.scheme'

|

no

|

http

|

网址方案。有效值为："http"或"https"。   'request.host'

|

yes

|

-

|

要连接到的主机。   'request.port'

|

yes

|

-

|

http 服务正在侦听的端口。   '请求路径'

|

no

|

-

|

网址路径。路径可以是静态文本或包含"胡须"模板。URL 查询字符串参数必须通过 'request.params' 属性指定。   '请求方法'

|

no

|

get

|

HTTP 方法。支持的值包括："头"、"获取"、"发布"、"放置"和"删除"。   'request.headers'

|

no

|

-

|

HTTP 请求标头。标题值可以是静态文本或包含"胡须"模板。   'request.params'

|

no

|

-

|

网址查询字符串参数。参数值可以是静态文本，也可以包含"胡须"模板。   '请求.网址'

|

no

|

-

|

允许您通过指定一个真实的 URL 来设置 'request.scheme'， 'request.host'、'request.port' 和 'request.params' 添加一次，例如'https：//www.example.org：1234/mypath？foo=bar'。不能与这四个参数中的 on 结合使用。设置这些参数时，单独指定它们可能会覆盖它们。   'request.auth.basic.username'

|

no

|

-

|

HTTP 基本身份验证用户名"request.auth.basic.password"

|

no

|

-

|

HTTP 基本身份验证密码"request.proxy.host"

|

no

|

-

|

连接到主机时要使用的代理主机。   'request.proxy.port'

|

no

|

-

|

连接到主机时要使用的代理端口。   "request.connection_timeout"

|

no

|

10s

|

设置 http 连接的超时。如果无法在此时间内建立连接，则输入将超时并失败。   "request.read_timeout"

|

no

|

10s

|

从 http 连接读取数据的超时。如果在此时间内未收到响应，则输入将超时并失败。   '请求.正文'

|

no

|

-

|

HTTP 请求正文。正文可以是静态文本，也可以包含"胡须"模板。   "提取"

|

no

|

-

|

要从输入响应中提取并用作有效负载的 JSON 键数组。如果输入生成较大的响应，则可用于过滤要用作有效负载的相关响应部分。   "response_content_type"

|

no

|

json

|

响应正文将包含的预期内容类型。支持的值是"json"、"yaml"和"text"。如果格式为"文本"，则"提取"属性不能存在。请注意，这将覆盖 HTTP响应中返回的标头。如果将其设置为"文本"，则将为响应的主体分配并通过有效负载的"_value"变量访问。   指定"路径"、"参数"、"标头"和"正文"值时，可以在执行上下文中引用以下变量：

姓名 |描述 ---|--- 'ctx.watch_id'

|

当前正在执行的监视的 ID。   "ctx.execution_time"

|

此表的时间执行开始。   "ctx.trigger.triggered_time"

|

触发此手表的时间。   "ctx.trigger.scheduled_time"

|

这只手表应该被触发的时间。   'ctx.metadata.*'

|

与监视关联的任何元数据。   « 观察者搜索输入 观察者链输入 »