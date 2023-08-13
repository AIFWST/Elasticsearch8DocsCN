

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« Getting started with Watcher](watcher-getting-started.md) [Encrypting
sensitive data in Watcher »](encrypting-data.md)

## 观察者如何工作

添加监视以在满足特定条件时自动执行操作。条件通常基于已加载到手表中的数据，也称为_Watch Payload_。这个有效负载可以从不同的来源加载 - 从Elasticsearch，外部HTTP服务，甚至是两者的组合。

例如，您可以将监视配置为在日志数据中的搜索表明过去 5 分钟内有太多 503 错误时向系统管理员发送电子邮件。

本主题介绍手表的元素以及手表的工作原理。

### 监视定义

监视由 _trigger_、_input_、_condition_ 和 _actions_ 组成。这些操作定义了满足条件后需要执行的操作。此外，您可以定义 _conditions_ 和 _transforms_ 以在执行操作之前处理和准备监视有效负载。

触发

     Determines when the watch is checked. A watch must have a trigger. 
[Input](input.html "Watcher inputs")

     Loads data into the watch payload. If no input is specified, an empty payload is loaded. 
[Condition](condition.html "Watcher conditions")

     Controls whether the watch actions are executed. If no condition is specified, the condition defaults to `always`. 
[Transform](transform.html "Payload transforms")

     Processes the watch payload to prepare it for the watch actions. You can define transforms at the watch level or define action-specific transforms. Optional. 
[Actions](actions.html "Watcher actions")

     Specify what happens when the watch condition is met. 

例如，以下代码片段显示了一个创建或更新监视请求，该请求定义查找日志错误事件的监视：

    
    
    PUT _watcher/watch/log_errors
    {
      "metadata" : { __"color" : "red"
      },
      "trigger" : { __"schedule" : {
          "interval" : "5m"
        }
      },
      "input" : { __"search" : {
          "request" : {
            "indices" : "log-events",
            "body" : {
              "size" : 0,
              "query" : { "match" : { "status" : "error" } }
            }
          }
        }
      },
      "condition" : { __"compare" : { "ctx.payload.hits.total" : { "gt" : 5 }}
      },
      "transform" : { __"search" : {
            "request" : {
              "indices" : "log-events",
              "body" : {
                "query" : { "match" : { "status" : "error" } }
              }
            }
        }
      },
      "actions" : { __"my_webhook" : {
          "webhook" : {
            "method" : "POST",
            "host" : "mylisteninghost",
            "port" : 9200,
            "path" : "/{{watch_id}}",
            "body" : "Encountered {{ctx.payload.hits.total}} errors"
          }
        },
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
        }
      }
    }

__

|

元数据 - 可以将可选的静态元数据附加到监视。   ---|---    __

|

触发器 - 此计划触发器每 5 分钟执行一次监视。   __

|

输入 - 此输入搜索"日志事件"索引中的错误，并将响应加载到监视有效负载中。   __

|

条件 - 此条件检查是否存在超过 5 个错误事件(搜索响应中的命中)。如果有，则继续执行所有"操作"。   __

|

转换 - 如果满足监视条件，则此转换通过使用默认搜索类型"query_then_fetch"搜索错误，将所有错误加载到监视有效负载中。所有监视操作都可以访问此有效负载。   __

|

操作 - 此手表有两个操作。"my_webhook"操作会通知第三方系统该问题。"email_administrator"操作会向系统管理员发送高优先级电子邮件。包含错误的监视有效负载将附加到电子邮件中。   ### 监视执行编辑

添加监视时，观察程序会立即向相应的触发器引擎注册其触发器。具有"计划"触发器的监视将注册到"计划程序"触发器引擎。

