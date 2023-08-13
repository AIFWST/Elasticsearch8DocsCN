

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Full text queries](full-text-queries.md)

[« Intervals query](query-dsl-intervals-query.md) [Match boolean prefix
query »](query-dsl-match-bool-prefix-query.md)

## 匹配查询

返回与提供的文本、数字、日期或布尔值匹配的文档。在匹配之前分析提供的文本。

"match"查询是用于执行全文搜索的标准查询，包括模糊匹配选项。

### 示例请求

    
    
    response = client.search(
      body: {
        query: {
          match: {
            message: {
              query: 'this is a test'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match": {
    	      "message": {
    	        "query": "this is a test"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "match": {
          "message": {
            "query": "this is a test"
          }
        }
      }
    }

### "匹配"的顶级参数

`<field>`

     (Required, object) Field you wish to search. 

### 参数 '<field>'

`query`

    

(必填)您希望在提供的""中找到的文本、数字、布尔值或日期<field>。

"match"查询在执行搜索之前分析任何提供的文本。这意味着"匹配"查询可以搜索"文本"字段以查找分析的令牌，而不是确切的术语。

`analyzer`

     (Optional, string) [Analyzer](analysis.html "Text analysis") used to convert the text in the `query` value into tokens. Defaults to the [index-time analyzer](specify-analyzer.html#specify-index-time-analyzer "How Elasticsearch determines the index analyzer") mapped for the `<field>`. If no analyzer is mapped, the index's default analyzer is used. 
`auto_generate_synonyms_phrase_query`

    

(可选，布尔值)如果为"true"，则会自动为多术语同义词创建匹配短语查询。默认为"真"。

有关示例，请参阅在匹配查询中使用同义词。

`boost`

    

(可选，浮动)用于降低或增加查询的相关性分数的浮点数。默认为"1.0"。

提升值相对于默认值"1.0"。介于"0"和"1.0"之间的提升值会降低相关性分数。大于"1.0"的值会增加相关性分数。

`fuzziness`

     (Optional, string) Maximum edit distance allowed for matching. See [Fuzziness](common-options.html#fuzziness "Fuzziness") for valid values and more information. See [Fuzziness in the match query](query-dsl-match-query.html#query-dsl-match-query-fuzziness "Fuzziness in the match query") for an example. 
`max_expansions`

     (Optional, integer) Maximum number of terms to which the query will expand. Defaults to `50`. 
`prefix_length`

     (Optional, integer) Number of beginning characters left unchanged for fuzzy matching. Defaults to `0`. 
`fuzzy_transpositions`

     (Optional, Boolean) If `true`, edits for fuzzy matching include transpositions of two adjacent characters (ab → ba). Defaults to `true`. 
`fuzzy_rewrite`

    

(可选，字符串)用于重写查询的方法。有关有效值和更多信息，请参阅"重写"参数。

如果"模糊性"参数不是"0"，则"匹配"查询默认使用"top_terms_blended_freqs_${max_expansions}"的"fuzzy_rewrite"方法。

`lenient`

     (Optional, Boolean) If `true`, format-based errors, such as providing a text `query` value for a [numeric](number.html "Numeric field types") field, are ignored. Defaults to `false`. 
`operator`

    

(可选，字符串)用于解释"query"值中的文本的布尔逻辑。有效值为：

"或"(默认)

     For example, a `query` value of `capital of Hungary` is interpreted as `capital OR of OR Hungary`. 
`AND`

     For example, a `query` value of `capital of Hungary` is interpreted as `capital AND of AND Hungary`. 

`minimum_should_match`

    

(可选，字符串)要返回的文档必须匹配的最小子句数。有关有效值和更多信息，请参阅"minimum_should_match"参数。

`zero_terms_query`

    

(可选，字符串)指示如果"分析器"删除所有令牌(例如使用"停止"筛选器时)，是否不返回任何文档。有效值为：

"无"(默认)

     No documents are returned if the `analyzer` removes all tokens. 
`all`

     Returns all documents, similar to a [`match_all`](query-dsl-match-all-query.html "Match all query") query. 

有关示例，请参阅零字词查询。

###Notes

#### 简短请求示例

您可以通过组合""和"查询"参数来简化匹配<field>查询语法。例如：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            message: 'this is a test'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match": {
    	      "message": "this is a test"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "match": {
          "message": "this is a test"
        }
      }
    }

#### 匹配查询的工作原理

"匹配"查询的类型为"布尔值"。这意味着对提供的文本进行分析，分析过程从提供的文本构造布尔查询。"operator"参数可以设置为"or"或"and"来控制布尔子句(默认为"or")。可以使用"minimum_should_match"参数设置要匹配的可选"should"子句的最小数量。

下面是一个带有"operator"参数的示例：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            message: {
              query: 'this is a test',
              operator: 'and'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match": {
    	      "message": {
    	        "query": "this is a test",
    	        "operator": "and"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "match": {
          "message": {
            "query": "this is a test",
            "operator": "and"
          }
        }
      }
    }

可以设置"分析器"以控制哪个分析器将对文本执行分析过程。它默认为字段显式映射定义或默认搜索分析器。

可以将"宽松"参数设置为"true"，以忽略由数据类型不匹配引起的异常，例如尝试使用文本查询字符串查询数值字段。默认为"假"。

#### 匹配查询中的模糊性

"模糊性"允许根据要查询的字段类型进行_fuzzy matching_。有关允许的设置，请参阅模糊性。

在这种情况下，可以设置"prefix_length"和"max_expansions"来控制模糊过程。如果设置了模糊选项，则查询将使用"top_terms_blended_freqs_${max_expansions}"作为其重写方法，"fuzzy_rewrite"参数允许控制查询的重写方式。

默认情况下允许模糊换位("ab"->"ba")，但可以通过将"fuzzy_transpositions"设置为"false"来禁用。

模糊匹配不适用于具有同义词的术语，也不适用于分析过程在同一位置生成多个标记的情况。在引擎盖下，这些术语被扩展为一个特殊的同义词查询，该查询混合了术语频率，不支持模糊扩展。

    
    
    response = client.search(
      body: {
        query: {
          match: {
            message: {
              query: 'this is a testt',
              fuzziness: 'AUTO'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match": {
    	      "message": {
    	        "query": "this is a testt",
    	        "fuzziness": "AUTO"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "match": {
          "message": {
            "query": "this is a testt",
            "fuzziness": "AUTO"
          }
        }
      }
    }

#### 零术语查询

如果使用的分析器像"stop"筛选器一样删除查询中的所有标记，则默认行为是根本不匹配任何文档。为了改变这一点，可以使用"zero_terms_query"选项，该选项接受"无"(默认值)和"all"，对应于"match_all"查询。

    
    
    response = client.search(
      body: {
        query: {
          match: {
            message: {
              query: 'to be or not to be',
              operator: 'and',
              zero_terms_query: 'all'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match": {
    	      "message": {
    	        "query": "to be or not to be",
    	        "operator": "and",
    	        "zero_terms_query": "all"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "match": {
          "message": {
            "query": "to be or not to be",
            "operator": "and",
            "zero_terms_query": "all"
          }
        }
      }
    }

####Synonyms

"match"查询支持使用令牌筛选器扩展多术语同义词thesynonym_graph。使用此筛选器时，分析器将为每个多术语同义词创建一个短语查询。例如，以下同义词："ny，New York"将产生：

'(纽约或("纽约"))"

也可以将多术语同义词与连词匹配：

    
    
    $params = [
        'body' => [
            'query' => [
                'match' => [
                    'message' => [
                        'query' => 'ny city',
                        'auto_generate_synonyms_phrase_query' => false,
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "match": {
                    "message": {
                        "query": "ny city",
                        "auto_generate_synonyms_phrase_query": False,
                    }
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          match: {
            message: {
              query: 'ny city',
              auto_generate_synonyms_phrase_query: false
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match": {
    	      "message": {
    	        "query": "ny city",
    	        "auto_generate_synonyms_phrase_query": false
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
          match: {
            message: {
              query: 'ny city',
              auto_generate_synonyms_phrase_query: false
            }
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
       "query": {
           "match" : {
               "message": {
                   "query" : "ny city",
                   "auto_generate_synonyms_phrase_query" : false
               }
           }
       }
    }

上面的示例创建了一个布尔查询：

"(纽约或(纽约和约克))城市"

将带有术语"ny"或连词"New AND York"的文档匹配。默认情况下，参数"auto_generate_synonyms_phrase_query"设置为"true"。

[« Intervals query](query-dsl-intervals-query.md) [Match boolean prefix
query »](query-dsl-match-bool-prefix-query.md)
