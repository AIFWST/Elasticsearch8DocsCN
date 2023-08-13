

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Search template examples with Mustache](search-template-with-mustache-
examples.md) [k-nearest neighbor (kNN) search »](knn-search.md)

## 对搜索结果进行排序

允许您在特定字段上添加一个或多个排序。每种排序也可以颠倒过来。排序是在每个字段级别定义的，"_score"的特殊字段名称用于按分数排序，"_doc"用于按索引顺序排序。

假设以下索引映射：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            post_date: {
              type: 'date'
            },
            user: {
              type: 'keyword'
            },
            name: {
              type: 'keyword'
            },
            age: {
              type: 'integer'
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
    	      "post_date": {
    	        "type": "date"
    	      },
    	      "user": {
    	        "type": "keyword"
    	      },
    	      "name": {
    	        "type": "keyword"
    	      },
    	      "age": {
    	        "type": "integer"
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
          "post_date": { "type": "date" },
          "user": {
            "type": "keyword"
          },
          "name": {
            "type": "keyword"
          },
          "age": { "type": "integer" }
        }
      }
    }
    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        sort: [
          {
            post_date: {
              order: 'asc',
              format: 'strict_date_optional_time_nanos'
            }
          },
          'user',
          {
            name: 'desc'
          },
          {
            age: 'desc'
          },
          '_score'
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "sort" : [
        { "post_date" : {"order" : "asc", "format": "strict_date_optional_time_nanos"}},
        "user",
        { "name" : "desc" },
        { "age" : "desc" },
        "_score"
      ],
      "query" : {
        "term" : { "user" : "kimchy" }
      }
    }

"_doc"除了是最有效的排序顺序之外，没有真正的用例。因此，如果您不关心返回文档的顺序，那么您应该按"_doc"排序。这在滚动时特别有帮助。

### 排序值

搜索响应包括每个文档的"排序"值。使用"format"参数为"日期"和"date_nanos"字段的"排序"值指定日期格式。以下搜索以"strict_date_optional_time_nanos"格式返回"post_date"字段的"排序"值。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        sort: [
          {
            post_date: {
              format: 'strict_date_optional_time_nanos'
            }
          }
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "sort" : [
        { "post_date" : {"format": "strict_date_optional_time_nanos"}}
      ],
      "query" : {
        "term" : { "user" : "kimchy" }
      }
    }

### 排序顺序

"order"选项可以具有以下值：

`asc`

|

按升序排序 ---|--- 'desc'

|

按降序排序 在对"_score"进行排序时，顺序默认为"desc"，对其他任何内容进行排序时，顺序默认为"asc"。

### 排序模式选项

Elasticsearch 支持按数组或多值字段排序。"mode"选项控制选择哪个数组值来对它所属的文档进行排序。"模式"选项可以具有以下值：

`min`

|

选择最低值。   ---|--- "最大"

|

选择最高值。   "总和"

|

使用所有值的总和作为排序值。仅适用于基于数字的数组字段。   '平均'

|

使用所有值的平均值作为排序值。仅适用于基于数字的数组字段。   "中位数"

|

使用所有值的中位数作为排序值。仅适用于基于数字的数组字段。   升序排序顺序中的默认排序模式是"min"——选取最低值。降序的默认排序模式为"max"——选取最大值。

#### 排序模式示例用法

