

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Span queries](span-queries.md)

[« Span field masking query](query-dsl-span-field-masking-query.md) [Span
multi-term query »](query-dsl-span-multi-term-query.md)

## 跨度优先查询

匹配范围接近字段的开头。span first query 映射到 Lucene 'SpanFirstQuery'。下面是一个示例：

    
    
    response = client.search(
      body: {
        query: {
          span_first: {
            match: {
              span_term: {
                "user.id": 'kimchy'
              }
            },
            end: 3
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "span_first": {
          "match": {
            "span_term": { "user.id": "kimchy" }
          },
          "end": 3
        }
      }
    }

"match"子句可以是任何其他跨度类型查询。"end"控制比赛中允许的最大结束位置。

[« Span field masking query](query-dsl-span-field-masking-query.md) [Span
multi-term query »](query-dsl-span-multi-term-query.md)
