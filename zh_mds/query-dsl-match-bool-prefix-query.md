

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Full text queries](full-text-queries.md)

[« Match query](query-dsl-match-query.md) [Match phrase query »](query-dsl-
match-query-phrase.md)

## 匹配布尔前缀查询

"match_bool_prefix"查询分析其输入并从术语构造"布尔"查询。每个术语(最后一个除外)都用于"术语"查询。最后一个术语用于"前缀"查询。"match_bool_prefix"查询，例如

    
    
    response = client.search(
      body: {
        query: {
          match_bool_prefix: {
            message: 'quick brown f'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "match_bool_prefix" : {
          "message" : "quick brown f"
        }
      }
    }

其中分析生成术语"快速"、"棕色"和"F"类似于以下"布尔"查询

    
    
    response = client.search(
      body: {
        query: {
          bool: {
            should: [
              {
                term: {
                  message: 'quick'
                }
              },
              {
                term: {
                  message: 'brown'
                }
              },
              {
                prefix: {
                  message: 'f'
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
        "bool" : {
          "should": [
            { "term": { "message": "quick" }},
            { "term": { "message": "brown" }},
            { "prefix": { "message": "f"}}
          ]
        }
      }
    }

"match_bool_prefix"查询和"match_phrase_prefix"之间的重要区别是，"match_phrase_prefix"查询将其词作为短语匹配，但"match_bool_prefix"查询可以在任何位置匹配其字词。上面的示例"match_bool_prefix"查询可以匹配包含"快速棕色狐狸"的字段，但它也可以匹配"棕色狐狸快速"。它还可以匹配包含术语"快速"、术语"棕色"和以"f"开头的术语的字段，出现在任何位置。

###Parameters

默认情况下，将使用来自查询字段映射的分析器分析"match_bool_prefix"查询的输入文本。可以使用"分析器"参数配置不同的搜索分析器

    
    
    response = client.search(
      body: {
        query: {
          match_bool_prefix: {
            message: {
              query: 'quick brown f',
              analyzer: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "match_bool_prefix": {
          "message": {
            "query": "quick brown f",
            "analyzer": "keyword"
          }
        }
      }
    }

"match_bool_prefix"查询支持"匹配"查询所述的"minimum_should_match"和"运算符"参数，将设置应用于构造的"bool"查询。在大多数情况下，构造的"bool"查询中的子句数将是分析查询文本生成的项数。

"模糊性"、"prefix_length"、"max_expansions"、"fuzzy_transpositions"和"fuzzy_rewrite"参数可以应用于为除最终术语之外的所有术语构造的"term"子查询。它们对为最终术语构造的前缀查询没有任何影响。

[« Match query](query-dsl-match-query.md) [Match phrase query »](query-dsl-
match-query-phrase.md)
