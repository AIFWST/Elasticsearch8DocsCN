

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Span queries](span-queries.md)

[« Span multi-term query](query-dsl-span-multi-term-query.md) [Span not
query »](query-dsl-span-not-query.md)

## 跨度近查询

匹配彼此接近的跨度。可以指定 _slop_ ，干预不匹配位置的最大数量，以及是否需要按顺序匹配。span near query映射到Lucene 'SpanNearQuery'。下面是一个示例：

    
    
    response = client.search(
      body: {
        query: {
          span_near: {
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
            ],
            slop: 12,
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
            { "span_term": { "field": "value1" } },
            { "span_term": { "field": "value2" } },
            { "span_term": { "field": "value3" } }
          ],
          "slop": 12,
          "in_order": false
        }
      }
    }

"子句"元素是一个或多个其他跨度类型查询的列表，"slop"控制允许的最大干预不匹配位置数。

[« Span multi-term query](query-dsl-span-multi-term-query.md) [Span not
query »](query-dsl-span-not-query.md)
