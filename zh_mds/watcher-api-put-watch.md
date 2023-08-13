

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Query watches API](watcher-api-query-watches.md) [Update Watcher index
settings »](watcher-api-update-settings.md)

## 创建或更新监视接口

在观察程序中注册新监视或更新现有监视。

###Request

"放_watcher/看/<watch_id>"

###Prerequisites

* 您必须具有"manage_watcher"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

注册手表后，代表手表的新文档将添加到".watches"索引中，其触发器会立即注册到相关触发器引擎。通常，对于"计划"触发器，计划程序是触发器引擎。

您必须使用 Kibana 或此 API 来创建监视。不要使用 Elasticsearch 索引 API 将手表直接添加到 '.watches' 索引中。如果启用了 Elasticsearchsecurity 功能，请不要授予用户对".watches"索引的"写入"权限。

添加监视时，还可以定义其初始活动状态。您可以通过设置"活动"参数来执行此操作。

#### 安全集成

启用 Elasticsearch 安全功能后，您的手表只能对存储手表的用户具有权限的索引进行索引或搜索。如果用户能够读取索引"a"，但不能读取索引"b"，则在执行监视时将同样适用。

### 路径参数

`<watch_id>`

     (Required, string) Identifier for the watch. 

### 查询参数

`active`

     (Optional, Boolean) Defines whether the watch is active or inactive by default. The default value is `true`, which means the watch is active by default. 

### 请求正文

手表具有以下字段：

姓名 |描述 ---|--- '触发器'

|

定义监视应何时运行的触发器。   "输入"

|

定义为监视加载数据的输入的输入。   "条件"

|

定义是否应运行操作的条件。   "行动"

|

条件与"转换"匹配时将运行的操作列表

|

处理监视有效负载以使其为监视操作做好准备的转换。   "元数据"

|

将复制到历史记录条目中的元数据 json。   "throttle_period"

|

运行操作之间的最短时间，默认值为 5 秒。可以在配置文件中使用"xpack.watcher.throttle.period.default_period"设置更改此默认值。如果同时指定了此值和"throttle_period_in_millis"参数，则观察程序将使用请求中包含的最后一个参数。   "throttle_period_in_millis"

|

运行操作之间的最短时间(以毫秒为单位)。默认为"5000"。如果同时指定了此值和"throttle_period"参数，则 Watcher 将使用请求中包含的最后一个参数。   ###Examplesedit

以下示例添加具有"my-watch"ID 的手表，该手表具有以下特征：

* 手表时间表每分钟触发一次。  * 监视搜索输入查找过去五分钟内发生的任何 404 HTTP 响应。  * 监视条件检查是否有任何搜索命中找到的位置。  * 找到后，监视操作会向管理员发送电子邮件。

    
    
    PUT _watcher/watch/my-watch
    {
      "trigger" : {
        "schedule" : { "cron" : "0 0/1 * * * ?" }
      },
      "input" : {
        "search" : {
          "request" : {
            "indices" : [
              "logstash*"
            ],
            "body" : {
              "query" : {
                "bool" : {
                  "must" : {
                    "match": {
                       "response": 404
                    }
                  },
                  "filter" : {
                    "range": {
                      "@timestamp": {
                        "from": "{{ctx.trigger.scheduled_time}}||-5m",
                        "to": "{{ctx.trigger.triggered_time}}"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      },
      "condition" : {
        "compare" : { "ctx.payload.hits.total" : { "gt" : 0 }}
      },
      "actions" : {
        "email_admin" : {
          "email" : {
            "to" : "admin@domain.host.com",
            "subject" : "404 recently encountered"
          }
        }
      }
    }

添加监视时，还可以定义其初始活动状态。您可以通过设置"活动"参数来执行此操作。以下命令添加监视并将其默认设置为非活动状态：

    
    
    PUT _watcher/watch/my-watch?active=false

如果省略"active"参数，则默认情况下手表处于活动状态。

[« Query watches API](watcher-api-query-watches.md) [Update Watcher index
settings »](watcher-api-update-settings.md)
