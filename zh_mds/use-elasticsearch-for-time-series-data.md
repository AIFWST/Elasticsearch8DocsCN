

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[How
to](how-to.md)

[« Size your shards](size-your-shards.md) [Troubleshooting
»](troubleshooting.md)

## 对时间序列数据使用 Elasticsearch

Elasticsearch 提供的功能可帮助您存储、管理和搜索时间序列数据，例如日志和指标。进入 Elasticsearch 后，您可以使用 Kibana 和其他 Elastic Stack 功能分析和可视化数据。

### 设置数据层

Elasticsearch 的 ILM 功能使用数据层自动将旧数据移动到硬件成本较低的节点。这有助于提高性能并降低存储成本。

热层和内容层是必需的。暖层、冷层和冷冻层是可选的。

在热层和暖层中使用高性能节点，以加快索引速度并更快地搜索最新数据。在冷层和冻结层中使用速度较慢、成本较低的节点来降低成本。

内容层通常不用于时序数据。但是，需要创建不属于数据流的系统索引和其他索引。

设置数据层的步骤因部署类型而异：

弹性搜索服务 自我管理

1. 登录弹性搜索服务控制台。  2. 从 Elasticsearch Service 主页或部署页面添加或选择您的部署。  3. 从部署菜单中，选择**编辑部署**。  4. 要启用数据层，请单击**添加容量**。

**启用自动缩放**

自动缩放会自动调整部署的容量以满足存储需求。若要启用自动缩放，请在"编辑部署"页上选择"**自动缩放此部署**"。自动缩放仅适用于 Elasticsearch Service。

要将节点分配给数据层，请将相应的节点角色添加到节点的"elasticsearch.yml"文件中。更改现有节点的角色需要滚动重启。

    
    
    # Content tier
    node.roles: [ data_content ]
    
    # Hot tier
    node.roles: [ data_hot ]
    
    # Warm tier
    node.roles: [ data_warm ]
    
    # Cold tier
    node.roles: [ data_cold ]
    
    # Frozen tier
    node.roles: [ data_frozen ]

建议在冻结层中使用专用节点。如果需要，可以将其他节点分配到多个层。

    
    
    node.roles: [ data_content, data_hot, data_warm ]

为节点分配群集所需的任何其他角色。例如，小型群集可能具有具有多个角色的节点。

    
    
    node.roles: [ master, ingest, ml, data_hot, transform ]

### 注册快照存储库

冷层和冻结层可以使用可搜索的快照来降低本地存储成本。

要使用可搜索的快照，您必须注册受支持的快照存储库。注册此存储库的步骤因部署类型和存储提供程序而异：

弹性搜索服务 自我管理

当您创建集群时，Elasticsearch Service 会自动注册默认的"找到快照"存储库。此存储库支持可搜索的快照。

"找到的快照"存储库特定于您的集群。要使用其他集群的默认存储库，请参阅云快照和还原文档。

您还可以将以下任何自定义存储库类型与可搜索快照一起使用：

* Google Cloud Storage (GCS) * Azure Blob Storage * Amazon Web Services (AWS)

将以下任何存储库类型与可搜索快照结合使用：

* AWS S3 * Google Cloud Storage * Azure Blob Storage * Hadoop Distributed File Store (HDFS) * 共享文件系统，如 NFS * 只读 HTTP 和 HTTPS 存储库

您还可以使用这些存储库类型的替代实现，例如 MinIO，只要它们完全兼容即可。使用存储库分析 API 分析存储库是否适合用于可搜索快照。

### 创建或编辑索引生命周期策略

数据流跨多个后备索引存储数据。ILM 使用索引生命周期策略在数据层中自动移动这些索引。

如果您使用 Fleet 或 Elastic Agent，请编辑 Elasticsearch 的内置生命周期策略之一。如果使用自定义应用程序，请创建自己的策略。无论哪种情况，请确保您的策略：

* 包括已配置的每个数据层的阶段。  * 计算从展期相变的阈值或"min_age"。  * 如果需要，在冷相和冻结阶段使用可搜索的快照。  * 包括删除阶段(如果需要)。

队列或弹性代理自定义应用程序

队列和弹性代理使用以下内置生命周期策略：

* "日志" * "指标" * "合成"

可以根据性能、复原能力和保留要求自定义这些策略。

要在 Kibana 中编辑策略，请打开主菜单并转到堆栈管理>索引生命周期策略**。点击您要修改的政策。

