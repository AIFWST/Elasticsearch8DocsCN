

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Normalizers](analysis-normalizers.md) [Simulate multi-component templates
»](simulate-multi-component-templates.md)

# 索引模板

本文介绍 Elasticsearch 7.8 中引入的可组合索引模板。有关索引模板以前工作原理的信息，请参阅旧版模板文档。

索引模板是一种告诉 Elasticsearch 在创建索引时如何配置索引的方法。对于数据流，索引模板在创建流的后备索引时对其进行配置。模板在创建索引之前配置**。创建索引时(手动或通过为文档编制索引)，模板设置将用作创建索引的基础。

有两种类型的模板：索引模板和组件模板。组件模板是配置映射、设置和别名的可重用构建基块。虽然可以使用组件模板来构造索引模板，但它们不会直接应用于一组索引。索引模板可以包含组件模板的集合，也可以直接指定设置、映射和别名。

以下条件适用于索引模板：

* 可组合模板优先于旧模板。如果没有可组合模板与给定索引匹配，则旧模板可能仍匹配并应用。  * 如果使用显式设置创建索引并且还与索引模板匹配，则创建索引请求中的设置优先于索引模板及其组件模板中指定的设置。  * 索引模板本身中指定的设置优先于其组件模板中的设置。  * 如果新的数据流或索引与多个索引模板匹配，则使用优先级最高的索引模板。

**避免索引模式冲突**

Elasticsearch 具有内置的索引模板，每个模板的优先级为 '100'，适用于以下索引模式：

* "日志-*-*" * "指标-*-*" * "合成-*-*" * "分析-*"

弹性代理使用这些模板来创建数据流。队列集成创建的索引模板使用类似的重叠索引模式，优先级最高为"200"。

如果您使用 Fleet 或弹性代理，请为索引模板分配低于"100"的优先级，以避免覆盖这些模板。否则，为避免意外应用模板，请执行下列一项或多项操作：

* 要禁用所有内置索引和组件模板，请使用群集更新设置 API 将"stack.templates.enabled"设置为"false"。  * 使用不重叠的索引模式。  * 为具有重叠模式的模板分配高于"200"的"优先级"。例如，如果您不使用 Fleet 或 Elastic 代理，并且想要为"logs-*"索引模式创建模板，请为模板分配优先级"500"。这可确保应用模板而不是"logs-*-*"的内置模板。

## 创建索引模板

使用索引模板和放置组件模板 API 来创建和更新索引模板。您还可以从 Kibana 中的堆栈管理中管理索引模板。

以下请求创建两个组件模板。

    
    
    response = client.cluster.put_component_template(
      name: 'component_template1',
      body: {
        template: {
          mappings: {
            properties: {
              "@timestamp": {
                type: 'date'
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.cluster.put_component_template(
      name: 'runtime_component_template',
      body: {
        template: {
          mappings: {
            runtime: {
              day_of_week: {
                type: 'keyword',
                script: {
                  source: "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _component_template/component_template1
    {
      "template": {
        "mappings": {
          "properties": {
            "@timestamp": {
              "type": "date"
            }
          }
        }
      }
    }
    
    PUT _component_template/runtime_component_template
    {
      "template": {
        "mappings": {
          "runtime": { __"day_of_week": {
              "type": "keyword",
              "script": {
                "source": "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
              }
            }
          }
        }
      }
    }

__

|

当新索引与模板匹配时，此组件模板会将名为"day_of_week"的运行时字段添加到映射中。   ---|--- 以下请求创建_composed of_这些组件模板的索引模板。

    
    
    response = client.indices.put_index_template(
      name: 'template_1',
      body: {
        index_patterns: [
          'te*',
          'bar*'
        ],
        template: {
          settings: {
            number_of_shards: 1
          },
          mappings: {
            _source: {
              enabled: true
            },
            properties: {
              host_name: {
                type: 'keyword'
              },
              created_at: {
                type: 'date',
                format: 'EEE MMM dd HH:mm:ss Z yyyy'
              }
            }
          },
          aliases: {
            mydata: {}
          }
        },
        priority: 500,
        composed_of: [
          'component_template1',
          'runtime_component_template'
        ],
        version: 3,
        _meta: {
          description: 'my custom'
        }
      }
    )
    puts response
    
    
    PUT _index_template/template_1
    {
      "index_patterns": ["te*", "bar*"],
      "template": {
        "settings": {
          "number_of_shards": 1
        },
        "mappings": {
          "_source": {
            "enabled": true
          },
          "properties": {
            "host_name": {
              "type": "keyword"
            },
            "created_at": {
              "type": "date",
              "format": "EEE MMM dd HH:mm:ss Z yyyy"
            }
          }
        },
        "aliases": {
          "mydata": { }
        }
      },
      "priority": 500,
      "composed_of": ["component_template1", "runtime_component_template"], __"version": 3,
      "_meta": {
        "description": "my custom"
      }
    }

[« Normalizers](analysis-normalizers.md) [Simulate multi-component templates
»](simulate-multi-component-templates.md)
