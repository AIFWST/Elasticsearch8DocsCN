

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Full text queries](full-text-queries.md)

[« Combined fields](query-dsl-combined-fields-query.md) [Query string query
»](query-dsl-query-string-query.md)

## 多匹配查询

"multi_match"查询基于"匹配"查询构建，以允许多字段查询：

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'this is a test',
                    'fields' => [
                        'subject',
                        'message',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "this is a test",
                    "fields": ["subject", "message"],
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'this is a test',
            fields: [
              'subject',
              'message'
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "this is a test",
    	      "fields": [
    	        "subject",
    	        "message"
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'this is a test',
            fields: [
              'subject',
              'message'
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query":    "this is a test", __"fields": [ "subject", "message" ] __}
      }
    }

__

|

查询字符串。   ---|---    __

|

要查询的字段。   #### "字段"和每个字段的增强编辑

字段可以用通配符指定，例如：

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'Will Smith',
                    'fields' => [
                        'title',
                        '*_name',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "Will Smith",
                    "fields": ["title", "*_name"],
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'Will Smith',
            fields: [
              'title',
              '*_name'
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "Will Smith",
    	      "fields": [
    	        "title",
    	        "*_name"
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'Will Smith',
            fields: [
              'title',
              '*_name'
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query":    "Will Smith",
          "fields": [ "title", "*_name" ] __}
      }
    }

__

|

查询"标题"、"first_name"和"last_name"字段。   ---|--- 可以使用插入符号 ('^') 表示法提升各个字段：

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'this is a test',
                    'fields' => [
                        'subject^3',
                        'message',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "this is a test",
                    "fields": ["subject^3", "message"],
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'this is a test',
            fields: [
              'subject^3',
              'message'
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "this is a test",
    	      "fields": [
    	        "subject^3",
    	        "message"
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'this is a test',
            fields: [
              'subject^3',
              'message'
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query" : "this is a test",
          "fields" : [ "subject^3", "message" ] __}
      }
    }

__

|

查询将"主题"字段的分数乘以 3，但保持"消息"字段的分数不变。   ---|--- 如果未提供"字段"，则"multi_match"查询默认为"index.query.default_field"索引设置，而索引设置又默认为"*"。'*'提取映射中符合术语查询条件的所有字段，并筛选元数据字段。然后将所有提取的字段组合在一起以构建查询。

### 字段数限制

默认情况下，查询可以包含的子句数有限制。此限制由"index.query.bool.max_clause_count"设置定义，该设置默认为"4096"。对于多重匹配查询，子句数的计算方法是字段数乘以字词数。

#### "multi_match"查询的类型：

"multi_match"查询在内部执行的方式取决于"type"参数，该参数可以设置为：

`best_fields`

|

( **默认** )查找与任何字段匹配的文档，但使用最佳字段中的"_score"。请参阅"best_fields"。   ---|--- "most_fields"

|

查找与任何字段匹配的文档，并合并每个字段中的"_score"。参见"most_fields"。   "cross_fields"

|

使用相同的"分析器"将字段视为一个大字段。在 **any** 字段中查找每个单词。参见"cross_fields"。   "短语"

|

对每个字段运行"match_phrase"查询，并使用最佳字段中的"_score"。参见"短语"和"phrase_prefix"。   "phrase_prefix"

|

对每个字段运行"match_phrase_prefix"查询，并使用最佳字段中的"_score"。参见"短语"和"phrase_prefix"。   "bool_prefix"

|

在每个字段上创建一个"match_bool_prefix"查询，并合并每个字段中的"_score"。参见"bool_prefix"。   ###'best_fields'编辑

当您搜索在同一字段中找到的多个单词时，"best_fields"类型最有用。例如，单个字段中的"棕色狐狸"比一个字段中的"棕色"和另一个字段中的"狐狸"更有意义。

"best_fields"类型为每个字段生成一个"匹配"查询，并将它们包装在"dis_max"查询中，以查找单个最佳匹配字段。例如，此查询：

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'brown fox',
                    'type' => 'best_fields',
                    'fields' => [
                        'subject',
                        'message',
                    ],
                    'tie_breaker' => 0.3,
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "brown fox",
                    "type": "best_fields",
                    "fields": ["subject", "message"],
                    "tie_breaker": 0.3,
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'brown fox',
            type: 'best_fields',
            fields: [
              'subject',
              'message'
            ],
            tie_breaker: 0.3
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "brown fox",
    	      "type": "best_fields",
    	      "fields": [
    	        "subject",
    	        "message"
    	      ],
    	      "tie_breaker": 0.3
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'brown fox',
            type: 'best_fields',
            fields: [
              'subject',
              'message'
            ],
            tie_breaker: 0.3
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query":      "brown fox",
          "type":       "best_fields",
          "fields":     [ "subject", "message" ],
          "tie_breaker": 0.3
        }
      }
    }

将执行为：

    
    
    $params = [
        'body' => [
            'query' => [
                'dis_max' => [
                    'queries' => [
                        [
                            'match' => [
                                'subject' => 'brown fox',
                            ],
                        ],
                        [
                            'match' => [
                                'message' => 'brown fox',
                            ],
                        ],
                    ],
                    'tie_breaker' => 0.3,
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "dis_max": {
                    "queries": [
                        {"match": {"subject": "brown fox"}},
                        {"match": {"message": "brown fox"}},
                    ],
                    "tie_breaker": 0.3,
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          dis_max: {
            queries: [
              {
                match: {
                  subject: 'brown fox'
                }
              },
              {
                match: {
                  message: 'brown fox'
                }
              }
            ],
            tie_breaker: 0.3
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "dis_max": {
    	      "queries": [
    	        {
    	          "match": {
    	            "subject": "brown fox"
    	          }
    	        },
    	        {
    	          "match": {
    	            "message": "brown fox"
    	          }
    	        }
    	      ],
    	      "tie_breaker": 0.3
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          dis_max: {
            queries: [
              {
                match: {
                  subject: 'brown fox'
                }
              },
              {
                match: {
                  message: 'brown fox'
                }
              }
            ],
            tie_breaker: 0.3
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "dis_max": {
          "queries": [
            { "match": { "subject": "brown fox" }},
            { "match": { "message": "brown fox" }}
          ],
          "tie_breaker": 0.3
        }
      }
    }

通常，"best_fields"类型使用**单个**最佳匹配字段的分数，但如果指定了"tie_breaker"，则按如下方式计算分数：

* 最佳匹配字段的分数 * 加上所有其他匹配字段的"tie_breaker * _score"

此外，接受"分析器"、"提升"、"运算符"、"minimum_should_match"、"模糊"、"宽松"、"prefix_length"、"max_expansions"、"fuzzy_rewrite"、"zero_terms_query"、"auto_generate_synonyms_phrase_query"和"fuzzy_transpositions"，如匹配查询中所述。

### "运算符"和"minimum_should_match"

"best_fields"和"most_fields"类型是_field centric_ - 它们为每个字段生成"匹配"查询。这意味着"运算符"和"minimum_should_match"参数分别应用于每个字段，这可能不是您想要的。

以这个查询为例：

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'Will Smith',
                    'type' => 'best_fields',
                    'fields' => [
                        'first_name',
                        'last_name',
                    ],
                    'operator' => 'and',
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "Will Smith",
                    "type": "best_fields",
                    "fields": ["first_name", "last_name"],
                    "operator": "and",
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'Will Smith',
            type: 'best_fields',
            fields: [
              'first_name',
              'last_name'
            ],
            operator: 'and'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "Will Smith",
    	      "type": "best_fields",
    	      "fields": [
    	        "first_name",
    	        "last_name"
    	      ],
    	      "operator": "and"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'Will Smith',
            type: 'best_fields',
            fields: [
              'first_name',
              'last_name'
            ],
            operator: 'and'
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query":      "Will Smith",
          "type":       "best_fields",
          "fields":     [ "first_name", "last_name" ],
          "operator":   "and" __}
      }
    }

__

|

所有条款都必须存在。   ---|--- 此查询按以下方式执行：

    
    
      (+first_name:will +first_name:smith)
    | (+last_name:will  +last_name:smith)

换句话说，**所有术语**必须存在于单个字段中**，文档才能匹配。

"combined_fields"查询提供了一种以术语为中心的方法，该方法基于每个术语处理"运算符"和"minimum_should_match"。另一种多重匹配模式"cross_fields"也解决了这个问题。

###'most_fields'

当查询包含以不同方式分析的相同文本的多个字段时，"most_fields"类型最有用。例如，主字段可能包含同义词、词干和没有变音符号的术语。第二个字段可能包含原始术语，第三个字段可能包含带状疱疹。通过组合所有三个字段的分数，我们可以将尽可能多的文档与主字段匹配，但使用第二个和第三个字段将最相似的结果推送到列表顶部。

此查询：

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'quick brown fox',
                    'type' => 'most_fields',
                    'fields' => [
                        'title',
                        'title.original',
                        'title.shingles',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "quick brown fox",
                    "type": "most_fields",
                    "fields": ["title", "title.original", "title.shingles"],
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'quick brown fox',
            type: 'most_fields',
            fields: [
              'title',
              'title.original',
              'title.shingles'
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "quick brown fox",
    	      "type": "most_fields",
    	      "fields": [
    	        "title",
    	        "title.original",
    	        "title.shingles"
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'quick brown fox',
            type: 'most_fields',
            fields: [
              'title',
              'title.original',
              'title.shingles'
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query":      "quick brown fox",
          "type":       "most_fields",
          "fields":     [ "title", "title.original", "title.shingles" ]
        }
      }
    }

将执行为：

    
    
    $params = [
        'body' => [
            'query' => [
                'bool' => [
                    'should' => [
                        [
                            'match' => [
                                'title' => 'quick brown fox',
                            ],
                        ],
                        [
                            'match' => [
                                'title.original' => 'quick brown fox',
                            ],
                        ],
                        [
                            'match' => [
                                'title.shingles' => 'quick brown fox',
                            ],
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
                    "should": [
                        {"match": {"title": "quick brown fox"}},
                        {"match": {"title.original": "quick brown fox"}},
                        {"match": {"title.shingles": "quick brown fox"}},
                    ]
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          bool: {
            should: [
              {
                match: {
                  title: 'quick brown fox'
                }
              },
              {
                match: {
                  "title.original": 'quick brown fox'
                }
              },
              {
                match: {
                  "title.shingles": 'quick brown fox'
                }
              }
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "bool": {
    	      "should": [
    	        {
    	          "match": {
    	            "title": "quick brown fox"
    	          }
    	        },
    	        {
    	          "match": {
    	            "title.original": "quick brown fox"
    	          }
    	        },
    	        {
    	          "match": {
    	            "title.shingles": "quick brown fox"
    	          }
    	        }
    	      ]
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
            should: [
              {
                match: {
                  title: 'quick brown fox'
                }
              },
              {
                match: {
                  'title.original': 'quick brown fox'
                }
              },
              {
                match: {
                  'title.shingles': 'quick brown fox'
                }
              }
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "bool": {
          "should": [
            { "match": { "title":          "quick brown fox" }},
            { "match": { "title.original": "quick brown fox" }},
            { "match": { "title.shingles": "quick brown fox" }}
          ]
        }
      }
    }

每个"匹配"子句的分数加在一起，就像"布尔"查询一样。

此外，接受"分析器"、"提升"、"运算符"、"minimum_should_match"、"模糊"、"宽松"、"prefix_length"、"max_expansions"、"fuzzy_rewrite"和"zero_terms_query"。

### "短语"和"phrase_prefix"

"短语"和"phrase_prefix"类型的行为与"best_fields"类似，但它们使用"match_phrase"或"match_phrase_prefix"查询而不是"匹配"查询。

此查询：

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'quick brown f',
                    'type' => 'phrase_prefix',
                    'fields' => [
                        'subject',
                        'message',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "quick brown f",
                    "type": "phrase_prefix",
                    "fields": ["subject", "message"],
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'quick brown f',
            type: 'phrase_prefix',
            fields: [
              'subject',
              'message'
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "quick brown f",
    	      "type": "phrase_prefix",
    	      "fields": [
    	        "subject",
    	        "message"
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'quick brown f',
            type: 'phrase_prefix',
            fields: [
              'subject',
              'message'
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query":      "quick brown f",
          "type":       "phrase_prefix",
          "fields":     [ "subject", "message" ]
        }
      }
    }

将执行为：

    
    
    $params = [
        'body' => [
            'query' => [
                'dis_max' => [
                    'queries' => [
                        [
                            'match_phrase_prefix' => [
                                'subject' => 'quick brown f',
                            ],
                        ],
                        [
                            'match_phrase_prefix' => [
                                'message' => 'quick brown f',
                            ],
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
                "dis_max": {
                    "queries": [
                        {"match_phrase_prefix": {"subject": "quick brown f"}},
                        {"match_phrase_prefix": {"message": "quick brown f"}},
                    ]
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          dis_max: {
            queries: [
              {
                match_phrase_prefix: {
                  subject: 'quick brown f'
                }
              },
              {
                match_phrase_prefix: {
                  message: 'quick brown f'
                }
              }
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "dis_max": {
    	      "queries": [
    	        {
    	          "match_phrase_prefix": {
    	            "subject": "quick brown f"
    	          }
    	        },
    	        {
    	          "match_phrase_prefix": {
    	            "message": "quick brown f"
    	          }
    	        }
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          dis_max: {
            queries: [
              {
                match_phrase_prefix: {
                  subject: 'quick brown f'
                }
              },
              {
                match_phrase_prefix: {
                  message: 'quick brown f'
                }
              }
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "dis_max": {
          "queries": [
            { "match_phrase_prefix": { "subject": "quick brown f" }},
            { "match_phrase_prefix": { "message": "quick brown f" }}
          ]
        }
      }
    }

此外，接受匹配中解释的"分析器"、"提升"、"宽大"和"zero_terms_query"，以及匹配短语中解释的"倾斜"。键入"phrase_prefix"还接受"max_expansions"。

### "短语"、"phrase_prefix"和"模糊"

"模糊度"参数不能与"短语"或"phrase_prefix"类型一起使用。

###'cross_fields'

"cross_fields"类型对于多个字段**应该**匹配的结构化文档特别有用。例如，在"first_name"和"last_name"字段中查询"Will Smith"时，最佳匹配项可能在一个字段中具有"Will"，而在另一个字段中具有"Smith"。

这听起来像是"most_fields"的工作，但这种方法有两个问题。第一个问题是"运算符"和"minimum_should_match"是按字段应用的，而不是按项应用的(请参阅上面的解释)。

第二个问题与相关性有关："first_name"和"last_name"字段中的不同术语频率可能会产生意想不到的结果。

例如，假设我们有两个人："威尔·史密斯"和"史密斯·琼斯"。史密斯"作为姓氏很常见(因此重要性不高)，但"史密斯"作为名字非常罕见(因此非常重要)。

如果我们搜索"Will Smith"，"Smith Jones"文档可能会出现在匹配更好的"Will Smith"之上，因为"first_name：smith"的分数超过了"first_name：will"加上"last_name：smith"的总和。

处理这些类型的查询的一种方法是简单地将"first_name"和"last_name"字段索引为单个"full_name"字段。当然，这只能在索引时完成。

"cross_field"类型尝试通过采用a_term centric_方法在查询时解决这些问题。它首先将查询字符串分析为单个术语，然后在任何字段中查找每个术语，就好像它们是 onebig 字段一样。

类似这样的查询：

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'Will Smith',
                    'type' => 'cross_fields',
                    'fields' => [
                        'first_name',
                        'last_name',
                    ],
                    'operator' => 'and',
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "Will Smith",
                    "type": "cross_fields",
                    "fields": ["first_name", "last_name"],
                    "operator": "and",
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'Will Smith',
            type: 'cross_fields',
            fields: [
              'first_name',
              'last_name'
            ],
            operator: 'and'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "Will Smith",
    	      "type": "cross_fields",
    	      "fields": [
    	        "first_name",
    	        "last_name"
    	      ],
    	      "operator": "and"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'Will Smith',
            type: 'cross_fields',
            fields: [
              'first_name',
              'last_name'
            ],
            operator: 'and'
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query":      "Will Smith",
          "type":       "cross_fields",
          "fields":     [ "first_name", "last_name" ],
          "operator":   "and"
        }
      }
    }

执行方式为：

    
    
    +(first_name:will last_name:will)
    +(first_name:smith last_name:smith)

换句话说，**所有术语**必须至少存在于一个字段中**，文档才能匹配。(将此与用于"best_fields"和"most_fields"的逻辑进行比较。

这解决了两个问题之一。通过_blending_所有场的项频率来解决不同项频率的问题，以平衡差异。

实际上，"first_name：smith"将被视为与"last_name：smith"具有相同的频率，加一。这将使"first_name"和"last_name"上的比赛具有相当的分数，而"last_name"的优势很小，因为它是最有可能包含"smith"的字段。

请注意，"cross_fields"通常只对"提升"为"1"的短字符串字段有用。否则，提升、术语频率和长度归一化会以这样的方式影响分数，以至于术语统计的混合不再有意义。

如果通过验证运行上述查询，它将返回以下说明：

    
    
    +blended("will",  fields: [first_name, last_name])
    +blended("smith", fields: [first_name, last_name])

此外，接受"分析器"、"提升"、"操作员"、"minimum_should_match"、"宽大"和"zero_terms_query"。

"cross_fields"类型以难以解释的复杂方式混合字段统计信息。分数组合甚至可能不正确，特别是当某些文档包含某些搜索字段但不是全部搜索字段时。您应该考虑将"combined_fields"查询作为替代方法，该查询也是以术语为中心的，但以更可靠的方式组合字段统计信息。

#### 'cross_field' 和分析

"cross_field"类型只能在具有相同分析器的字段上以术语为中心的模式工作。具有相同分析器的字段将分组在一起，如上例所示。如果有多个组，查询将使用任何组中的最佳分数。

例如，如果我们有一个具有相同分析器的"first"和"last"字段，以及使用"edge_ngram"analyzer的"first.edge"和"last.edge"，则此查询：

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'Jon',
                    'type' => 'cross_fields',
                    'fields' => [
                        'first',
                        'first.edge',
                        'last',
                        'last.edge',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "Jon",
                    "type": "cross_fields",
                    "fields": ["first", "first.edge", "last", "last.edge"],
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'Jon',
            type: 'cross_fields',
            fields: [
              'first',
              'first.edge',
              'last',
              'last.edge'
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "Jon",
    	      "type": "cross_fields",
    	      "fields": [
    	        "first",
    	        "first.edge",
    	        "last",
    	        "last.edge"
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'Jon',
            type: 'cross_fields',
            fields: [
              'first',
              'first.edge',
              'last',
              'last.edge'
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query":      "Jon",
          "type":       "cross_fields",
          "fields":     [
            "first", "first.edge",
            "last",  "last.edge"
          ]
        }
      }
    }

将执行为：

    
    
        blended("jon", fields: [first, last])
    | (
        blended("j",   fields: [first.edge, last.edge])
        blended("jo",  fields: [first.edge, last.edge])
        blended("jon", fields: [first.edge, last.edge])
    )

换句话说，"first"和"last"将被分组在一起并被视为单个字段，而"first.edge"和"last.edge"将被组合在一起并被视为单个字段。

拥有多个组很好，但是当与"运算符"或"minimum_should_match"结合使用时，它可能会遇到与"most_fields"或"best_fields"相同的问题。

您可以轻松地将此查询重写为两个单独的"cross_fields"查询和一个"dis_max"查询，并将"minimum_should_match"参数应用于其中一个：

    
    
    response = client.search(
      body: {
        query: {
          dis_max: {
            queries: [
              {
                multi_match: {
                  query: 'Will Smith',
                  type: 'cross_fields',
                  fields: [
                    'first',
                    'last'
                  ],
                  minimum_should_match: '50%'
                }
              },
              {
                multi_match: {
                  query: 'Will Smith',
                  type: 'cross_fields',
                  fields: [
                    '*.edge'
                  ]
                }
              }
            ]
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "dis_max": {
          "queries": [
            {
              "multi_match" : {
                "query":      "Will Smith",
                "type":       "cross_fields",
                "fields":     [ "first", "last" ],
                "minimum_should_match": "50%" __}
            },
            {
              "multi_match" : {
                "query":      "Will Smith",
                "type":       "cross_fields",
                "fields":     [ "*.edge" ]
              }
            }
          ]
        }
      }
    }

__

|

"will"或"smith"必须出现在"first"或"last"字段中---|--- 您可以通过在查询中指定"分析器"参数来强制将所有字段放入同一组。

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'Jon',
                    'type' => 'cross_fields',
                    'analyzer' => 'standard',
                    'fields' => [
                        'first',
                        'last',
                        '*.edge',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "Jon",
                    "type": "cross_fields",
                    "analyzer": "standard",
                    "fields": ["first", "last", "*.edge"],
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'Jon',
            type: 'cross_fields',
            analyzer: 'standard',
            fields: [
              'first',
              'last',
              '*.edge'
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "Jon",
    	      "type": "cross_fields",
    	      "analyzer": "standard",
    	      "fields": [
    	        "first",
    	        "last",
    	        "*.edge"
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'Jon',
            type: 'cross_fields',
            analyzer: 'standard',
            fields: [
              'first',
              'last',
              '*.edge'
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
       "multi_match" : {
          "query":      "Jon",
          "type":       "cross_fields",
          "analyzer":   "standard", __"fields":     [ "first", "last", "*.edge" ]
        }
      }
    }

__

|

对所有字段使用"标准"分析器。   ---|---将执行为：

    
    
    blended("will",  fields: [first, first.edge, last.edge, last])
    blended("smith", fields: [first, first.edge, last.edge, last])

####'tie_breaker'

默认情况下，每个术语的"混合"查询将使用组中任何字段返回的最佳分数。然后，在跨组合并分数时，查询将使用任何组中的最佳分数。"tie_breaker"参数可以更改以下两个步骤的行为：

`0.0`

|

从(例如)"first_name：will"和"last_name：will"(默认)中取出一个最佳分数---|---"1.0"

|

将(例如)"first_name：will"和"last_name：will"的分数相加 "0.0 < n < 1.0"

|

取单个最佳分数加上"tie_breaker"乘以其他匹配字段/组中的每个分数 ### "cross_fields"和"模糊度"

"模糊"参数不能与"cross_fields"类型一起使用。

###'bool_prefix'

"bool_prefix"类型的评分行为类似于"most_fields"，但使用"match_bool_prefix"查询而不是"匹配"查询。

    
    
    $params = [
        'body' => [
            'query' => [
                'multi_match' => [
                    'query' => 'quick brown f',
                    'type' => 'bool_prefix',
                    'fields' => [
                        'subject',
                        'message',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "multi_match": {
                    "query": "quick brown f",
                    "type": "bool_prefix",
                    "fields": ["subject", "message"],
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          multi_match: {
            query: 'quick brown f',
            type: 'bool_prefix',
            fields: [
              'subject',
              'message'
            ]
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "quick brown f",
    	      "type": "bool_prefix",
    	      "fields": [
    	        "subject",
    	        "message"
    	      ]
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          multi_match: {
            query: 'quick brown f',
            type: 'bool_prefix',
            fields: [
              'subject',
              'message'
            ]
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "multi_match" : {
          "query":      "quick brown f",
          "type":       "bool_prefix",
          "fields":     [ "subject", "message" ]
        }
      }
    }

支持匹配查询中解释的"分析器"、"提升"、"运算符"、"minimum_should_match"、"宽松"、"zero_terms_query"和"auto_generate_synonyms_phrase_query"参数。用于构造术语查询的术语支持"模糊"、"prefix_length"、"max_expansions"、"fuzzy_rewrite"和"fuzzy_transpositions"参数，但对从最终术语构造的前缀查询没有影响。

此查询类型不支持"slop"参数。

[« Combined fields](query-dsl-combined-fields-query.md) [Query string query
»](query-dsl-query-string-query.md)