您还可以使用更新生命周期策略 API。

    
    
    PUT _ilm/policy/logs
    {
      "policy": {
        "phases": {
          "hot": {
            "actions": {
              "rollover": {
                "max_primary_shard_size": "50gb"
              }
            }
          },
          "warm": {
            "min_age": "30d",
            "actions": {
              "shrink": {
                "number_of_shards": 1
              },
              "forcemerge": {
                "max_num_segments": 1
              }
            }
          },
          "cold": {
            "min_age": "60d",
            "actions": {
              "searchable_snapshot": {
                "snapshot_repository": "found-snapshots"
              }
            }
          },
          "frozen": {
            "min_age": "90d",
            "actions": {
              "searchable_snapshot": {
                "snapshot_repository": "found-snapshots"
              }
            }
          },
          "delete": {
            "min_age": "735d",
            "actions": {
              "delete": {}
            }
          }
        }
      }
    }

要在 Kibana 中创建策略，请打开主菜单并转到**堆栈管理>索引生命周期策略**。单击**创建策略**。

您还可以使用更新生命周期策略 API。

    
    
    PUT _ilm/policy/my-lifecycle-policy
    {
      "policy": {
        "phases": {
          "hot": {
            "actions": {
              "rollover": {
                "max_primary_shard_size": "50gb"
              }
            }
          },
          "warm": {
            "min_age": "30d",
            "actions": {
              "shrink": {
                "number_of_shards": 1
              },
              "forcemerge": {
                "max_num_segments": 1
              }
            }
          },
          "cold": {
            "min_age": "60d",
            "actions": {
              "searchable_snapshot": {
                "snapshot_repository": "found-snapshots"
              }
            }
          },
          "frozen": {
            "min_age": "90d",
            "actions": {
              "searchable_snapshot": {
                "snapshot_repository": "found-snapshots"
              }
            }
          },
          "delete": {
            "min_age": "735d",
            "actions": {
              "delete": {}
            }
          }
        }
      }
    }

### 创建组件模板

如果您使用队列或弹性代理，请跳到搜索并可视化您的数据。队列和弹性代理使用内置模板为您创建数据流。

如果使用自定义应用程序，则需要设置自己的数据流。数据流需要匹配的索引模板。在大多数情况下，您可以使用一个或多个组件模板来组合此索引模板。通常使用单独的组件模板进行映射和索引设置。这允许您在多个索引模板中重用组件模板。

创建组件模板时，包括：

* "@timestamp"字段的"日期"或"date_nanos"映射。如果您没有指定映射，Elasticsearch 会将"@timestamp"映射为带有默认选项的"日期"字段。  * "index.lifecycle.name"索引设置中的生命周期策略。

映射字段时使用弹性通用架构 (ECS)。默认情况下，ECS 字段与多个弹性堆栈功能集成。

如果您不确定如何映射字段，请使用运行时字段在搜索时从非结构化内容中提取字段。例如，您可以将日志消息索引到"通配符"字段，然后在搜索期间从此字段中提取 IP 地址和其他数据。

要在 Kibana 中创建组件模板，请打开主菜单并转到 **堆栈管理>索引管理**。在"**索引模板**"视图中，单击**创建组件模板**。

您还可以使用创建组件模板 API。

    
    
    response = client.cluster.put_component_template(
      name: 'my-mappings',
      body: {
        template: {
          mappings: {
            properties: {
              "@timestamp": {
                type: 'date',
                format: 'date_optional_time||epoch_millis'
              },
              message: {
                type: 'wildcard'
              }
            }
          }
        },
        _meta: {
          description: 'Mappings for @timestamp and message fields',
          "my-custom-meta-field": 'More arbitrary metadata'
        }
      }
    )
    puts response
    
    response = client.cluster.put_component_template(
      name: 'my-settings',
      body: {
        template: {
          settings: {
            "index.lifecycle.name": 'my-lifecycle-policy'
          }
        },
        _meta: {
          description: 'Settings for ILM',
          "my-custom-meta-field": 'More arbitrary metadata'
        }
      }
    )
    puts response
    
    
    # Creates a component template for mappings
    PUT _component_template/my-mappings
    {
      "template": {
        "mappings": {
          "properties": {
            "@timestamp": {
              "type": "date",
              "format": "date_optional_time||epoch_millis"
            },
            "message": {
              "type": "wildcard"
            }
          }
        }
      },
      "_meta": {
        "description": "Mappings for @timestamp and message fields",
        "my-custom-meta-field": "More arbitrary metadata"
      }
    }
    
    # Creates a component template for index settings
    PUT _component_template/my-settings
    {
      "template": {
        "settings": {
          "index.lifecycle.name": "my-lifecycle-policy"
        }
      },
      "_meta": {
        "description": "Settings for ILM",
        "my-custom-meta-field": "More arbitrary metadata"
      }
    }

