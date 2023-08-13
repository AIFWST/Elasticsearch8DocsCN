

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Span queries](span-queries.md)

[« Span queries](span-queries.md) [Span field masking query »](query-dsl-
span-field-masking-query.md)

## 跨度包含查询

返回包含另一个范围查询的匹配项。包含查询的跨度映射到 Lucene 'SpanContainingQuery'。下面是一个示例：

    
    
    response = client.search(
      body: {
        query: {
          span_containing: {
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
        "span_containing": {
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

"大"和"小"子句可以是任何跨度类型查询。返回包含来自"小"的匹配项的"大"匹配范围。

[« Span queries](span-queries.md) [Span field masking query »](query-dsl-
span-field-masking-query.md)
