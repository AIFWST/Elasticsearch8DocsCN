

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Run downsampling manually](downsampling-manual.md) [Example: Parse logs
in the Common Log Format »](common-log-format-example.md)

# 引入管道

引入管道允许您在编制索引之前对数据执行常见转换。例如，可以使用管道删除字段、从文本中提取值以及丰富数据。

管道由一系列称为处理器的可配置任务组成。每个处理器按顺序运行，对传入的文档进行特定更改。处理器运行后，Elasticsearch 会将转换后的文档添加到您的数据流或索引中。

!采集管道图

您可以使用 Kibana 的采集管道功能或采集 API 创建和管理采集管道。Elasticsearch将管道存储在集群状态。

###Prerequisites

* 具有"摄取"节点角色的节点处理管道处理。要使用引入管道，群集必须至少有一个具有"引入"角色的节点。对于繁重的摄取负载，我们建议创建专用的摄取节点。  * 如果启用了 Elasticsearch 安全功能，您必须具有"manage_pipeline"集群权限才能管理采集管道。要使用 Kibana 的 **采集管道** 功能，您还需要"集群：监视器/节点/信息"集群权限。  * 包括"扩充"处理器的管道需要额外的设置。请参阅_Enrich您的data_。

### 创建和管理管道

在 Kibana 中，打开主菜单并单击"堆栈管理">"摄取管道"。在列表视图中，您可以：

* 查看管道列表并深入了解详细信息 * 编辑或克隆现有管道 * 删除管道

!Kibana 的采集管道列表视图

若要创建管道，请单击"**创建管道">"新建管道**"。有关示例教程，请参阅_Example：分析logs_。

通过 CSV 新建管道选项，您可以使用 CSV 创建将自定义数据映射到弹性通用架构 (ECS) 的采集管道。将自定义数据映射到 ECS 使数据更易于搜索，并允许您重复使用其他数据集中的可视化。如需开始使用，请查看将自定义数据映射到 ECS。

