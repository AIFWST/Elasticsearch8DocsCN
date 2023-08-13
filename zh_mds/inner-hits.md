

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Paginate search results](paginate-search-results.md) [Retrieve selected
fields from a search »](search-fields.md)

## 检索内部命中

父联接和嵌套功能允许返回在不同作用域中具有匹配项的文档。在父/子情况下，基于子文档中的匹配项返回父文档，或基于父文档中的匹配项返回子文档。在嵌套情况下，根据嵌套内部对象的匹配项返回文档。

在这两种情况下，导致返回文档的不同范围中的实际匹配项都将被隐藏。在许多情况下，了解哪些内部嵌套对象(在嵌套的情况下)或子/父文档(在父/子文档的情况下)导致返回某些信息非常有用。内部命中功能可用于此目的。此功能返回搜索响应中导致搜索命中在不同范围内匹配的附加嵌套命中。

可以通过在"嵌套"、"has_child"或"has_parent"查询和筛选器上定义"inner_hits"定义来使用内部命中。结构如下所示：

    
    
    "<query>" : {
        "inner_hits" : {
            <inner_hits_options>
        }
    }

如果在支持它的查询上定义了"inner_hits"，则每个搜索命中将包含一个具有以下结构的"inner_hits"json 对象：

    
    
    "hits": [
         {
            "_index": ...,
            "_type": ...,
            "_id": ...,
            "inner_hits": {
               "<inner_hits_name>": {
                  "hits": {
                     "total": ...,
                     "hits": [
                        {
                           "_id": ...,
                           ...
                        },
                        ...
                     ]
                  }
               }
            },
            ...
         },
         ...
    ]

###Options

内部命中支持以下选项：

`from`

|

与每个"inner_hits"中要获取的第一个命中的位置的偏移量变为常规搜索命中。   ---|---"大小"

|

每个"inner_hits"返回的最大命中数。默认情况下，将返回前三名匹配命中。   "排序"

|

内部命中应如何按"inner_hits"排序。默认情况下，命中按分数排序。   "名称"

|

要用于响应中特定内部命中定义的名称。在单个搜索请求中定义了多个内部命中时很有用。默认值取决于在哪个查询中定义内部命中。对于"has_child"查询和筛选，这是子类型，"has_parent"查询和筛选是父类型，嵌套查询和筛选器这是嵌套路径。   内部点击还支持以下每个文档的功能：

* 突出显示 * 解释 * 搜索字段 * 源过滤 * 脚本字段 * 文档值字段 * 包括版本 * 包括序列号和主要术语

### 嵌套内部命中

嵌套的"inner_hits"可用于将嵌套的内部对象作为搜索命中的内部对象包含在内。

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        mappings: {
          properties: {
            comments: {
              type: 'nested'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'test',
      id: 1,
      refresh: true,
      body: {
        title: 'Test title',
        comments: [
          {
            author: 'kimchy',
            number: 1
          },
          {
            author: 'nik9000',
            number: 2
          }
        ]
      }
    )
    puts response
    
    response = client.search(
      index: 'test',
      body: {
        query: {
          nested: {
            path: 'comments',
            query: {
              match: {
                "comments.number": 2
              }
            },
            inner_hits: {}
          }
        }
      }
    )
    puts response
    
    
    PUT test
    {
      "mappings": {
        "properties": {
          "comments": {
            "type": "nested"
          }
        }
      }
    }
    
    PUT test/_doc/1?refresh
    {
      "title": "Test title",
      "comments": [
        {
          "author": "kimchy",
          "number": 1
        },
        {
          "author": "nik9000",
          "number": 2
        }
      ]
    }
    
    POST test/_search
    {
      "query": {
        "nested": {
          "path": "comments",
          "query": {
            "match": {"comments.number" : 2}
          },
          "inner_hits": {} __}
      }
    }

__

|

嵌套查询中的内部命中定义。无需定义其他选项。   ---|--- 可以从上述搜索请求生成的响应代码段示例：

    
    
    {
      ...,
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
          {
            "_index": "test",
            "_id": "1",
            "_score": 1.0,
            "_source": ...,
            "inner_hits": {
              "comments": { __"hits": {
                  "total" : {
                      "value": 1,
                      "relation": "eq"
                  },
                  "max_score": 1.0,
                  "hits": [
                    {
                      "_index": "test",
                      "_id": "1",
                      "_nested": {
                        "field": "comments",
                        "offset": 1
                      },
                      "_score": 1.0,
                      "_source": {
                        "author": "nik9000",
                        "number": 2
                      }
                    }
                  ]
                }
              }
            }
          }
        ]
      }
    }

