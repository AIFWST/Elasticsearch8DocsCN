

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Tutorial: semantic search with ELSER](semantic-search-elser.md) [Query
and filter context »](query-filter-context.md)

# 查询DSL

Elasticsearch提供了一个基于JSON的完整查询DSL(领域特定语言)来定义查询。将查询 DSL 视为查询的 AST(抽象语法树)，由两种类型的子句组成：

叶查询子句

     Leaf query clauses look for a particular value in a particular field, such as the [`match`](query-dsl-match-query.html "Match query"), [`term`](query-dsl-term-query.html "Term query") or [`range`](query-dsl-range-query.html "Range query") queries. These queries can be used by themselves. 
Compound query clauses

     Compound query clauses wrap other leaf **or** compound queries and are used to combine multiple queries in a logical fashion (such as the [`bool`](query-dsl-bool-query.html "Boolean query") or [`dis_max`](query-dsl-dis-max-query.html "Disjunction max query") query), or to alter their behaviour (such as the [`constant_score`](query-dsl-constant-score-query.html "Constant score query") query). 

查询子句的行为会有所不同，具体取决于它们是在查询上下文还是筛选器上下文中使用。

允许昂贵的查询

    

某些类型的查询由于其实现方式而通常执行缓慢，这可能会影响集群的稳定性。这些查询可以分类如下：

* 需要执行线性扫描以识别匹配项的查询：

    * [`script` queries](query-dsl-script-query.html "Script query")
    * queries on [numeric](number.html "Numeric field types"), [date](date.html "Date field type"), [boolean](boolean.html "Boolean field type"), [ip](ip.html "IP field type"), [geo_point](geo-point.html "Geopoint field type") or [keyword](keyword.html "Keyword type family") fields that are not indexed but have [doc values](doc-values.html "doc_values") enabled 

* 前期成本高的查询：

    * [`fuzzy` queries](query-dsl-fuzzy-query.html "Fuzzy query") (except on [`wildcard`](keyword.html#wildcard-field-type "Wildcard field type") fields) 
    * [`regexp` queries](query-dsl-regexp-query.html "Regexp query") (except on [`wildcard`](keyword.html#wildcard-field-type "Wildcard field type") fields) 
    * [`prefix` queries](query-dsl-prefix-query.html "Prefix query") (except on [`wildcard`](keyword.html#wildcard-field-type "Wildcard field type") fields or those without [`index_prefixes`](index-prefixes.html "index_prefixes")) 
    * [`wildcard` queries](query-dsl-wildcard-query.html "Wildcard query") (except on [`wildcard`](keyword.html#wildcard-field-type "Wildcard field type") fields) 
    * [`range` queries](query-dsl-range-query.html "Range query") on [`text`](text.html "Text type family") and [`keyword`](keyword.html "Keyword type family") fields 

* 联接查询 * 每个文档成本可能较高的查询：

    * [`script_score` queries](query-dsl-script-score-query.html "Script score query")
    * [`percolate` queries](query-dsl-percolate-query.html "Percolate query")

通过将"search.allow_expensive_queries"设置的值设置为"false"(默认为"true")，可以防止此类查询的执行。

[« Tutorial: semantic search with ELSER](semantic-search-elser.md) [Query
and filter context »](query-filter-context.md)
