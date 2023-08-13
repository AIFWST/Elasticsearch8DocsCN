

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Compound queries](compound-queries.md)

[« Constant score query](query-dsl-constant-score-query.md) [Function score
query »](query-dsl-function-score-query.md)

## 析取最大查询

返回与一个或多个包装查询(称为查询子句或子句)匹配的文档。

如果返回的文档与多个查询子句匹配，则"dis_max"查询会为文档分配任何匹配子句中最高的相关性分数，以及任何其他匹配子查询的平局增量。

### 示例请求

    
    
    response = client.search(
      body: {
        query: {
          dis_max: {
            queries: [
              {
                term: {
                  title: 'Quick pets'
                }
              },
              {
                term: {
                  body: 'Quick pets'
                }
              }
            ],
            tie_breaker: 0.7
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "dis_max": {
          "queries": [
            { "term": { "title": "Quick pets" } },
            { "term": { "body": "Quick pets" } }
          ],
          "tie_breaker": 0.7
        }
      }
    }

### dis_max"的顶级参数

`queries`

     (Required, array of query objects) Contains one or more query clauses. Returned documents **must match one or more** of these queries. If a document matches multiple queries, Elasticsearch uses the highest [relevance score](query-filter-context.html "Query and filter context"). 
`tie_breaker`

    

(可选，浮动)介于"0"和"1.0"之间的浮点数，用于提高与多个查询子句匹配的文档的相关度分数。默认为"0.0"。

您可以使用"tie_breaker"值为在多个字段中包含相同术语的文档分配更高的相关性分数，而不是仅在这些多个字段中包含此术语的文档，而不会将其与多个字段中两个不同术语的更好情况混淆。

如果文档匹配多个子句，则"dis_max"查询将按如下方式计算文档的相关性分数：

1. 从得分最高的匹配子句中获取相关性分数。  2. 将任何其他匹配子句的分数乘以"tie_breaker"值。  3. 将最高分添加到乘以的分数中。

如果"tie_breaker"值大于"0.0"，则所有匹配子句计数，但得分最高的子句计数最多。

[« Constant score query](query-dsl-constant-score-query.md) [Function score
query »](query-dsl-function-score-query.md)
