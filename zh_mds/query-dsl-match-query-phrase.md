

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Full text queries](full-text-queries.md)

[« Match boolean prefix query](query-dsl-match-bool-prefix-query.md) [Match
phrase prefix query »](query-dsl-match-query-phrase-prefix.md)

## 匹配短语查询

"match_phrase"查询分析文本，并从分析的文本中创建"短语"查询。例如：

    
    
    response = client.search(
      body: {
        query: {
          match_phrase: {
            message: 'this is a test'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match_phrase": {
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
        "match_phrase": {
          "message": "this is a test"
        }
      }
    }

短语查询以任何顺序将术语与可配置的"slop"(默认为 0)匹配。转置项的斜角为 2。

可以设置"分析器"以控制哪个分析器将对文本执行分析过程。它默认为字段显式映射定义或默认搜索分析器，例如：

    
    
    response = client.search(
      body: {
        query: {
          match_phrase: {
            message: {
              query: 'this is a test',
              analyzer: 'my_analyzer'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match_phrase": {
    	      "message": {
    	        "query": "this is a test",
    	        "analyzer": "my_analyzer"
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
        "match_phrase": {
          "message": {
            "query": "this is a test",
            "analyzer": "my_analyzer"
          }
        }
      }
    }

此查询也接受"zero_terms_query"，如"match"查询中所述。

[« Match boolean prefix query](query-dsl-match-bool-prefix-query.md) [Match
phrase prefix query »](query-dsl-match-query-phrase-prefix.md)
