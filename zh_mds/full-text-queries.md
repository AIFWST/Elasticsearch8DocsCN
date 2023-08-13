

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Function score query](query-dsl-function-score-query.md) [Intervals query
»](query-dsl-intervals-query.md)

## 全文查询

全文查询使您能够搜索分析的文本字段，例如电子邮件正文。查询字符串使用在索引编制期间应用于字段的同一分析器进行处理。

此组中的查询包括：

"间隔"查询

     A full text query that allows fine-grained control of the ordering and proximity of matching terms. 
[`match` query](query-dsl-match-query.html "Match query")

     The standard query for performing full text queries, including fuzzy matching and phrase or proximity queries. 
[`match_bool_prefix` query](query-dsl-match-bool-prefix-query.html "Match
boolean prefix query")

     Creates a `bool` query that matches each term as a `term` query, except for the last term, which is matched as a `prefix` query 
[`match_phrase` query](query-dsl-match-query-phrase.html "Match phrase query")

     Like the `match` query but used for matching exact phrases or word proximity matches. 
[`match_phrase_prefix` query](query-dsl-match-query-phrase-prefix.html "Match
phrase prefix query")

     Like the `match_phrase` query, but does a wildcard search on the final word. 
[`multi_match` query](query-dsl-multi-match-query.html "Multi-match query")

     The multi-field version of the `match` query. 
[`combined_fields` query](query-dsl-combined-fields-query.html "Combined
fields")

     Matches over multiple fields as if they had been indexed into one combined field. 
[`query_string` query](query-dsl-query-string-query.html "Query string query")

     Supports the compact Lucene [query string syntax](query-dsl-query-string-query.html#query-string-syntax "Query string syntax"), allowing you to specify AND|OR|NOT conditions and multi-field search within a single query string. For expert users only. 
[`simple_query_string` query](query-dsl-simple-query-string-query.html "Simple
query string query")

     A simpler, more robust version of the `query_string` syntax suitable for exposing directly to users. 

[« Function score query](query-dsl-function-score-query.md) [Intervals query
»](query-dsl-intervals-query.md)