调度程序跟踪时间并根据其计划触发监视。在每个节点上，包含一个".watches"分片，一个调度程序，绑定到观察程序生命周期运行。即使考虑了所有主节点和副本，当触发监视时，观察程序也会确保每个监视仅在其中一个分片上触发。添加的副本分片越多，可以执行的监视就越分散。如果添加或删除副本，则需要重新加载所有监视。如果重新定位分片，则此特定分片的主副本和所有副本都将重新加载。

由于监视是在监视分片所在的节点上执行的，因此可以使用分片分配筛选创建专用的观察程序节点。

您可以使用专用的"node.attr.role： watcher"属性配置节点，然后按如下所示配置".watches"索引：

    
    
    response = client.indices.put_settings(
      index: '.watches',
      body: {
        "index.routing.allocation.include.role": 'watcher'
      }
    )
    puts response
    
    
    PUT .watches/_settings
    {
      "index.routing.allocation.include.role": "watcher"
    }

当观察程序服务停止时，计划程序将随之停止。触发器引擎使用与用于执行监视的线程池不同的线程池。

触发监视时，观察程序会将其排队等待执行。创建"watch_record"文档并将其添加到观看历史记录中，并且手表的状态设置为"awaits_execution"。

当执行开始时，观察程序会为监视创建监视执行上下文。执行上下文为脚本和模板提供对监视元数据、有效负载、监视 ID、执行时间和触发器信息的访问权限。有关更多信息，请参阅监视执行上下文。

在执行过程中，观察程序：

1. 将输入数据作为有效负载加载到监视执行上下文中。这使数据可用于执行过程中的所有后续步骤。此步骤由手表的输入控制。  2. 评估监视条件以确定是否继续处理监视。如果满足条件(计算结果为"true")，则处理将推进到下一步。如果未满足(计算结果为"false")，则停止执行监视。  3. 将转换应用于监视有效负载(如果需要)。  4. 在满足条件且监视不受限制的情况下执行监视操作。

当监视执行完成后，执行结果将记录为a_Watch Record_在监视历史记录中。监视记录包括执行时间和持续时间、是否满足监视条件以及执行的每个操作的状态。

下图显示了监视执行过程：

！观看执行

### 监视确认和限制

观察程序支持基于时间和基于确认的限制。这使您能够防止对同一事件重复执行操作。

默认情况下，Watcher 使用基于时间的限制，限制周期为 5 秒。这意味着，如果手表每秒执行一次，则即使始终满足条件，其操作最多每 5 秒执行一次。您可以基于每个操作或在监视级别配置限制周期。

通过基于确认的限制，您可以告诉 Watcher 只要满足监视的条件，就不再发送有关监视的通知。一旦条件的计算结果为"false"，确认将被清除，观察者恢复正常执行监视操作。

有关详细信息，请参阅确认和限制。

### 监视活动状态

默认情况下，当您添加监视时，它会立即设置为 _active_ 状态，向相应的触发器引擎注册，并根据其配置的触发器执行。

您还可以将监视设置为 _inactive_ 状态。非活动监视未注册到触发器引擎，并且永远无法触发。

要在创建监视时将其设置为非活动状态，请将"活动"参数设置为 _inactive_。要停用现有手表，请使用停用手表 API。要重新激活非活动监视，请使用激活监视 API。

您可以使用执行监视 API 强制执行监视，即使监视处于非活动状态也是如此。

停用手表在各种情况下都很有用。例如，如果您有一台监视外部系统的手表，并且您需要关闭该系统进行维护，则可以停用该手表以防止它在维护时段内错误地报告可用性问题。

停用手表还可以让您将其保留以备将来使用，而无需将其从系统中删除。

### 脚本和模板

定义监视时可以使用脚本和模板。脚本和模板可以引用监视执行上下文中的元素，包括监视有效负载。执行上下文定义可在脚本中使用的变量和模板中的参数占位符。

Watcher 使用 Elasticsearch 脚本基础架构，该基础架构支持sinline和存储。脚本和模板由Elasticsearch编译和缓存，以优化重复执行。还支持自动加载。有关详细信息，请参阅编写脚本and_How以编写scripts_。

