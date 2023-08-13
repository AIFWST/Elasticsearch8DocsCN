

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Specialized queries](specialized-queries.md)

[« More like this query](query-dsl-mlt-query.md) [Rank feature query
»](query-dsl-rank-feature-query.md)

## 渗透查询

"percolate"查询可用于匹配存储在索引中的查询。"percolate"查询本身包含将用作查询以与存储的查询匹配的文档。

### 示例用法

为了提供一个简单的示例，本文档对渗透查询和文档都使用一个索引"my-index-000001"。当只注册了几个渗透查询时，此设置可以很好地工作。对于较重的使用量，建议将查询和文档存储在单独的索引中。有关更多详细信息，请参阅引擎盖下的工作原理。

创建包含两个字段的索引：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            message: {
              type: 'text'
            },
            query: {
              type: 'percolator'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "mappings": {
        "properties": {
          "message": {
            "type": "text"
          },
          "query": {
            "type": "percolator"
          }
        }
      }
    }

"message"字段是用于在将"percolator"查询中定义的文档编入索引之前对其进行预处理的字段。

"查询"字段用于为查询文档编制索引。它将保存表示实际 Elasticsearch 查询的 ajson 对象。"查询"字段已配置为使用渗滤器字段类型。此字段类型理解查询 dsl 并以这样一种方式存储查询，以便以后可以使用它来匹配在"percolate"查询上定义的文档。

在渗滤器中注册查询：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        query: {
          match: {
            message: 'bonsai tree'
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_doc/1?refresh
    {
      "query": {
        "match": {
          "message": "bonsai tree"
        }
      }
    }

将文档与注册的渗滤器查询匹配：

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "percolate": {
          "field": "query",
          "document": {
            "message": "A new bonsai tree in the office"
          }
        }
      }
    }

上述请求将产生以下响应：

    
    
    {
      "took": 13,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.26152915,
        "hits": [
          { __"_index": "my-index-000001",
            "_id": "1",
            "_score": 0.26152915,
            "_source": {
              "query": {
                "match": {
                  "message": "bonsai tree"
                }
              }
            },
            "fields" : {
              "_percolator_document_slot" : [0] __}
          }
        ]
      }
    }

__

|

ID 为 '1' 的查询与我们的文档匹配。   ---|---    __

|

"_percolator_document_slot"字段指示与此查询匹配的文档。在同时渗透多个文档时很有用。   ###Parametersedit

渗透文档时需要以下参数：

`field`

|

类型为"渗滤器"的字段，用于保存索引查询。这是必需参数。   ---|---"名称"

|

用于"_percolator_document_slot"字段的后缀，以防指定了多个"percolate"查询。这是一个可选参数。   "文档"

|

正在渗透的文档的源。   "文件"

|

与"document"参数类似，但通过jsonarray接受多个文档。   "document_type"

|

正在渗透的文档的类型/映射。此参数已弃用，将在 Elasticsearch 8.0 中删除。   除了指定要渗透的文档的源外，还可以从已存储的文档中检索源。然后，"percolate"查询将在内部执行 get 请求以获取该文档。

在这种情况下，"文档"参数可以替换为以下参数：

`index`

|

文档所在的索引。这是必需的参数。   ---|---"类型"

|

要提取的文档的类型。此参数已弃用，并将在 Elasticsearch 8.0 中删除。   'id'

|

要提取的文档的 ID。这是必需的参数。   "路由"

|

(可选)用于获取要渗透的文档的路由。   "偏好"

|

可选地，首选项用于获取要渗透的文档。   "版本"

|

(可选)要提取的文档的预期版本。   ### 在过滤器上下文中渗透编辑

如果您对分数不感兴趣，通过将渗滤器查询包装在"布尔"查询的过滤器子句中或"constant_score"查询中，可以预期性能更好：

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "constant_score": {
          "filter": {
            "percolate": {
              "field": "query",
              "document": {
                "message": "A new bonsai tree in the office"
              }
            }
          }
        }
      }
    }

在索引时，从渗滤器查询中提取术语，渗滤器通常只需查看这些提取的项即可确定查询是否匹配。但是，计算分数需要反序列化每个匹配的查询，并针对渗透的文档运行它，这是一个成本更高的操作。因此，如果不需要计算分数，则"percolate"查询应包装在"constant_score"查询或"bool"查询的过滤器子句中。

请注意，"percolate"查询永远不会被查询缓存缓存。

### 渗透多个文档

"percolate"查询可以将多个文档与索引的渗滤器查询同时匹配。在单个请求中渗透多个文档可以提高性能，因为查询只需要解析和匹配一次而不是多次。

