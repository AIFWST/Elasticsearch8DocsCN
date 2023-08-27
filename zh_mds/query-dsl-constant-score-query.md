

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Compound queries](compound-queries.md)

[« Boosting query](query-dsl-boosting-query.md) [Disjunction max query
»](query-dsl-dis-max-query.md)

## 常量分数查询

包装筛选器查询并返回相关性分数等于"boost"参数值的每个匹配文档。

    
    
    response = client.search(
      body: {
        query: {
          constant_score: {
            filter: {
              term: {
                "user.id": 'kimchy'
              }
            },
            boost: 1.2
          }
        }
      }
    )

puts response

    GET /_search
    {
      "query": {
        "constant_score": {
          "filter": {
            "term": { "user.id": "kimchy" }
          },
          "boost": 1.2
        }
      }
    }

### constant_score"的顶级参数

`filter`:
(必需，查询对象)要运行的筛选器查询。任何返回的文档都必须与此查询匹配。

筛选器查询不计算相关性分数。为了提高性能，Elasticsearch 会自动缓存常用的过滤器查询。

`boost`:
（可选，float）浮点数用作与“筛选器”查询匹配的每个文档的常量 [相关性分数](query-filter-context.md)。
默认为“1.0”。

[« Boosting query](uery-dsl-boosting-query.md) [Disjunction max query
»](query-dsl-dis-max-query.md)
