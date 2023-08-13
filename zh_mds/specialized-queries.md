

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Span within query](query-dsl-span-within-query.md) [Distance feature
query »](query-dsl-distance-feature-query.md)

## 专用查询

此组包含不适合其他组的查询：

"distance_feature"查询

     A query that computes scores based on the dynamically computed distances between the origin and documents' `date`, `date_nanos`, and `geo_point` fields. It is able to efficiently skip non-competitive hits. 
[`more_like_this` query](query-dsl-mlt-query.html "More like this query")

     This query finds documents which are similar to the specified text, document, or collection of documents. 
[`percolate` query](query-dsl-percolate-query.html "Percolate query")

     This query finds queries that are stored as documents that match with the specified document. 
[`rank_feature` query](query-dsl-rank-feature-query.html "Rank feature query")

     A query that computes scores based on the values of numeric features and is able to efficiently skip non-competitive hits. 
[`script` query](query-dsl-script-query.html "Script query")

     This query allows a script to act as a filter. Also see the [`function_score` query](query-dsl-function-score-query.html "Function score query"). 
[`script_score` query](query-dsl-script-score-query.html "Script score query")

     A query that allows to modify the score of a sub-query with a script. 
[`wrapper` query](query-dsl-wrapper-query.html "Wrapper query")

     A query that accepts other queries as json or yaml string. 
[`pinned` query](query-dsl-pinned-query.html "Pinned Query")

     A query that promotes selected documents over others matching a given query. 

[« Span within query](query-dsl-span-within-query.md) [Distance feature
query »](query-dsl-distance-feature-query.md)
