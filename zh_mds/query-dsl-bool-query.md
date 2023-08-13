

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Compound queries](compound-queries.md)

[« Compound queries](compound-queries.md) [Boosting query »](query-dsl-
boosting-query.md)

## 布尔查询

匹配与其他查询的布尔组合匹配的文档的查询。bool query 映射到 Lucene 'BooleanQuery'。它是使用一个或多个布尔子句构建的，每个子句都有一个类型化实例。发生类型包括：

发生 |描述 ---|--- "必须"

|

子句(查询)必须出现在匹配文档中，并将影响分数。   "过滤器"

|

子句(查询)必须出现在匹配的文档中。但是，与"必须"不同的是，查询的分数将被忽略。筛选器子句在筛选器上下文中执行，这意味着将忽略评分，并考虑对子句进行缓存。   "应该"

|

子句(查询)应出现在匹配文档中。   "must_not"

|

子句(查询)不得出现在匹配文档中。子句在筛选器上下文中执行，这意味着将忽略评分，并将子句视为强制缓存。由于忽略了评分，因此返回所有文档的分数为"0"。   "bool"查询采用_more匹配是better_的方法，因此每个匹配的"必须"或"应该"子句的分数将相加，为每个文档提供最终的"_score"。

    
    
    response = client.search(
      body: {
        query: {
          bool: {
            must: {
              term: {
                "user.id": 'kimchy'
              }
            },
            filter: {
              term: {
                tags: 'production'
              }
            },
            must_not: {
              range: {
                age: {
                  gte: 10,
                  lte: 20
                }
              }
            },
            should: [
              {
                term: {
                  tags: 'env1'
                }
              },
              {
                term: {
                  tags: 'deployed'
                }
              }
            ],
            minimum_should_match: 1,
            boost: 1
          }
        }
      }
    )
    puts response
    
    
    POST _search
    {
      "query": {
        "bool" : {
          "must" : {
            "term" : { "user.id" : "kimchy" }
          },
          "filter": {
            "term" : { "tags" : "production" }
          },
          "must_not" : {
            "range" : {
              "age" : { "gte" : 10, "lte" : 20 }
            }
          },
          "should" : [
            { "term" : { "tags" : "env1" } },
            { "term" : { "tags" : "deployed" } }
          ],
          "minimum_should_match" : 1,
          "boost" : 1.0
        }
      }
    }

### 使用"minimum_should_match"

您可以使用"minimum_should_match"参数指定返回的文档_必须_匹配的"应该"子句的数量或百分比。

如果"bool"查询至少包含一个"should"子句，而不包含"must"或"filter"子句，则默认值为"1"。否则，默认值为"0"。

有关其他有效值，请参阅"minimum_should_match"参数。

### 使用"bool.filter"评分

在"filter"元素下指定的查询对评分没有影响 - 分数以"0"返回。分数仅受已指定的查询影响。例如，以下所有三个查询都返回"状态"字段包含术语"活动"的所有文档。

