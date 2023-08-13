

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Date/Time and Interval Functions and Operators](sql-functions-
datetime.md) [Mathematical Functions »](sql-functions-math.md)

## 全文搜索函数

执行全文搜索时应使用搜索函数，即在使用"MATCH"或"QUERY"谓词时。在所谓的搜索上下文之外，这些函数将返回默认值，例如"0"或"NULL"。

Elasticsearch SQL 根据评分需求优化针对 Elasticsearch 执行的所有查询。在搜索请求中使用"track_scores"或禁用分数计算的"_doc"排序，Elasticsearch SQL 指示 Elasticsearch 在不需要分数时不要计算分数。例如，每次在 SQL 查询中遇到"SCORE()"函数时，都会计算分数。

###'匹配'

**Synopsis:**

    
    
    MATCH(
        field_exp,   __constant_exp __[, options]) __

**输入**：

__

|

要匹配的字段 ---|--- __

|

匹配文本 __

|

附加参数;可选**描述**：一个全文搜索选项，以谓词的形式，在Elasticsearch SQL中可用，使用户可以控制强大的匹配和multi_match Elasticsearch查询。

第一个参数是要匹配的一个或多个字段。如果它只接收一个值，Elasticsearch SQL将使用"匹配"查询来执行搜索：

    
    
    SELECT author, name FROM library WHERE MATCH(author, 'frank');
    
        author     |       name
    ---------------+-------------------
    Frank Herbert  |Dune
    Frank Herbert  |Dune Messiah
    Frank Herbert  |Children of Dune
    Frank Herbert  |God Emperor of Dune

但是，它也可以接收字段列表及其相应的可选"boost"值。在这种情况下，Elasticsearch SQL 将使用"multi_match"查询来匹配文档：

    
    
    SELECT author, name, SCORE() FROM library WHERE MATCH('author^2,name^5', 'frank dune');
    
        author     |       name        |    SCORE()
    ---------------+-------------------+---------------
    Frank Herbert  |Dune               |11.443176
    Frank Herbert  |Dune Messiah       |9.446629
    Frank Herbert  |Children of Dune   |8.043278
    Frank Herbert  |God Emperor of Dune|7.0029488

Elasticsearch 中的"multi_match"查询可以选择按字段提升，使用"^"字符为正在搜索的字段提供优先权重(在评分方面)。在上面的示例中，在两个字段中搜索"坦率沙丘"文本时，"姓名"字段在最终分数中的权重大于"作者"字段。