在下面的示例中，字段价格每个单据有多个价格。在这种情况下，结果命中将根据每个文档的平均价格按价格升序排序。

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        product: 'chocolate',
        price: [
          20,
          4
        ]
      }
    )
    puts response
    
    response = client.search(
      body: {
        query: {
          term: {
            product: 'chocolate'
          }
        },
        sort: [
          {
            price: {
              order: 'asc',
              mode: 'avg'
            }
          }
        ]
      }
    )
    puts response
    
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "product": "chocolate",
    	  "price": [
    	    20,
    	    4
    	  ]
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "term": {
    	      "product": "chocolate"
    	    }
    	  },
    	  "sort": [
    	    {
    	      "price": {
    	        "order": "asc",
    	        "mode": "avg"
    	      }
    	    }
    	  ]
    	}`)),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    PUT /my-index-000001/_doc/1?refresh
    {
       "product": "chocolate",
       "price": [20, 4]
    }
    
    POST /_search
    {
       "query" : {
          "term" : { "product" : "chocolate" }
       },
       "sort" : [
          {"price" : {"order" : "asc", "mode" : "avg"}}
       ]
    }

### 对数值字段进行排序

对于数值字段，也可以使用"numeric_type"选项将值从一种类型转换为另一种类型。此选项接受以下值：[''double'， "long"， "date"， "date_nanos"']，对于跨排序字段映射不同的多个数据流或索引的搜索非常有用。

例如，考虑以下两个指数：

    
    
    response = client.indices.create(
      index: 'index_double',
      body: {
        mappings: {
          properties: {
            field: {
              type: 'double'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"index_double",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "field": {
    	        "type": "double"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /index_double
    {
      "mappings": {
        "properties": {
          "field": { "type": "double" }
        }
      }
    }
    
    
    response = client.indices.create(
      index: 'index_long',
      body: {
        mappings: {
          properties: {
            field: {
              type: 'long'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"index_long",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "field": {
    	        "type": "long"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /index_long
    {
      "mappings": {
        "properties": {
          "field": { "type": "long" }
        }
      }
    }

由于"field"在第一个索引中映射为"double"，在第二个索引中映射为"long"，因此默认情况下无法使用此字段对查询两个索引的请求进行排序。但是，您可以使用"numeric_type"选项将类型强制为一个或另一个，以便强制所有索引的特定类型：

    
    
    $params = [
        'index' => 'index_long,index_double',
        'body' => [
            'sort' => [
                [
                    'field' => [
                        'numeric_type' => 'double',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        index=["index_long", "index_double"],
        body={"sort": [{"field": {"numeric_type": "double"}}]},
    )
    print(resp)
    
    
    response = client.search(
      index: 'index_long,index_double',
      body: {
        sort: [
          {
            field: {
              numeric_type: 'double'
            }
          }
        ]
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("index_long,index_double"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    {
    	      "field": {
    	        "numeric_type": "double"
    	      }
    	    }
    	  ]
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      index: 'index_long,index_double',
      body: {
        sort: [
          {
            field: {
              numeric_type: 'double'
            }
          }
        ]
      }
    })
    console.log(response)
    
    
    POST /index_long,index_double/_search
    {
       "sort" : [
          {
            "field" : {
                "numeric_type" : "double"
            }
          }
       ]
    }

在上面的示例中，"index_long"索引的值被强制转换为双精度值，以便与"index_double"索引生成的值兼容。也可以将浮点字段转换为"long"但请注意，在这种情况下，浮点数将替换为小于或等于参数的最大值(如果值为负，则大于或等于)并且等于数学整数。

此选项还可用于将使用毫秒分辨率的"日期"字段转换为具有纳秒分辨率的"date_nanos"字段。以以下两个指数为例：

    
    
    response = client.indices.create(
      index: 'index_double',
      body: {
        mappings: {
          properties: {
            field: {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"index_double",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "field": {
    	        "type": "date"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /index_double
    {
      "mappings": {
        "properties": {
          "field": { "type": "date" }
        }
      }
    }
    
    
    response = client.indices.create(
      index: 'index_long',
      body: {
        mappings: {
          properties: {
            field: {
              type: 'date_nanos'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"index_long",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "field": {
    	        "type": "date_nanos"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /index_long
    {
      "mappings": {
        "properties": {
          "field": { "type": "date_nanos" }
        }
      }
    }

这些索引中的值以不同的分辨率存储，因此对这些字段进行排序将始终对"date_nanos"(升序)之前的"日期"进行排序。使用"numeric_type"类型选项，可以为排序设置单一分辨率，设置为"日期"会将"date_nanos"转换为毫秒分辨率，而"date_nanos"会将"日期"字段中的值转换为纳秒分辨率：

    
    
    $params = [
        'index' => 'index_long,index_double',
        'body' => [
            'sort' => [
                [
                    'field' => [
                        'numeric_type' => 'date_nanos',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        index=["index_long", "index_double"],
        body={"sort": [{"field": {"numeric_type": "date_nanos"}}]},
    )
    print(resp)
    
    
    res, err := es.Search(
    	es.Search.WithIndex("index_long,index_double"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    {
    	      "field": {
    	        "numeric_type": "date_nanos"
    	      }
    	    }
    	  ]
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      index: 'index_long,index_double',
      body: {
        sort: [
          {
            field: {
              numeric_type: 'date_nanos'
            }
          }
        ]
      }
    })
    console.log(response)
    
    
    POST /index_long,index_double/_search
    {
       "sort" : [
          {
            "field" : {
                "numeric_type" : "date_nanos"
            }
          }
       ]
    }

为避免溢出，不能在 1970 年之前和 2262 年之后的日期上应用转换为"date_nanos"，因为纳秒表示为长整型。

### 在嵌套对象中排序。

Elasticsearch 还支持按一个或多个嵌套对象内的字段进行排序。按嵌套字段排序支持具有"嵌套"排序选项，具有以下属性：

`path`

     Defines on which nested object to sort. The actual sort field must be a direct field inside this nested object. When sorting by nested field, this field is mandatory. 
`filter`

     A filter that the inner objects inside the nested path should match with in order for its field values to be taken into account by sorting. Common case is to repeat the query / filter inside the nested filter or query. By default no `filter` is active. 
`max_children`

     The maximum number of children to consider per root document when picking the sort value. Defaults to unlimited. 
`nested`

     Same as top-level `nested` but applies to another nested path within the current nested object. 

如果嵌套字段是在没有"嵌套"上下文的排序中定义的，则 Elasticsearch 将抛出错误。

#### 嵌套排序示例

在下面的示例中，"offer"是一个类型为"嵌套"的字段。需要指定嵌套的"路径";否则，Elasticsearch 不知道需要捕获哪些嵌套级别的排序值。

    
    
    $params = [
        'body' => [
            'query' => [
                'term' => [
                    'product' => 'chocolate',
                ],
            ],
            'sort' => [
                [
                    'offer.price' => [
                        'mode' => 'avg',
                        'order' => 'asc',
                        'nested' => [
                            'path' => 'offer',
                            'filter' => [
                                'term' => [
                                    'offer.color' => 'blue',
                                ],
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
            "query": {"term": {"product": "chocolate"}},
            "sort": [
                {
                    "offer.price": {
                        "mode": "avg",
                        "order": "asc",
                        "nested": {
                            "path": "offer",
                            "filter": {"term": {"offer.color": "blue"}},
                        },
                    }
                }
            ],
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          term: {
            product: 'chocolate'
          }
        },
        sort: [
          {
            "offer.price": {
              mode: 'avg',
              order: 'asc',
              nested: {
                path: 'offer',
                filter: {
                  term: {
                    "offer.color": 'blue'
                  }
                }
              }
            }
          }
        ]
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "term": {
    	      "product": "chocolate"
    	    }
    	  },
    	  "sort": [
    	    {
    	      "offer.price": {
    	        "mode": "avg",
    	        "order": "asc",
    	        "nested": {
    	          "path": "offer",
    	          "filter": {
    	            "term": {
    	              "offer.color": "blue"
    	            }
    	          }
    	        }
    	      }
    	    }
    	  ]
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          term: {
            product: 'chocolate'
          }
        },
        sort: [
          {
            'offer.price': {
              mode: 'avg',
              order: 'asc',
              nested: {
                path: 'offer',
                filter: {
                  term: {
                    'offer.color': 'blue'
                  }
                }
              }
            }
          }
        ]
      }
    })
    console.log(response)
    
    
    POST /_search
    {
       "query" : {
          "term" : { "product" : "chocolate" }
       },
       "sort" : [
           {
              "offer.price" : {
                 "mode" :  "avg",
                 "order" : "asc",
                 "nested": {
                    "path": "offer",
                    "filter": {
                       "term" : { "offer.color" : "blue" }
                    }
                 }
              }
           }
        ]
    }

在下面的示例中，"父"和"子"字段的类型为"嵌套"。需要在每个级别指定"嵌套路径";否则，Elasticsearch不知道需要在哪些嵌套级别上捕获排序值。

    
    
    $params = [
        'body' => [
            'query' => [
                'nested' => [
                    'path' => 'parent',
                    'query' => [
                        'bool' => [
                            'must' => [
                                'range' => [
                                    'parent.age' => [
                                        'gte' => 21,
                                    ],
                                ],
                            ],
                            'filter' => [
                                'nested' => [
                                    'path' => 'parent.child',
                                    'query' => [
                                        'match' => [
                                            'parent.child.name' => 'matt',
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
            'sort' => [
                [
                    'parent.child.age' => [
                        'mode' => 'min',
                        'order' => 'asc',
                        'nested' => [
                            'path' => 'parent',
                            'filter' => [
                                'range' => [
                                    'parent.age' => [
                                        'gte' => 21,
                                    ],
                                ],
                            ],
                            'nested' => [
                                'path' => 'parent.child',
                                'filter' => [
                                    'match' => [
                                        'parent.child.name' => 'matt',
                                    ],
                                ],
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
                "nested": {
                    "path": "parent",
                    "query": {
                        "bool": {
                            "must": {"range": {"parent.age": {"gte": 21}}},
                            "filter": {
                                "nested": {
                                    "path": "parent.child",
                                    "query": {
                                        "match": {"parent.child.name": "matt"}
                                    },
                                }
                            },
                        }
                    },
                }
            },
            "sort": [
                {
                    "parent.child.age": {
                        "mode": "min",
                        "order": "asc",
                        "nested": {
                            "path": "parent",
                            "filter": {"range": {"parent.age": {"gte": 21}}},
                            "nested": {
                                "path": "parent.child",
                                "filter": {
                                    "match": {"parent.child.name": "matt"}
                                },
                            },
                        },
                    }
                }
            ],
        },
    )
    print(resp)
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "nested": {
    	      "path": "parent",
    	      "query": {
    	        "bool": {
    	          "must": {
    	            "range": {
    	              "parent.age": {
    	                "gte": 21
    	              }
    	            }
    	          },
    	          "filter": {
    	            "nested": {
    	              "path": "parent.child",
    	              "query": {
    	                "match": {
    	                  "parent.child.name": "matt"
    	                }
    	              }
    	            }
    	          }
    	        }
    	      }
    	    }
    	  },
    	  "sort": [
    	    {
    	      "parent.child.age": {
    	        "mode": "min",
    	        "order": "asc",
    	        "nested": {
    	          "path": "parent",
    	          "filter": {
    	            "range": {
    	              "parent.age": {
    	                "gte": 21
    	              }
    	            }
    	          },
    	          "nested": {
    	            "path": "parent.child",
    	            "filter": {
    	              "match": {
    	                "parent.child.name": "matt"
    	              }
    	            }
    	          }
    	        }
    	      }
    	    }
    	  ]
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          nested: {
            path: 'parent',
            query: {
              bool: {
                must: {
                  range: {
                    'parent.age': {
                      gte: 21
                    }
                  }
                },
                filter: {
                  nested: {
                    path: 'parent.child',
                    query: {
                      match: {
                        'parent.child.name': 'matt'
                      }
                    }
                  }
                }
              }
            }
          }
        },
        sort: [
          {
            'parent.child.age': {
              mode: 'min',
              order: 'asc',
              nested: {
                path: 'parent',
                filter: {
                  range: {
                    'parent.age': {
                      gte: 21
                    }
                  }
                },
                nested: {
                  path: 'parent.child',
                  filter: {
                    match: {
                      'parent.child.name': 'matt'
                    }
                  }
                }
              }
            }
          }
        ]
      }
    })
    console.log(response)
    
    
    POST /_search
    {
       "query": {
          "nested": {
             "path": "parent",
             "query": {
                "bool": {
                    "must": {"range": {"parent.age": {"gte": 21}}},
                    "filter": {
                        "nested": {
                            "path": "parent.child",
                            "query": {"match": {"parent.child.name": "matt"}}
                        }
                    }
                }
             }
          }
       },
       "sort" : [
          {
             "parent.child.age" : {
                "mode" :  "min",
                "order" : "asc",
                "nested": {
                   "path": "parent",
                   "filter": {
                      "range": {"parent.age": {"gte": 21}}
                   },
                   "nested": {
                      "path": "parent.child",
                      "filter": {
                         "match": {"parent.child.name": "matt"}
                      }
                   }
                }
             }
          }
       ]
    }

按脚本排序和按地理距离排序时，也支持嵌套排序。

### 缺失值

"missing"参数指定如何处理缺少排序字段的文档："缺失"值可以设置为"_last"、"_first"或自定义值(将用于缺少的文档作为排序值)。默认值为"_last"。

例如：

    
    
    response = client.search(
      body: {
        sort: [
          {
            price: {
              missing: '_last'
            }
          }
        ],
        query: {
          term: {
            product: 'chocolate'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    {
    	      "price": {
    	        "missing": "_last"
    	      }
    	    }
    	  ],
    	  "query": {
    	    "term": {
    	      "product": "chocolate"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "sort" : [
        { "price" : {"missing" : "_last"} }
      ],
      "query" : {
        "term" : { "product" : "chocolate" }
      }
    }

如果嵌套的内部对象与"nested.filter"不匹配，则使用缺失值。

### 忽略未映射的字段

默认情况下，如果没有与字段关联的映射，则搜索请求将失败。"unmapped_type"选项允许您忽略没有映射且不按它们排序的字段。此参数的值用于确定要发出的排序值。下面是如何使用它的示例：

    
    
    response = client.search(
      body: {
        sort: [
          {
            price: {
              unmapped_type: 'long'
            }
          }
        ],
        query: {
          term: {
            product: 'chocolate'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    {
    	      "price": {
    	        "unmapped_type": "long"
    	      }
    	    }
    	  ],
    	  "query": {
    	    "term": {
    	      "product": "chocolate"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "sort" : [
        { "price" : {"unmapped_type" : "long"} }
      ],
      "query" : {
        "term" : { "product" : "chocolate" }
      }
    }

如果查询的任何索引没有"价格"的映射，那么Elasticsearch将处理它，就好像存在"long"类型的映射一样，此索引中的所有文档都没有此字段的值。

### 地理距离排序

允许按"_geo_distance"排序。下面是一个示例，假设"pin.location"是类型为"geo_point"的字段：

    
    
    response = client.search(
      body: {
        sort: [
          {
            _geo_distance: {
              "pin.location": [
                -70,
                40
              ],
              order: 'asc',
              unit: 'km',
              mode: 'min',
              distance_type: 'arc',
              ignore_unmapped: true
            }
          }
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    {
    	      "_geo_distance": {
    	        "pin.location": [
    	          -70,
    	          40
    	        ],
    	        "order": "asc",
    	        "unit": "km",
    	        "mode": "min",
    	        "distance_type": "arc",
    	        "ignore_unmapped": true
    	      }
    	    }
    	  ],
    	  "query": {
    	    "term": {
    	      "user": "kimchy"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "sort" : [
        {
          "_geo_distance" : {
              "pin.location" : [-70, 40],
              "order" : "asc",
              "unit" : "km",
              "mode" : "min",
              "distance_type" : "arc",
              "ignore_unmapped": true
          }
        }
      ],
      "query" : {
        "term" : { "user" : "kimchy" }
      }
    }

`distance_type`

     How to compute the distance. Can either be `arc` (default), or `plane` (faster, but inaccurate on long distances and close to the poles). 
`mode`

     What to do in case a field has several geo points. By default, the shortest distance is taken into account when sorting in ascending order and the longest distance when sorting in descending order. Supported values are `min`, `max`, `median` and `avg`. 
`unit`

     The unit to use when computing sort values. The default is `m` (meters). 
`ignore_unmapped`

     Indicates if the unmapped field should be treated as a missing value. Setting it to `true` is equivalent to specifying an `unmapped_type` in the field sort. The default is `false` (unmapped field cause the search to fail). 

地理距离排序不支持可配置的缺失值：当文档没有用于距离计算的字段的值时，距离将始终被视为等于"无穷大"。

提供坐标时支持以下格式：

#### Lat Lon asProperties

    
    
    response = client.search(
      body: {
        sort: [
          {
            _geo_distance: {
              "pin.location": {
                lat: 40,
                lon: -70
              },
              order: 'asc',
              unit: 'km'
            }
          }
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    {
    	      "_geo_distance": {
    	        "pin.location": {
    	          "lat": 40,
    	          "lon": -70
    	        },
    	        "order": "asc",
    	        "unit": "km"
    	      }
    	    }
    	  ],
    	  "query": {
    	    "term": {
    	      "user": "kimchy"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "sort" : [
        {
          "_geo_distance" : {
            "pin.location" : {
              "lat" : 40,
              "lon" : -70
            },
            "order" : "asc",
            "unit" : "km"
          }
        }
      ],
      "query" : {
        "term" : { "user" : "kimchy" }
      }
    }

#### Lat Lon 饰 WKTString

以已知文本格式。

    
    
    response = client.search(
      body: {
        sort: [
          {
            _geo_distance: {
              "pin.location": 'POINT (-70 40)',
              order: 'asc',
              unit: 'km'
            }
          }
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "sort": [
        {
          "_geo_distance": {
            "pin.location": "POINT (-70 40)",
            "order": "asc",
            "unit": "km"
          }
        }
      ],
      "query": {
        "term": { "user": "kimchy" }
      }
    }

####Geohash

    
    
    response = client.search(
      body: {
        sort: [
          {
            _geo_distance: {
              "pin.location": 'drm3btev3e86',
              order: 'asc',
              unit: 'km'
            }
          }
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    {
    	      "_geo_distance": {
    	        "pin.location": "drm3btev3e86",
    	        "order": "asc",
    	        "unit": "km"
    	      }
    	    }
    	  ],
    	  "query": {
    	    "term": {
    	      "user": "kimchy"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "sort": [
        {
          "_geo_distance": {
            "pin.location": "drm3btev3e86",
            "order": "asc",
            "unit": "km"
          }
        }
      ],
      "query": {
        "term": { "user": "kimchy" }
      }
    }

#### Lat Lon asArray

格式为"lon， lat]"，请注意，此处的 lon/lat 顺序以符合 [GeoJSON.

    
    
    response = client.search(
      body: {
        sort: [
          {
            _geo_distance: {
              "pin.location": [
                -70,
                40
              ],
              order: 'asc',
              unit: 'km'
            }
          }
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    {
    	      "_geo_distance": {
    	        "pin.location": [
    	          -70,
    	          40
    	        ],
    	        "order": "asc",
    	        "unit": "km"
    	      }
    	    }
    	  ],
    	  "query": {
    	    "term": {
    	      "user": "kimchy"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "sort": [
        {
          "_geo_distance": {
            "pin.location": [ -70, 40 ],
            "order": "asc",
            "unit": "km"
          }
        }
      ],
      "query": {
        "term": { "user": "kimchy" }
      }
    }

### 多个参考点

例如，多个地理点可以作为包含任何"geo_point"格式的数组传递

    
    
    response = client.search(
      body: {
        sort: [
          {
            _geo_distance: {
              "pin.location": [
                [
                  -70,
                  40
                ],
                [
                  -71,
                  42
                ]
              ],
              order: 'asc',
              unit: 'km'
            }
          }
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    {
    	      "_geo_distance": {
    	        "pin.location": [
    	          [
    	            -70,
    	            40
    	          ],
    	          [
    	            -71,
    	            42
    	          ]
    	        ],
    	        "order": "asc",
    	        "unit": "km"
    	      }
    	    }
    	  ],
    	  "query": {
    	    "term": {
    	      "user": "kimchy"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "sort": [
        {
          "_geo_distance": {
            "pin.location": [ [ -70, 40 ], [ -71, 42 ] ],
            "order": "asc",
            "unit": "km"
          }
        }
      ],
      "query": {
        "term": { "user": "kimchy" }
      }
    }

等等。

然后，文档的最终距离将是文档中包含的所有点到排序请求中给出的所有点的"最小"/"最大"/"平均"(通过"模式"定义)距离。

### 基于脚本的排序

允许根据自定义脚本进行排序，下面是一个示例：

    
    
    response = client.search(
      body: {
        query: {
          term: {
            user: 'kimchy'
          }
        },
        sort: {
          _script: {
            type: 'number',
            script: {
              lang: 'painless',
              source: "doc['field_name'].value * params.factor",
              params: {
                factor: 1.1
              }
            },
            order: 'asc'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "term": {
    	      "user": "kimchy"
    	    }
    	  },
    	  "sort": {
    	    "_script": {
    	      "type": "number",
    	      "script": {
    	        "lang": "painless",
    	        "source": "doc['field_name'].value * params.factor",
    	        "params": {
    	          "factor": 1.1
    	        }
    	      },
    	      "order": "asc"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "term": { "user": "kimchy" }
      },
      "sort": {
        "_script": {
          "type": "number",
          "script": {
            "lang": "painless",
            "source": "doc['field_name'].value * params.factor",
            "params": {
              "factor": 1.1
            }
          },
          "order": "asc"
        }
      }
    }

### 曲目分数

对字段进行排序时，不会计算分数。通过将"track_scores"设置为 true，仍会计算和跟踪分数。

    
    
    response = client.search(
      body: {
        track_scores: true,
        sort: [
          {
            post_date: {
              order: 'desc'
            }
          },
          {
            name: 'desc'
          },
          {
            age: 'desc'
          }
        ],
        query: {
          term: {
            user: 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "track_scores": true,
    	  "sort": [
    	    {
    	      "post_date": {
    	        "order": "desc"
    	      }
    	    },
    	    {
    	      "name": "desc"
    	    },
    	    {
    	      "age": "desc"
    	    }
    	  ],
    	  "query": {
    	    "term": {
    	      "user": "kimchy"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "track_scores": true,
      "sort" : [
        { "post_date" : {"order" : "desc"} },
        { "name" : "desc" },
        { "age" : "desc" }
      ],
      "query" : {
        "term" : { "user" : "kimchy" }
      }
    }

### 内存注意事项

排序时，相关的排序字段值将加载到内存中。这意味着每个分片应该有足够的内存来包含它们。对于基于字符串的类型，不应分析/标记排序的字段。对于数值类型，如果可能，建议将类型显式设置为较窄的类型(如"短"、"整数"和"浮点数")。

[« Search template examples with Mustache](search-template-with-mustache-
examples.md) [k-nearest neighbor (kNN) search »](knn-search.md)
