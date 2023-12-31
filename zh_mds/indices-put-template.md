

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Create or update component template API](indices-component-template.md)
[Create or update index template API »](indices-templates-v1.md)

## 创建或更新索引模板API

创建或更新索引模板。索引模板定义可自动应用于新索引的设置、映射和别名。

    
    
    response = client.indices.put_index_template(
      name: 'template_1',
      body: {
        index_patterns: [
          'te*'
        ],
        priority: 1,
        template: {
          settings: {
            number_of_shards: 2
          }
        }
      }
    )
    puts response
    
    
    PUT /_index_template/template_1
    {
      "index_patterns" : ["te*"],
      "priority" : 1,
      "template": {
        "settings" : {
          "number_of_shards" : 2
        }
      }
    }

###Request

"放/_index_template/<index-template>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

###Description

Elasticsearch 根据与索引名称匹配的通配符模式将模板应用于新索引。

索引模板在数据流或索引创建期间应用。对于数据流，这些设置和映射在创建流的支持索引时应用。

创建索引请求中指定的设置和映射将覆盖索引模板中指定的任何设置或映射。

对索引模板的更改不会影响现有索引，包括数据流的现有后备索引。

#### 索引模板中的注释

您可以在索引模板中使用 C 样式 /* */ 阻止注释。您可以在请求正文中的任何位置包含注释，但左大括号之前除外。

### 路径参数

`<index-template>`

     (Required, string) Name of the index template to create. 

### 查询参数

