

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Joining queries](joining-queries.md)

[« Joining queries](joining-queries.md) [Has child query »](query-dsl-has-
child-query.md)

## 嵌套查询

包装另一个查询以搜索嵌套字段。

"嵌套"查询搜索嵌套字段对象，就好像它们被索引为单独的文档一样。如果对象与搜索匹配，则"嵌套"查询返回根父文档。

### 示例请求

#### 索引设置

若要使用"嵌套"查询，索引必须包含嵌套字段映射。例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            "obj1": {
              type: 'nested'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "obj1": {
    	        "type": "nested"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001
    {
      "mappings": {
        "properties": {
          "obj1": {
            "type": "nested"
          }
        }
      }
    }

#### 示例查询

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          nested: {
            path: 'obj1',
            query: {
              bool: {
                must: [
                  {
                    match: {
                      "obj1.name": 'blue'
                    }
                  },
                  {
                    range: {
                      "obj1.count": {
                        gt: 5
                      }
                    }
                  }
                ]
              }
            },
            score_mode: 'avg'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("my-index-000001"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "nested": {
    	      "path": "obj1",
    	      "query": {
    	        "bool": {
    	          "must": [
    	            {
    	              "match": {
    	                "obj1.name": "blue"
    	              }
    	            },
    	            {
    	              "range": {
    	                "obj1.count": {
    	                  "gt": 5
    	                }
    	              }
    	            }
    	          ]
    	        }
    	      },
    	      "score_mode": "avg"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /my-index-000001/_search
    {
      "query": {
        "nested": {
          "path": "obj1",
          "query": {
            "bool": {
              "must": [
                { "match": { "obj1.name": "blue" } },
                { "range": { "obj1.count": { "gt": 5 } } }
              ]
            }
          },
          "score_mode": "avg"
        }
      }
    }

### "嵌套"的顶级参数

`path`

     (Required, string) Path to the nested object you wish to search. 
`query`

    

(必需，查询对象)您希望在"路径"中的嵌套对象上运行的查询。如果对象与搜索匹配，则"嵌套"查询返回根父文档。

您可以使用包含完整路径的点表示法(如"obj1.name")搜索嵌套字段。

自动支持并检测多级嵌套，导致内部嵌套查询自动匹配相关的嵌套级别，而不是根(如果它存在于另一个嵌套查询中)。

有关示例，请参阅多级嵌套查询。

`score_mode`

    

(可选，字符串)指示匹配子对象的分数如何影响根父文档的相关性分数。有效值为：

"平均"(默认)

     Use the mean relevance score of all matching child objects. 
`max`

     Uses the highest relevance score of all matching child objects. 
`min`

     Uses the lowest relevance score of all matching child objects. 
`none`

     Do not use the relevance scores of matching child objects. The query assigns parent documents a score of `0`. 
`sum`

     Add together the relevance scores of all matching child objects. 

`ignore_unmapped`

    

(可选，布尔值)指示是否忽略未映射的"路径"并且不返回任何文档而不是错误。默认为"假"。

如果为"false"，则当"path"是未映射的字段时，Elasticsearch 将返回错误。

您可以使用此参数查询可能不包含字段"path"的多个索引。

###Notes

#### 脚本查询的上下文

如果在嵌套查询中运行"脚本"查询，则只能访问嵌套文档中的文档值，而不能访问父文档或根文档。

#### 多级嵌套查询

若要查看多级嵌套查询的工作原理，首先需要一个包含字段的索引。以下请求使用嵌套的"make"和"model"字段定义"驱动程序"索引的映射。

    
    
    response = client.indices.create(
      index: 'drivers',
      body: {
        mappings: {
          properties: {
            driver: {
              type: 'nested',
              properties: {
                last_name: {
                  type: 'text'
                },
                vehicle: {
                  type: 'nested',
                  properties: {
                    make: {
                      type: 'text'
                    },
                    model: {
                      type: 'text'
                    }
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"drivers",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "driver": {
    	        "type": "nested",
    	        "properties": {
    	          "last_name": {
    	            "type": "text"
    	          },
    	          "vehicle": {
    	            "type": "nested",
    	            "properties": {
    	              "make": {
    	                "type": "text"
    	              },
    	              "model": {
    	                "type": "text"
    	              }
    	            }
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /drivers
    {
      "mappings": {
        "properties": {
          "driver": {
            "type": "nested",
            "properties": {
              "last_name": {
                "type": "text"
              },
              "vehicle": {
                "type": "nested",
                "properties": {
                  "make": {
                    "type": "text"
                  },
                  "model": {
                    "type": "text"
                  }
                }
              }
            }
          }
        }
      }
    }

接下来，将一些文档索引到"驱动程序"索引。

    
    
    $params = [
        'index' => 'drivers',
        'id' => '1',
        'body' => [
            'driver' => [
                'last_name' => 'McQueen',
                'vehicle' => [
                    [
                        'make' => 'Powell Motors',
                        'model' => 'Canyonero',
                    ],
                    [
                        'make' => 'Miller-Meteor',
                        'model' => 'Ecto-1',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->index($params);
    $params = [
        'index' => 'drivers',
        'id' => '2',
        'body' => [
            'driver' => [
                'last_name' => 'Hudson',
                'vehicle' => [
                    [
                        'make' => 'Mifune',
                        'model' => 'Mach Five',
                    ],
                    [
                        'make' => 'Miller-Meteor',
                        'model' => 'Ecto-1',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->index($params);
    
    
    resp = client.index(
        index="drivers",
        id="1",
        body={
            "driver": {
                "last_name": "McQueen",
                "vehicle": [
                    {"make": "Powell Motors", "model": "Canyonero"},
                    {"make": "Miller-Meteor", "model": "Ecto-1"},
                ],
            }
        },
    )
    print(resp)
    
    resp = client.index(
        index="drivers",
        id="2",
        refresh=True,
        body={
            "driver": {
                "last_name": "Hudson",
                "vehicle": [
                    {"make": "Mifune", "model": "Mach Five"},
                    {"make": "Miller-Meteor", "model": "Ecto-1"},
                ],
            }
        },
    )
    print(resp)
    
    
    response = client.index(
      index: 'drivers',
      id: 1,
      body: {
        driver: {
          last_name: 'McQueen',
          vehicle: [
            {
              make: 'Powell Motors',
              model: 'Canyonero'
            },
            {
              make: 'Miller-Meteor',
              model: 'Ecto-1'
            }
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'drivers',
      id: 2,
      refresh: true,
      body: {
        driver: {
          last_name: 'Hudson',
          vehicle: [
            {
              make: 'Mifune',
              model: 'Mach Five'
            },
            {
              make: 'Miller-Meteor',
              model: 'Ecto-1'
            }
          ]
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Index(
    		"drivers",
    		strings.NewReader(`{
    	  "driver": {
    	    "last_name": "McQueen",
    	    "vehicle": [
    	      {
    	        "make": "Powell Motors",
    	        "model": "Canyonero"
    	      },
    	      {
    	        "make": "Miller-Meteor",
    	        "model": "Ecto-1"
    	      }
    	    ]
    	  }
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"drivers",
    		strings.NewReader(`{
    	  "driver": {
    	    "last_name": "Hudson",
    	    "vehicle": [
    	      {
    	        "make": "Mifune",
    	        "model": "Mach Five"
    	      },
    	      {
    	        "make": "Miller-Meteor",
    	        "model": "Ecto-1"
    	      }
    	    ]
    	  }
    	}`),
    		es.Index.WithDocumentID("2"),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    const response0 = await client.index({
      index: 'drivers',
      id: '1',
      body: {
        driver: {
          last_name: 'McQueen',
          vehicle: [
            {
              make: 'Powell Motors',
              model: 'Canyonero'
            },
            {
              make: 'Miller-Meteor',
              model: 'Ecto-1'
            }
          ]
        }
      }
    })
    console.log(response0)
    
    const response1 = await client.index({
      index: 'drivers',
      id: '2',
      refresh: true,
      body: {
        driver: {
          last_name: 'Hudson',
          vehicle: [
            {
              make: 'Mifune',
              model: 'Mach Five'
            },
            {
              make: 'Miller-Meteor',
              model: 'Ecto-1'
            }
          ]
        }
      }
    })
    console.log(response1)
    
    
    PUT /drivers/_doc/1
    {
      "driver" : {
            "last_name" : "McQueen",
            "vehicle" : [
                {
                    "make" : "Powell Motors",
                    "model" : "Canyonero"
                },
                {
                    "make" : "Miller-Meteor",
                    "model" : "Ecto-1"
                }
            ]
        }
    }
    
    PUT /drivers/_doc/2?refresh
    {
      "driver" : {
            "last_name" : "Hudson",
            "vehicle" : [
                {
                    "make" : "Mifune",
                    "model" : "Mach Five"
                },
                {
                    "make" : "Miller-Meteor",
                    "model" : "Ecto-1"
                }
            ]
        }
    }

现在，您可以使用多级嵌套查询根据"make"和"model"字段匹配文档。

    
    
    response = client.search(
      index: 'drivers',
      body: {
        query: {
          nested: {
            path: 'driver',
            query: {
              nested: {
                path: 'driver.vehicle',
                query: {
                  bool: {
                    must: [
                      {
                        match: {
                          "driver.vehicle.make": 'Powell Motors'
                        }
                      },
                      {
                        match: {
                          "driver.vehicle.model": 'Canyonero'
                        }
                      }
                    ]
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("drivers"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "nested": {
    	      "path": "driver",
    	      "query": {
    	        "nested": {
    	          "path": "driver.vehicle",
    	          "query": {
    	            "bool": {
    	              "must": [
    	                {
    	                  "match": {
    	                    "driver.vehicle.make": "Powell Motors"
    	                  }
    	                },
    	                {
    	                  "match": {
    	                    "driver.vehicle.model": "Canyonero"
    	                  }
    	                }
    	              ]
    	            }
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /drivers/_search
    {
      "query": {
        "nested": {
          "path": "driver",
          "query": {
            "nested": {
              "path": "driver.vehicle",
              "query": {
                "bool": {
                  "must": [
                    { "match": { "driver.vehicle.make": "Powell Motors" } },
                    { "match": { "driver.vehicle.model": "Canyonero" } }
                  ]
                }
              }
            }
          }
        }
      }
    }

搜索请求返回以下响应：

    
    
    {
      "took" : 5,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 3.7349272,
        "hits" : [
          {
            "_index" : "drivers",
            "_id" : "1",
            "_score" : 3.7349272,
            "_source" : {
              "driver" : {
                "last_name" : "McQueen",
                "vehicle" : [
                  {
                    "make" : "Powell Motors",
                    "model" : "Canyonero"
                  },
                  {
                    "make" : "Miller-Meteor",
                    "model" : "Ecto-1"
                  }
                ]
              }
            }
          }
        ]
      }
    }

#### 'must_not' 子句和 'nested'query

如果"嵌套"查询与文档中的一个或多个嵌套对象匹配，它将文档作为命中返回。即使文档中的其他嵌套对象与查询不匹配，这也适用。使用包含内部"must_not"子句的"嵌套"查询时，请记住这一点。

使用"inner_hits"参数查看哪些嵌套对象与"嵌套"查询匹配。

例如，以下搜索使用带有内部"must_not"子句的外部"嵌套"查询。

    
    
    response = client.indices.create(
      index: 'my-index',
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
      index: 'my-index',
      id: 1,
      refresh: true,
      body: {
        comments: [
          {
            author: 'kimchy'
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index',
      id: 2,
      refresh: true,
      body: {
        comments: [
          {
            author: 'kimchy'
          },
          {
            author: 'nik9000'
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index',
      id: 3,
      refresh: true,
      body: {
        comments: [
          {
            author: 'nik9000'
          }
        ]
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index',
      body: {
        query: {
          nested: {
            path: 'comments',
            query: {
              bool: {
                must_not: [
                  {
                    term: {
                      "comments.author": 'nik9000'
                    }
                  }
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index
    {
      "mappings": {
        "properties": {
          "comments": {
            "type": "nested"
          }
        }
      }
    }
    
    PUT my-index/_doc/1?refresh
    {
      "comments": [
        {
          "author": "kimchy"
        }
      ]
    }
    
    PUT my-index/_doc/2?refresh
    {
      "comments": [
        {
          "author": "kimchy"
        },
        {
          "author": "nik9000"
        }
      ]
    }
    
    PUT my-index/_doc/3?refresh
    {
      "comments": [
        {
          "author": "nik9000"
        }
      ]
    }
    
    POST my-index/_search
    {
      "query": {
        "nested": {
          "path": "comments",
          "query": {
            "bool": {
              "must_not": [
                {
                  "term": {
                    "comments.author": "nik9000"
                  }
                }
              ]
            }
          }
        }
      }
    }

搜索返回：

    
    
    {
      ...
      "hits" : {
        ...
        "hits" : [
          {
            "_index" : "my-index",
            "_id" : "1",
            "_score" : 0.0,
            "_source" : {
              "comments" : [
                {
                  "author" : "kimchy"
                }
              ]
            }
          },
          {
            "_index" : "my-index",
            "_id" : "2",
            "_score" : 0.0,
            "_source" : {
              "comments" : [
                {
                  "author" : "kimchy"              __},
                {
                  "author" : "nik9000" __}
              ]
            }
          }
        ]
      }
    }

__

|

此嵌套对象与查询匹配。因此，搜索将返回对象的父文档作为命中。   ---|---    __

|

此嵌套对象与查询不匹配。由于同一文档中的另一个嵌套对象确实与查询匹配，因此搜索仍会返回父文档作为命中符。   若要排除具有与"嵌套"查询匹配的任何嵌套对象的文档，请使用外部"must_not"子句。

    
    
    response = client.search(
      index: 'my-index',
      body: {
        query: {
          bool: {
            must_not: [
              {
                nested: {
                  path: 'comments',
                  query: {
                    term: {
                      "comments.author": 'nik9000'
                    }
                  }
                }
              }
            ]
          }
        }
      }
    )
    puts response
    
    
    POST my-index/_search
    {
      "query": {
        "bool": {
          "must_not": [
            {
              "nested": {
                "path": "comments",
                "query": {
                  "term": {
                    "comments.author": "nik9000"
                  }
                }
              }
            }
          ]
        }
      }
    }

搜索返回：

    
    
    {
      ...
      "hits" : {
        ...
        "hits" : [
          {
            "_index" : "my-index",
            "_id" : "1",
            "_score" : 0.0,
            "_source" : {
              "comments" : [
                {
                  "author" : "kimchy"
                }
              ]
            }
          }
        ]
      }
    }

[« Joining queries](joining-queries.md) [Has child query »](query-dsl-has-
child-query.md)
