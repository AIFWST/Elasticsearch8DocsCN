

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Pinned Query](query-dsl-pinned-query.md) [Exists query »](query-dsl-
exists-query.md)

## 术语级查询

您可以使用**术语级查询**根据结构化数据中的精确值查找文档。结构化数据的示例包括日期范围、IP 地址、价格或产品 ID。

与全文查询不同，术语级查询不分析搜索词。相反，术语级查询与字段中存储的确切术语匹配。

术语级查询仍使用"规范化器"属性规范化"关键字"字段的搜索词。有关更多详细信息，请参阅"规范化器"。

### 术语级查询的类型

"存在"查询

     Returns documents that contain any indexed value for a field. 
[`fuzzy` query](query-dsl-fuzzy-query.html "Fuzzy query")

     Returns documents that contain terms similar to the search term. Elasticsearch measures similarity, or fuzziness, using a [Levenshtein edit distance](https://en.wikipedia.org/wiki/Levenshtein_distance). 
[`ids` query](query-dsl-ids-query.html "IDs")

     Returns documents based on their [document IDs](mapping-id-field.html "_id field"). 
[`prefix` query](query-dsl-prefix-query.html "Prefix query")

     Returns documents that contain a specific prefix in a provided field. 
[`range` query](query-dsl-range-query.html "Range query")

     Returns documents that contain terms within a provided range. 
[`regexp` query](query-dsl-regexp-query.html "Regexp query")

     Returns documents that contain terms matching a [regular expression](https://en.wikipedia.org/wiki/Regular_expression). 
[`term` query](query-dsl-term-query.html "Term query")

     Returns documents that contain an exact term in a provided field. 
[`terms` query](query-dsl-terms-query.html "Terms query")

     Returns documents that contain one or more exact terms in a provided field. 
[`terms_set` query](query-dsl-terms-set-query.html "Terms set query")

     Returns documents that contain a minimum number of exact terms in a provided field. You can define the minimum number of matching terms using a field or script. 
[`wildcard` query](query-dsl-wildcard-query.html "Wildcard query")

     Returns documents that contain terms matching a wildcard pattern. 

[« Pinned Query](query-dsl-pinned-query.md) [Exists query »](query-dsl-
exists-query.md)
