

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Example watches](example-watches.md)

[« Example watches](example-watches.md) [Watcher limitations »](watcher-
limitations.md)

## 监视 Elasticsearchcluster 的状态

您可以轻松配置基本监视来监控 Elasticsearch 集群的运行状况：

* 安排监视并定义获取群集运行状况的输入。  * 添加评估运行状况的条件，以确定是否需要采取措施。  * 如果群集为红色，则执行操作。

#### 安排监视并添加输入

监视计划控件通常显示触发监视。监视输入获取要评估的数据。

定义计划的最简单方法是指定间隔。例如，以下计划每 10 秒运行一次：

    
    
    PUT _watcher/watch/cluster_health_watch
    {
      "trigger" : {
        "schedule" : { "interval" : "10s" } __}
    }

__

|

计划通常配置为运行频率较低。本示例将间隔设置为 10 秒，以便您可以轻松看到正在触发的监视。由于此手表运行频繁，因此在完成实验后不要忘记删除手表。   ---|--- 要获取集群的状态，可以调用 Elasticsearch 集群运行状况 API：

    
    
    response = client.cluster.health(
      pretty: true
    )
    puts response
    
    
    GET _cluster/health?pretty

要将运行状况加载到手表中，只需添加一个调用群集运行状况 API 的 HTTPinput：

    
    
    PUT _watcher/watch/cluster_health_watch
    {
      "trigger" : {
        "schedule" : { "interval" : "10s" }
      },
      "input" : {
        "http" : {
          "request" : {
            "host" : "localhost",
            "port" : 9200,
            "path" : "/_cluster/health"
          }
        }
      }
    }

如果您使用的是安全性，则还需要提供一些身份验证凭据作为监视配置的一部分：

    
    
    PUT _watcher/watch/cluster_health_watch
    {
      "trigger" : {
        "schedule" : { "interval" : "10s" }
      },
      "input" : {
        "http" : {
          "request" : {
            "host" : "localhost",
            "port" : 9200,
            "path" : "/_cluster/health",
            "auth": {
              "basic": {
                "username": "elastic",
                "password": "x-pack-test-password"
              }
            }
          }
        }
      }
    }

最好创建一个具有使用此类监视配置所需的最低权限的用户。

根据集群的配置方式，在监视可以访问集群之前，可能需要其他设置，例如密钥库、信任库或证书。有关详细信息，请参阅观察程序设置。

如果您查看监视历史记录，您会发现每次执行监视时，群集状态都会记录为"watch_record"的一部分。

例如，以下请求从观看历史记录中检索最近十条监视记录：

    
    
    response = client.search(
      index: '.watcher-history*',
      body: {
        sort: [
          {
            "result.execution_time": 'desc'
          }
        ]
      }
    )
    puts response
    
    
    GET .watcher-history*/_search
    {
      "sort" : [
        { "result.execution_time" : "desc" }
      ]
    }

#### 添加条件

条件评估已加载到监视中的数据，并确定是否需要执行任何操作。由于已定义将群集状态加载到监视中的输入，因此可以定义检查该状态的条件。

例如，您可以添加一个条件来检查状态是否为 RED。

    
    
    PUT _watcher/watch/cluster_health_watch
    {
      "trigger" : {
        "schedule" : { "interval" : "10s" } __},
      "input" : {
        "http" : {
          "request" : {
           "host" : "localhost",
           "port" : 9200,
           "path" : "/_cluster/health"
          }
        }
      },
      "condition" : {
        "compare" : {
          "ctx.payload.status" : { "eq" : "red" }
        }
      }
    }

__

|

计划通常配置为运行频率较低。本示例将间隔设置为 10 秒，以便您可以轻松看到正在触发的监视。   ---|--- 如果您查看观看历史记录，就会发现每次执行观看时，状况结果都会记录为"watch_record"的一部分。

若要检查是否满足条件，可以运行以下查询。

    
    
    response = client.search(
      index: '.watcher-history*',
      pretty: true,
      body: {
        query: {
          match: {
            "result.condition.met": true
          }
        }
      }
    )
    puts response
    
    
    GET .watcher-history*/_search?pretty
    {
      "query" : {
        "match" : { "result.condition.met" : true }
      }
    }

#### 采取行动

在观看历史记录中记录"watch_records"很好，但Watcher的真正功能是能够执行某些操作来响应警报。监视的操作定义了当监视条件为真时要执行的操作 - 您可以发送电子邮件、调用第三方 webhook 或将文档写入 Elasticsearch 索引或在满足监视条件时进行日志。

例如，您可以添加一个操作，以便在状态为 RED 时为集群状态信息编制索引。

    
    
    PUT _watcher/watch/cluster_health_watch
    {
      "trigger" : {
        "schedule" : { "interval" : "10s" }
      },
      "input" : {
        "http" : {
          "request" : {
           "host" : "localhost",
           "port" : 9200,
           "path" : "/_cluster/health"
          }
        }
      },
      "condition" : {
        "compare" : {
          "ctx.payload.status" : { "eq" : "red" }
        }
      },
      "actions" : {
        "send_email" : {
          "email" : {
            "to" : "username@example.org",
            "subject" : "Cluster Status Warning",
            "body" : "Cluster status is RED"
          }
        }
      }
    }

要让 Watcher 发送电子邮件，您必须在"elasticsearch.yml"配置文件中配置一个电子邮件帐户，然后重新启动 Elasticsearch。要添加电子邮件帐户，请设置"xpack.notification.email.account"属性。

例如，以下代码片段配置了一个名为"work"的单个 Gmail 帐户：

    
    
    xpack.notification.email.account:
      work:
        profile: gmail
        email_defaults:
          from: <email> __smtp:
          auth: true
          starttls.enable: true
          host: smtp.gmail.com
          port: 587
          user: <username> __password: <password> __

__

|

将"<email>"替换为要发送通知的电子邮件地址。   ---|---    __

|

将"<username>"替换为您的 Gmail 用户名(通常是您的 Gmail 地址)。   __

|

将"<password>"替换为您的 Gmail 密码。   如果为电子邮件帐户启用了高级安全选项，则需要执行其他步骤才能从 Watcher 发送电子邮件。有关详细信息，请参阅配置电子邮件帐户。

您可以查看观看记录或"status_index"以查看操作是否已执行。

    
    
    response = client.search(
      index: '.watcher-history*',
      pretty: true,
      body: {
        query: {
          match: {
            "result.condition.met": true
          }
        }
      }
    )
    puts response
    
    
    GET .watcher-history*/_search?pretty
    {
      "query" : {
        "match" : { "result.condition.met" : true }
      }
    }

#### 删除手表

由于"cluster_health_watch"配置为每 10 秒运行一次，因此请确保在完成试验后将其删除。否则，您将无限期地向自己发送垃圾邮件。

要删除监视，请使用删除监视 API：

    
    
    response = client.watcher.delete_watch(
      id: 'cluster_health_watch'
    )
    puts response
    
    
    DELETE _watcher/watch/cluster_health_watch

[« Example watches](example-watches.md) [Watcher limitations »](watcher-
limitations.md)