还可以使用引入 API 来创建和管理管道。以下创建管道 API 请求创建一个包含两个"设置"处理器的管道，后跟一个"小写"处理器。处理器按指定的顺序依次运行。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        description: 'My optional pipeline description',
        processors: [
          {
            set: {
              description: 'My optional processor description',
              field: 'my-long-field',
              value: 10
            }
          },
          {
            set: {
              description: "Set 'my-boolean-field' to true",
              field: 'my-boolean-field',
              value: true
            }
          },
          {
            lowercase: {
              field: 'my-keyword-field'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "description": "My optional pipeline description",
      "processors": [
        {
          "set": {
            "description": "My optional processor description",
            "field": "my-long-field",
            "value": 10
          }
        },
        {
          "set": {
            "description": "Set 'my-boolean-field' to true",
            "field": "my-boolean-field",
            "value": true
          }
        },
        {
          "lowercase": {
            "field": "my-keyword-field"
          }
        }
      ]
    }

### 管理管道版本

创建或更新管道时，可以指定可选的"版本"整数。可以将此版本号与"if_version"参数一起使用，以有条件地更新管道。指定"if_version"参数时，成功的更新将递增管道的版本。

    
    
    PUT _ingest/pipeline/my-pipeline-id
    {
      "version": 1,
      "processors": [ ... ]
    }

要使用 API 取消设置"版本"编号，请替换或更新管道而不指定"版本"参数。

### 测试管道

在生产中使用管道之前，建议使用示例文档对其进行测试。在 Kibana 中创建或编辑管线时，请单击"**添加文档**"。在"**文档**"选项卡中，提供示例文档，然后单击"**运行管道**"。

!在 Kibana 中测试管道

还可以使用模拟管道 API 测试管道。您可以在请求路径中指定已配置的管道。例如，以下请求测试"my-pipeline"。

    
    
    response = client.ingest.simulate(
      id: 'my-pipeline',
      body: {
        docs: [
          {
            _source: {
              "my-keyword-field": 'FOO'
            }
          },
          {
            _source: {
              "my-keyword-field": 'BAR'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _ingest/pipeline/my-pipeline/_simulate
    {
      "docs": [
        {
          "_source": {
            "my-keyword-field": "FOO"
          }
        },
        {
          "_source": {
            "my-keyword-field": "BAR"
          }
        }
      ]
    }

或者，您可以在请求正文中指定管道及其处理器。

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          processors: [
            {
              lowercase: {
                field: 'my-keyword-field'
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              "my-keyword-field": 'FOO'
            }
          },
          {
            _source: {
              "my-keyword-field": 'BAR'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _ingest/pipeline/_simulate
    {
      "pipeline": {
        "processors": [
          {
            "lowercase": {
              "field": "my-keyword-field"
            }
          }
        ]
      },
      "docs": [
        {
          "_source": {
            "my-keyword-field": "FOO"
          }
        },
        {
          "_source": {
            "my-keyword-field": "BAR"
          }
        }
      ]
    }

API 返回转换后的文档：

    
    
    {
      "docs": [
        {
          "doc": {
            "_index": "_index",
            "_id": "_id",
            "_version": "-3",
            "_source": {
              "my-keyword-field": "foo"
            },
            "_ingest": {
              "timestamp": "2099-03-07T11:04:03.000Z"
            }
          }
        },
        {
          "doc": {
            "_index": "_index",
            "_id": "_id",
            "_version": "-3",
            "_source": {
              "my-keyword-field": "bar"
            },
            "_ingest": {
              "timestamp": "2099-03-07T11:04:04.000Z"
            }
          }
        }
      ]
    }

### 将管道添加到索引请求

使用"管道"查询参数将管道应用于单个或批量索引请求的文档。

    
    
    response = client.index(
      index: 'my-data-stream',
      pipeline: 'my-pipeline',
      body: {
        "@timestamp": '2099-03-07T11:04:05.000Z',
        "my-keyword-field": 'foo'
      }
    )
    puts response
    
    response = client.bulk(
      index: 'my-data-stream',
      pipeline: 'my-pipeline',
      body: [
        {
          create: {}
        },
        {
          "@timestamp": '2099-03-07T11:04:06.000Z',
          "my-keyword-field": 'foo'
        },
        {
          create: {}
        },
        {
          "@timestamp": '2099-03-07T11:04:07.000Z',
          "my-keyword-field": 'bar'
        }
      ]
    )
    puts response
    
    
    POST my-data-stream/_doc?pipeline=my-pipeline
    {
      "@timestamp": "2099-03-07T11:04:05.000Z",
      "my-keyword-field": "foo"
    }
    
    PUT my-data-stream/_bulk?pipeline=my-pipeline
    { "create":{ } }
    { "@timestamp": "2099-03-07T11:04:06.000Z", "my-keyword-field": "foo" }
    { "create":{ } }
    { "@timestamp": "2099-03-07T11:04:07.000Z", "my-keyword-field": "bar" }

还可以将"管道"参数与通过查询更新或重新索引 API 一起使用。

    
    
    response = client.update_by_query(
      index: 'my-data-stream',
      pipeline: 'my-pipeline'
    )
    puts response
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-data-stream'
        },
        dest: {
          index: 'my-new-data-stream',
          op_type: 'create',
          pipeline: 'my-pipeline'
        }
      }
    )
    puts response
    
    
    POST my-data-stream/_update_by_query?pipeline=my-pipeline
    
    POST _reindex
    {
      "source": {
        "index": "my-data-stream"
      },
      "dest": {
        "index": "my-new-data-stream",
        "op_type": "create",
        "pipeline": "my-pipeline"
      }
    }

### 设置默认管道

使用"index.default_pipeline"索引设置设置默认管道。如果未指定"pipeline"参数，Elasticsearch 将此管道应用于索引请求。

### 设置最终管道

使用"index.final_pipeline"索引设置设置最终管道。Elasticsearch 在请求或默认管道之后应用此管道，即使两者都未指定。

### Pipelines forBeats

要将采集管道添加到 Elastic Beat，请在".yml"中的"output.elasticsearch"下指定"管道<BEAT_NAME>"参数。例如，对于Filebeat，您可以在"filebeat.yml"中指定"pipeline"。

    
    
    output.elasticsearch:
      hosts: ["localhost:9200"]
      pipeline: my-pipeline

### Fleet 和 ElasticAgent 的管道

Elastic 代理集成附带默认采集管道，可在索引之前预处理和丰富数据。Fleet使用包含管道索引设置的索引模板应用这些管道。Elasticsearch 根据流的命名方案将这些模板与您的队列数据流进行匹配。

每个默认集成管道都调用一个不存在的、不受版本控制的"@custom"摄取管道。如果未更改，则此管道调用对数据没有影响。但是，您可以修改此调用，以便为跨升级保留的集成创建自定义管道。请参阅教程：使用自定义管道转换数据以了解更多信息。

Fleet 不会为**自定义日志**集成提供默认摄取管道，但您可以使用索引模板或自定义配置为此集成指定管道。

选项 1：索引模板**

1. 创建并测试采集管道。将管道命名为"日志 - <dataset-name>默认"。这样可以更轻松地跟踪集成的管道。

例如，以下请求为"我的应用"数据集创建一个管道。管道的名称为"日志-my_app-默认值"。

    
        PUT _ingest/pipeline/logs-my_app-default
    {
      "description": "Pipeline for `my_app` dataset",
      "processors": [ ... ]
    }

2. 创建一个索引模板，将您的管道包含在"index.default_pipeline"或"index.final_pipeline"索引设置中。确保模板已启用数据流。模板的索引模式应与"logs-<dataset-name>-*"匹配。

您可以使用 Kibana 的索引管理功能或创建索引模板 API 创建此模板。

例如，以下请求创建与"logs-my_app-*"匹配的模板。该模板使用包含"index.default_pipeline"索引设置的组件模板。

    
        # Creates a component template for index settings
    PUT _component_template/logs-my_app-settings
    {
      "template": {
        "settings": {
          "index.default_pipeline": "logs-my_app-default",
          "index.lifecycle.name": "logs"
        }
      }
    }
    
    # Creates an index template matching `logs-my_app-*`
    PUT _index_template/logs-my_app-template
    {
      "index_patterns": ["logs-my_app-*"],
      "data_stream": { },
      "priority": 500,
      "composed_of": ["logs-my_app-settings", "logs-my_app-mappings"]
    }

3. 在 Fleet 中添加或编辑**自定义日志**集成时，单击**配置集成>自定义日志文件>高级选项**。  4. 在 **数据集名称** 中，指定数据集的名称。Fleet 会将用于集成的新数据添加到生成的"日志 - <dataset-name>默认"数据流中。

例如，如果数据集的名称为"my_app"，则 Fleet 会将新数据添加到"日志my_app默认"数据流中。

!在队列中设置自定义日志集成

5. 使用滚动更新 API 滚动更新数据流。这可确保 Elasticsearch 将索引模板及其管道设置应用于任何用于集成的新数据。           响应 = client.indices.rollover( 别名： 'logs-my_app-default' ) 放置响应 POST 日志-my_app-默认/_rollover/

选项 2：自定义配置**

1. 创建并测试采集管道。将管道命名为"日志 - <dataset-name>默认"。这样可以更轻松地跟踪集成的管道。

例如，以下请求为"我的应用"数据集创建一个管道。管道的名称为"日志-my_app-默认值"。

    
        PUT _ingest/pipeline/logs-my_app-default
    {
      "description": "Pipeline for `my_app` dataset",
      "processors": [ ... ]
    }

2. 在 Fleet 中添加或编辑**自定义日志**集成时，单击**配置集成>自定义日志文件>高级选项**。  3. 在 **数据集名称** 中，指定数据集的名称。Fleet 会将用于集成的新数据添加到生成的"日志 - <dataset-name>默认"数据流中。

例如，如果数据集的名称为"my_app"，则 Fleet 会将新数据添加到"日志my_app默认"数据流中。

4. 在"**自定义配置**"中，在"管道"策略设置中指定管道。

!自定义日志集成的自定义管道配置

**弹性剂独立**

如果您独立运行 Elastic 代理，则可以使用包含"index.default_pipeline"或"index.final_pipeline"索引设置的索引模板应用管道。或者，您可以在"弹性代理.yml"配置中指定"管道"策略设置。请参阅安装独立的 ElasticAgents。

### 企业搜索中的管道

当您为 EnterpriseSearch 用例创建 Elasticsearch 索引时，例如，使用 Web 爬网程序或连接器，这些索引会自动使用特定的采集管道进行设置。这些处理器有助于优化搜索内容。有关详细信息，请参阅企业级搜索文档。

### 访问处理器中的源字段

处理器对传入文档的源字段具有读写访问权限。要访问处理器中的字段键，请使用其字段名称。以下"设置"处理器访问"我的长字段"。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            set: {
              field: 'my-long-field',
              value: 10
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "set": {
            "field": "my-long-field",
            "value": 10
          }
        }
      ]
    }

您还可以在前面加上"_source"前缀。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            set: {
              field: '_source.my-long-field',
              value: 10
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "set": {
            "field": "_source.my-long-field",
            "value": 10
          }
        }
      ]
    }

使用点表示法访问对象字段。

如果文档包含拼合对象，请先使用"dot_expander"处理器展开它们。其他摄取处理器无法访问平展的对象。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            dot_expander: {
              description: "Expand 'my-object-field.my-property'",
              field: 'my-object-field.my-property'
            }
          },
          {
            set: {
              description: "Set 'my-object-field.my-property' to 10",
              field: 'my-object-field.my-property',
              value: 10
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "dot_expander": {
            "description": "Expand 'my-object-field.my-property'",
            "field": "my-object-field.my-property"
          }
        },
        {
          "set": {
            "description": "Set 'my-object-field.my-property' to 10",
            "field": "my-object-field.my-property",
            "value": 10
          }
        }
      ]
    }

多个处理器参数支持胡须模板代码段。要访问模板代码段中的字段值，请将字段名称括在三重大括号中："{{{字段名称}}}"。您可以使用模板代码段动态设置字段名称。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            set: {
              description: "Set dynamic '<service>' field to 'code' value",
              field: '{{{service}}}',
              value: '{{{code}}}'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "set": {
            "description": "Set dynamic '<service>' field to 'code' value",
            "field": "{{{service}}}",
            "value": "{{{code}}}"
          }
        }
      ]
    }