上面的两个选项都可以与"MATCH()"谓词的可选第三个参数结合使用，其中可以为"match"或"""multi_match"查询指定其他配置参数(用分号";"分隔)。例如：

    
    
    SELECT author, name, SCORE() FROM library WHERE MATCH(name, 'to the star', 'operator=OR;fuzziness=AUTO:1,5;minimum_should_match=1')
    ORDER BY SCORE() DESC LIMIT 2;
    
         author      |                name                |    SCORE()
    -----------------+------------------------------------+---------------
    Douglas Adams    |The Hitchhiker's Guide to the Galaxy|3.1756816
    Peter F. Hamilton|Pandora's Star                      |3.0997515

单字段"MATCH()"变体(对于"match"Elasticsearch查询)允许的可选参数是："分析器"，"auto_generate_synonyms_phrase_query"，"宽松"，"模糊"，"fuzzy_transpositions"，"fuzzy_rewrite"，"minimum_should_match"，"运算符"，"max_expansions"，"prefix_length"。

多字段"MATCH()"变体(用于"multi_match"Elasticsearch查询)允许的可选参数为："分析器"，"auto_generate_synonyms_phrase_query"，"宽松"，"模糊"，"fuzzy_transpositions"，"fuzzy_rewrite"，"minimum_should_match"，"运算符"，"max_expansions"，"prefix_length"，"slop"，"tie_breaker"，"type"。

###'查询'

**Synopsis:**

    
    
    QUERY(
        constant_exp __[, options]) __

**输入**：

__

|

查询文本 ---|--- __

|

附加参数;可选**描述**：就像"MATCH"一样，"QUERY"是一个全文搜索谓词，它允许用户控制Elasticsearch中的query_string查询。

第一个参数基本上是将按原样传递给"query_string"查询的输入，这意味着"query_string"在其"查询"字段中接受的任何内容也可以在此处使用：

    
    
    SELECT author, name, SCORE() FROM library WHERE QUERY('name:dune');
    
        author     |       name        |    SCORE()
    ---------------+-------------------+---------------
    Frank Herbert  |Dune               |2.2886353
    Frank Herbert  |Dune Messiah       |1.8893257
    Frank Herbert  |Children of Dune   |1.6086556
    Frank Herbert  |God Emperor of Dune|1.4005898

一个更高级的例子，展示了"query_string"支持的更多功能，当然可以使用Elasticsearch SQL：

    
    
    SELECT author, name, page_count, SCORE() FROM library WHERE QUERY('_exists_:"author" AND page_count:>200 AND (name:/star.*/ OR name:duna~)');
    
          author      |       name        |  page_count   |    SCORE()
    ------------------+-------------------+---------------+---------------
    Frank Herbert     |Dune               |604            |3.7164764
    Frank Herbert     |Dune Messiah       |331            |3.4169943
    Frank Herbert     |Children of Dune   |408            |3.2064917
    Frank Herbert     |God Emperor of Dune|454            |3.0504425
    Peter F. Hamilton |Pandora's Star     |768            |3.0
    Robert A. Heinlein|Starship Troopers  |335            |3.0

上面的查询使用"_exists_"查询来选择在"作者"字段中具有值的文档，"page_count"的范围查询以及"name"字段的正则表达式和模糊查询。

如果需要自定义"query_string"公开的各种配置选项，可以使用第二个 _optional_ 参数来完成。可以用分号";"分隔指定多个设置：

    
    
    SELECT author, name, SCORE() FROM library WHERE QUERY('dune god', 'default_operator=and;default_field=name');
    
        author     |       name        |    SCORE()
    ---------------+-------------------+---------------
    Frank Herbert  |God Emperor of Dune|3.6984892

"QUERY()"允许的可选参数包括："allow_leading_wildcard"、"analyze_wildcard"、"分析器"、"auto_generate_synonyms_phrase_query"、"default_field"、"default_operator"、"enable_position_increments"、"转义"、"模糊"、"fuzzy_max_expansions"、"fuzzy_prefix_length"、"fuzzy_rewrite"、"fuzzy_transpositions"、"宽松"、"max_determinized_states"、"minimum_should_match"、"phrase_slop"、"重写"、"quote_analyzer"、"quote_field_suffix"、"tie_breaker"、"time_区域"、"类型"。

###'分数'

**Synopsis:**

    
    
    SCORE()

**输入** ： _无_

**输出**："双精度"数值

**描述**：返回给定输入与已执行查询的相关性。分数越高，数据越相关。

当在"WHERE"子句中执行多个文本查询时，它们的分数将使用与Elasticsearch的布尔查询相同的规则进行组合。

通常，"SCORE"用于根据查询结果的相关性对查询结果进行排序：

    
    
    SELECT SCORE(), * FROM library WHERE MATCH(name, 'dune') ORDER BY SCORE() DESC;
    
        SCORE()    |    author     |       name        |  page_count   |    release_date
    ---------------+---------------+-------------------+---------------+--------------------
    2.2886353      |Frank Herbert  |Dune               |604            |1965-06-01T00:00:00Z
    1.8893257      |Frank Herbert  |Dune Messiah       |331            |1969-10-15T00:00:00Z
    1.6086556      |Frank Herbert  |Children of Dune   |408            |1976-04-21T00:00:00Z
    1.4005898      |Frank Herbert  |God Emperor of Dune|454            |1981-05-28T00:00:00Z

但是，返回分数而不按其排序是完全可以的：

    
    
    SELECT SCORE() AS score, name, release_date FROM library WHERE QUERY('dune') ORDER BY YEAR(release_date) DESC;
    
         score     |       name        |    release_date
    ---------------+-------------------+--------------------
    1.4005898      |God Emperor of Dune|1981-05-28T00:00:00Z
    1.6086556      |Children of Dune   |1976-04-21T00:00:00Z
    1.8893257      |Dune Messiah       |1969-10-15T00:00:00Z
    2.2886353      |Dune               |1965-06-01T00:00:00Z

[« Date/Time and Interval Functions and Operators](sql-functions-
datetime.md) [Mathematical Functions »](sql-functions-math.md)
