

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `meta`](mapping-field-meta.md) [`normalizer` »](normalizer.md)

##'字段'

出于不同的目的，以不同的方式为同一字段编制索引通常很有用。这就是_multi-fields_的目的。例如，可以将"字符串"字段映射为用于全文搜索的"文本"字段，并映射为用于排序或聚合的"关键字"字段：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            city: {
              type: 'text',
              fields: {
                raw: {
                  type: 'keyword'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        city: 'New York'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        city: 'York'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            city: 'york'
          }
        },
        sort: {
          "city.raw": 'asc'
        },
        aggregations: {
          "Cities": {
            terms: {
              field: 'city.raw'
            }
          }
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Indices.Create(
    		"my-index-000001",
    		es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "city": {
    	        "type": "text",
    	        "fields": {
    	          "raw": {
    	            "type": "keyword"
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "city": "New York"
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "city": "York"
    	}`),
    		es.Index.WithDocumentID("2"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("my-index-000001"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match": {
    	      "city": "york"
    	    }
    	  },
    	  "sort": {
    	    "city.raw": "asc"
    	  },
    	  "aggs": {
    	    "Cities": {
    	      "terms": {
    	        "field": "city.raw"
    	      }
    	    }
    	  }
    	}`)),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "city": {
            "type": "text",
            "fields": {
              "raw": { __"type":  "keyword"
              }
            }
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "city": "New York"
    }
    
    PUT my-index-000001/_doc/2
    {
      "city": "York"
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "city": "york" __}
      },
      "sort": {
        "city.raw": "asc" __},
      "aggs": {
        "Cities": {
          "terms": {
            "field": "city.raw" __}
        }
      }
    }

__

|

"城市.raw"字段是"城市"字段的"关键字"版本。   ---|---    __

|

"城市"字段可用于全文搜索。   __

|

"city.raw"字段可用于排序和聚合 您可以使用更新映射 API 向现有字段添加多字段。

如果在添加多字段时索引(或数据流)包含文档，则这些文档将没有新多字段的值。您可以使用按查询更新 API 填充新的多字段。

多字段映射与父字段的映射完全分开。多字段不会从其父字段继承任何映射选项。多字段不会更改原始"_source"字段。

### 具有多个分析器的多字段

多字段的另一个用例是以不同的方式分析同一字段以提高相关性。例如，我们可以用"标准"分析器索引一个字段，它将文本分解为单词，再使用"英语"分析器将单词词干成它们的根形式：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            text: {
              type: 'text',
              fields: {
                english: {
                  type: 'text',
                  analyzer: 'english'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        text: 'quick brown fox'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        text: 'quick brown foxes'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          multi_match: {
            query: 'quick brown foxes',
            fields: [
              'text',
              'text.english'
            ],
            type: 'most_fields'
          }
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Indices.Create(
    		"my-index-000001",
    		es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "text": {
    	        "type": "text",
    	        "fields": {
    	          "english": {
    	            "type": "text",
    	            "analyzer": "english"
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "text": "quick brown fox"
    	} `),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "text": "quick brown foxes"
    	} `),
    		es.Index.WithDocumentID("2"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("my-index-000001"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "multi_match": {
    	      "query": "quick brown foxes",
    	      "fields": [
    	        "text",
    	        "text.english"
    	      ],
    	      "type": "most_fields"
    	    }
    	  }
    	}`)),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "text": { __"type": "text",
            "fields": {
              "english": { __"type":     "text",
                "analyzer": "english"
              }
            }
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    { "text": "quick brown fox" } __PUT my-index-000001/_doc/2
    { "text": "quick brown foxes" } __GET my-index-000001/_search
    {
      "query": {
        "multi_match": {
          "query": "quick brown foxes",
          "fields": [ __"text",
            "text.english"
          ],
          "type": "most_fields" __}
      }
    }

__

|

"文本"字段使用"标准"分析器。   ---|---    __

|

"text.english"字段使用"english"分析器。   __

|

索引两个文档，一个使用"fox"，另一个使用"foxes"。   __

|

查询"text"和"text.english"字段并合并分数。   "文本"字段在第一个文档中包含术语"fox"，在第二个文档中包含术语"foxes"。"text.english"字段包含两个文档的"fox"，因为"foxes"的词干是"fox"。

查询字符串还由"文本"字段的"标准"分析器分析，以及"text.english"字段的"英语"分析器进行分析。词干字段允许查询"foxes"也匹配仅包含"fox"的文档。这使我们能够匹配尽可能多的文档。通过查询无词干的"文本"字段，我们提高了文档的相关性分数与"狐狸"完全匹配。

[« `meta`](mapping-field-meta.md) [`normalizer` »](normalizer.md)
