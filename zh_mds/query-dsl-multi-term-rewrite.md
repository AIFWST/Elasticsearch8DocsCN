

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« `minimum_should_match` parameter](query-dsl-minimum-should-match.md)
[Regular expression syntax »](regexp-syntax.md)

## '重写'参数

此参数仅适用于专家用户。更改此参数的值可能会影响搜索性能和相关性。

Elasticsearch在内部使用Apache Lucene来支持索引和搜索。在其原始形式中，Lucene 无法执行以下查询：

* "模糊" * "前缀" * "query_string" * "正则表达式" * "通配符"

为了执行它们，Lucene 将这些查询更改为更简单的形式，例如"bool"查询或位集。

"重写"参数确定：

* Lucene 如何计算每个匹配文档的相关度分数 * Lucene 是否将原始查询更改为"布尔"查询或位集 * 如果更改为"布尔"查询，则包含哪些"术语"查询子句

### 有效值

"constant_score"(默认)

     Uses the `constant_score_boolean` method for fewer matching terms. Otherwise, this method finds all matching terms in sequence and returns matching documents using a bit set. 
`constant_score_boolean`

    

为每个文档分配一个与"boost"参数相等的相关性分数。

此方法将原始查询更改为"bool"查询。此"bool"查询包含每个匹配字词的"should"子句和"term"查询。

此方法可能会导致最终的"bool"查询超过"index.query.bool.max_clause_count"设置中的子句限制。如果查询超过此限制，Elasticsearch 将返回错误。

`scoring_boolean`

    

计算每个匹配文档的相关性分数。

此方法将原始查询更改为"bool"查询。此"bool"查询包含每个匹配字词的"should"子句和"term"查询。

此方法可能会导致最终的"bool"查询超过"index.query.bool.max_clause_count"设置中的子句限制。如果查询超过此限制，Elasticsearch 将返回错误。

`top_terms_blended_freqs_N`

    

计算每个匹配文档的相关性分数，就好像所有术语具有相同的频率一样。此频率是所有匹配项的最大频率。

此方法将原始查询更改为"bool"查询。此"bool"查询包含每个匹配字词的"should"子句和"term"查询。

最终的"布尔"查询仅包括对评分最高的"N"项的"术语"查询。

您可以使用此方法避免超出"index.query.bool.max_clause_count"设置中的子句限制。

`top_terms_boost_N`

    

为每个匹配的文档分配一个与"boost"参数相等的相关性分数。

此方法将原始查询更改为"bool"查询。此"bool"查询包含每个匹配字词的"should"子句和"term"查询。

最终的"布尔"查询仅包括前"N"个术语的"术语"查询。

您可以使用此方法避免超出"index.query.bool.max_clause_count"设置中的子句限制。

`top_terms_N`

    

计算每个匹配文档的相关性分数。

此方法将原始查询更改为"bool"查询。此"bool"查询包含每个匹配字词的"should"子句和"term"查询。

最终的"布尔"查询仅包括对评分最高的"N"项的"术语"查询。

您可以使用此方法避免超出"index.query.bool.max_clause_count"设置中的子句限制。

### "重写"参数的性能注意事项

对于大多数用途，我们建议使用"constant_score"、"constant_score_boolean"或"top_terms_boost_N"重写方法。

其他方法计算相关性分数。这些分数计算通常很昂贵，并且不会改善查询结果。

[« `minimum_should_match` parameter](query-dsl-minimum-should-match.md)
[Regular expression syntax »](regexp-syntax.md)