在同时渗透多个文档时，每个匹配的percolator查询返回的"_percolator_document_slot"字段非常重要。它指示哪些文档与特定渗滤器查询匹配。这些数字与"文档"数组中的插槽相关，该数组在"percolate"查询中指定。

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "percolate": {
          "field": "query",
          "documents": [ __{
              "message": "bonsai tree"
            },
            {
              "message": "new tree"
            },
            {
              "message": "the office"
            },
            {
              "message": "office tree"
            }
          ]
        }
      }
    }

__

|

文档数组包含 4 个将同时渗透的文档。   ---|--- { "采取"： 13， "timed_out"： 假， "_shards"： { "总计"： 1， "成功"： 1， "跳过" ： 0， "失败"： 0 }， "命中"： { "总计" ： { "值"： 1， "关系"： "eq" }， "max_score"： 0.7093853， "命中"： [ { "_index"： "my-index-000001"， "_id"： "1"， "_score"： 0.7093853， "_source"： { "查询"： { "匹配"： {                 "消息"： "盆景树" } } }， "字段" ： { "_percolator_document_slot" ： [0， 1， 3] __} } ] } }

__

|

"_percolator_document_slot"表示"percolate"查询中指定的第一个、第二个和最后一个文档与此查询匹配。   ---|--- ### 渗透现有文档编辑

为了渗透新索引的文档，可以使用"渗透"查询。根据索引请求的响应，可以使用"_id"和其他元信息立即渗透新添加的文档。

####Example

基于前面的示例。

索引我们要渗透的文档：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        message: 'A new bonsai tree in the office'
      }
    )
    puts response
    
    
    PUT /my-index-000001/_doc/2
    {
      "message" : "A new bonsai tree in the office"
    }

索引响应：

    
    
    {
      "_index": "my-index-000001",
      "_id": "2",
      "_version": 1,
      "_shards": {
        "total": 2,
        "successful": 1,
        "failed": 0
      },
      "result": "created",
      "_seq_no" : 1,
      "_primary_term" : 1
    }

渗透现有文档，使用索引响应作为构建新搜索请求的基础：

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "percolate": {
          "field": "query",
          "index": "my-index-000001",
          "id": "2",
          "version": 1 __}
      }
    }

__

|

该版本是可选的，但在某些情况下很有用。我们可以确保我们试图渗透我们刚刚索引的文档。索引后可能会进行更改，如果是这种情况，搜索请求将失败并出现版本冲突错误。   ---|--- 返回的搜索响应与上一个示例中相同。

### 渗透查询和突出显示

在突出显示时，"percolate"查询以特殊方式处理。查询命中用于突出显示"percolate"查询中提供的文档。而通过常规突出显示查询，搜索请求用于突出显示命中。

####Example

此示例基于第一个示例的映射。

保存查询：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 3,
      refresh: true,
      body: {
        query: {
          match: {
            message: 'brown fox'
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_doc/3?refresh
    {
      "query": {
        "match": {
          "message": "brown fox"
        }
      }
    }

保存另一个查询：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 4,
      refresh: true,
      body: {
        query: {
          match: {
            message: 'lazy dog'
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_doc/4?refresh
    {
      "query": {
        "match": {
          "message": "lazy dog"
        }
      }
    }

在启用"percolate"查询和突出显示的情况下执行搜索请求：

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "percolate": {
          "field": "query",
          "document": {
            "message": "The quick brown fox jumps over the lazy dog"
          }
        }
      },
      "highlight": {
        "fields": {
          "message": {}
        }
      }
    }

这将产生以下响应。

    
    
    {
      "took": 7,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 2,
            "relation": "eq"
        },
        "max_score": 0.26152915,
        "hits": [
          {
            "_index": "my-index-000001",
            "_id": "3",
            "_score": 0.26152915,
            "_source": {
              "query": {
                "match": {
                  "message": "brown fox"
                }
              }
            },
            "highlight": {
              "message": [
                "The quick <em>brown</em> <em>fox</em> jumps over the lazy dog" __]
            },
            "fields" : {
              "_percolator_document_slot" : [0]
            }
          },
          {
            "_index": "my-index-000001",
            "_id": "4",
            "_score": 0.26152915,
            "_source": {
              "query": {
                "match": {
                  "message": "lazy dog"
                }
              }
            },
            "highlight": {
              "message": [
                "The quick brown fox jumps over the <em>lazy</em> <em>dog</em>" __]
            },
            "fields" : {
              "_percolator_document_slot" : [0]
            }
          }
        ]
      }
    }

__

|

文档中突出显示了每个查询的术语。   ---|--- 搜索请求中的查询不是突出显示渗滤器命中，而是突出显示"渗滤器"查询中定义的文档。

当像下面的要求一样同时渗透多个文档时，突出显示的响应是不同的：

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "percolate": {
          "field": "query",
          "documents": [
            {
              "message": "bonsai tree"
            },
            {
              "message": "new tree"
            },
            {
              "message": "the office"
            },
            {
              "message": "office tree"
            }
          ]
        }
      },
      "highlight": {
        "fields": {
          "message": {}
        }
      }
    }

