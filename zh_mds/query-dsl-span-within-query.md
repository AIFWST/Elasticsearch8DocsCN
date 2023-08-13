

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Span queries](span-queries.md)

[« Span term query](query-dsl-span-term-query.md) [Specialized queries
»](specialized-queries.md)

## 跨度查询

返回包含在另一个范围查询中的匹配项。span withinquery映射到Lucene 'SpanWithinQuery'。下面是一个示例：

    
    
    response = client.search(
      body: {
        query: {
          span_within: {
            little: {
              span_term: {
                "field1": 'foo'
              }
            },
            big: {
              span_near: {
                clauses: [
                  {
                    span_term: {
                      "field1": 'bar'
                    }
                  },
                  {
                    span_term: {
                      "field1": 'baz'
                    }
                  }
                ],
                slop: 5,
                in_order: true
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
        "span_within": {
          "little": {
            "span_term": { "field1": "foo" }
          },
          "big": {
            "span_near": {
              "clauses": [
                { "span_term": { "field1": "bar" } },
                { "span_term": { "field1": "baz" } }
              ],
              "slop": 5,
              "in_order": true
            }
          }
        }
      }
    }

"大"和"小"子句可以是任何跨度类型查询。将返回包含在"大"中的"小"中的匹配范围。

[« Span term query](query-dsl-span-term-query.md) [Specialized queries
»](specialized-queries.md)
