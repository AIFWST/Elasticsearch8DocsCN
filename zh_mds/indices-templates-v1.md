

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Create or update index template API](indices-put-template.md) [Delete
component template API »](indices-delete-component-template.md)

## 创建或更新索引模板API

本文档介绍旧版索引模板，这些模板已弃用，将由 Elasticsearch 7.8 中引入的可组合模板取代。有关可组合模板的信息，请参阅索引模板。

创建或更新索引模板。

    
    
    $params = [
        'name' => 'template_1',
        'body' => [
            'index_patterns' => [
                'te*',
                'bar*',
            ],
            'settings' => [
                'number_of_shards' => 1,
            ],
            'mappings' => [
                '_source' => [
                    'enabled' => false,
                ],
                'properties' => [
                    'host_name' => [
                        'type' => 'keyword',
                    ],
                    'created_at' => [
                        'type' => 'date',
                        'format' => 'EEE MMM dd HH:mm:ss Z yyyy',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->indices()->putTemplate($params);
    
    
    resp = client.indices.put_template(
        name="template_1",
        body={
            "index_patterns": ["te*", "bar*"],
            "settings": {"number_of_shards": 1},
            "mappings": {
                "_source": {"enabled": False},
                "properties": {
                    "host_name": {"type": "keyword"},
                    "created_at": {
                        "type": "date",
                        "format": "EEE MMM dd HH:mm:ss Z yyyy",
                    },
                },
            },
        },
    )
    print(resp)
    
    
    const response = await client.indices.putTemplate({
      name: 'template_1',
      body: {
        index_patterns: [
          'te*',
          'bar*'
        ],
        settings: {
          number_of_shards: 1
        },
        mappings: {
          _source: {
            enabled: false
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
        }
      }
    })
    console.log(response)
    
    
    PUT _template/template_1
    {
      "index_patterns": ["te*", "bar*"],
      "settings": {
        "number_of_shards": 1
      },
      "mappings": {
        "_source": {
          "enabled": false
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
      }
    }

###Request

"放/_template/<index-template>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

###Description

索引模板定义创建新索引时可以自动应用的设置和映射。Elasticsearch 根据与索引名称匹配的索引模式将模板应用于新索引。

可组合模板始终优先于旧模板。如果不可组合模板与新索引匹配，则会根据其顺序应用匹配的旧模板。

索引模板仅在索引创建期间应用。对索引模板的更改不会影响现有索引。在创建索引 API 请求中指定的设置和映射将覆盖索引模板中指定的任何设置或映射。

#### 索引模板中的注释

您可以在索引模板中使用 C 样式 /* */ 阻止注释。您可以在请求正文中的任何位置包含注释，但左大括号之前除外。

#### 获取模板

请参阅获取索引模板(旧版)。

### 路径参数

`<index-template>`

     (Required, string) Name of the index template to create. 

### 查询参数

`create`

     (Optional, Boolean) If `true`, this request cannot replace or update existing index templates. Defaults to `false`. 
`order`

    

(可选，整数)如果索引匹配多个模板，则 Elasticsearch 应用此模板的顺序。

首先合并具有较低"顺序"值的模板。具有较高"顺序"值的模板稍后合并，覆盖具有较低值的模板。

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`index_patterns`

     (Required, array of strings) Array of wildcard expressions used to match the names of indices during creation. 
`aliases`

    

(可选，对象的对象)索引的别名。

"别名"对象的属性

`<alias>`

    

(必填，对象)键是别名。索引别名支持日期数学。

对象正文包含别名的选项。支持空对象。

""的属性<alias>

`filter`

     (Optional, [Query DSL object](query-dsl.html "Query DSL")) Query used to limit documents the alias can access. 
`index_routing`

     (Optional, string) Value used to route indexing operations to a specific shard. If specified, this overwrites the `routing` value for indexing operations. 
`is_hidden`

     (Optional, Boolean) If `true`, the alias is [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices"). Defaults to `false`. All indices for the alias must have the same `is_hidden` value. 
`is_write_index`

     (Optional, Boolean) If `true`, the index is the [write index](aliases.html#write-index "Write index") for the alias. Defaults to `false`. 
`routing`

     (Optional, string) Value used to route indexing and search operations to a specific shard. 
`search_routing`

     (Optional, string) Value used to route search operations to a specific shard. If specified, this overwrites the `routing` value for search operations. 

`mappings`

    

(可选，映射对象)索引中字段的映射。如果指定，此映射可以包括：

* 字段名称 * 字段数据类型 * 映射参数

请参阅映射。

`settings`

     (Optional, [index setting object](index-modules.html#index-modules-settings "Index Settings")) Configuration options for the index. See [Index Settings](index-modules.html#index-modules-settings "Index Settings"). 
`version`

     (Optional, integer) Version number used to manage index templates externally. This number is not automatically generated by Elasticsearch. 

###Examples

#### 具有索引别名的索引模板

可以在索引模板中包含索引别名。

    
    
    PUT _template/template_1
    {
      "index_patterns" : ["te*"],
      "settings" : {
        "number_of_shards" : 1
      },
      "aliases" : {
        "alias1" : {},
        "alias2" : {
          "filter" : {
            "term" : {"user.id" : "kimchy" }
          },
          "routing" : "shard-1"
        },
        "{index}-alias" : {} __}
    }

__

|

在索引创建期间，别名中的"{index}"占位符将替换为应用模板的实际索引名称。   ---|--- #### 索引匹配多个模板编辑

多个索引模板可能与一个索引匹配，在这种情况下，设置和映射都将合并到索引的最终配置中。可以使用"order"参数控制合并的顺序，首先应用较低的顺序，较高的顺序覆盖它们。例如：

    
    
    PUT /_template/template_1
    {
      "index_patterns" : ["te*"],
      "order" : 0,
      "settings" : {
        "number_of_shards" : 1
      },
      "mappings" : {
        "_source" : { "enabled" : false }
      }
    }
    
    PUT /_template/template_2
    {
      "index_patterns" : ["tes*"],
      "order" : 1,
      "settings" : {
        "number_of_shards" : 1
      },
      "mappings" : {
        "_source" : { "enabled" : true }
      }
    }

上述操作将禁用存储"_source"，但对于以"tes*"开头的索引，仍将启用"_source"。请注意，对于映射，合并是"深度"的，这意味着可以在高阶模板上轻松添加/覆盖基于特定对象/属性的映射，而低阶模板提供了基础。

具有相同订单值的多个匹配模板将导致不确定的合并顺序。

#### 模板版本控制

您可以使用"版本"参数将可选版本号添加到索引模板。外部系统可以使用这些版本号来简化模板管理。

'version' 参数是完全可选的，不是由 Elasticsearch 自动生成的。

要取消设置"版本"，请替换模板而不指定版本。

    
    
    response = client.indices.put_template(
      name: 'template_1',
      body: {
        index_patterns: [
          'my-index-*'
        ],
        order: 0,
        settings: {
          number_of_shards: 1
        },
        version: 123
      }
    )
    puts response
    
    
    PUT /_template/template_1
    {
      "index_patterns" : ["my-index-*"],
      "order" : 0,
      "settings" : {
        "number_of_shards" : 1
      },
      "version": 123
    }

若要检查"版本"，可以使用带有"filter_path"查询参数的获取索引模板 API 仅返回版本号：

    
    
    $params = [
        'name' => 'template_1',
    ];
    $response = $client->indices()->getTemplate($params);
    
    
    resp = client.indices.get_template(
        name="template_1", filter_path="*.version",
    )
    print(resp)
    
    
    response = client.indices.get_template(
      name: 'template_1',
      filter_path: '*.version'
    )
    puts response
    
    
    const response = await client.indices.getTemplate({
      name: 'template_1',
      filter_path: '*.version'
    })
    console.log(response)
    
    
    GET /_template/template_1?filter_path=*.version

API 返回以下响应：

    
    
    {
      "template_1" : {
        "version" : 123
      }
    }

[« Create or update index template API](indices-put-template.md) [Delete
component template API »](indices-delete-component-template.md)
