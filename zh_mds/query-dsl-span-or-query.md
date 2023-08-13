

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Span queries](span-queries.md)

[« Span not query](query-dsl-span-not-query.md) [Span term query »](query-
dsl-span-term-query.md)

## 跨度或查询

匹配其范围子句的并集。span 或查询映射到 Lucene'SpanOrQuery'。下面是一个示例：

    
    
    response = client.search(
      body: {
        query: {
          span_or: {
            clauses: [
              {
                span_term: {
                  field: 'value1'
                }
              },
              {
                span_term: {
                  field: 'value2'
                }
              },
              {
                span_term: {
                  field: 'value3'
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
        "span_or" : {
          "clauses" : [
            { "span_term" : { "field" : "value1" } },
            { "span_term" : { "field" : "value2" } },
            { "span_term" : { "field" : "value3" } }
          ]
        }
      }
    }

"子句"元素是一个或多个其他跨度类型查询的列表。

[« Span not query](query-dsl-span-not-query.md) [Span term query »](query-
dsl-span-term-query.md)
