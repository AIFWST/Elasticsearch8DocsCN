

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Shape query](query-dsl-shape-query.md) [Nested query »](query-dsl-nested-
query.md)

## 连接查询

在像Elasticsearch这样的分布式系统中执行完整的SQL风格的连接是非常昂贵的。相反，Elasticsearch提供了两种形式的连接，它们旨在水平扩展。

"嵌套"查询

     Documents may contain fields of type [`nested`](nested.html "Nested field type"). These fields are used to index arrays of objects, where each object can be queried (with the `nested` query) as an independent document. 
[`has_child`](query-dsl-has-child-query.html "Has child query") and
[`has_parent`](query-dsl-has-parent-query.html "Has parent query") queries

     A [`join` field relationship](parent-join.html "Join field type") can exist between documents within a single index. The `has_child` query returns parent documents whose child documents match the specified query, while the `has_parent` query returns child documents whose parent document matches the specified query. 

另请参阅"terms"查询中的术语查找机制，该机制允许您从另一个文档中包含的值构建"terms"查询。

####Notes

##### 允许昂贵的查询

如果"search.allow_expensive_queries"设置为 false，则不会执行联接查询。

[« Shape query](query-dsl-shape-query.md) [Nested query »](query-dsl-nested-
query.md)
