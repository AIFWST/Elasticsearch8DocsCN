

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Binary field type](binary.md) [Completion field type »](completion.md)

## 布尔字段类型

布尔字段接受 JSON "真"和"假"值，但也可以接受解释为 true 或 false 的字符串：

假值

|

'false'， 'false'， '""' (空字符串) ---|--- 真值

|

"真"、"真"，例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            is_published: {
              type: 'boolean'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        is_published: 'true'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          term: {
            is_published: true
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "is_published": {
            "type": "boolean"
          }
        }
      }
    }
    
    POST my-index-000001/_doc/1?refresh
    {
      "is_published": "true" __}
    
    GET my-index-000001/_search
    {
      "query": {
        "term": {
          "is_published": true __}
      }
    }

__

|

使用"true"为文档编制索引，该文档被解释为"true"。   ---|---    __

|

搜索带有 JSON "true"的文档。   像"terms"聚合这样的聚合使用"1"和"0"作为"键"，字符串"true"和"false"作为"key_as_string"。在脚本中使用布尔字段时，返回"true"和"false"：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        is_published: true
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      refresh: true,
      body: {
        is_published: false
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        aggregations: {
          publish_state: {
            terms: {
              field: 'is_published'
            }
          }
        },
        sort: [
          'is_published'
        ],
        fields: [
          {
            field: 'weight'
          }
        ],
        runtime_mappings: {
          weight: {
            type: 'long',
            script: "emit(doc['is_published'].value ? 10 : 0)"
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_doc/1?refresh
    {
      "is_published": true
    }
    
    POST my-index-000001/_doc/2?refresh
    {
      "is_published": false
    }
    
    GET my-index-000001/_search
    {
      "aggs": {
        "publish_state": {
          "terms": {
            "field": "is_published"
          }
        }
      },
      "sort": [ "is_published" ],
      "fields": [
        {"field": "weight"}
      ],
      "runtime_mappings": {
        "weight": {
          "type": "long",
          "script": "emit(doc['is_published'].value ? 10 : 0)"
        }
      }
    }

### "布尔"字段的参数

"布尔"字段接受以下参数：

"doc_values"

|

字段是否应以列步幅方式存储在磁盘上，以便以后可用于排序、聚合或脚本编写？接受"真"(默认值)或"假"。   ---|--- "索引"

|

该字段是否应该快速搜索？接受"真"(默认值)和"假"。仅启用了"doc_values"的字段仍可以使用基于术语或范围的查询进行查询，尽管速度较慢。   "ignore_malformed"

|

默认情况下，尝试将错误的数据类型索引到字段中会引发异常，并拒绝整个文档。如果此参数设置为 true，则允许忽略异常。格式错误的字段未编制索引，但文档中的其他字段将正常处理。接受"真"或"假"。请注意，如果使用"script"参数，则无法设置此选项。   "null_value"

|

接受上面列出的任何真值或假值。该值将替换为任何显式的"空"值。默认为"null"，表示该字段被视为缺失。请注意，如果使用"script"参数，则无法设置此选项。   "on_script_error"

|

定义当由"script"参数定义的脚本在索引时引发错误时要执行的操作。接受"fail"(默认)，这将导致整个文档被拒绝，以及"继续"，这将在文档的"_ignored"元数据字段中注册字段并继续索引。仅当还设置了"脚本"字段时，才能设置此参数。   "脚本"

|

如果设置了此参数，则字段将索引此脚本生成的值，而不是直接从源读取值。如果在输入文档上为此字段设置了值，则该文档将被拒绝并显示错误。脚本的格式与其运行时等效的格式相同。   "商店"

|

字段值是否应与"_source"字段分开存储和检索。接受"真"或"假"(默认值)。   "元"

|

有关字段的元数据。   ### 合成'_source'编辑

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"布尔"字段在其默认配置中支持合成的"_source"。合成"_source"不能与"copy_to"一起使用，也不能禁用"doc_values"。

合成源总是对"布尔"字段进行排序。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            bool: {
              type: 'boolean'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        bool: [
          true,
          false,
          true,
          false
        ]
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "bool": { "type": "boolean" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "bool": [true, false, true, false]
    }

将成为：

    
    
    {
      "bool": [false, false, true, true]
    }

[« Binary field type](binary.md) [Completion field type »](completion.md)
