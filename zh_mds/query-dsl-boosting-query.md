

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Compound queries](compound-queries.md)

[« Boolean query](query-dsl-bool-query.md) [Constant score query »](query-
dsl-constant-score-query.md)

## 提升查询

返回与"正"查询匹配的文档，同时降低也与"负"查询匹配的文档的相关性分数。

您可以使用"提升"查询降级某些文档，而不会将其从搜索结果中排除。

### 示例请求

    
    
    response = client.search(
      body: {
        query: {
          boosting: {
            positive: {
              term: {
                text: 'apple'
              }
            },
            negative: {
              term: {
                text: 'pie tart fruit crumble tree'
              }
            },
            negative_boost: 0.5
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "boosting": {
          "positive": {
            "term": {
              "text": "apple"
            }
          },
          "negative": {
            "term": {
              "text": "pie tart fruit crumble tree"
            }
          },
          "negative_boost": 0.5
        }
      }
    }

### 用于"提升"的顶级参数

`positive`

     (Required, query object) Query you wish to run. Any returned documents must match this query. 
`negative`

    

(必需，查询对象)用于降低匹配文档的相关度分数的查询。

如果返回的文档与"正"查询和此查询匹配，则"提升"查询将按如下方式计算文档的最终相关性分数：

1. 从"正面"查询中获取原始相关性分数。  2. 将分数乘以"negative_boost"值。

`negative_boost`

     (Required, float) Floating point number between `0` and `1.0` used to decrease the [relevance scores](query-filter-context.html#relevance-scores "Relevance scores") of documents matching the `negative` query. 

[« Boolean query](query-dsl-bool-query.md) [Constant score query »](query-
dsl-constant-score-query.md)
