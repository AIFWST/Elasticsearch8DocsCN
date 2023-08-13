

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
streams](data-streams.md) ›[Time series data stream (TSDS)](tsds.md)

[« Time series data stream (TSDS)](tsds.md) [Time series index settings
»](tsds-index-settings.md)

## 设置时序数据流 (TSDS)

若要设置时序数据流 (TSDS)")，请执行以下步骤：

1. 检查先决条件。  2. 创建索引生命周期策略。  3. 创建映射组件模板。  4. 创建索引设置组件模板。  5. 创建索引模板。  6. 创建 TSDS。  7. 保护 TSDS。

####Prerequisites

* 在创建 TSDS 之前，您应该熟悉数据流和 TSDS 概念")。  * 要学习本教程，您必须具有以下权限：

    * [Cluster privileges](security-privileges.html#privileges-list-cluster "Cluster privileges"): `manage_ilm` and `manage_index_templates`. 
    * [Index privileges](security-privileges.html#privileges-list-indices "Indices privileges"): `create_doc` and `create_index` for any TSDS you create or convert. To roll over a TSDS, you must have the `manage` privilege. 

#### 创建索引生命周期策略

虽然是可选的，但我们建议使用 ILM 来自动管理您的 TSDS 的后备索引。ILM 需要一个索引生命周期策略。

我们建议您为策略中的"滚动更新"操作指定"max_age"条件。这可确保 TSDS 后备索引的"@timestamp"范围一致。例如，为"翻转"操作设置"max_age""1d"可确保您的备份索引始终包含一天的数据。

    
    
    PUT _ilm/policy/my-weather-sensor-lifecycle-policy
    {
      "policy": {
        "phases": {
          "hot": {
            "actions": {
              "rollover": {
                "max_age": "1d",
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

#### 创建映射组件模板

TSDS 需要匹配的索引模板。在大多数情况下，您可以使用一个或多个组件模板来撰写此索引模板。通常使用单独的组件模板进行映射和索引设置。这允许您在多个索引模板中重用组件模板。

对于 TSDS，映射组件模板必须包括以下各项的映射：

* 一个或多个维度字段，time_series_dimension"值为"true"。这些维度中至少有一个必须是普通的"关键字"字段。

(可选)模板还可以包含以下各项的映射：

* 一个或多个指标字段，使用"time_series_metric"映射参数标记。  * "@timestamp"字段的"日期"或"date_nanos"映射。如果您没有指定映射，Elasticsearch 会将"@timestamp"映射为带有默认选项的"日期"字段。

    
    
    response = client.cluster.put_component_template(
      name: 'my-weather-sensor-mappings',
      body: {
        template: {
          mappings: {
            properties: {
              sensor_id: {
                type: 'keyword',
                time_series_dimension: true
              },
              location: {
                type: 'keyword',
                time_series_dimension: true
              },
              temperature: {
                type: 'half_float',
                time_series_metric: 'gauge'
              },
              humidity: {
                type: 'half_float',
                time_series_metric: 'gauge'
              },
              "@timestamp": {
                type: 'date',
                format: 'strict_date_optional_time'
              }
            }
          }
        },
        _meta: {
          description: 'Mappings for weather sensor data'
        }
      }
    )
    puts response
    
    
    PUT _component_template/my-weather-sensor-mappings
    {
      "template": {
        "mappings": {
          "properties": {
            "sensor_id": {
              "type": "keyword",
              "time_series_dimension": true
            },
            "location": {
              "type": "keyword",
              "time_series_dimension": true
            },
            "temperature": {
              "type": "half_float",
              "time_series_metric": "gauge"
            },
            "humidity": {
              "type": "half_float",
              "time_series_metric": "gauge"
            },
            "@timestamp": {
              "type": "date",
              "format": "strict_date_optional_time"
            }
          }
        }
      },
      "_meta": {
        "description": "Mappings for weather sensor data"
      }
    }

#### 创建索引设置组件模板

(可选)TSDS 的索引设置组件模板可以包括：

* "index.lifecycle.name"索引设置中的生命周期策略。  * "index.look_ahead_time"索引设置。  * 其他索引设置，例如 TSDS 的后备索引的"index.codec"。

不要在组件模板中指定"index.routing_path"索引设置。如果选择，可以直接在索引模板中配置"index.routing_path"，如以下步骤所示。

    
    
    response = client.cluster.put_component_template(
      name: 'my-weather-sensor-settings',
      body: {
        template: {
          settings: {
            "index.lifecycle.name": 'my-lifecycle-policy',
            "index.look_ahead_time": '3h',
            "index.codec": 'best_compression'
          }
        },
        _meta: {
          description: 'Index settings for weather sensor data'
        }
      }
    )
    puts response
    
    
    PUT _component_template/my-weather-sensor-settings
    {
      "template": {
        "settings": {
          "index.lifecycle.name": "my-lifecycle-policy",
          "index.look_ahead_time": "3h",
          "index.codec": "best_compression"
        }
      },
      "_meta": {
        "description": "Index settings for weather sensor data"
      }
    }

#### 创建索引模板

使用组件模板创建索引模板。在索引模板中，指定：

* 与 TSDS 名称匹配的一个或多个索引模式。我们建议使用我们的数据流命名方案。  * 模板已启用数据流。  * 设置为"time_series"的"index.mode"对象。  * 可选："index.routing_path"索引设置。设置值应仅与普通"关键字"维度字段匹配，并应直接在索引模板中设置。如果未显式定义，则使用将"time_series_dimension"设置为"true"的所有映射从映射生成"index.routing_path"设置。  * 包含您的映射和其他索引设置的组件模板。  * 优先级高于"200"，以避免与内置模板发生冲突。请参阅避免索引模式冲突。

    
    
    response = client.indices.put_index_template(
      name: 'my-weather-sensor-index-template',
      body: {
        index_patterns: [
          'metrics-weather_sensors-*'
        ],
        data_stream: {},
        template: {
          settings: {
            "index.mode": 'time_series',
            "index.routing_path": [
              'sensor_id',
              'location'
            ]
          }
        },
        composed_of: [
          'my-weather-sensor-mappings',
          'my-weather-sensor-settings'
        ],
        priority: 500,
        _meta: {
          description: 'Template for my weather sensor data'
        }
      }
    )
    puts response
    
    
    PUT _index_template/my-weather-sensor-index-template
    {
      "index_patterns": ["metrics-weather_sensors-*"],
      "data_stream": { },
      "template": {
        "settings": {
          "index.mode": "time_series",
          "index.routing_path": [ "sensor_id", "location" ]
        }
      },
      "composed_of": [ "my-weather-sensor-mappings", "my-weather-sensor-settings" ],
      "priority": 500,
      "_meta": {
        "description": "Template for my weather sensor data"
      }
    }

#### 创建 TSDS

索引请求将文档添加到 TSDS。TSDS中的文件必须包括：

* "@timestamp"字段 * 一个或多个维度字段。至少一个维度必须是与"index.routing_path"索引设置匹配的"关键字"字段(如果已指定)。如果未明确指定，则"index.routing_path"将自动设置为将"time_series_dimension"设置为"true"的任何映射。

要自动创建 TSDS，请提交以 TSDS 名称为目标的索引请求。此名称必须与索引模板的索引模式之一匹配。

若要测试以下示例，请将时间戳更新为当前时间的三小时内。添加到 TSDS 的数据必须始终在可接受的时间范围内。

    
    
    PUT metrics-weather_sensors-dev/_bulk
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:21:15.000Z", "sensor_id": "HAL-000001", "location": "plains", "temperature": 26.7,"humidity": 49.9 }
    { "create":{ } }
    { "@timestamp": "2099-05-06T16:25:42.000Z", "sensor_id": "SYKENET-000001", "location": "swamp", "temperature": 32.4, "humidity": 88.9 }
    
    POST metrics-weather_sensors-dev/_doc
    {
      "@timestamp": "2099-05-06T16:21:15.000Z",
      "sensor_id": "SYKENET-000001",
      "location": "swamp",
      "temperature": 32.4,
      "humidity": 88.9
    }

您也可以使用创建数据流API手动创建TSDS。TSDS 的名称必须仍与模板的索引模式之一匹配。

    
    
    response = client.indices.create_data_stream(
      name: 'metrics-weather_sensors-dev'
    )
    puts response
    
    
    PUT _data_stream/metrics-weather_sensors-dev

#### 保护TSDS

使用索引特权控制对 TSDS 的访问。授予对 aTSDS 的权限将授予对其后备索引的相同权限。

有关示例，请参阅数据流权限。

#### 将现有数据流转换为 aTSDS

您还可以使用上述步骤将现有的常规数据流转换为 TSDS。在这种情况下，您需要：

* 编辑现有的索引生命周期策略、组件模板和索引模板，而不是创建新的模板。  * 无需创建 TSDS，而是手动滚动其写入索引。这可确保当前写入索引和任何新的支持索引具有"索引模式"time_series"。

您可以使用滚动更新 API 手动滚动更新写入索引。

    
        response = client.indices.rollover(
      alias: 'metrics-weather_sensors-dev'
    )
    puts response
    
        POST metrics-weather_sensors-dev/_rollover

#### 下一步是什么？

现在您已经设置了 TSDS，您可以像管理和使用常规数据流一样使用它。有关详细信息，请参阅：

* _Use数据stream_ * 更改数据流的映射和设置 * 数据流 API

[« Time series data stream (TSDS)](tsds.md) [Time series index settings
»](tsds-index-settings.md)