第一个查询为所有文档分配分数"0"，因为未指定评分查询：

    
    
    $params = [
        'body' => [
            'query' => [
                'bool' => [
                    'filter' => [
                        'term' => [
                            'status' => 'active',
                        ],
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={"query": {"bool": {"filter": {"term": {"status": "active"}}}}},
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          bool: {
            filter: {
              term: {
                status: 'active'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "bool": {
    	      "filter": {
    	        "term": {
    	          "status": "active"
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          bool: {
            filter: {
              term: {
                status: 'active'
              }
            }
          }
        }
      }
    })
    console.log(response)
    
    
    GET _search
    {
      "query": {
        "bool": {
          "filter": {
            "term": {
              "status": "active"
            }
          }
        }
      }
    }

此"bool"查询具有"match_all"查询，该查询为所有文档分配分数"1.0"。

    
    
    $params = [
        'body' => [
            'query' => [
                'bool' => [
                    'must' => [
                        'match_all' => [
                        ],
                    ],
                    'filter' => [
                        'term' => [
                            'status' => 'active',
                        ],
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "bool": {
                    "must": {"match_all": {}},
                    "filter": {"term": {"status": "active"}},
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              term: {
                status: 'active'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "bool": {
    	      "must": {
    	        "match_all": {}
    	      },
    	      "filter": {
    	        "term": {
    	          "status": "active"
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          bool: {
            must: {
              match_all: {}
            },
            filter: {
              term: {
                status: 'active'
              }
            }
          }
        }
      }
    })
    console.log(response)
    
    
    GET _search
    {
      "query": {
        "bool": {
          "must": {
            "match_all": {}
          },
          "filter": {
            "term": {
              "status": "active"
            }
          }
        }
      }
    }

此"constant_score"查询的行为方式与上面的第二个示例完全相同。"constant_score"查询为筛选器匹配的所有文档分配分数"1.0"。

    
    
    $params = [
        'body' => [
            'query' => [
                'constant_score' => [
                    'filter' => [
                        'term' => [
                            'status' => 'active',
                        ],
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "constant_score": {"filter": {"term": {"status": "active"}}}
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          constant_score: {
            filter: {
              term: {
                status: 'active'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "constant_score": {
    	      "filter": {
    	        "term": {
    	          "status": "active"
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          constant_score: {
            filter: {
              term: {
                status: 'active'
              }
            }
          }
        }
      }
    })
    console.log(response)
    
    
    GET _search
    {
      "query": {
        "constant_score": {
          "filter": {
            "term": {
              "status": "active"
            }
          }
        }
      }
    }

### 命名查询

每个查询在其顶级定义中接受"_name"。可以使用命名查询来跟踪哪些查询与返回的文档匹配。如果使用命名查询，则响应将包含每个匹配的"matched_queries"属性。

    
    
    response = client.search(
      body: {
        query: {
          bool: {
            should: [
              {
                match: {
                  "name.first": {
                    query: 'shay',
                    _name: 'first'
                  }
                }
              },
              {
                match: {
                  "name.last": {
                    query: 'banon',
                    _name: 'last'
                  }
                }
              }
            ],
            filter: {
              terms: {
                "name.last": [
                  'banon',
                  'kimchy'
                ],
                _name: 'test'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "bool": {
          "should": [
            { "match": { "name.first": { "query": "shay", "_name": "first" } } },
            { "match": { "name.last": { "query": "banon", "_name": "last" } } }
          ],
          "filter": {
            "terms": {
              "name.last": [ "banon", "kimchy" ],
              "_name": "test"
            }
          }
        }
      }
    }

名为"include_named_queries_score"的请求参数控制是否返回与匹配查询关联的分数。设置后，响应包括一个"matched_queries"映射，其中包含作为键匹配的查询的名称及其关联的分数作为值。

请注意，分数可能不对文档的最终分数产生影响，例如，出现在筛选器或must_notcontexts中的命名查询，或者出现在忽略或修改分数(如"constant_score"或"function_score_query")的子句中。

    
    
    response = client.search(
      include_named_queries_score: true,
      body: {
        query: {
          bool: {
            should: [
              {
                match: {
                  "name.first": {
                    query: 'shay',
                    _name: 'first'
                  }
                }
              },
              {
                match: {
                  "name.last": {
                    query: 'banon',
                    _name: 'last'
                  }
                }
              }
            ],
            filter: {
              terms: {
                "name.last": [
                  'banon',
                  'kimchy'
                ],
                _name: 'test'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search?include_named_queries_score
    {
      "query": {
        "bool": {
          "should": [
            { "match": { "name.first": { "query": "shay", "_name": "first" } } },
            { "match": { "name.last": { "query": "banon", "_name": "last" } } }
          ],
          "filter": {
            "terms": {
              "name.last": [ "banon", "kimchy" ],
              "_name": "test"
            }
          }
        }
      }
    }

此功能在搜索响应中的每个命中时重新运行每个命名查询。通常，这会给请求增加少量开销。但是，对大量命中使用计算成本高昂的命名查询可能会增加大量开销。例如，命名查询与许多存储桶上的"top_hits"聚合相结合可能会导致更长的响应时间。

[« Compound queries](compound-queries.md) [Boosting query »](query-dsl-
boosting-query.md)
