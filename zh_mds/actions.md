

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« Watcher script condition](condition-script.md) [Running an action for
each element in an array »](action-foreach.md)

## 观察程序操作

当满足手表的条件时，除非受到限制，否则将执行其操作。一个手表可以执行多个操作。操作一次执行完成，每个操作独立执行。执行操作时遇到的任何故障都会记录在操作结果和监视历史记录中。

如果未为监视定义任何操作，则不会执行任何操作。但是，"watch_record"仍会写入观看历史记录。

操作可以访问执行上下文中的有效负载。他们可以使用它以他们需要的任何方式支持他们的执行。例如，有效负载可以用作模板化电子邮件正文的模型。

观察程序支持以下操作：

* "电子邮件" * "Webhook" * "索引" * "日志记录" * "松弛" * "PagerDuty" * "Jira"

### 确认和限制

在监视执行期间，一旦满足条件，就会根据配置操作决定是否应限制监视。操作限制的主要目的是防止同一手表执行过多的相同操作。

例如，假设您有一个监视，用于检测应用程序日志条目中的错误。手表每五分钟触发一次，并在最后一小时内搜索错误。在这种情况下，如果出现错误，则会在一段时间内检查手表并根据相同的错误多次执行其操作。因此，系统管理员会收到有关同一问题的多个通知，这可能很烦人。

为了解决此问题，观察程序支持基于时间的限制。您可以在操作配置中定义限制期，以限制执行操作的频率。设置限制周期时，如果操作已在限制周期时间范围内执行("现在 - 限制期")，则 Watcher 会阻止重复执行操作。

以下代码片段显示了上述方案的监视 - 将限制期与"email_administrator"操作相关联：

    
    
    PUT _watcher/watch/error_logs_alert
    {
      "metadata" : {
        "color" : "red"
      },
      "trigger" : {
        "schedule" : {
          "interval" : "5m"
        }
      },
      "input" : {
        "search" : {
          "request" : {
            "indices" : "log-events",
            "body" : {
              "size" : 0,
              "query" : { "match" : { "status" : "error" } }
            }
          }
        }
      },
      "condition" : {
        "compare" : { "ctx.payload.hits.total" : { "gt" : 5 }}
      },
      "actions" : {
        "email_administrator" : {
          "throttle_period": "15m", __"email" : { __"to" : "sys.admino@host.domain",
            "subject" : "Encountered {{ctx.payload.hits.total}} errors",
            "body" : "Too many error in the system, see attached data",
            "attachments" : {
              "attached_data" : {
                "data" : {
                  "format" : "json"
                }
              }
            },
            "priority" : "high"
          }
        }
      }
    }

__

|

后续的"email_administrator"操作执行之间将至少有 15 分钟。   ---|---    __

|

有关详细信息，请参阅电子邮件操作。   您还可以在手表级别定义限制周期。监视级别限制周期用作监视中定义的所有操作的默认限制周期：

    
    
    PUT _watcher/watch/log_event_watch
    {
      "trigger" : {
        "schedule" : { "interval" : "5m" }
      },
      "input" : {
        "search" : {
          "request" : {
            "indices" : "log-events",
            "body" : {
              "size" : 0,
              "query" : { "match" : { "status" : "error" } }
            }
          }
        }
      },
      "condition" : {
        "compare" : { "ctx.payload.hits.total" : { "gt" : 5 }}
      },
      "throttle_period" : "15m", __"actions" : {
        "email_administrator" : {
          "email" : {
            "to" : "sys.admino@host.domain",
            "subject" : "Encountered {{ctx.payload.hits.total}} errors",
            "body" : "Too many error in the system, see attached data",
            "attachments" : {
              "attached_data" : {
                "data" : {
                  "format" : "json"
                }
              }
            },
            "priority" : "high"
          }
        },
        "notify_pager" : {
          "webhook" : {
            "method" : "POST",
            "host" : "pager.service.domain",
            "port" : 1234,
            "path" : "/{{watch_id}}",
            "body" : "Encountered {{ctx.payload.hits.total}} errors"
          }
        }
      }
    }

__

|

后续操作执行之间至少有 15 分钟(适用于"email_administrator"和"notify_pager"操作)---|--- 如果未在操作或监视级别定义限制周期，则应用全局默认限制周期。最初，此值设置为 5 秒。要更改全局默认值，请在"elasticsearch.yml"中配置"xpack.watcher.execution.default_throttle_period"设置：

    
    
    xpack.watcher.execution.default_throttle_period: 15m

观察程序还支持基于确认的限制。您可以使用 ack watch API 确认 awatch，以防止在监视条件保持"true"时再次执行监视操作。这实质上告诉观察者"我收到了通知并且我正在处理它，请不要再通知我此错误"。已确认的监视操作将保持"已确认"状态，直到监视的状态评估结果为"假"。发生这种情况时，操作的状态将更改为"awaits_successful_execution"。

要确认操作，请使用确认监视 API：

    
    
    POST _watcher/watch/<id>/_ack/<action_ids>

其中""是<id>监视的 ID，"<action_ids>"是要确认的操作 ID 的逗号分隔列表。要确认所有操作，请省略"actions"参数。

下图说明了在监视执行期间为监视的每个操作所做的限制决策：

！操作限制

### 将 SSL/TLS 与 OpenJDK 结合使用

由于每个发行商都可以自由选择如何打包OpenJDK，因此即使版本完全相同，OpenJDK发行版也可能包含不同Linux发行版下的不同部分。

这可能会导致使用 TLS 的任何操作或输入出现问题，例如"jira"、"pagerduty"、"slack"或"webhook"，因为缺少 CA 证书。如果在编写连接到 TLS 端点的监视时遇到 TLS 错误，则应尝试升级到适用于您的平台的最新可用 OpenJDK发行版，如果这没有帮助，请尝试升级到 Oracle JDK。

[« Watcher script condition](condition-script.md) [Running an action for
each element in an array »](action-foreach.md)