### 访问处理器中的元数据字段

处理器可以按名称访问以下元数据字段：

* "_index" * "_id" * "_routing" * "_dynamic_templates"

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            set: {
              description: "Set '_routing' to 'geoip.country_iso_code' value",
              field: '_routing',
              value: '{{{geoip.country_iso_code}}}'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "set": {
            "description": "Set '_routing' to 'geoip.country_iso_code' value",
            "field": "_routing",
            "value": "{{{geoip.country_iso_code}}}"
          }
        }
      ]
    }

使用 Mustache 模板代码段访问元数据字段值。例如，'{{{_routing}}}' 检索文档的传送值。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            set: {
              description: 'Use geo_point dynamic template for address field',
              field: '_dynamic_templates',
              value: {
                address: 'geo_point'
              }
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "set": {
            "description": "Use geo_point dynamic template for address field",
            "field": "_dynamic_templates",
            "value": {
              "address": "geo_point"
            }
          }
        }
      ]
    }

上面的集合处理器告诉 ES 使用名为 'geo_point' 的动态模板作为字段 'address' 如果该字段尚未在索引的映射中定义。如果已在批量请求中定义字段"地址"，则此处理器将覆盖动态模板，但对批量请求中定义的其他动态模板没有影响。

如果自动生成文档 ID，则不能在处理器中使用"{{{_id}}}"。Elasticsearch 在摄取后分配自动生成的"_id"值。

