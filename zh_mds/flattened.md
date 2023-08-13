

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Dense vector field type](dense-vector.md) [Geopoint field type »](geo-
point.md)

## 平展字段类型

默认情况下，对象中的每个子字段都是单独映射和索引的。如果事先不知道子字段的名称或类型，则会动态映射它们。

"平展"类型提供了一种替代方法，其中整个对象被映射为单个字段。给定一个对象，"平展"映射将解析出其叶值，并将它们作为关键字索引到一个字段中。然后，可以通过简单的查询和聚合搜索对象的内容。

此数据类型可用于为具有大量或未知数量的唯一键的对象编制索引。只为整个 JSONobject 创建一个字段映射，这有助于防止映射爆炸具有太多不同的字段映射。

另一方面，扁平化的对象字段在搜索功能方面存在权衡。仅允许基本查询，不支持数字范围查询或突出显示。有关限制的更多信息，请参阅支持的操作部分。

"平展"映射类型不应用于索引所有文档内容，因为它将所有值视为关键字，并且不提供完整的搜索功能。默认方法，其中每个子字段在映射中都有自己的条目，在大多数情况下效果很好。

可以按如下方式创建拼合对象字段：

    
    
    response = client.indices.create(
      index: 'bug_reports',
      body: {
        mappings: {
          properties: {
            title: {
              type: 'text'
            },
            labels: {
              type: 'flattened'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'bug_reports',
      id: 1,
      body: {
        title: 'Results are not sorted correctly.',
        labels: {
          priority: 'urgent',
          release: [
            'v1.2.5',
            'v1.3.0'
          ],
          timestamp: {
            created: 1_541_458_026,
            closed: 1_541_457_010
          }
        }
      }
    )
    puts response
    
    
    PUT bug_reports
    {
      "mappings": {
        "properties": {
          "title": {
            "type": "text"
          },
          "labels": {
            "type": "flattened"
          }
        }
      }
    }
    
    POST bug_reports/_doc/1
    {
      "title": "Results are not sorted correctly.",
      "labels": {
        "priority": "urgent",
        "release": ["v1.2.5", "v1.3.0"],
        "timestamp": {
          "created": 1541458026,
          "closed": 1541457010
        }
      }
    }

在编制索引期间，将为 JSON 对象中的每个叶值创建令牌。这些值作为字符串关键字编制索引，不对数字或日期进行分析或特殊处理。

查询顶级"平展"字段将搜索对象中的所有叶值：

    
    
    response = client.search(
      index: 'bug_reports',
      body: {
        query: {
          term: {
            labels: 'urgent'
          }
        }
      }
    )
    puts response
    
    
    POST bug_reports/_search
    {
      "query": {
        "term": {"labels": "urgent"}
      }
    }

若要查询平展对象中的特定键，请使用对象点表示法：

    
    
    response = client.search(
      index: 'bug_reports',
      body: {
        query: {
          term: {
            "labels.release": 'v1.3.0'
          }
        }
      }
    )
    puts response
    
    
    POST bug_reports/_search
    {
      "query": {
        "term": {"labels.release": "v1.3.0"}
      }
    }

### 支持的操作

由于值的索引方式相似，"平展"字段与"关键字"字段共享许多相同的映射和搜索功能。

目前，平展的对象字段可用于以下查询类型：

* "术语"、"术语"和"terms_set" * "前缀" * "范围" * "匹配"和"multi_match" * "query_string"和"simple_query_string" * "存在"

查询时，无法使用通配符引用字段键，例如 '{ "term"： {"labels.time*"： 1541457010}}'。请注意，所有查询(包括"range")都将值视为字符串关键字。"平展"字段不支持突出显示。

可以对平展的对象字段进行排序，也可以执行简单关键字样式的聚合，例如"术语"。与查询一样，对数字没有特殊支持 - JSON 对象中的所有值都被视为关键字。排序时，这意味着值是按词典顺序比较的。

当前无法存储拼合的对象字段。无法在映射中指定"store"参数。

### 检索平展字段

字段值和具体子字段可以使用 fieldsparameter.content 进行检索。由于"平展"字段将具有潜在多个子字段的整个对象映射为单个字段，因此响应包含来自"_source"的未更改结构。

但是，可以通过在请求中显式指定单个子字段来获取它们。这仅适用于具体路径，但不适用于通配符：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            flattened_field: {
              type: 'flattened'
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
        flattened_field: {
          subfield: 'value'
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        fields: [
          'flattened_field.subfield'
        ],
        _source: false
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "flattened_field": {
            "type": "flattened"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1?refresh=true
    {
      "flattened_field" : {
        "subfield" : "value"
      }
    }
    
    POST my-index-000001/_search
    {
      "fields": ["flattened_field.subfield"],
      "_source": false
    }
    
    
    {
      "took": 2,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [{
          "_index": "my-index-000001",
          "_id": "1",
          "_score": 1.0,
          "fields": {
            "flattened_field.subfield" : [ "value" ]
          }
        }]
      }
    }

您还可以使用无痛脚本从平展字段的子字段中检索值。不要<field_name>在 Painless 脚本中包含 'doc['].value'，而是使用 'doc['<field_name>.<sub-field_name>']。值'。例如，如果您将名为"label"的字段与"release"子字段平展，则您的Painlessscript将是"doc['labels.release'].value"。

例如，假设您的映射包含两个字段，其中一个为"平展"类型：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            title: {
              type: 'text'
            },
            labels: {
              type: 'flattened'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "title": {
            "type": "text"
          },
          "labels": {
            "type": "flattened"
          }
        }
      }
    }

索引一些包含映射字段的文档。"标签"字段有三个子字段：

    
    
    response = client.bulk(
      index: 'my-index-000001',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          title: 'Something really urgent',
          labels: {
            priority: 'urgent',
            release: [
              'v1.2.5',
              'v1.3.0'
            ],
            timestamp: {
              created: 1_541_458_026,
              closed: 1_541_457_010
            }
          }
        },
        {
          index: {}
        },
        {
          title: 'Somewhat less urgent',
          labels: {
            priority: 'high',
            release: [
              'v1.3.0'
            ],
            timestamp: {
              created: 1_541_458_026,
              closed: 1_541_457_010
            }
          }
        },
        {
          index: {}
        },
        {
          title: 'Not urgent',
          labels: {
            priority: 'low',
            release: [
              'v1.2.0'
            ],
            timestamp: {
              created: 1_541_458_026,
              closed: 1_541_457_010
            }
          }
        }
      ]
    )
    puts response
    
    
    POST /my-index-000001/_bulk?refresh
    {"index":{}}
    {"title":"Something really urgent","labels":{"priority":"urgent","release":["v1.2.5","v1.3.0"],"timestamp":{"created":1541458026,"closed":1541457010}}}
    {"index":{}}
    {"title":"Somewhat less urgent","labels":{"priority":"high","release":["v1.3.0"],"timestamp":{"created":1541458026,"closed":1541457010}}}
    {"index":{}}
    {"title":"Not urgent","labels":{"priority":"low","release":["v1.2.0"],"timestamp":{"created":1541458026,"closed":1541457010}}}

由于"标签"是"平展"字段类型，因此整个对象将映射为单个字段。要在无痛脚本中从此子字段中检索值，请使用"doc['<field_name>.<sub-field_name>']。值"格式。

    
    
    "script": {
      "source": """
        if (doc['labels.release'].value.equals('v1.3.0'))
        {emit(doc['labels.release'].value)}
        else{emit('Version mismatch')}
      """

### 拼合对象字段的参数

接受以下映射参数：

`depth_limit`

|

平展对象字段的最大允许深度(以嵌套内部对象为单位)。如果平展的对象字段超过此限制，则会引发错误。默认为"20"。请注意，"depth_limit"可以通过更新映射 API 动态更新。   ---|--- "doc_values"

|

字段是否应以列步幅方式存储在磁盘上，以便以后可用于排序、聚合或脚本编写？接受"真"(默认值)或"假"。   "eager_global_ordinals"

|

刷新时是否应该急切地加载全局序数？接受"真"或"假"(默认值)。在经常用于术语聚合的字段上启用此功能是一个好主意。   "ignore_above"

|

超过此限制的叶值将不会编制索引。默认情况下，没有限制，所有值都将被索引。请注意，此限制适用于平展对象字段中的叶值，而不是整个字段的长度。   "索引"

|

确定字段是否应可搜索。接受"真"(默认值)或"假"。   "index_options"

|

出于评分目的，应在索引中存储哪些信息。默认为"docs"，但也可以设置为"频率"，以便在计算分数时考虑术语频率。   "null_value"

|

一个字符串值，用于替换平展对象字段中的任何显式"null"值。默认为"null"，这意味着空 sields 被视为丢失。   "相似性"

|

应使用哪种评分算法或_相似性_。默认为"BM25"。   "split_queries_on_whitespace"

|

全文查询在为此字段生成查询时是否应拆分空格上的输入。接受"真"或"假"(默认值)。   "time_series_dimensions"

|

(可选，字符串数组)平展对象内的字段列表，其中每个字段是时间序列的一个维度。每个字段都是使用根字段的相对路径指定的，并且不包含根字段名称。   ### 合成'_source'编辑

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

平展字段在其默认配置中支持合成的"_source"。合成"_source"不能在禁用"doc_values"的情况下使用。

合成源始终按字母顺序排序，并对平展字段进行重复数据删除。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            flattened: {
              type: 'flattened'
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
        flattened: {
          field: [
            'apple',
            'apple',
            'banana',
            'avocado',
            '10',
            '200',
            'AVOCADO',
            'Banana',
            'Tangerine'
          ]
        }
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "flattened": { "type": "flattened" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "flattened": {
        "field": [ "apple", "apple", "banana", "avocado", "10", "200", "AVOCADO", "Banana", "Tangerine" ]
      }
    }

将成为：

    
    
    {
      "flattened": {
        "field": [ "10", "200", "AVOCADO", "Banana", "Tangerine", "apple", "avocado", "banana" ]
      }
    }

合成源始终使用嵌套对象而不是对象数组。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            flattened: {
              type: 'flattened'
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
        flattened: {
          field: [
            {
              id: 1,
              name: 'foo'
            },
            {
              id: 2,
              name: 'bar'
            },
            {
              id: 3,
              name: 'baz'
            }
          ]
        }
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "flattened": { "type": "flattened" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "flattened": {
          "field": [
            { "id": 1, "name": "foo" },
            { "id": 2, "name": "bar" },
            { "id": 3, "name": "baz" }
          ]
      }
    }

将成为(注意嵌套对象而不是"扁平"数组)：

    
    
    {
        "flattened": {
          "field": {
              "id": [ "1", "2", "3" ],
              "name": [ "bar", "baz", "foo" ]
          }
        }
    }

合成源始终对单元素数组使用单值字段。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            flattened: {
              type: 'flattened'
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
        flattened: {
          field: [
            'foo'
          ]
        }
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "flattened": { "type": "flattened" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "flattened": {
        "field": [ "foo" ]
      }
    }

将成为(注意嵌套对象而不是"扁平"数组)：

    
    
    {
      "flattened": {
        "field": "foo"
      }
    }

[« Dense vector field type](dense-vector.md) [Geopoint field type »](geo-
point.md)
