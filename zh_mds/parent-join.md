

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« IP field type](ip.md) [Keyword type family »](keyword.md)

## 联接字段类型

"join"数据类型是一个特殊字段，用于在同一索引的文档内创建父/子关系。"关系"部分定义了文档中一组可能的关系，每个关系都是父名称和子名称。

我们不建议使用多个级别的关系来复制非关系模型。每个关系级别都会在查询时增加内存和计算方面的开销。为了获得更好的搜索性能，请改为对数据进行非规范化。

父/子关系可以定义如下：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            my_id: {
              type: 'keyword'
            },
            my_join_field: {
              type: 'join',
              relations: {
                question: 'answer'
              }
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
          "my_id": {
            "type": "keyword"
          },
          "my_join_field": { __"type": "join",
            "relations": {
              "question": "answer" __}
          }
        }
      }
    }

__

|

字段的名称 ---|--- __

|

定义单个关系，其中"问题"是"答案"的父级。   要使用联接为文档编制索引，必须在"源"中提供关系的名称和文档的可选父级。例如，以下示例在"问题"上下文中创建两个"父"文档：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        my_id: '1',
        text: 'This is a question',
        my_join_field: {
          name: 'question'
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      refresh: true,
      body: {
        my_id: '2',
        text: 'This is another question',
        my_join_field: {
          name: 'question'
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?refresh
    {
      "my_id": "1",
      "text": "This is a question",
      "my_join_field": {
        "name": "question" __}
    }
    
    PUT my-index-000001/_doc/2?refresh
    {
      "my_id": "2",
      "text": "This is another question",
      "my_join_field": {
        "name": "question"
      }
    }

__

|

本文档是"问题"文档。   ---|--- 为父文档编制索引时，可以选择仅指定关系的名称作为快捷方式，而不是将其封装在普通的对象注释中：

    
    
    PUT my-index-000001/_doc/1?refresh
    {
      "my_id": "1",
      "text": "This is a question",
      "my_join_field": "question" __}
    
    PUT my-index-000001/_doc/2?refresh
    {
      "my_id": "2",
      "text": "This is another question",
      "my_join_field": "question"
    }

__

|

父文档的简单表示法仅使用关系名称。   ---|--- 为子项编制索引时，必须在"_source"中添加关系的名称以及文档的父 ID。

需要在同一分片中索引父文档的世系，因此必须始终使用其更大的父 ID 路由子文档。

例如，以下示例演示如何为两个"子"文档编制索引：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 3,
      routing: 1,
      refresh: true,
      body: {
        my_id: '3',
        text: 'This is an answer',
        my_join_field: {
          name: 'answer',
          parent: '1'
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 4,
      routing: 1,
      refresh: true,
      body: {
        my_id: '4',
        text: 'This is another answer',
        my_join_field: {
          name: 'answer',
          parent: '1'
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/3?routing=1&refresh __{
      "my_id": "3",
      "text": "This is an answer",
      "my_join_field": {
        "name": "answer", __"parent": "1" __}
    }
    
    PUT my-index-000001/_doc/4?routing=1 &refresh
    {
      "my_id": "4",
      "text": "This is another answer",
      "my_join_field": {
        "name": "answer",
        "parent": "1"
      }
    }

__

|

路由值是必需的，因为父文档和子文档必须在同一分片上编制索引 ---|--- __

|

"答案"是本文档的联接名称 __

|

此子文档的父 ID ### 父联接和性能编辑

连接字段不应像关系数据库中的连接那样使用。在 Elasticsearch 中，良好性能的关键是将数据非规范化为文档。每个联接字段("has_child"或"has_parent"查询都会给查询性能增加大量税收。它还可以触发要构建的全局序数。

连接字段有意义的唯一情况是，如果数据包含一对多关系，其中一个实体的数量明显超过另一个实体。此类案例的一个示例是这些产品的产品和优惠的用例。在报价数量明显超过产品数量的情况下，将产品建模为父文档并将产品/服务建模为子文档是有意义的。

### 父联接限制

* 每个索引只允许一个"连接"字段映射。  * 父文档和子文档必须在同一分片上编制索引。这意味着在获取、删除或更新子文档时需要提供相同的"路由"值。  * 一个元素可以有多个子元素，但只能有一个父元素。  * 可以为现有的"连接"字段添加新关系。  * 也可以向现有元素添加子元素，但前提是该元素已经是父元素。

### 使用父联接进行搜索

父联接创建一个字段来索引文档中关系的名称("my_parent"、"my_child"等)。

它还为每个父/子关系创建一个字段。此字段的名称是"join"字段的名称，后跟"#"和其中父字段的名称。例如，对于"my_parent"->["my_child"，"another_child"]关系，"join"字段会创建一个名为"my_join_field#my_parent"的附加字段。

此字段包含文档链接到的父"_id"(如果文档是子文档)("my_child"或"another_child")，如果文档是父文档，则包含文档的"_id"("my_parent")。

搜索包含"join"字段的索引时，搜索响应中始终返回这两个字段：

    
    
    GET my-index-000001/_search
    {
      "query": {
        "match_all": {}
      },
      "sort": ["my_id"]
    }

将返回：

    
    
    {
      ...,
      "hits": {
        "total": {
          "value": 4,
          "relation": "eq"
        },
        "max_score": null,
        "hits": [
          {
            "_index": "my-index-000001",
            "_id": "1",
            "_score": null,
            "_source": {
              "my_id": "1",
              "text": "This is a question",
              "my_join_field": "question"         __},
            "sort": [
              "1"
            ]
          },
          {
            "_index": "my-index-000001",
            "_id": "2",
            "_score": null,
            "_source": {
              "my_id": "2",
              "text": "This is another question",
              "my_join_field": "question" __},
            "sort": [
              "2"
            ]
          },
          {
            "_index": "my-index-000001",
            "_id": "3",
            "_score": null,
            "_routing": "1",
            "_source": {
              "my_id": "3",
              "text": "This is an answer",
              "my_join_field": {
                "name": "answer", __"parent": "1" __}
            },
            "sort": [
              "3"
            ]
          },
          {
            "_index": "my-index-000001",
            "_id": "4",
            "_score": null,
            "_routing": "1",
            "_source": {
              "my_id": "4",
              "text": "This is another answer",
              "my_join_field": {
                "name": "answer",
                "parent": "1"
              }
            },
            "sort": [
              "4"
            ]
          }
        ]
      }
    }

__

|

本文档属于"问题"连接---|---__

|

本文档属于"问题"加入__

|

本文档属于"答案"加入__

|

子文档的链接父 ID ### 父联接查询和聚合编辑

有关详细信息，请参阅"has_child"和"has_parent"查询、"子项"聚合和内部命中。

"join"字段的值可在聚合和脚本中访问，并且可以使用"parent_id"查询进行查询：

    
    
    GET my-index-000001/_search
    {
      "query": {
        "parent_id": { __"type": "answer",
          "id": "1"
        }
      },
      "aggs": {
        "parents": {
          "terms": {
            "field": "my_join_field#question", __"size": 10
          }
        }
      },
      "runtime_mappings": {
        "parent": {
          "type": "long",
          "script": """
            emit(Integer.parseInt(doc['my_join_field#question'].value)) __"""
        }
      },
      "fields": [
        { "field": "parent" }
      ]
    }

__

|

查询"父 id"字段(另请参阅"has_parent"查询和"has_child"查询)---|---__

|

在"父 ID"字段上进行聚合(另请参阅"子级"聚合)__

|

访问脚本中的"父 ID"字段。   ### 全局序号编辑

"join"字段使用全局序号来加速连接。对分片进行任何更改后，需要重建全局序数。分片中存储的父 id 值越多，为"join"字段重建全局序数所需的时间就越长。

默认情况下，全局序数是急切构建的：如果索引已更改，"join"字段的全局序数将作为刷新的一部分重新生成。这可能会为刷新增加大量时间。但是，大多数情况下，这是正确的权衡，否则在使用第一个父级联接查询或聚合时会重新生成全局序号。这可能会给用户带来显著的延迟峰值，通常情况更糟，因为当发生多次写入时，可能会尝试在单个刷新间隔内重建"join"字段的多个全局序数。

当"join"字段不经常使用并且写入频繁发生时，禁用预先加载可能是有意义的：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            my_join_field: {
              type: 'join',
              relations: {
                question: 'answer'
              },
              eager_global_ordinals: false
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
          "my_join_field": {
            "type": "join",
            "relations": {
               "question": "answer"
            },
            "eager_global_ordinals": false
          }
        }
      }
    }

可以按父关系检查全局序号使用的堆量，如下所示：

    
    
    response = client.indices.stats(
      metric: 'fielddata',
      human: true,
      fields: 'my_join_field'
    )
    puts response
    
    response = client.nodes.stats(
      metric: 'indices',
      index_metric: 'fielddata',
      human: true,
      fields: 'my_join_field'
    )
    puts response
    
    
    # Per-index
    GET _stats/fielddata?human&fields=my_join_field#question
    
    # Per-node per-index
    GET _nodes/stats/indices/fielddata?human&fields=my_join_field#question

### 每个父级有多个孩子

也可以为单个父级定义多个子项：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            my_join_field: {
              type: 'join',
              relations: {
                question: [
                  'answer',
                  'comment'
                ]
              }
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
          "my_join_field": {
            "type": "join",
            "relations": {
              "question": ["answer", "comment"]  __}
          }
        }
      }
    }

__

|

"问题"是"答案"和"评论"的父级。   ---|--- ### 多级父联接编辑

我们不建议使用多个级别的关系来复制非关系模型。每个关系级别都会在查询时增加内存和计算方面的开销。为了获得更好的搜索性能，请改为对数据进行非规范化。

多层次的父/子：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            my_join_field: {
              type: 'join',
              relations: {
                question: [
                  'answer',
                  'comment'
                ],
                answer: 'vote'
              }
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
          "my_join_field": {
            "type": "join",
            "relations": {
              "question": ["answer", "comment"],  __"answer": "vote" __}
          }
        }
      }
    }

__

|

"问题"是"答案"和"评论"的父级---|---__

|

"answer"是"vote"的父级 上面的映射表示以下树：

    
    
       question
        /    \
       /      \
    comment  answer
               |
               |
              vote

为孙文档编制索引需要一个等于祖父级(世系的大父级)的"路由"值：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 3,
      routing: 1,
      refresh: true,
      body: {
        text: 'This is a vote',
        my_join_field: {
          name: 'vote',
          parent: '2'
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/3?routing=1&refresh __{
      "text": "This is a vote",
      "my_join_field": {
        "name": "vote",
        "parent": "2" __}
    }

__

|

此子文档必须与其父文档和父文档位于同一分片上 ---|--- __

|

此文档的父 ID(必须指向"答案"文档)« IP 字段类型 关键字类型系列 »