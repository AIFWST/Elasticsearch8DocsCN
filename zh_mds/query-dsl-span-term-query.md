

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Span queries](span-queries.md)

[« Span or query](query-dsl-span-or-query.md) [Span within query »](query-
dsl-span-within-query.md)

## 跨度术语查询

匹配包含术语的范围。span term query映射到Lucene'SpanTermQuery'。下面是一个示例：

    
    
    response = client.search(
      body: {
        query: {
          span_term: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "span_term" : { "user.id" : "kimchy" }
      }
    }

提升也可以与查询相关联：

    
    
    response = client.search(
      body: {
        query: {
          span_term: {
            "user.id": {
              value: 'kimchy',
              boost: 2
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "span_term" : { "user.id" : { "value" : "kimchy", "boost" : 2.0 } }
      }
    }

或：

    
    
    response = client.search(
      body: {
        query: {
          span_term: {
            "user.id": {
              term: 'kimchy',
              boost: 2
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "span_term" : { "user.id" : { "term" : "kimchy", "boost" : 2.0 } }
      }
    }

[« Span or query](query-dsl-span-or-query.md) [Span within query »](query-
dsl-span-within-query.md)
