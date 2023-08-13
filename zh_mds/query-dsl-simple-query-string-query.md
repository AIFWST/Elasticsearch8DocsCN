

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Full text queries](full-text-queries.md)

[« Query string query](query-dsl-query-string-query.md) [Geo queries »](geo-
queries.md)

## 简单查询字符串查询

使用具有有限但容错语法的分析器，基于提供的查询字符串返回文档。

此查询使用简单的语法来分析提供的查询字符串，并将其拆分为基于特殊运算符的术语。然后，查询在返回匹配文档之前独立分析每个术语。

虽然其语法比"query_string"查询更受限制，但"simple_query_string"查询不会返回无效语法的错误。相反，它会忽略查询字符串的任何无效部分。

### 示例请求

    
    
    response = client.search(
      body: {
        query: {
          simple_query_string: {
            query: '"fried eggs" +(eggplant | potato) -frittata',
            fields: [
              'title^5',
              'body'
            ],
            default_operator: 'and'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "simple_query_string" : {
            "query": "\"fried eggs\" +(eggplant | potato) -frittata",
            "fields": ["title^5", "body"],
            "default_operator": "and"
        }
      }
    }

### simple_query_string"的顶级参数

`query`

     (Required, string) Query string you wish to parse and use for search. See [Simple query string syntax](query-dsl-simple-query-string-query.html#simple-query-string-syntax "Simple query string syntax"). 
`fields`

    

(可选，字符串数组)要搜索的字段数组。

此字段接受通配符表达式。您还可以使用插入符号 ('^') 表示法提高与特定字段匹配项的相关性分数。有关示例，请参阅"字段"参数中的通配符和每个字段的提升。

默认为"index.query.default_field"索引设置，默认值为"*"。"*"值提取符合术语查询条件的所有字段，并筛选元数据字段。然后，如果未指定"前缀"，则合并所有提取的字段以构建查询。

一次可以查询的字段数有限制。它由"index.query.bool.max_clause_count"搜索设置定义，默认为"1024"。

`default_operator`

    

(可选，字符串)如果未指定运算符，则用于解释查询字符串中的文本的默认布尔逻辑。有效值为：

"或"(默认)

     For example, a query string of `capital of Hungary` is interpreted as `capital OR of OR Hungary`. 
`AND`

     For example, a query string of `capital of Hungary` is interpreted as `capital AND of AND Hungary`. 

`analyze_wildcard`

     (Optional, Boolean) If `true`, the query attempts to analyze wildcard terms in the query string. Defaults to `false`. 
`analyzer`

     (Optional, string) [Analyzer](analysis.html "Text analysis") used to convert text in the query string into tokens. Defaults to the [index-time analyzer](specify-analyzer.html#specify-index-time-analyzer "How Elasticsearch determines the index analyzer") mapped for the `default_field`. If no analyzer is mapped, the index's default analyzer is used. 
`auto_generate_synonyms_phrase_query`

     (Optional, Boolean) If `true`, the parser creates a [`match_phrase`](query-dsl-match-query-phrase.html "Match phrase query") query for each [multi-position token](token-graphs.html#token-graphs-multi-position-tokens "Multi-position tokens"). Defaults to `true`. For examples, see [Multi-position tokens](query-dsl-simple-query-string-query.html#simple-query-string-synonyms "Multi-position tokens"). 
`flags`

     (Optional, string) List of enabled operators for the [simple query string syntax](query-dsl-simple-query-string-query.html#simple-query-string-syntax "Simple query string syntax"). Defaults to `ALL` (all operators). See [Limit operators](query-dsl-simple-query-string-query.html#supported-flags "Limit operators") for valid values. 
`fuzzy_max_expansions`

     (Optional, integer) Maximum number of terms to which the query expands for fuzzy matching. Defaults to `50`. 
`fuzzy_prefix_length`

     (Optional, integer) Number of beginning characters left unchanged for fuzzy matching. Defaults to `0`. 
`fuzzy_transpositions`

     (Optional, Boolean) If `true`, edits for fuzzy matching include transpositions of two adjacent characters (ab → ba). Defaults to `true`. 
`lenient`

     (Optional, Boolean) If `true`, format-based errors, such as providing a text value for a [numeric](number.html "Numeric field types") field, are ignored. Defaults to `false`. 
`minimum_should_match`

     (Optional, string) Minimum number of clauses that must match for a document to be returned. See the [`minimum_should_match` parameter](query-dsl-minimum-should-match.html "minimum_should_match parameter") for valid values and more information. 
`quote_field_suffix`

    

(可选，字符串)后缀追加到查询字符串中的带引号的文本。

您可以使用此后缀对精确匹配使用不同的分析方法。请参阅将精确搜索与词干分析混合使用。

###Notes

#### 简单查询字符串语法

"simple_query_string"查询支持以下运算符：

* "+"表示 AND 操作 * "|" 表示 OR 操作 * "-" 否定单个标记 * "将多个标记括起来以表示用于搜索的短语 * 术语末尾的"*"表示前缀查询 * "("和")"表示优先级 * 单词后的"~N"表示编辑距离(模糊度) * 短语后的"~N"表示数量

若要按字面意思使用这些字符之一，请使用前面的反斜杠 ('\') 对其进行转义。

这些运算符的行为可能因"default_operator"值而异。例如：

    
    
    response = client.search(
      body: {
        query: {
          simple_query_string: {
            fields: [
              'content'
            ],
            query: 'foo bar -baz'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "simple_query_string": {
          "fields": [ "content" ],
          "query": "foo bar -baz"
        }
      }
    }

此搜索旨在仅返回包含"foo"或"bar"的文档，这些文档也不包含"baz"。但是，由于"OR"的"default_operator"，此搜索实际上返回包含"foo"或"bar"的文档以及不包含"baz"的任何文档。若要按预期返回文档，请将查询字符串更改为"foo bar +-baz"。

#### 极限运算符

可以使用"flags"参数来限制简单查询字符串语法支持的运算符。

若要仅显式启用特定运算符，请使用"|"分隔符。例如，"标志"值为"OR|和|PREFIX' 禁用除"OR"、"AND"和"PREFIX"之外的所有运算符。

    
    
    response = client.search(
      body: {
        query: {
          simple_query_string: {
            query: 'foo | bar + baz*',
            flags: 'OR|AND|PREFIX'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "simple_query_string": {
          "query": "foo | bar + baz*",
          "flags": "OR|AND|PREFIX"
        }
      }
    }

##### 有效值

可用的标志包括：

"全部"(默认)

     Enables all optional operators. 
`AND`

     Enables the `+` AND operator. 
`ESCAPE`

     Enables `\` as an escape character. 
`FUZZY`

     Enables the `~N` operator after a word, where `N` is an integer denoting the allowed edit distance for matching. See [Fuzziness](common-options.html#fuzziness "Fuzziness"). 
`NEAR`

     Enables the `~N` operator, after a phrase where `N` is the maximum number of positions allowed between matching tokens. Synonymous to `SLOP`. 
`NONE`

     Disables all operators. 
`NOT`

     Enables the `-` NOT operator. 
`OR`

     Enables the `\|` OR operator. 
`PHRASE`

     Enables the `"` quotes operator used to search for phrases. 
`PRECEDENCE`

     Enables the `(` and `)` operators to control operator precedence. 
`PREFIX`

     Enables the `*` prefix operator. 
`SLOP`

     Enables the `~N` operator, after a phrase where `N` is maximum number of positions allowed between matching tokens. Synonymous to `NEAR`. 
`WHITESPACE`

     Enables whitespace as split characters. 

#### "字段"参数中的通配符和每字段提升

字段可以用通配符指定，例如：

    
    
    response = client.search(
      body: {
        query: {
          simple_query_string: {
            query: 'Will Smith',
            fields: [
              'title',
              '*_name'
            ]
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "simple_query_string" : {
          "query":    "Will Smith",
          "fields": [ "title", "*_name" ] __}
      }
    }

__

|

查询"标题"、"first_name"和"last_name"字段。   ---|--- 可以使用插入符号 ('^') 表示法提升各个字段：

    
    
    response = client.search(
      body: {
        query: {
          simple_query_string: {
            query: 'this is a test',
            fields: [
              'subject^3',
              'message'
            ]
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "simple_query_string" : {
          "query" : "this is a test",
          "fields" : [ "subject^3", "message" ] __}
      }
    }

__

|

"主题"字段的重要性是"消息"字段的三倍。   ---|--- #### 多位置令牌编辑

默认情况下，"simple_query_string"查询分析器为查询字符串中的每个多位置标记创建一个"match_phrase"查询。例如，解析器为多词同义词"ny， New York"创建一个"match_phrase"查询：

'(纽约或("纽约"))"

要将多位置令牌与"AND"连接匹配，请将"auto_generate_synonyms_phrase_query"设置为"false"：

    
    
    response = client.search(
      body: {
        query: {
          simple_query_string: {
            query: 'ny city',
            auto_generate_synonyms_phrase_query: false
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "simple_query_string": {
          "query": "ny city",
          "auto_generate_synonyms_phrase_query": false
        }
      }
    }

对于上面的示例，解析器创建以下"bool"查询：

"(纽约或(纽约和约克))城市)"

此"bool"查询将文档与术语"ny"或连词"newAND york"匹配。

[« Query string query](query-dsl-query-string-query.md) [Geo queries »](geo-
queries.md)
