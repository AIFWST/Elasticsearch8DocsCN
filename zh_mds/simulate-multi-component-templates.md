

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
templates](index-templates.md)

[« Index templates](index-templates.md) [Config
ignore_missing_component_templates »](ignore_missing_component_templates.md)

## 模拟多组件模板

由于模板不仅可以由多个组件模板组成，还可以由索引模板本身组成，因此有两个模拟 API 来确定生成的索引设置。

要模拟将应用于特定索引名称的设置，请执行以下操作：

    
    
    POST /_index_template/_simulate_index/my-index-000001

要模拟将从现有模板应用的设置，请执行以下操作：

    
    
    POST /_index_template/_simulate/template_1

您还可以在模拟请求中指定模板定义。这使您能够在添加新模板之前验证设置是否将按预期应用。

    
    
    response = client.cluster.put_component_template(
      name: 'ct1',
      body: {
        template: {
          settings: {
            "index.number_of_shards": 2
          }
        }
      }
    )
    puts response
    
    response = client.cluster.put_component_template(
      name: 'ct2',
      body: {
        template: {
          settings: {
            "index.number_of_replicas": 0
          },
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
    
    response = client.indices.simulate_template(
      body: {
        index_patterns: [
          'my*'
        ],
        template: {
          settings: {
            "index.number_of_shards": 3
          }
        },
        composed_of: [
          'ct1',
          'ct2'
        ]
      }
    )
    puts response
    
    
    PUT /_component_template/ct1
    {
      "template": {
        "settings": {
          "index.number_of_shards": 2
        }
      }
    }
    
    PUT /_component_template/ct2
    {
      "template": {
        "settings": {
          "index.number_of_replicas": 0
        },
        "mappings": {
          "properties": {
            "@timestamp": {
              "type": "date"
            }
          }
        }
      }
    }
    
    POST /_index_template/_simulate
    {
      "index_patterns": ["my*"],
      "template": {
        "settings" : {
            "index.number_of_shards" : 3
        }
      },
      "composed_of": ["ct1", "ct2"]
    }

响应显示将应用于匹配索引的设置、映射和别名，以及其配置将被模拟模板正文或更高优先级模板取代的任何重叠模板。

    
    
    {
      "template" : {
        "settings" : {
          "index" : {
            "number_of_shards" : "3",   __"number_of_replicas" : "0",
            "routing" : {
              "allocation" : {
                "include" : {
                  "_tier_preference" : "data_content"
                }
              }
            }
          }
        },
        "mappings" : {
          "properties" : {
            "@timestamp" : {
              "type" : "date" __}
          }
        },
        "aliases" : { }
      },
      "overlapping" : [
        {
          "name" : "template_1", __"index_patterns" : [
            "my*"
          ]
        }
      ]
    }

__

|

模拟模板正文的分片数 ---|--- __

|

从"ct2"组件模板 __ 继承的"@timestamp"字段

|

任何匹配但优先级较低的重叠模板 « 索引模板 Configignore_missing_component_templates »