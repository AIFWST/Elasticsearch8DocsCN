

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Joining queries](joining-queries.md)

[« Has child query](query-dsl-has-child-query.md) [Parent ID query »](query-
dsl-parent-id-query.md)

## 有父查询

返回其联接父文档与提供的查询匹配的子文档。您可以使用联接字段映射在同一索引中的文档之间创建父子关系。

由于它执行联接，因此与其他查询相比，"has_parent"查询速度较慢。其性能会随着匹配父文档数量的增加而降低。搜索中的每个"has_parent"查询都会显著增加查询时间。

### 示例请求

#### 索引设置

若要使用"has_parent"查询，索引必须包含联接字段映射。例如：

    
    
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
            },
            tag: {
              type: 'keyword'
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
          },
          "tag": {
            "type": "keyword"
          }
        }
      }
    }

#### 示例查询

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "has_parent": {
          "parent_type": "parent",
          "query": {
            "term": {
              "tag": {
                "value": "Elasticsearch"
              }
            }
          }
        }
      }
    }

### has_parent"的顶级参数

`parent_type`

     (Required, string) Name of the parent relationship mapped for the [join](parent-join.html "Join field type") field. 
`query`

     (Required, query object) Query you wish to run on parent documents of the `parent_type` field. If a parent document matches the search, the query returns its child documents. 
`score`

    

(可选，布尔值)指示是否将匹配的父文档的相关性分数聚合到其子文档中。默认为"假"。

如果为"false"，则 Elasticsearch 将忽略父文档的相关性分数。Elasticsearch 还为每个子文档分配一个相关性分数，该分数等于"query"的"boost"，默认为"1"。

如果为"true"，则匹配父文档的相关性分数将聚合到其子文档的相关性分数中。

`ignore_unmapped`

    

(可选，布尔值)指示是否忽略未映射的"parent_type"并且不返回任何文档而不是错误。默认为"假"。

如果为"false"，则在取消映射"parent_type"时，Elasticsearch 将返回错误。

您可以使用此参数查询多个可能不包含 'parent_type' 的索引。

###Notes

####Sorting

不能使用标准排序选项对"has_parent"查询的结果进行排序。

如果需要按父文档中的字段对返回的文档进行排序，请使用"function_score"查询并按"_score"排序。例如，以下查询按其父文档的"view_count"字段对返回的文档进行排序。

    
    
    GET /_search
    {
      "query": {
        "has_parent": {
          "parent_type": "parent",
          "score": true,
          "query": {
            "function_score": {
              "script_score": {
                "script": "_score * doc['view_count'].value"
              }
            }
          }
        }
      }
    }

[« Has child query](query-dsl-has-child-query.md) [Parent ID query »](query-
dsl-parent-id-query.md)
