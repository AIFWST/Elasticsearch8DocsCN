

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Joining queries](joining-queries.md)

[« Has parent query](query-dsl-has-parent-query.md) [Match all query
»](query-dsl-match-all-query.md)

## 家长 ID 查询

返回联接到特定父文档的子文档。可以使用联接字段映射在同一索引中的文档之间创建父子关系。

### 示例请求

#### 索引设置

要使用"parent_id"查询，索引必须包含联接字段映射。若要了解如何为"parent_id"查询设置索引，请尝试以下示例。

1. 使用联接字段映射创建索引。           响应 = client.index.create( index： 'my-index-000001'， body： { mappings： { properties： { "my-join-field"： { type： 'join'， relations： { "my-parent"： 'my-child' } } } } } ) put response PUT /my-index-000001 { "mappings"： { "properties"： { "my-join-field"： { "type"： "join"， "relations"： {             "我的父母"： "我的孩子" } } } } }

2. 索引 ID 为"1"的父文档。           响应 = client.index( index： 'my-index-000001'， id： 1， refresh： true， body： { text： 'This is a parent document.'， "my-join-field"： 'my-parent' } ) put response PUT /my-index-000001/_doc/1？refresh { "text"： "This is a parent document."， "my-join-field"： "my-parent" }

3. 为父文档的子文档编制索引。           PUT /my-index-000001/_doc/2？routeing=1&refresh { "text"： "This is a child document."， "my-join-field"： { "name"： "my-child"， "parent"： "1" } }

#### 示例查询

以下搜索返回 ID 为"1"的父文档的子文档。

    
    
    GET /my-index-000001/_search
    {
      "query": {
          "parent_id": {
              "type": "my-child",
              "id": "1"
          }
      }
    }

### parent_id"的顶级参数

`type`

     (Required, string) Name of the child relationship mapped for the [join](parent-join.html "Join field type") field. 
`id`

     (Required, string) ID of the parent document. The query will return child documents of this parent document. 
`ignore_unmapped`

    

(可选，布尔值)指示是否忽略未映射的"类型"并且不返回任何文档而不是错误。默认为"假"。

如果为"false"，则在取消映射"type"时，Elasticsearch 将返回错误。

您可以使用此参数查询可能不包含"type"的多个索引。

[« Has parent query](query-dsl-has-parent-query.md) [Match all query
»](query-dsl-match-all-query.md)