### 访问处理器中的摄取元数据

摄取处理器可以使用"_ingest"键添加和访问摄取元数据。

与源字段和元数据字段不同，默认情况下，Elasticsearch 不会索引摄取元数据字段。Elasticsearch 还允许以"_ingest"键开头的源字段。如果您的数据包含此类源字段，请使用"_source._ingest"访问它们。

默认情况下，管道仅创建"_ingest.timestamp"引入元数据字段。此字段包含 Elasticsearch 收到文档索引请求时的时间戳。要索引"_ingest.timestamp"或其他摄取元数据字段，请使用"set"处理器。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            set: {
              description: "Index the ingest timestamp as 'event.ingested'",
              field: 'event.ingested',
              value: '{{{_ingest.timestamp}}}'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "set": {
            "description": "Index the ingest timestamp as 'event.ingested'",
            "field": "event.ingested",
            "value": "{{{_ingest.timestamp}}}"
          }
        }
      ]
    }

### 处理管道故障

管道的处理器按顺序运行。默认情况下，当其中一个处理器发生故障或遇到错误时，管道处理将停止。

若要忽略处理器故障并运行管道的其余处理器，请将"ignore_failure"设置为"true"。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            rename: {
              description: "Rename 'provider' to 'cloud.provider'",
              field: 'provider',
              target_field: 'cloud.provider',
              ignore_failure: true
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "rename": {
            "description": "Rename 'provider' to 'cloud.provider'",
            "field": "provider",
            "target_field": "cloud.provider",
            "ignore_failure": true
          }
        }
      ]
    }

