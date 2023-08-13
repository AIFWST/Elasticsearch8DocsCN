

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
streams](data-streams.md)

[« Data streams](data-streams.md) [Use a data stream »](use-a-data-
stream.md)

## 设置数据流

要设置数据流，请执行以下步骤：

1. 创建索引生命周期策略 2.创建组件模板 3.创建索引模板 4.创建数据流 5.保护数据流

您还可以将索引别名转换为数据流。

如果您使用队列或弹性代理，请跳过本教程。队列和弹性代理为您设置数据流。请参阅队列的数据流文档。

### 创建索引生命周期策略

虽然是可选的，但我们建议使用 ILM 自动管理数据流的支持索引。ILM 需要一个索引生命周期策略。

要在 Kibana 中创建索引生命周期策略，请打开主菜单并转至堆栈管理>索引生命周期策略**。单击**创建策略**。

您还可以使用创建生命周期策略 API。

    
    
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

数据流需要匹配的索引模板。在大多数情况下，您可以使用一个或多个组件模板来组合此索引模板。通常使用单独的组件模板进行映射和索引设置。这允许您在多个索引模板中重用组件模板。

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

### 创建数据流

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

您还可以使用创建数据流 API 手动创建流。流的名称仍必须与模板的索引模式之一匹配。

    
    
    response = client.indices.create_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
    
    PUT _data_stream/my-data-stream

### 保护数据流

使用索引权限控制对数据流的访问。授予权限 数据流对其后备索引授予相同的权限。

有关示例，请参阅数据流权限。

### 将索引别名转换为数据流

在 Elasticsearch 7.9 之前，您通常使用带有 writeindex 的索引别名来管理时间序列数据。数据流取代了此功能，需要较少的维护，并自动与数据层集成。

要将具有写入索引的索引别名转换为具有相同名称的数据流，请使用迁移到数据流 API。在转换期间，别名的索引将成为流的隐藏支持索引。别名的写入索引成为流的写入索引。流仍需要启用了数据流的匹配索引模板。

    
    
    POST _data_stream/_migrate/my-time-series-data

### 获取有关数据流的信息

要获取有关 Kibana 中数据流的信息，请打开主菜单并转到**堆栈管理>索引管理**。在"**数据流**"视图中，单击数据流的名称。

您还可以使用获取数据流 API。

    
    
    response = client.indices.get_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
    
    GET _data_stream/my-data-stream

### 删除数据流

要在 Kibana 中删除数据流及其后备索引，请打开主菜单并转到堆栈管理>索引管理**。在"**数据流**"视图中，单击垃圾桶图标。仅当您具有数据流的"delete_index"安全权限时，才会显示该图标。

您还可以使用删除数据流 API。

    
    
    response = client.indices.delete_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
    
    DELETE _data_stream/my-data-stream

[« Data streams](data-streams.md) [Use a data stream »](use-a-data-
stream.md)
