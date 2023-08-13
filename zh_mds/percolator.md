

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Object field type](object.md) [Point field type »](point.md)

## 渗滤器字段类型

"percolator"字段类型将 json 结构解析为本机查询并存储该查询，以便 percolate 查询可以使用它来匹配提供的文档。

任何包含 json 对象的字段都可以配置为渗滤器字段。渗滤器字段类型没有设置。只需配置"渗滤器"字段类型就足以指示 Elasticsearch 将字段视为查询。

如果以下映射为"查询"字段配置了"渗滤器"字段类型：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            query: {
              type: 'percolator'
            },
            field: {
              type: 'text'
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
          "query": {
            "type": "percolator"
          },
          "field": {
            "type": "text"
          }
        }
      }
    }

然后，您可以为查询编制索引：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 'match_value',
      body: {
        query: {
          match: {
            field: 'value'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/match_value
    {
      "query": {
        "match": {
          "field": "value"
        }
      }
    }

渗滤器查询中引用的字段必须**已**存在于与用于渗滤的索引关联的映射中。为了确保这些字段存在，请通过创建索引或更新映射 API 添加或更新映射。

#### 重新索引渗滤器查询

有时需要重新索引渗滤器查询，以便从新版本中对"渗滤器"字段类型的改进中受益。

可以使用重新索引 api 重新索引渗滤器查询。让我们看一下以下具有渗滤器字段类型的索引：

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        mappings: {
          properties: {
            query: {
              type: 'percolator'
            },
            body: {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            add: {
              index: 'index',
              alias: 'queries'
            }
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'queries',
      id: 1,
      refresh: true,
      body: {
        query: {
          match: {
            body: 'quick brown fox'
          }
        }
      }
    )
    puts response
    
    
    PUT index
    {
      "mappings": {
        "properties": {
          "query" : {
            "type" : "percolator"
          },
          "body" : {
            "type": "text"
          }
        }
      }
    }
    
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "index",
            "alias": "queries" __}
        }
      ]
    }
    
    PUT queries/_doc/1?refresh
    {
      "query" : {
        "match" : {
          "body" : "quick brown fox"
        }
      }
    }

__

|

始终建议为索引定义别名，以便在重新索引系统/应用程序的情况下不需要更改即可知道渗滤器查询现在位于不同的索引中。   ---|--- 假设你要升级到一个新的主要版本，为了让新的Elasticsearch版本仍然能够读取你的查询，你需要将你的查询重新索引到当前Elasticsearch版本的新索引中：

    
    
    response = client.indices.create(
      index: 'new_index',
      body: {
        mappings: {
          properties: {
            query: {
              type: 'percolator'
            },
            body: {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    response = client.reindex(
      refresh: true,
      body: {
        source: {
          index: 'index'
        },
        dest: {
          index: 'new_index'
        }
      }
    )
    puts response
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            remove: {
              index: 'index',
              alias: 'queries'
            }
          },
          {
            add: {
              index: 'new_index',
              alias: 'queries'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT new_index
    {
      "mappings": {
        "properties": {
          "query" : {
            "type" : "percolator"
          },
          "body" : {
            "type": "text"
          }
        }
      }
    }
    
    POST /_reindex?refresh
    {
      "source": {
        "index": "index"
      },
      "dest": {
        "index": "new_index"
      }
    }
    
    POST _aliases
    {
      "actions": [ __{
          "remove": {
            "index" : "index",
            "alias": "queries"
          }
        },
        {
          "add": {
            "index": "new_index",
            "alias": "queries"
          }
        }
      ]
    }

__

|

如果您有别名，请不要忘记将其指向新索引。   ---|--- 通过"query"别名执行"percolate"查询：

    
    
    response = client.search(
      index: 'queries',
      body: {
        query: {
          percolate: {
            field: 'query',
            document: {
              body: 'fox jumps over the lazy dog'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /queries/_search
    {
      "query": {
        "percolate" : {
          "field" : "query",
          "document" : {
            "body" : "fox jumps over the lazy dog"
          }
        }
      }
    }

现在从新索引返回匹配项：

    
    
    {
      "took": 3,
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
        "max_score": 0.13076457,
        "hits": [
          {
            "_index": "new_index", __"_id": "1",
            "_score": 0.13076457,
            "_source": {
              "query": {
                "match": {
                  "body": "quick brown fox"
                }
              }
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

渗滤器查询命中现在从新索引中呈现。   ---|--- #### 优化查询时间 文本分析编辑

当渗滤器验证渗滤器候选匹配时，它将解析，执行查询时文本分析，并实际对正在渗透的文档运行渗滤器查询。这是针对每个候选匹配项以及每次执行"percolate"查询时完成的。如果查询时间文本分析是查询解析中相对昂贵的部分，则文本分析可能成为渗透时花费时间的主要因素。当渗滤器最终验证许多候选渗滤器查询匹配项时，此查询分析开销可能会变得明显。

避免在渗透时文本分析中最昂贵的部分。在索引渗滤器查询时，可以选择执行文本分析的昂贵部分。这需要使用两个不同的分析器。第一个分析器实际上执行需要执行的文本分析(昂贵的部分)。第二个分析器(通常是空格)只是拆分第一个分析器生成的生成令牌。然后，在索引渗滤器查询之前，应使用分析api来使用更昂贵的分析器分析查询文本。应使用分析 API 的结果(令牌)替换渗滤器查询中的原始查询文本。重要的是，现在应将查询配置为从映射中覆盖分析器，并且仅覆盖第二个分析器。大多数基于文本的查询都支持"分析器"选项("匹配"、"query_string"、"simple_query_string")。使用这种方法，昂贵的文本分析执行一次而不是多次。

让我们通过一个简化的示例来演示此工作流。

假设我们要索引以下渗滤器查询：

    
    
    {
      "query" : {
        "match" : {
          "body" : {
            "query" : "missing bicycles"
          }
        }
      }
    }

使用这些设置和映射：

    
    
    response = client.indices.create(
      index: 'test_index',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'porter_stem'
                ]
              }
            }
          }
        },
        mappings: {
          properties: {
            query: {
              type: 'percolator'
            },
            body: {
              type: 'text',
              analyzer: 'my_analyzer'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /test_index
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer" : {
              "tokenizer": "standard",
              "filter" : ["lowercase", "porter_stem"]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "query" : {
            "type": "percolator"
          },
          "body" : {
            "type": "text",
            "analyzer": "my_analyzer" __}
        }
      }
    }

__

|

就此示例而言，此分析器被认为是昂贵的。   ---|--- 首先，我们需要在编制索引之前使用 analyze API 执行文本分析：

    
    
    response = client.indices.analyze(
      index: 'test_index',
      body: {
        analyzer: 'my_analyzer',
        text: 'missing bicycles'
      }
    )
    puts response
    
    
    POST /test_index/_analyze
    {
      "analyzer" : "my_analyzer",
      "text" : "missing bicycles"
    }

这将产生以下响应：

    
    
    {
      "tokens": [
        {
          "token": "miss",
          "start_offset": 0,
          "end_offset": 7,
          "type": "<ALPHANUM>",
          "position": 0
        },
        {
          "token": "bicycl",
          "start_offset": 8,
          "end_offset": 16,
          "type": "<ALPHANUM>",
          "position": 1
        }
      ]
    }

返回顺序中的所有标记都需要替换渗滤器查询中的查询文本：

    
    
    response = client.index(
      index: 'test_index',
      id: 1,
      refresh: true,
      body: {
        query: {
          match: {
            body: {
              query: 'miss bicycl',
              analyzer: 'whitespace'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /test_index/_doc/1?refresh
    {
      "query" : {
        "match" : {
          "body" : {
            "query" : "miss bicycl",
            "analyzer" : "whitespace" __}
        }
      }
    }

__

|

在此处选择空格分析器很重要，否则将使用映射中定义的分析器，这违背了使用此工作流的意义。请注意，"whitespace"是一个内置的分析器，如果需要使用不同的分析器，则需要首先在索引的设置中配置它。   ---|--- 在索引渗滤器流之前，应为每个渗滤器查询执行分析 api。

在渗透时没有任何变化，可以正常定义"percolate"查询：

    
    
    response = client.search(
      index: 'test_index',
      body: {
        query: {
          percolate: {
            field: 'query',
            document: {
              body: 'Bycicles are missing'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /test_index/_search
    {
      "query": {
        "percolate" : {
          "field" : "query",
          "document" : {
            "body" : "Bycicles are missing"
          }
        }
      }
    }

这会导致如下响应：

    
    
    {
      "took": 6,
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
        "max_score": 0.13076457,
        "hits": [
          {
            "_index": "test_index",
            "_id": "1",
            "_score": 0.13076457,
            "_source": {
              "query": {
                "match": {
                  "body": {
                    "query": "miss bicycl",
                    "analyzer": "whitespace"
                  }
                }
              }
            },
            "fields" : {
              "_percolator_document_slot" : [0]
            }
          }
        ]
      }
    }

#### 优化通配符查询。

通配符查询比渗滤器的其他查询更昂贵，尤其是在通配符表达式很大的情况下。

对于带有前缀通配符表达式的"通配符"查询或仅使用"前缀"查询，可以使用"edge_ngram"标记筛选器将这些查询替换为配置了"edge_ngram"标记筛选器的字段上的常规"term"查询。

使用自定义分析设置创建索引：

    
    
    response = client.indices.create(
      index: 'my_queries1',
      body: {
        settings: {
          analysis: {
            analyzer: {
              wildcard_prefix: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'wildcard_edge_ngram'
                ]
              }
            },
            filter: {
              wildcard_edge_ngram: {
                type: 'edge_ngram',
                min_gram: 1,
                max_gram: 32
              }
            }
          }
        },
        mappings: {
          properties: {
            query: {
              type: 'percolator'
            },
            my_field: {
              type: 'text',
              fields: {
                prefix: {
                  type: 'text',
                  analyzer: 'wildcard_prefix',
                  search_analyzer: 'standard'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my_queries1
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "wildcard_prefix": { __"type": "custom",
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "wildcard_edge_ngram"
              ]
            }
          },
          "filter": {
            "wildcard_edge_ngram": { __"type": "edge_ngram",
              "min_gram": 1,
              "max_gram": 32
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "query": {
            "type": "percolator"
          },
          "my_field": {
            "type": "text",
            "fields": {
              "prefix": { __"type": "text",
                "analyzer": "wildcard_prefix",
                "search_analyzer": "standard"
              }
            }
          }
        }
      }
    }

__

|

生成仅在索引时使用的前缀标记的分析器。   ---|---    __

|

根据您的前缀搜索需求增加"min_gram"并减少"max_gram"设置。   __

|

此多字段应用于使用"术语"或"匹配"查询而不是"前缀"或"通配符"查询进行前缀搜索。   然后，而不是为以下查询编制索引：

    
    
    {
      "query": {
        "wildcard": {
          "my_field": "abc*"
        }
      }
    }

应为以下查询编制索引：

    
    
    response = client.index(
      index: 'my_queries1',
      id: 1,
      refresh: true,
      body: {
        query: {
          term: {
            "my_field.prefix": 'abc'
          }
        }
      }
    )
    puts response
    
    
    PUT /my_queries1/_doc/1?refresh
    {
      "query": {
        "term": {
          "my_field.prefix": "abc"
        }
      }
    }

这种方式可以比第一个查询更有效地处理第二个查询。

以下搜索请求将与之前索引的渗滤器查询匹配：

    
    
    response = client.search(
      index: 'my_queries1',
      body: {
        query: {
          percolate: {
            field: 'query',
            document: {
              my_field: 'abcd'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_queries1/_search
    {
      "query": {
        "percolate": {
          "field": "query",
          "document": {
            "my_field": "abcd"
          }
        }
      }
    }
    
    
    {
      "took": 6,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.18864399,
        "hits": [
          {
            "_index": "my_queries1",
            "_id": "1",
            "_score": 0.18864399,
            "_source": {
              "query": {
                "term": {
                  "my_field.prefix": "abc"
                }
              }
            },
            "fields": {
              "_percolator_document_slot": [
                0
              ]
            }
          }
        ]
      }
    }

相同的技术也可用于加快后缀通配符搜索的速度。在"edge_ngram"令牌筛选器之前使用"反向"令牌筛选器。

    
    
    response = client.indices.create(
      index: 'my_queries2',
      body: {
        settings: {
          analysis: {
            analyzer: {
              wildcard_suffix: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'reverse',
                  'wildcard_edge_ngram'
                ]
              },
              wildcard_suffix_search_time: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'reverse'
                ]
              }
            },
            filter: {
              wildcard_edge_ngram: {
                type: 'edge_ngram',
                min_gram: 1,
                max_gram: 32
              }
            }
          }
        },
        mappings: {
          properties: {
            query: {
              type: 'percolator'
            },
            my_field: {
              type: 'text',
              fields: {
                suffix: {
                  type: 'text',
                  analyzer: 'wildcard_suffix',
                  search_analyzer: 'wildcard_suffix_search_time'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my_queries2
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "wildcard_suffix": {
              "type": "custom",
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "reverse",
                "wildcard_edge_ngram"
              ]
            },
            "wildcard_suffix_search_time": {
              "type": "custom",
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "reverse"
              ]
            }
          },
          "filter": {
            "wildcard_edge_ngram": {
              "type": "edge_ngram",
              "min_gram": 1,
              "max_gram": 32
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "query": {
            "type": "percolator"
          },
          "my_field": {
            "type": "text",
            "fields": {
              "suffix": {
                "type": "text",
                "analyzer": "wildcard_suffix",
                "search_analyzer": "wildcard_suffix_search_time" __}
            }
          }
        }
      }
    }

__

|

搜索时也需要自定义分析器，否则查询词不会被反转，否则不会与保留的后缀标记匹配。   ---|--- 然后，而不是索引以下查询：

    
    
    {
      "query": {
        "wildcard": {
          "my_field": "*xyz"
        }
      }
    }

应为以下查询编制索引：

    
    
    response = client.index(
      index: 'my_queries2',
      id: 2,
      refresh: true,
      body: {
        query: {
          match: {
            "my_field.suffix": 'xyz'
          }
        }
      }
    )
    puts response
    
    
    PUT /my_queries2/_doc/2?refresh
    {
      "query": {
        "match": { __"my_field.suffix": "xyz"
        }
      }
    }

__

|

应使用"匹配"查询而不是"term"查询，因为文本分析需要反转查询词。   ---|--- 以下搜索请求将与之前索引的渗滤器查询匹配：

    
    
    response = client.search(
      index: 'my_queries2',
      body: {
        query: {
          percolate: {
            field: 'query',
            document: {
              my_field: 'wxyz'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_queries2/_search
    {
      "query": {
        "percolate": {
          "field": "query",
          "document": {
            "my_field": "wxyz"
          }
        }
      }
    }

#### 专用渗滤器索引

渗透查询可以添加到任何索引。除了将这些查询添加到数据所在的索引中，还可以将这些查询添加到专用索引中。这样做的好处是，这个专用的渗滤器索引可以有自己的索引设置(例如主分片和副本分片的数量)。如果选择具有专用的渗透索引，则需要确保来自普通索引的映射在渗透索引上也可用。否则，可能会错误地分析渗透查询。

#### 强制将未映射的字段作为字符串处理

在某些情况下，不知道注册了哪种类型的渗滤器查询，如果按渗滤器查询引用的字段不存在字段映射，则添加渗滤器查询将失败。这意味着需要更新映射以具有适当设置的字段，然后可以添加渗滤器查询。但有时，如果所有未映射的字段都像处理默认文本字段一样处理就足够了。在这些情况下，可以将"index.percolator.map_unmapped_fields_as_text"设置配置为"true"(默认为"false")，然后如果 apercolator 查询中引用的字段不存在，它将作为默认文本字段进行处理，以便添加渗透器查询不会失败。

####Limitations

#####Parent/儿童

由于"percolate"查询一次处理一个文档，因此它不支持针对子文档(如"has_child"和"has_parent")运行的查询和筛选器。

##### 获取查询

有许多查询在查询解析期间通过 get 调用获取数据。例如，使用术语查找时的"术语"查询，使用索引脚本时的"模板"查询，使用预索引形状时的"geo_shape"。当这些查询按"渗滤器"字段类型索引时，get调用将执行一次。因此，每次"渗滤器"查询评估这些查询时，都会获取术语、形状等。因为索引时间将被使用。需要注意的重要一点是，每次在主分片和副本分片上索引渗滤器查询时，都会提取这些查询执行的术语，因此，如果源索引在索引时发生更改，则实际编制索引的术语可能会在分片副本之间有所不同。

##### 脚本查询

"脚本"查询中的脚本只能访问文档值字段。"percolate"查询将提供的文档索引为内存中索引。此内存索引不支持存储字段，因此不会存储"_source"字段和其他存储字段。这就是为什么在"脚本"查询中"_source"和其他存储字段不可用的原因。

##### 字段别名

包含字段别名的渗滤器查询可能并不总是按预期方式运行。特别是，如果注册了包含字段别名的渗滤器查询，然后在映射中更新该别名以引用其他字段，则存储的查询仍将引用原始目标字段。若要选取对字段别名的更改，必须显式重新索引渗透器查询。

[« Object field type](object.md) [Point field type »](point.md)