`create`

     (Optional, Boolean) If `true`, this request cannot replace or update existing index templates. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`composed_of`

     (Optional, array of strings) An ordered list of component template names. Component templates are merged in the order specified, meaning that the last component template specified has the highest precedence. See [Composing multiple component templates](indices-put-template.html#multiple-component-templates "Composing aliases, mappings, and settings") for an example. 

`data_stream`

    

(可选，对象)如果包含此对象，则模板用于创建数据流及其支持索引。支持空对象。

数据流需要具有"data_stream"对象的匹配索引模板。请参见创建索引模板。

"data_stream"的属性

`allow_custom_routing`

     (Optional, Boolean) If `true`, the data stream supports [custom routing](mapping-routing-field.html "_routing field"). Defaults to `false`. 
`hidden`

     (Optional, Boolean) If `true`, the data stream is [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices"). Defaults to `false`. 
`index_mode`

    

(可选，字符串)要创建的数据流的类型。有效值为"null"(常规数据流)和"time_series"(时间序列数据流"))。

如果为"time_series"，则每个后备索引的"index.mode"索引设置为"time_series"。

`index_patterns`

    

(必需，字符串数组)通配符 ('*') 表达式数组，用于在创建过程中匹配数据流和索引的名称。

Elasticsearch 包含多个内置索引模板。若要避免与这些模板发生命名冲突，请参阅避免索引模式冲突。

`_meta`

     (Optional, object) Optional user metadata about the index template. May have any contents. This map is not automatically generated by Elasticsearch. 
`priority`

     (Optional, integer) Priority to determine index template precedence when a new data stream or index is created. The index template with the highest priority is chosen. If no priority is specified the template is treated as though it is of priority 0 (lowest priority). This number is not automatically generated by Elasticsearch. 
`template`

    

(可选，对象)要应用的模板。它可以选择性地包括"别名"、"映射"或"设置"配置。

"模板"的属性

`aliases`

    

(可选，对象的对象)要添加的别名。

如果索引模板包含"data_stream"对象，则这些是数据流别名。否则，这些是索引别名。数据流别名会忽略"index_routing"、"路由"和"search_routing"选项。

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

    
    
    PUT _index_template/template_1
    {
      "index_patterns" : ["te*"],
      "template": {
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
    }

__

|

在索引创建期间，别名中的"{index}"占位符将替换为应用模板的实际索引名称。   ---|--- #### 多个匹配模板编辑

如果多个索引模板与新索引或数据流的名称匹配，则使用具有最高优先级的模板。例如：

    
    
    PUT /_index_template/template_1
    {
      "index_patterns" : ["t*"],
      "priority" : 0,
      "template": {
        "settings" : {
          "number_of_shards" : 1,
          "number_of_replicas": 0
        },
        "mappings" : {
          "_source" : { "enabled" : false }
        }
      }
    }
    
    PUT /_index_template/template_2
    {
      "index_patterns" : ["te*"],
      "priority" : 1,
      "template": {
        "settings" : {
          "number_of_shards" : 2
        },
        "mappings" : {
          "_source" : { "enabled" : true }
        }
      }
    }

对于以"te*"开头的索引，将启用"_source"，并且索引将具有两个主分片和一个副本，因为只会应用"template_2"。

不允许具有相同优先级的重叠索引模式的多个模板，并且尝试创建与具有相同优先级的现有索引模板匹配的模板时，将引发错误。

#### 模板版本控制

您可以使用"版本"参数将版本号添加到索引模板。外部系统可以使用这些版本号来简化模板管理。

"version"参数是可选的，不会由Elasticsearch自动生成或使用。

要取消设置"版本"，请替换模板而不指定版本。

    
    
    response = client.indices.put_index_template(
      name: 'template_1',
      body: {
        index_patterns: [
          'foo',
          'bar'
        ],
        priority: 0,
        template: {
          settings: {
            number_of_shards: 1
          }
        },
        version: 123
      }
    )
    puts response
    
    
    PUT /_index_template/template_1
    {
      "index_patterns" : ["foo", "bar"],
      "priority" : 0,
      "template": {
        "settings" : {
            "number_of_shards" : 1
        }
      },
      "version": 123
    }

若要检查"版本"，可以使用获取索引模板 API。

#### 模板元数据

可以使用"_meta"参数将任意元数据添加到索引模板。此用户定义的对象存储在群集状态中，因此最好保持简短。

"_meta"参数是可选的，不会由Elasticsearch自动生成或使用。

要取消设置"_meta"，请替换模板而不指定模板。

    
    
    response = client.indices.put_index_template(
      name: 'template_1',
      body: {
        index_patterns: [
          'foo',
          'bar'
        ],
        template: {
          settings: {
            number_of_shards: 3
          }
        },
        _meta: {
          description: 'set number of shards to three',
          serialization: {
            class: 'MyIndexTemplate',
            id: 17
          }
        }
      }
    )
    puts response
    
    
    PUT /_index_template/template_1
    {
      "index_patterns": ["foo", "bar"],
      "template": {
        "settings" : {
            "number_of_shards" : 3
        }
      },
      "_meta": {
        "description": "set number of shards to three",
        "serialization": {
          "class": "MyIndexTemplate",
          "id": 17
        }
      }
    }

若要检查"_meta"，可以使用获取索引模板 API。

#### 数据流定义

若要对数据流使用索引模板，该模板必须包含"data_stream"对象。请参见创建索引模板。

    
    
    response = client.indices.put_index_template(
      name: 'template_1',
      body: {
        index_patterns: [
          'logs-*'
        ],
        data_stream: {}
      }
    )
    puts response
    
    
    PUT /_index_template/template_1
    {
      "index_patterns": ["logs-*"],
      "data_stream": { }
    }

#### 编写别名、映射和设置

当在索引模板的"composed_of"字段中指定多个组件模板时，它们将按指定的顺序合并，这意味着后面的组件模板会覆盖早期的组件模板。接下来，将合并父索引模板中的任何映射、设置或别名。最后，合并索引请求本身的任何配置。

在此示例中，两个组件模板的顺序更改了索引的分片数：

    
    
    PUT /_component_template/template_with_2_shards
    {
      "template": {
        "settings": {
          "index.number_of_shards": 2
        }
      }
    }
    
    PUT /_component_template/template_with_3_shards
    {
      "template": {
        "settings": {
          "index.number_of_shards": 3
        }
      }
    }
    
    PUT /_index_template/template_1
    {
      "index_patterns": ["t*"],
      "composed_of": ["template_with_2_shards", "template_with_3_shards"]
    }

在这种情况下，匹配"t*"的索引将有三个主分片。如果组合模板的顺序颠倒，索引将有两个主分片。

映射定义以递归方式合并，这意味着以后的映射组件可以引入新的字段映射并更新映射配置。如果字段映射已包含在较早的组件中，则其定义将被较早的组件完全覆盖。

这种递归合并策略不仅适用于字段映射，也适用于"dynamic_templates"和"meta"等根选项。如果较早的组件包含"dynamic_templates"块，则默认情况下，新的"dynamic_templates"条目将附加到末尾。如果已存在具有相同键的条目，则新定义将覆盖该条目。

[« Create or update component template API](indices-component-template.md)
[Create or update index template API »](indices-templates-v1.md)
