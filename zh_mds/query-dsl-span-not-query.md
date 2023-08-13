

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Span queries](span-queries.md)

[« Span near query](query-dsl-span-near-query.md) [Span or query »](query-
dsl-span-or-query.md)

## 跨度不查询

删除与另一个跨度查询重叠的匹配项，或者在另一个 SpanQuery 之前(由参数"pre"控制)或 y 标记后(由参数"post"控制)的 xtoken 内的匹配项。span not query映射到Lucene 'SpanNotQuery'。下面是一个示例：

    
    
    response = client.search(
      body: {
        query: {
          span_not: {
            include: {
              span_term: {
                "field1": 'hoya'
              }
            },
            exclude: {
              span_near: {
                clauses: [
                  {
                    span_term: {
                      "field1": 'la'
                    }
                  },
                  {
                    span_term: {
                      "field1": 'hoya'
                    }
                  }
                ],
                slop: 0,
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
        "span_not": {
          "include": {
            "span_term": { "field1": "hoya" }
          },
          "exclude": {
            "span_near": {
              "clauses": [
                { "span_term": { "field1": "la" } },
                { "span_term": { "field1": "hoya" } }
              ],
              "slop": 0,
              "in_order": true
            }
          }
        }
      }
    }

"include"和"exclude"子句可以是任何跨度类型查询。"include"子句是筛选其匹配项的跨度查询，而"排除"子句是其匹配项不得与返回的匹配项重叠的跨度查询。

在上面的示例中，所有带有术语 hoya 的文档都会被过滤，但前面有 _la_ 的文档除外。

其他顶级选项：

`pre`

|

如果设置了包含范围之前的令牌数量，则不能与排除范围重叠。默认值为 0。   ---|--- "帖子"

|

如果设置了包含范围之后的令牌数量，则不能与排除范围重叠。默认值为 0。   "远"

|

如果设置了包含范围内的令牌数量，则不能与排除范围重叠。相当于同时设置"前"和"后"。   « 跨度接近查询 跨度或查询 »