使用"on_failure"参数指定处理器发生故障后立即运行的处理器列表。如果指定了"on_failure"，Elasticsearch 之后会运行管道的剩余处理器，即使"on_failure"配置为空也是如此。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            rename: {
              description: "Rename 'provider' to 'cloud.provider'",
              field: 'provider',
              target_field: 'cloud.provider',
              on_failure: [
                {
                  set: {
                    description: "Set 'error.message'",
                    field: 'error.message',
                    value: "Field 'provider' does not exist. Cannot rename to 'cloud.provider'",
                    override: false
                  }
                }
              ]
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "rename": {
            "description": "Rename 'provider' to 'cloud.provider'",
            "field": "provider",
            "target_field": "cloud.provider",
            "on_failure": [
              {
                "set": {
                  "description": "Set 'error.message'",
                  "field": "error.message",
                  "value": "Field 'provider' does not exist. Cannot rename to 'cloud.provider'",
                  "override": false
                }
              }
            ]
          }
        }
      ]
    }

嵌套"on_failure"处理器列表以进行嵌套错误处理。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            rename: {
              description: "Rename 'provider' to 'cloud.provider'",
              field: 'provider',
              target_field: 'cloud.provider',
              on_failure: [
                {
                  set: {
                    description: "Set 'error.message'",
                    field: 'error.message',
                    value: "Field 'provider' does not exist. Cannot rename to 'cloud.provider'",
                    override: false,
                    on_failure: [
                      {
                        set: {
                          description: "Set 'error.message.multi'",
                          field: 'error.message.multi',
                          value: 'Document encountered multiple ingest errors',
                          override: true
                        }
                      }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "rename": {
            "description": "Rename 'provider' to 'cloud.provider'",
            "field": "provider",
            "target_field": "cloud.provider",
            "on_failure": [
              {
                "set": {
                  "description": "Set 'error.message'",
                  "field": "error.message",
                  "value": "Field 'provider' does not exist. Cannot rename to 'cloud.provider'",
                  "override": false,
                  "on_failure": [
                    {
                      "set": {
                        "description": "Set 'error.message.multi'",
                        "field": "error.message.multi",
                        "value": "Document encountered multiple ingest errors",
                        "override": true
                      }
                    }
                  ]
                }
              }
            ]
          }
        }
      ]
    }

您还可以为管道指定"on_failure"。如果没有"on_failure"值的处理器发生故障，Elasticsearch 将使用此管道级参数作为回退。Elasticsearch 不会尝试运行管道的剩余处理器。

    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [ ... ],
      "on_failure": [
        {
          "set": {
            "description": "Index document to 'failed-<index>'",
            "field": "_index",
            "value": "failed-{{{ _index }}}"
          }
        }
      ]
    }

有关管道故障的其他信息，请参阅文档元数据字段"on_failure_message"、"on_failure_processor_type"、"on_failure_processor_tag"和"on_failure_pipeline"。这些字段只能从"on_failure"块内访问。

以下示例使用元数据字段在文档中包含有关管道故障的信息。

    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [ ... ],
      "on_failure": [
        {
          "set": {
            "description": "Record error information",
            "field": "error_information",
            "value": "Processor {{ _ingest.on_failure_processor_type }} with tag {{ _ingest.on_failure_processor_tag }} in pipeline {{ _ingest.on_failure_pipeline }} failed with message {{ _ingest.on_failure_message }}"
          }
        }
      ]
    }

### 有条件地运行处理器

每个处理器都支持可选的"if"条件，以无痛脚本的形式编写。如果提供，则处理器仅在"if"条件为"true"时运行。

"if"条件脚本在 Painless 的摄取处理器上下文中运行。在"if"条件下，"ctx"值是只读的。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            drop: {
              description: "Drop documents with 'network.name' of 'Guest'",
              if: "ctx?.network?.name == 'Guest'"
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "drop": {
            "description": "Drop documents with 'network.name' of 'Guest'",
            "if": "ctx?.network?.name == 'Guest'"
          }
        }
      ]
    }

如果启用了"script.painless.regex.enabled"集群设置，则可以在"if"条件脚本中使用正则表达式。有关支持的语法，请参阅无痛正则表达式。

如果可能，请避免使用正则表达式。昂贵的正则表达式扫描会降低索引速度。

    
    
    response = client.ingest.put_pipeline(
      id: 'my-pipeline',
      body: {
        processors: [
          {
            set: {
              description: "If 'url.scheme' is 'http', set 'url.insecure' to true",
              if: 'ctx.url?.scheme =~ /^http[^s]/',
              field: 'url.insecure',
              value: true
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "set": {
            "description": "If 'url.scheme' is 'http', set 'url.insecure' to true",
            "if": "ctx.url?.scheme =~ /^http[^s]/",
            "field": "url.insecure",
            "value": true
          }
        }
      ]
    }

您必须在一行上将"if"条件指定为有效的 JSON。但是，您可以使用 Kibana 控制台的三引号语法来编写和调试更大的脚本。

如果可能，请避免使用复杂或昂贵的"if"条件脚本。昂贵的条件脚本可能会降低索引速度。

    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "drop": {
            "description": "Drop documents that don't contain 'prod' tag",
            "if": """
                Collection tags = ctx.tags;
                if(tags != null){
                  for (String tag : tags) {
                    if (tag.toLowerCase().contains('prod')) {
                      return false;
                    }
                  }
                }
                return true;
            """
          }
        }
      ]
    }