略有不同的反应：

    
    
    {
      "took": 13,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.7093853,
        "hits": [
          {
            "_index": "my-index-000001",
            "_id": "1",
            "_score": 0.7093853,
            "_source": {
              "query": {
                "match": {
                  "message": "bonsai tree"
                }
              }
            },
            "fields" : {
              "_percolator_document_slot" : [0, 1, 3]
            },
            "highlight" : { __"0_message" : [
                  " <em>bonsai</em> <em>tree</em>"
              ],
              "3_message" : [
                  "office <em>tree</em>"
              ],
              "1_message" : [
                  "new <em>tree</em>"
              ]
            }
          }
        ]
      }
    }

__

|

突出显示字段已以它们所属的文档插槽为前缀，以便知道哪个突出显示字段属于哪个文档。   ---|--- ### 指定多个渗透查询编辑

可以在单个搜索请求中指定多个"percolate"查询：

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "bool": {
          "should": [
            {
              "percolate": {
                "field": "query",
                "document": {
                  "message": "bonsai tree"
                },
                "name": "query1" __}
            },
            {
              "percolate": {
                "field": "query",
                "document": {
                  "message": "tulip flower"
                },
                "name": "query2" __}
            }
          ]
        }
      }
    }

__

|

"name"参数将用于标识哪个渗滤器文档插槽属于哪个"渗透"查询。   ---|--- "_percolator_document_slot"字段名称将以"_name"参数中指定的内容为后缀。如果未指定，则将使用"field"参数，在这种情况下将导致歧义。

上面的搜索请求返回类似于以下内容的响应：

    
    
    {
      "took": 13,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.26152915,
        "hits": [
          {
            "_index": "my-index-000001",
            "_id": "1",
            "_score": 0.26152915,
            "_source": {
              "query": {
                "match": {
                  "message": "bonsai tree"
                }
              }
            },
            "fields" : {
              "_percolator_document_slot_query1" : [0] __}
          }
        ]
      }
    }

__

|

"_percolator_document_slot_query1"渗滤器插槽字段指示这些匹配的插槽来自"_name"参数设置为"query1"的"percolate"查询。   ---|--- ### 它是如何工作的

将文档索引为配置了渗滤器字段类型映射的索引时，文档的查询部分将解析为 Lucene 查询并存储到 Lucene 索引中。存储查询的二进制表示形式，但查询的术语也被分析并存储到索引字段中。

在搜索时，请求中指定的文档被解析为 Lucene 文档，并存储在内存中的临时 Lucene 索引中。此内存中索引只能保存这一个文档，并为此进行了优化。在此之后，将根据内存中索引中的术语构建一个特殊查询，该查询根据其索引查询词选择候选渗滤器查询。然后，如果这些查询确实匹配，则由内存中索引进行评估。

在执行"percolate"查询期间，选择候选渗滤器查询匹配项是一项重要的性能优化，因为它可以显著减少内存中索引需要评估的候选匹配项的数量。"percolate"查询可以执行此操作的原因是，在对渗透器查询编制索引期间，正在提取查询词并使用渗透器查询编制索引。不幸的是，渗滤器无法从所有查询中提取术语(例如"通配符"或"geo_shape"查询)，因此在某些情况下，渗滤器无法进行选择优化(例如，如果在布尔查询的必需子句中定义了不受支持的查询，或者不支持的查询是渗滤器文档中的唯一查询)。这些查询由渗滤器标记，可以通过运行以下搜索找到：

    
    
    response = client.search(
      body: {
        query: {
          term: {
            "query.extraction_result": 'failed'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "term" : {
          "query.extraction_result" : "failed"
        }
      }
    }

上面的示例假定映射中存在类型为"渗滤器"的"查询"字段。

鉴于渗透的设计，对渗透查询和要渗透的文档使用单独的索引通常是有意义的，而不是像我们在示例中所做的那样使用单个索引。此方法有几个好处：

* 由于渗透查询包含一组与渗透文档不同的字段集，因此使用两个单独的索引允许以更密集、更高效的方式存储字段。  * 渗透查询的扩展方式与其他查询不同，因此渗透性能可能会受益于使用不同的索引配置，例如主分片的数量。

###Notes

#### 允许昂贵的查询

如果"search.allow_expensive_queries"设置为 false，则不会执行渗透查询。

[« More like this query](query-dsl-mlt-query.md) [Rank feature query
»](query-dsl-rank-feature-query.md)
