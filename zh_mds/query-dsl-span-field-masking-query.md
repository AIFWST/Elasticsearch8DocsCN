

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Span queries](span-queries.md)

[« Span containing query](query-dsl-span-containing-query.md) [Span first
query »](query-dsl-span-first-query.md)

## 跨度字段掩码查询

包装器，允许跨度查询通过_谎言_来参与复合单字段跨度查询。span 字段掩码查询映射到 Lucene 的"SpanFieldMaskingQuery"

这可用于支持跨不同字段的"跨度接近"或"跨度或"跨域或"等查询，这通常是不允许的。

当使用多个分析器为同一内容编制索引时，跨度字段掩码查询与**多字段**结合使用非常宝贵。例如，我们可以使用标准分析器将文本分解为单词，然后再次使用英语分析器将单词词根形式。

Example:

    
    
    response = client.search(
      body: {
        query: {
          span_near: {
            clauses: [
              {
                span_term: {
                  text: 'quick brown'
                }
              },
              {
                span_field_masking: {
                  query: {
                    span_term: {
                      "text.stems": 'fox'
                    }
                  },
                  field: 'text'
                }
              }
            ],
            slop: 5,
            in_order: false
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "span_near": {
          "clauses": [
            {
              "span_term": {
                "text": "quick brown"
              }
            },
            {
              "span_field_masking": {
                "query": {
                  "span_term": {
                    "text.stems": "fox"
                  }
                },
                "field": "text"
              }
            }
          ],
          "slop": 5,
          "in_order": false
        }
      }
    }

注意：由于 span 字段掩码查询返回屏蔽字段，因此将使用提供的字段名称的规范进行评分。这可能会导致意外的评分行为。

[« Span containing query](query-dsl-span-containing-query.md) [Span first
query »](query-dsl-span-first-query.md)
