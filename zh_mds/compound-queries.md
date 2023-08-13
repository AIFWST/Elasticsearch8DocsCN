

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Query and filter context](query-filter-context.md) [Boolean query
»](query-dsl-bool-query.md)

## 复合查询

复合查询包装其他复合查询或叶查询，以合并其结果和分数、更改其行为或从查询切换到筛选上下文。

此组中的查询包括：

"布尔"查询

     The default query for combining multiple leaf or compound query clauses, as `must`, `should`, `must_not`, or `filter` clauses. The `must` and `should` clauses have their scores combined -- the more matching clauses, the better -- while the `must_not` and `filter` clauses are executed in filter context. 
[`boosting` query](query-dsl-boosting-query.html "Boosting query")

     Return documents which match a `positive` query, but reduce the score of documents which also match a `negative` query. 
[`constant_score` query](query-dsl-constant-score-query.html "Constant score
query")

     A query which wraps another query, but executes it in filter context. All matching documents are given the same "constant" `_score`. 
[`dis_max` query](query-dsl-dis-max-query.html "Disjunction max query")

     A query which accepts multiple queries, and returns any documents which match any of the query clauses. While the `bool` query combines the scores from all matching queries, the `dis_max` query uses the score of the single best- matching query clause. 
[`function_score` query](query-dsl-function-score-query.html "Function score
query")

     Modify the scores returned by the main query with functions to take into account factors like popularity, recency, distance, or custom algorithms implemented with scripting. 

[« Query and filter context](query-filter-context.md) [Boolean query
»](query-dsl-bool-query.md)