您还可以将存储的脚本指定为"if"条件。

    
    
    PUT _scripts/my-prod-tag-script
    {
      "script": {
        "lang": "painless",
        "source": """
          Collection tags = ctx.tags;
          if(tags != null){
            for (String tag : tags) {
              if (tag.toLowerCase().contains('prod')) {
                return false;
              }
            }
          }
          return true;
        """
      }
    }
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "drop": {
            "description": "Drop documents that don't contain 'prod' tag",
            "if": { "id": "my-prod-tag-script" }
          }
        }
      ]
    }

传入文档通常包含对象字段。如果处理器脚本尝试访问父对象不存在的字段，Elasticsearch 将返回"NullPointerException"。若要避免这些异常，请使用 null 安全运算符，例如"？"。'，并将脚本编写为 benull 安全。

例如，'ctx.network？。name.equalsIgnoreCase('Guest')' 不是 null safe.'ctx.network？.名称"可以返回空值。将脚本重写为"Guest".equalsIgnoreCase(ctx.network？)。name)'，这是空安全的，因为"来宾"始终为非空。

如果无法将脚本重写为空安全，请包括显式空检查。

    
    
    PUT _ingest/pipeline/my-pipeline
    {
      "processors": [
        {
          "drop": {
            "description": "Drop documents that contain 'network.name' of 'Guest'",
            "if": "ctx.network?.name != null && ctx.network.name.contains('Guest')"
          }
        }
      ]
    }

### 有条件地应用管道

将"if"条件与"管道"处理器结合使用，以根据您的条件将其他管道应用于文档。您可以将此管道用作索引模板中的默认管道，用于配置多个数据流或索引。

    
    
    response = client.ingest.put_pipeline(
      id: 'one-pipeline-to-rule-them-all',
      body: {
        processors: [
          {
            pipeline: {
              description: "If 'service.name' is 'apache_httpd', use 'httpd_pipeline'",
              if: "ctx.service?.name == 'apache_httpd'",
              name: 'httpd_pipeline'
            }
          },
          {
            pipeline: {
              description: "If 'service.name' is 'syslog', use 'syslog_pipeline'",
              if: "ctx.service?.name == 'syslog'",
              name: 'syslog_pipeline'
            }
          },
          {
            fail: {
              description: "If 'service.name' is not 'apache_httpd' or 'syslog', return a failure message",
              if: "ctx.service?.name != 'apache_httpd' && ctx.service?.name != 'syslog'",
              message: 'This pipeline requires service.name to be either `syslog` or `apache_httpd`'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/one-pipeline-to-rule-them-all
    {
      "processors": [
        {
          "pipeline": {
            "description": "If 'service.name' is 'apache_httpd', use 'httpd_pipeline'",
            "if": "ctx.service?.name == 'apache_httpd'",
            "name": "httpd_pipeline"
          }
        },
        {
          "pipeline": {
            "description": "If 'service.name' is 'syslog', use 'syslog_pipeline'",
            "if": "ctx.service?.name == 'syslog'",
            "name": "syslog_pipeline"
          }
        },
        {
          "fail": {
            "description": "If 'service.name' is not 'apache_httpd' or 'syslog', return a failure message",
            "if": "ctx.service?.name != 'apache_httpd' && ctx.service?.name != 'syslog'",
            "message": "This pipeline requires service.name to be either `syslog` or `apache_httpd`"
          }
        }
      ]
    }

### 获取管道使用情况统计信息

使用节点统计信息 API 获取全局和每个管道的引入统计信息。使用这些统计信息来确定哪些管道运行最频繁或花费最多时间进行处理。

    
    
    response = client.nodes.stats(
      metric: 'ingest',
      filter_path: 'nodes.*.ingest'
    )
    puts response
    
    
    GET _nodes/stats/ingest?filter_path=nodes.*.ingest

[« Run downsampling manually](downsampling-manual.md) [Example: Parse logs
in the Common Log Format »](common-log-format-example.md)