### 创建索引模板

使用组件模板创建索引模板。指定：

* 与数据流名称匹配的一个或多个索引模式。我们建议使用我们的数据流命名方案。  * 模板已启用数据流。  * 包含映射和索引设置的任何组件模板。  * 优先级高于"200"，以避免与内置模板发生冲突。请参阅避免索引模式冲突。

要在 Kibana 中创建索引模板，请打开主菜单并转到 **堆栈管理>索引管理**。在"**索引模板**"视图中，单击"**创建模板**"。

您还可以使用创建索引模板 API。包括"data_stream"对象以启用数据流。

    
    
    response = client.indices.put_index_template(
      name: 'my-index-template',
      body: {
        index_patterns: [
          'my-data-stream*'
        ],
        data_stream: {},
        composed_of: [
          'my-mappings',
          'my-settings'
        ],
        priority: 500,
        _meta: {
          description: 'Template for my time series data',
          "my-custom-meta-field": 'More arbitrary metadata'
        }
      }
    )
    puts response
    
    
    PUT _index_template/my-index-template
    {
      "index_patterns": ["my-data-stream*"],
      "data_stream": { },
      "composed_of": [ "my-mappings", "my-settings" ],
      "priority": 500,
      "_meta": {
        "description": "Template for my time series data",
        "my-custom-meta-field": "More arbitrary metadata"
      }
    }

### 向数据流添加数据

索引请求将文档添加到数据流。这些请求必须使用"创建"的"op_type"。文档必须包含"@timestamp"字段。

要自动创建数据流，请提交以数据流名称为目标的索引请求。此名称必须与索引模板的索引模式之一匹配。

    
    
    PUT my-data-stream/_bulk
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:21:15.000Z", "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736" }
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:25:42.000Z", "message": "192.0.2.255 - - [06/May/2099:16:25:42 +0000] \"GET /favicon.ico HTTP/1.0\" 200 3638" }
    
    POST my-data-stream/_doc
    {
      "@timestamp": "2099-05-06T16:21:15.000Z",
      "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736"
    }

### 搜索和可视化您的数据

要在 Kibana 中浏览和搜索数据，请打开主菜单并选择**发现**。请参阅 Kibana 的发现文档。

使用 Kibana 的仪表板功能在图表、表格、地图等中可视化您的数据。请参阅 Kibana 的仪表板文档。

您还可以使用搜索 API 搜索和聚合数据。使用运行时字段和 grok 模式在搜索时从日志消息和其他非结构化内容中动态提取数据。

    
    
    GET my-data-stream/_search
    {
      "runtime_mappings": {
        "source.ip": {
          "type": "ip",
          "script": """
            String sourceip=grok('%{IPORHOST:sourceip} .*').extract(doc[ "message" ].value)?.sourceip;
            if (sourceip != null) emit(sourceip);
          """
        }
      },
      "query": {
        "bool": {
          "filter": [
            {
              "range": {
                "@timestamp": {
                  "gte": "now-1d/d",
                  "lt": "now/d"
                }
              }
            },
            {
              "range": {
                "source.ip": {
                  "gte": "192.0.2.0",
                  "lte": "192.0.2.255"
                }
              }
            }
          ]
        }
      },
      "fields": [
        "*"
      ],
      "_source": false,
      "sort": [
        {
          "@timestamp": "desc"
        },
        {
          "source.ip": "desc"
        }
      ]
    }

默认情况下，Elasticsearch 搜索是同步的。跨冻结数据、长时间范围或大型数据集进行搜索可能需要更长的时间。使用异步搜索 API 在后台运行搜索。有关更多搜索选项，请参阅搜索您的数据。

    
    
    POST my-data-stream/_async_search
    {
      "runtime_mappings": {
        "source.ip": {
          "type": "ip",
          "script": """
            String sourceip=grok('%{IPORHOST:sourceip} .*').extract(doc[ "message" ].value)?.sourceip;
            if (sourceip != null) emit(sourceip);
          """
        }
      },
      "query": {
        "bool": {
          "filter": [
            {
              "range": {
                "@timestamp": {
                  "gte": "now-2y/d",
                  "lt": "now/d"
                }
              }
            },
            {
              "range": {
                "source.ip": {
                  "gte": "192.0.2.0",
                  "lte": "192.0.2.255"
                }
              }
            }
          ]
        }
      },
      "fields": [
        "*"
      ],
      "_source": false,
      "sort": [
        {
          "@timestamp": "desc"
        },
        {
          "source.ip": "desc"
        }
      ]
    }

[« Size your shards](size-your-shards.md) [Troubleshooting
»](troubleshooting.md)
