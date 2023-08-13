

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Match all query](query-dsl-match-all-query.md) [Span containing query
»](query-dsl-span-containing-query.md)

## 跨度查询

跨度查询是低级位置查询，它提供对指定术语的顺序和邻近度的专家控制。这些通常用于对法律文件或专利进行非常具体的查询。

只允许在外部跨度查询上设置 boost。复合跨度查询(如 span_near)仅使用内部跨度查询的匹配跨度列表来查找自己的跨度，然后使用它们来生成分数。从不计算内部跨度查询的分数，这就是不允许提升的原因：它们只影响分数的计算方式，而不会影响跨度。

跨度查询不能与非跨度查询混合使用("span_multi"查询除外)。

此组中的查询包括：

"span_containing"查询

     Accepts a list of span queries, but only returns those spans which also match a second span query. 
[`span_field_masking` query](query-dsl-span-field-masking-query.html "Span
field masking query")

     Allows queries like `span-near` or `span-or` across different fields. 
[`span_first` query](query-dsl-span-first-query.html "Span first query")

     Accepts another span query whose matches must appear within the first N positions of the field. 
[`span_multi` query](query-dsl-span-multi-term-query.html "Span multi-term
query")

     Wraps a [`term`](query-dsl-term-query.html "Term query"), [`range`](query-dsl-range-query.html "Range query"), [`prefix`](query-dsl-prefix-query.html "Prefix query"), [`wildcard`](query-dsl-wildcard-query.html "Wildcard query"), [`regexp`](query-dsl-regexp-query.html "Regexp query"), or [`fuzzy`](query-dsl-fuzzy-query.html "Fuzzy query") query. 
[`span_near` query](query-dsl-span-near-query.html "Span near query")

     Accepts multiple span queries whose matches must be within the specified distance of each other, and possibly in the same order. 
[`span_not` query](query-dsl-span-not-query.html "Span not query")

     Wraps another span query, and excludes any documents which match that query. 
[`span_or` query](query-dsl-span-or-query.html "Span or query")

     Combines multiple span queries -- returns documents which match any of the specified queries. 
[`span_term` query](query-dsl-span-term-query.html "Span term query")

     The equivalent of the [`term` query](query-dsl-term-query.html "Term query") but for use with other span queries. 
[`span_within` query](query-dsl-span-within-query.html "Span within query")

     The result from a single span query is returned as long is its span falls within the spans returned by a list of other span queries. 

[« Match all query](query-dsl-match-all-query.md) [Span containing query
»](query-dsl-span-containing-query.md)