#### 监视执行上下文

以下代码片段显示了_Watch ExecutionContext_的基本结构：

    
    
    {
      "ctx" : {
        "metadata" : { ... }, __"payload" : { ... }, __"watch_id" : " <id>", __"execution_time" : "20150220T00:00:10Z", __"trigger" : { __"triggered_time" : "20150220T00:00:10Z",
          "scheduled_time" : "20150220T00:00:00Z"
        },
        "vars" : { ... } __}

__

|

监视定义中指定的任何静态元数据。   ---|---    __

|

当前监视有效负载。   __

|

正在执行的监视的 ID。   __

|

显示监视执行开始时间的时间戳。   __

|

有关触发器事件的信息。对于"计划"触发器，这包括"triggered_time"(触发手表的时间)和"scheduled_time"(计划触发手表的时间)。   __

|

在执行期间可由不同构造设置和访问的动态变量。这些变量的作用域为单个执行(即它们不会持久化，并且不能在同一监视的不同执行之间使用) #### 使用脚本编辑

可以使用脚本来定义条件和转换。默认脚本语言为无痛。

从 5.0 开始，Elasticsearch 附带了新的 Painless 脚本语言。除了提供广泛的功能集外，它最大的特点是它被正确沙盒化并且可以安全地在系统中的任何位置(包括inWatcher)使用，而无需启用动态脚本。

脚本可以引用监视执行上下文中的任何值或通过脚本参数显式传递的值。

例如，如果手表元数据包含"color"字段(例如"metadata"： {"color"： "red"}')，您可以使用 via 'ctx.metadata.color' 变量访问其值。如果传入"color"参数作为条件或转换定义的一部分(例如"参数"：{"color"： "red"}')，则可以通过"color"变量访问其值。

#### 使用模板

您可以使用模板定义监视的动态内容。在执行时，模板从监视执行上下文中提取数据。例如，您可以使用模板使用存储在监视有效负载中的数据填充"电子邮件"操作的"主题"字段。模板还可以访问通过模板参数显式传递的值。

您可以使用胡须脚本语言指定模板。

例如，以下代码片段显示了模板如何在发送的电子邮件中启用动态主题：

    
    
    {
      "actions" : {
        "email_notification" : {
          "email" : {
            "subject" : "{{ctx.metadata.color}} alert"
          }
        }
      }
    }

##### 内联模板和脚本

要定义内联模板或脚本，只需直接在字段的值中指定它。例如，以下代码片段使用引用上下文元数据中的"color"值的内联模板配置"电子邮件"操作的主题。

    
    
    "actions" : {
      "email_notification" : {
         "email" : {
           "subject" : "{{ctx.metadata.color}} alert"
         }
       }
      }
    }

对于脚本，您只需将内联脚本指定为"脚本"字段的值。例如：

    
    
    "condition" : {
      "script" : "return true"
    }

还可以通过使用正式对象定义作为字段值来显式指定内联类型。例如：

    
    
    "actions" : {
      "email_notification" : {
        "email" : {
          "subject" : {
             "source" : "{{ctx.metadata.color}} alert"
          }
        }
      }
    }

脚本的正式对象定义为：

    
    
    "condition" : {
      "script" : {
        "source": "return true"
      }
    }

##### 存储的模板和脚本

如果存储模板和脚本，则可以按 id 引用它们。

要引用存储的脚本或模板，请使用正式对象定义并在"id"字段中指定其 id。例如，以下代码段引用了"email_notification_subject"模板：

    
    
    {
      ...
      "actions" : {
        "email_notification" : {
          "email" : {
            "subject" : {
              "id" : "email_notification_subject",
              "params" : {
                "color" : "red"
              }
            }
          }
        }
      }
    }

[« Getting started with Watcher](watcher-getting-started.md) [Encrypting
sensitive data in Watcher »](encrypting-data.md)
