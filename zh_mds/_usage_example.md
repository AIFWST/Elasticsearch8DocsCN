

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
templates](index-templates.md) ›[Config
ignore_missing_component_templates](ignore_missing_component_templates.md)

[« Config
ignore_missing_component_templates](ignore_missing_component_templates.md)
[Data streams »](data-streams.md)

## 用法示例

在下文中，将创建一个组件模板和一个索引模板。索引模板引用两个组件模板，但仅存在"@package"一个。

创建组件模板"日志foo_component1"。这必须在索引模板之前创建，因为它不是可选的：

    
    
    response = client.cluster.put_component_template(
      name: 'logs-foo_component1',
      body: {
        template: {
          mappings: {
            properties: {
              "host.name": {
                type: 'keyword'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _component_template/logs-foo_component1
    {
      "template": {
        "mappings": {
          "properties": {
            "host.name": {
              "type": "keyword"
            }
          }
        }
      }
    }

接下来，将创建索引模板，并引用两个组件模板：

    
    
      "composed_of": ["logs-foo_component1", "logs-foo_component2"]

以前，只创建了"logs-foo_component1"强制模板，这意味着缺少"logs-foo_component2"。因此，以下条目被添加到配置中：

    
    
      "ignore_missing_component_templates": ["logs-foo_component2"],

在创建模板期间，它不会验证"logs-foo_component2"是否存在：

    
    
    response = client.indices.put_index_template(
      name: 'logs-foo',
      body: {
        index_patterns: [
          'logs-foo-*'
        ],
        data_stream: {},
        composed_of: [
          'logs-foo_component1',
          'logs-foo_component2'
        ],
        ignore_missing_component_templates: [
          'logs-foo_component2'
        ],
        priority: 500
      }
    )
    puts response
    
    
    PUT _index_template/logs-foo
    {
      "index_patterns": ["logs-foo-*"],
      "data_stream": { },
      "composed_of": ["logs-foo_component1", "logs-foo_component2"],
      "ignore_missing_component_templates": ["logs-foo_component2"],
      "priority": 500
    }

已成功创建索引模板"logs-foo"。可以基于此模板创建数据流：

    
    
    response = client.indices.create_data_stream(
      name: 'logs-foo-bar'
    )
    puts response
    
    
    PUT _data_stream/logs-foo-bar

查看数据流的映射，它将包含"host.name"字段。

在稍后阶段，可能会添加缺少的组件模板：

    
    
    response = client.cluster.put_component_template(
      name: 'logs-foo_component2',
      body: {
        template: {
          mappings: {
            properties: {
              "host.ip": {
                type: 'ip'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _component_template/logs-foo_component2
    {
      "template": {
        "mappings": {
          "properties": {
            "host.ip": {
              "type": "ip"
            }
          }
        }
      }
    }

这不会对数据流产生直接影响。映射"host.ip"仅在数据流下次自动滚动更新或触发手动滚动更新时才会显示在数据流映射中：

    
    
    response = client.indices.rollover(
      alias: 'logs-foo-bar'
    )
    puts response
    
    
    POST logs-foo-bar/_rollover

[« Config
ignore_missing_component_templates](ignore_missing_component_templates.md)
[Data streams »](data-streams.md)
