

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Span queries](span-queries.md)

[« Span first query](query-dsl-span-first-query.md) [Span near query
»](query-dsl-span-near-query.md)

## 跨度多术语查询

"span_multi"查询允许您将"多术语查询"(通配符、模糊、前缀、范围或正则表达式查询之一)包装为"span 查询"，因此可以嵌套。例：

    
    
    response = client.search(
      body: {
        query: {
          span_multi: {
            match: {
              prefix: {
                "user.id": {
                  value: 'ki'
                }
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
        "span_multi": {
          "match": {
            "prefix": { "user.id": { "value": "ki" } }
          }
        }
      }
    }

提升也可以与查询相关联：

    
    
    response = client.search(
      body: {
        query: {
          span_multi: {
            match: {
              prefix: {
                "user.id": {
                  value: 'ki',
                  boost: 1.08
                }
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
        "span_multi": {
          "match": {
            "prefix": { "user.id": { "value": "ki", "boost": 1.08 } }
          }
        }
      }
    }

如果与查询匹配的术语数超过布尔查询限制(默认值为 4096)，则"span_multi"查询将遇到太多子句失败。为了避免无限扩展，您可以将多术语查询的重写方法设置为"top_terms_*"重写。或者，如果您仅在"前缀"查询中使用"span_multi"，则可以改为激活"文本"字段的"index_prefixes"字段选项。这会将字段上的任何前缀查询重写为与索引前缀匹配的单个术语查询。

[« Span first query](query-dsl-span-first-query.md) [Span near query
»](query-dsl-span-near-query.md)
