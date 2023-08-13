

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Shrink index API](indices-shrink-index.md) [Simulate index template API
»](indices-simulate-template.md)

## 模拟索引接口

从现有索引模板返回将应用于指定索引的索引配置。

    
    
    POST /_index_template/_simulate_index/my-index-000001

###Request

"发布/_index_template/_simulate_index/<index>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

### 路径参数

`<index>`

     (Required, string) Name of the index to simulate. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`include_defaults`

     (Optional, Boolean) Functionality in  [preview]  This functionality is in technical preview and may be changed or removed in a future release. Elastic will apply best effort to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.  . If `true`, return all default settings in the response. Defaults to `false`. 

### 响应正文

`overlapping`

    

(阵列)也与索引匹配但被更高优先级模板取代的任何模板。如果不存在重叠的模板，则响应包括一个空数组。

"重叠"的属性

`name`

     (string) Name of the superseded template. 
`index_patterns`

     (array) Index patterns that the superseded template applies to. 

`template`

    

(对象)将应用于索引的设置、映射和别名。

"模板"的属性

`aliases`

    

(对象)索引的别名。如果没有应用别名，响应将返回一个空的"别名"对象。

`<alias>`

    

(对象)键是别名。对象主体包含别名的选项。

""的属性<alias>

`filter`

     ([Query DSL object](query-dsl.html "Query DSL")) Query used to limit documents the alias can access. 
`index_routing`

     (string) Value used to route indexing operations to a specific shard. This overwrites the `routing` value for indexing operations. 
`is_hidden`

     (Boolean) If `true`, the alias is [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices"). 
`is_write_index`

     (Boolean) If `true`, the index is the [write index](aliases.html#write-index "Write index") for the alias. 
`routing`

     (string) Value used to route indexing and search operations to a specific shard. 
`search_routing`

     (string) Value used to route search operations to a specific shard. This overwrites the `routing` value for search operations. 

`mappings`

    

(可选，映射对象)索引中字段的映射。如果指定，此映射可以包括：

* 字段名称 * 字段数据类型 * 映射参数

请参阅映射。

如果未应用映射，则从响应中省略。

`settings`

    

(可选，索引设置对象)索引的配置选项。请参阅索引设置。

如果未应用任何设置，则响应包括空对象。

###Examples

以下示例显示了现有模板将应用于"my-index-000001"的配置。

    
    
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
    
    response = client.indices.put_index_template(
      name: 'final-template',
      body: {
        index_patterns: [
          'my-index-*'
        ],
        composed_of: [
          'ct1',
          'ct2'
        ],
        priority: 5
      }
    )
    puts response
    
    
    PUT /_component_template/ct1                    __{
      "template": {
        "settings": {
          "index.number_of_shards": 2
        }
      }
    }
    
    PUT /_component_template/ct2 __{
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
    
    PUT /_index_template/final-template __{
      "index_patterns": ["my-index-*"],
      "composed_of": ["ct1", "ct2"],
      "priority": 5
    }
    
    POST /_index_template/_simulate_index/my-index-000001 __

__

|

创建一个组件模板 ('ct1')，将分片数设置为 2 ---|--- __

|

创建第二个组件模板 ('ct2')，该模板将副本数设置为 0 并定义映射 __

|

创建使用组件模板 __ 的索引模板("最终模板")

|

显示将应用于"my-index-000001"的配置 响应显示"最终模板"应用的索引设置、映射和别名：

    
    
    {
      "template" : {
        "settings" : {
          "index" : {
            "number_of_shards" : "2",
            "number_of_replicas" : "0",
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
              "type" : "date"
            }
          }
        },
        "aliases" : { }
      },
      "overlapping" : [
        {
          "name" : "template_1",
          "index_patterns" : [
            "my-index-*"
          ]
        }
      ]
    }

[« Shrink index API](indices-shrink-index.md) [Simulate index template API
»](indices-simulate-template.md)
