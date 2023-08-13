

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Joining queries](joining-queries.md)

[« Nested query](query-dsl-nested-query.md) [Has parent query »](query-dsl-
has-parent-query.md)

## 有子查询

返回其联接子文档与提供的查询匹配的父文档。您可以使用联接字段映射在同一索引中的文档之间创建父子关系。

因为它执行联接，所以与其他查询相比，"has_child"速度较慢。其性能会随着指向唯一父文档的匹配子文档数量的增加而降低。搜索中的每个"has_child"查询都会显著增加查询时间。

如果关心查询性能，请不要使用此查询。如果需要使用"has_child"查询，请尽可能少使用它。

### 示例请求

#### 索引设置

若要使用"has_child"查询，索引必须包含联接字段映射。例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            "my-join-field": {
              type: 'join',
              relations: {
                parent: 'child'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "mappings": {
        "properties": {
          "my-join-field": {
            "type": "join",
            "relations": {
              "parent": "child"
            }
          }
        }
      }
    }

#### 示例查询

    
    
    GET /_search
    {
      "query": {
        "has_child": {
          "type": "child",
          "query": {
            "match_all": {}
          },
          "max_children": 10,
          "min_children": 2,
          "score_mode": "min"
        }
      }
    }

### has_child"的顶级参数

`type`

     (Required, string) Name of the child relationship mapped for the [join](parent-join.html "Join field type") field. 
`query`

     (Required, query object) Query you wish to run on child documents of the `type` field. If a child document matches the search, the query returns the parent document. 
`ignore_unmapped`

    

(可选，布尔值)指示是否忽略未映射的"类型"并且不返回任何文档而不是错误。默认为"假"。

如果为"false"，则在取消映射"type"时，Elasticsearch 将返回错误。

您可以使用此参数查询可能不包含"type"的多个索引。

`max_children`

     (Optional, integer) Maximum number of child documents that match the `query` allowed for a returned parent document. If the parent document exceeds this limit, it is excluded from the search results. 
`min_children`

     (Optional, integer) Minimum number of child documents that match the `query` required to match the query for a returned parent document. If the parent document does not meet this limit, it is excluded from the search results. 
`score_mode`

    

(可选，字符串)指示匹配子文档的分数如何影响根父文档的相关性分数。有效值为：

"无"(默认)

     Do not use the relevance scores of matching child documents. The query assigns parent documents a score of `0`. 
`avg`

     Use the mean relevance score of all matching child documents. 
`max`

     Uses the highest relevance score of all matching child documents. 
`min`

     Uses the lowest relevance score of all matching child documents. 
`sum`

     Add together the relevance scores of all matching child documents. 

###Notes

####Sorting

不能使用标准排序选项对"has_child"查询的结果进行排序。

如果需要按子文档中的字段对返回的文档进行排序，请使用"function_score"查询并按"_score"排序。例如，以下查询按其子文档的"click_count"字段对返回的文档进行排序。

    
    
    GET /_search
    {
      "query": {
        "has_child": {
          "type": "child",
          "query": {
            "function_score": {
              "script_score": {
                "script": "_score * doc['click_count'].value"
              }
            }
          },
          "score_mode": "max"
        }
      }
    }

[« Nested query](query-dsl-nested-query.md) [Has parent query »](query-dsl-
has-parent-query.md)