__

|

搜索请求中的内部命中定义中使用的名称。自定义密钥可以通过"名称"选项使用。   ---|--- 在上面的示例中，"_nested"元数据至关重要，因为它定义了此内部命中来自哪个内部嵌套对象。"字段"定义嵌套命中来自的对象数组字段，以及相对于其在"_source"中的位置的"偏移量"。由于排序和评分，命中对象在"inner_hits"中的实际位置通常与嵌套内部对象定义的位置不同。

默认情况下，对于"inner_hits"中的命中对象，也会返回"_source"，但可以更改。通过"_source"过滤功能，可以返回或禁用源的一部分。如果存储的字段是在当时的级别上定义的，则也可以通过"字段"功能返回这些字段。

一个重要的默认值是，在"inner_hits"内部的命中返回的"_source"相对于"_nested"元数据。因此，在上面的示例中，每个嵌套命中仅返回注释部分，而不是包含注释的顶级文档的整个源。

#### 嵌套的内部命中和"_source"

嵌套文档没有"_source"字段，因为整个文档源与根文档一起存储在其"_source"字段下。要仅包含嵌套文档的源，将解析根文档的源，并且仅将嵌套文档的相关位作为源包含在内部命中。对每个匹配的嵌套文档执行此操作会影响执行整个搜索请求所需的时间，尤其是当"size"和内部命中项的"size"设置为高于默认值时。为了避免嵌套内部命中相对昂贵的源提取，可以禁用包含源并仅依赖文档值字段。喜欢这个：

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        mappings: {
          properties: {
            comments: {
              type: 'nested'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'test',
      id: 1,
      refresh: true,
      body: {
        title: 'Test title',
        comments: [
          {
            author: 'kimchy',
            text: 'comment text'
          },
          {
            author: 'nik9000',
            text: 'words words words'
          }
        ]
      }
    )
    puts response
    
    response = client.search(
      index: 'test',
      body: {
        query: {
          nested: {
            path: 'comments',
            query: {
              match: {
                "comments.text": 'words'
              }
            },
            inner_hits: {
              _source: false,
              docvalue_fields: [
                'comments.text.keyword'
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    PUT test
    {
      "mappings": {
        "properties": {
          "comments": {
            "type": "nested"
          }
        }
      }
    }
    
    PUT test/_doc/1?refresh
    {
      "title": "Test title",
      "comments": [
        {
          "author": "kimchy",
          "text": "comment text"
        },
        {
          "author": "nik9000",
          "text": "words words words"
        }
      ]
    }
    
    POST test/_search
    {
      "query": {
        "nested": {
          "path": "comments",
          "query": {
            "match": {"comments.text" : "words"}
          },
          "inner_hits": {
            "_source" : false,
            "docvalue_fields" : [
              "comments.text.keyword"
            ]
          }
        }
      }
    }

### 嵌套对象字段和内部内容的分层级别。

如果映射具有多个级别的分层嵌套对象字段，则可以通过点注释路径访问每个级别。例如，如果有一个包含"votes"嵌套字段的"注释"嵌套字段，并且投票应该直接返回根命中，则可以定义以下路径：

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        mappings: {
          properties: {
            comments: {
              type: 'nested',
              properties: {
                votes: {
                  type: 'nested'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'test',
      id: 1,
      refresh: true,
      body: {
        title: 'Test title',
        comments: [
          {
            author: 'kimchy',
            text: 'comment text',
            votes: []
          },
          {
            author: 'nik9000',
            text: 'words words words',
            votes: [
              {
                value: 1,
                voter: 'kimchy'
              },
              {
                value: -1,
                voter: 'other'
              }
            ]
          }
        ]
      }
    )
    puts response
    
    response = client.search(
      index: 'test',
      body: {
        query: {
          nested: {
            path: 'comments.votes',
            query: {
              match: {
                "comments.votes.voter": 'kimchy'
              }
            },
            inner_hits: {}
          }
        }
      }
    )
    puts response
    
    
    PUT test
    {
      "mappings": {
        "properties": {
          "comments": {
            "type": "nested",
            "properties": {
              "votes": {
                "type": "nested"
              }
            }
          }
        }
      }
    }
    
    PUT test/_doc/1?refresh
    {
      "title": "Test title",
      "comments": [
        {
          "author": "kimchy",
          "text": "comment text",
          "votes": []
        },
        {
          "author": "nik9000",
          "text": "words words words",
          "votes": [
            {"value": 1 , "voter": "kimchy"},
            {"value": -1, "voter": "other"}
          ]
        }
      ]
    }
    
    POST test/_search
    {
      "query": {
        "nested": {
          "path": "comments.votes",
            "query": {
              "match": {
                "comments.votes.voter": "kimchy"
              }
            },
            "inner_hits" : {}
        }
      }
    }

看起来像：

    
    
    {
      ...,
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.6931471,
        "hits": [
          {
            "_index": "test",
            "_id": "1",
            "_score": 0.6931471,
            "_source": ...,
            "inner_hits": {
              "comments.votes": { __"hits": {
                  "total" : {
                      "value": 1,
                      "relation": "eq"
                  },
                  "max_score": 0.6931471,
                  "hits": [
                    {
                      "_index": "test",
                      "_id": "1",
                      "_nested": {
                        "field": "comments",
                        "offset": 1,
                        "_nested": {
                          "field": "votes",
                          "offset": 0
                        }
                      },
                      "_score": 0.6931471,
                      "_source": {
                        "value": 1,
                        "voter": "kimchy"
                      }
                    }
                  ]
                }
              }
            }
          }
        ]
      }
    }

此间接引用仅支持嵌套内部命中。

### 父/子内部命中

父/子"inner_hits"可用于包含父项或子项：

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        mappings: {
          properties: {
            my_join_field: {
              type: 'join',
              relations: {
                my_parent: 'my_child'
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'test',
      id: 1,
      refresh: true,
      body: {
        number: 1,
        my_join_field: 'my_parent'
      }
    )
    puts response
    
    response = client.index(
      index: 'test',
      id: 2,
      routing: 1,
      refresh: true,
      body: {
        number: 1,
        my_join_field: {
          name: 'my_child',
          parent: '1'
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'test',
      body: {
        query: {
          has_child: {
            type: 'my_child',
            query: {
              match: {
                number: 1
              }
            },
            inner_hits: {}
          }
        }
      }
    )
    puts response
    
    
    PUT test
    {
      "mappings": {
        "properties": {
          "my_join_field": {
            "type": "join",
            "relations": {
              "my_parent": "my_child"
            }
          }
        }
      }
    }
    
    PUT test/_doc/1?refresh
    {
      "number": 1,
      "my_join_field": "my_parent"
    }
    
    PUT test/_doc/2?routing=1&refresh
    {
      "number": 1,
      "my_join_field": {
        "name": "my_child",
        "parent": "1"
      }
    }
    
    POST test/_search
    {
      "query": {
        "has_child": {
          "type": "my_child",
          "query": {
            "match": {
              "number": 1
            }
          },
          "inner_hits": {}    __}
      }
    }

__

|

内部命中定义，如嵌套示例中所示。   ---|--- 可以从上述搜索请求生成的响应代码段示例：

    
    
    {
      ...,
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
          {
            "_index": "test",
            "_id": "1",
            "_score": 1.0,
            "_source": {
              "number": 1,
              "my_join_field": "my_parent"
            },
            "inner_hits": {
              "my_child": {
                "hits": {
                  "total": {
                    "value": 1,
                    "relation": "eq"
                  },
                  "max_score": 1.0,
                  "hits": [
                    {
                      "_index": "test",
                      "_id": "2",
                      "_score": 1.0,
                      "_routing": "1",
                      "_source": {
                        "number": 1,
                        "my_join_field": {
                          "name": "my_child",
                          "parent": "1"
                        }
                      }
                    }
                  ]
                }
              }
            }
          }
        ]
      }
    }

[« Paginate search results](paginate-search-results.md) [Retrieve selected
fields from a search »](search-fields.md)
