

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Full text queries](full-text-queries.md)

[« Multi-match query](query-dsl-multi-match-query.md) [Simple query string
query »](query-dsl-simple-query-string-query.md)

## 查询字符串查询

此页包含有关"query_string"查询类型的信息。有关在 Elasticsearch 中运行搜索查询的信息，请参阅搜索您的数据。

使用具有严格语法的分析器，根据提供的查询字符串返回文档。

此查询使用语法根据运算符(如"AND"或"NOT")分析和拆分提供的查询字符串。然后，查询在返回匹配文档之前独立分析每个拆分文本。

您可以使用"query_string"查询创建复杂的搜索，其中包括通配符、跨多个字段的搜索等。虽然是通用的，但查询是严格的，如果查询字符串包含任何无效语法，则会返回错误。

由于它会为任何无效语法返回错误，因此我们不建议对搜索框使用"query_string"查询。

如果不需要支持查询语法，请考虑使用"match"查询。如果需要查询语法的功能，请使用不太严格的"simple_query_string"查询。

### 示例请求

运行以下搜索时，"query_string"查询将"(纽约市)或(大苹果)"分为两部分："纽约市"和"大苹果"。然后，"内容"字段的分析器在返回匹配文档之前将每个部分独立转换为令牌。由于查询语法不使用空格作为运算符，因此"New York City"将按原样传递给分析器。

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            query: '(new york city) OR (big apple)',
            default_field: 'content'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "query": "(new york city) OR (big apple)",
    	      "default_field": "content"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "query": "(new york city) OR (big apple)",
          "default_field": "content"
        }
      }
    }

### query_string"的顶级参数

`query`

     (Required, string) Query string you wish to parse and use for search. See [Query string syntax](query-dsl-query-string-query.html#query-string-syntax "Query string syntax"). 
`default_field`

    

(可选，字符串)如果查询字符串中未提供任何字段，则搜索默认字段。支持通配符 ("*")。

默认为"index.query.default_field"索引设置，默认值为"*"。"*"值提取符合术语查询条件的所有字段，并筛选元数据字段。然后，如果未指定"前缀"，则合并所有提取的字段以构建查询。

在所有符合条件的字段中搜索不包括嵌套文档。使用"嵌套"查询搜索这些文档。

对于具有大量字段的映射，在所有符合条件的字段中搜索可能会很昂贵。

字段数乘以一次可以查询的术语有限制。它由"index.query.bool.max_clause_count"搜索设置定义，默认为4096。

`allow_leading_wildcard`

     (Optional, Boolean) If `true`, the wildcard characters `*` and `?` are allowed as the first character of the query string. Defaults to `true`. 
`analyze_wildcard`

     (Optional, Boolean) If `true`, the query attempts to analyze wildcard terms in the query string. Defaults to `false`. 
`analyzer`

     (Optional, string) [Analyzer](analysis.html "Text analysis") used to convert text in the query string into tokens. Defaults to the [index-time analyzer](specify-analyzer.html#specify-index-time-analyzer "How Elasticsearch determines the index analyzer") mapped for the `default_field`. If no analyzer is mapped, the index's default analyzer is used. 
`auto_generate_synonyms_phrase_query`

     (Optional, Boolean) If `true`, [match phrase](query-dsl-match-query-phrase.html "Match phrase query") queries are automatically created for multi-term synonyms. Defaults to `true`. See [Synonyms and the `query_string` query](query-dsl-query-string-query.html#query-string-synonyms "Synonyms and the query_string query") for an example. 
`boost`

    

(可选，浮动)用于降低或增加查询的相关性分数的浮点数。默认为"1.0"。

提升值相对于默认值"1.0"。介于"0"和"1.0"之间的提升值会降低相关性分数。大于"1.0"的值会增加相关性分数。

`default_operator`

    

(可选，字符串)如果未指定运算符，则用于解释查询字符串中的文本的默认布尔逻辑。有效值为：

"或"(默认)

     For example, a query string of `capital of Hungary` is interpreted as `capital OR of OR Hungary`. 
`AND`

     For example, a query string of `capital of Hungary` is interpreted as `capital AND of AND Hungary`. 

`enable_position_increments`

     (Optional, Boolean) If `true`, enable position increments in queries constructed from a `query_string` search. Defaults to `true`. 
`fields`

    

(可选，字符串数组)要搜索的字段数组。支持通配符("*")。

可以使用此参数查询跨多个字段进行搜索。请参阅搜索多个字段。

`fuzziness`

     (Optional, string) Maximum edit distance allowed for fuzzy matching. For fuzzy syntax, see [Fuzziness](query-dsl-query-string-query.html#query-string-fuzziness "Fuzziness"). 
`fuzzy_max_expansions`

     (Optional, integer) Maximum number of terms to which the query expands for fuzzy matching. Defaults to `50`. 
`fuzzy_prefix_length`

     (Optional, integer) Number of beginning characters left unchanged for fuzzy matching. Defaults to `0`. 
`fuzzy_transpositions`

     (Optional, Boolean) If `true`, edits for fuzzy matching include transpositions of two adjacent characters (ab → ba). Defaults to `true`. 
`lenient`

     (Optional, Boolean) If `true`, format-based errors, such as providing a text value for a [numeric](number.html "Numeric field types") field, are ignored. Defaults to `false`. 
`max_determinized_states`

    

(可选，整数)查询所需的最大自动机状态数。默认值为"10000"。

Elasticsearch在内部使用Apache Lucene来解析正则表达式。Lucene 将每个正则表达式转换为包含许多确定状态的无限自动机。

您可以使用此参数来防止该转换无意中消耗过多资源。您可能需要增加此限制才能运行复杂的正则表达式。

`minimum_should_match`

     (Optional, string) Minimum number of clauses that must match for a document to be returned. See the [`minimum_should_match` parameter](query-dsl-minimum-should-match.html "minimum_should_match parameter") for valid values and more information. See [How `minimum_should_match` works](query-dsl-query-string-query.html#query-string-min-should-match "How minimum_should_match works") for an example. 
`quote_analyzer`

    

(可选，字符串)用于将查询字符串中的带引号的文本转换为标记的分析器。默认为为"default_field"映射的"search_quote_analyzer"。

对于引用的文本，此参数将覆盖"分析器"参数中指定的分析器。

`phrase_slop`

     (Optional, integer) Maximum number of positions allowed between matching tokens for phrases. Defaults to `0`. If `0`, exact phrase matches are required. Transposed terms have a slop of `2`. 
`quote_field_suffix`

    

(可选，字符串)后缀追加到查询字符串中的带引号的文本。

您可以使用此后缀对精确匹配使用不同的分析方法。请参阅将精确搜索与词干分析混合使用。

`rewrite`

     (Optional, string) Method used to rewrite the query. For valid values and more information, see the [`rewrite` parameter](query-dsl-multi-term-rewrite.html "rewrite parameter"). 
`time_zone`

    

(可选，字符串)协调世界时 (UTC) 偏移量或 IANA 时区，用于将查询字符串中的"日期"值转换为 UTC。

有效值为 ISO 8601 UTC 偏移量(例如"+01：00"或"08：00")和 IANA时区 ID(例如"美国/Los_Angeles"。

"time_zone"参数不会影响"now"的日期数学值。"now"始终是 UTC 格式的当前系统时间。但是，"time_zone"参数会转换使用"now"和日期数学舍入计算的日期。例如，"time_zone"参数将转换值"now/d"。

###Notes

#### 查询字符串语法

查询字符串"迷你语言"由查询字符串和"搜索"API 中的"q"查询字符串参数使用。

查询字符串被解析为一系列 _terms_ 和 _运算符_。术语可以是单个单词 - "快速"或"棕色" - 或一个短语，用双引号括起来 - "快速棕色" - 以相同的顺序搜索短语中的所有单词。

运算符允许您自定义搜索 - 可用选项说明如下。

##### 字段名称

您可以在查询语法中指定要搜索的字段：

* 其中"状态"字段包含"活动"状态：活动

* 其中"标题"字段包含"快速"或"棕色"标题：(快速或棕色)

* 其中"作者"字段包含确切的短语"约翰·史密斯"作者："约翰·史密斯"

* 其中"名字"字段包含"Alice"(注意我们需要如何用反斜杠转义空格) first\ name：Alice

* 其中任何字段"book.title"、"book.content"或"book.date"包含"quick"或"brown"(请注意我们需要如何用反斜杠转义"*")：book.\*:(快速或棕色)

* 其中字段"title"具有任何非空值：_exists_：title

#####Wildcards

通配符搜索可以针对单个术语运行，使用"？"替换单个字符，使用"*"替换零个或多个字符：

    
    
    qu?ck bro*

请注意，通配符查询可能会使用大量内存并且性能非常糟糕 - 只需考虑需要查询多少个术语才能匹配查询字符串"a* b* c*"。

纯通配符 '\*' 被重写为"存在"查询以提高效率。因此，通配符"字段：*""将匹配具有空值的文档，如下所示：

    
    
    {
      "field": ""
    }

...如果字段缺失或设置了如下所示的显式空值，则不会匹配：

    
    
    {
      "field": null
    }

在单词开头允许通配符(例如"*ing"')特别繁重，因为索引中的所有术语都需要检查，以防它们匹配。可以通过将"allow_leading_wildcard"设置为"false"来禁用前导通配符。

仅应用在字符级别操作的分析链部分。因此，例如，如果分析器同时执行小写和词干提取，则只会应用小写：对缺少某些字母的单词执行词干提取是错误的。

通过将"analyze_wildcard"设置为 true，将分析以"*"结尾的查询，并通过确保前 N-1 个令牌上的精确匹配和最后一个令牌上的前缀匹配，从不同的令牌中构建布尔查询。

##### 正则表达式

正则表达式模式可以通过用正斜杠 ('"/"') 包装来嵌入查询字符串中：

    
    
    name:/joh?n(ath[oa]n)/

支持的正则表达式语法在_Regular expressionsyntax_中进行了说明。

"allow_leading_wildcard"参数对正则表达式没有任何控制。如下所示的查询字符串将强制 Elasticsearch 访问索引中的每个术语：

    
    
    /.*n/

谨慎使用！

#####Fuzziness

您可以使用"~"运算符运行"模糊"查询：

    
    
    quikc~ brwn~ foks~

对于这些查询，查询字符串将规范化。如果存在，则仅应用分析器中的某些过滤器。有关适用筛选器的列表，请参阅 _规范化程序_。

该查询使用 Damerau-Levenshteindistance 查找最多有两个更改的所有术语，其中更改是插入、删除或替换单个字符，或两个相邻字符的转置。

默认_edit distance_为"2"，但编辑距离"1"应该足以捕获 80% 的人类拼写错误。它可以指定为：

    
    
    quikc~1

### 避免将模糊与通配符混合

_不支持混合模糊和通配符运算符。混合时，不应用其中一个运算符。例如，您可以搜索"app~1"(模糊)或"app*"(通配符)，但搜索"app*~1"不会应用模糊运算符("~1")。

##### 邻近搜索

短语查询(例如"john smith")期望所有术语的顺序完全相同，而邻近查询允许指定的单词进一步分开或以不同的顺序排列。就像模糊查询可以指定单词中字符的最大编辑距离一样，邻近搜索允许我们指定短语中单词的最大编辑距离：

    
    
    "fox quick"~5

字段中的文本越接近查询字符串中指定的原始顺序，该文档的相关性就越高。与上述示例查询相比，短语"快速狐狸"将被认为比"快速棕色狐狸"更相关。

#####Ranges

可以为日期、数字或字符串字段指定范围。包含范围用方括号"[最小到最大]"指定，用大括号"{最小到最大}"指定排除范围。

* 2012年所有日子： 日期：[2012-01-01 TO 2012-12-31]

* 数字 1..5 计数：[1 到 5]

* 介于"alpha"和"omega"之间的标签，不包括"alpha"和"omega"：标签：{alpha TO omega}

* 从 10 开始的数字计数：[10 到 *]

* 2012年之前的日期：{* TO 2012-01-01}

大括号和方括号可以组合：

* 从 1 到但不包括 5 的数字计数：[1 到 5}

一侧无界的范围可以使用以下语法：

    
    
    age:>10
    age:>=10
    age:<10
    age:<=10

要将上限和下限与简化语法相结合，您需要使用"AND"运算符连接两个子句：

    
    
    age:(>=10 AND <20)
    age:(+>=10 +<20)

查询字符串中的范围分析可能很复杂且容易出错。使用显式"范围"查询要可靠得多。

#####Boosting

使用 _boost_ 运算符"^"使一个术语比另一个术语更相关。例如，如果我们想找到所有关于狐狸的文档，但我们对快速狐狸特别感兴趣：

    
    
    quick^2 fox

默认的"boost"值为 1，但可以是任何正浮点数。0 到 1 之间的提升会降低相关性。

提升也可以应用于短语或组：

    
    
    "john smith"^2   (foo bar)^4

##### 布尔运算符

默认情况下，只要一个术语匹配，所有术语都是可选的。搜索"foo bar baz"将找到包含一个或多个"foo"或"bar"或"baz"的任何文档。我们已经讨论了上面的"default_operator"，它允许您强制所有术语都是必需的，但也有 _boolean运算符_，可以在查询字符串本身中使用以提供更多控制。

首选运算符是"+"(此术语 **必须** 存在)和"-"(此术语 **不得** 存在)。所有其他术语都是可选的。例如，此查询：

    
    
    quick brown +fox -news

声明：

* "狐狸"必须存在 * "新闻"不得存在 * "快速"和"棕色"是可选的 - 它们的存在增加了相关性

熟悉的布尔运算符"AND"、"OR"和"NOT"(也写为"&&"、"||"和"！")也受支持，但请注意它们不遵循通常的优先级规则，因此每当多个运算符一起使用时，都应使用括号。例如，可以将前面的查询重写为：

"((快速和狐狸)或(棕色和狐狸)或狐狸)而不是新闻"

     This form now replicates the logic from the original query correctly, but the relevance scoring bears little resemblance to the original. 

相比之下，使用"match"查询重写的同一查询如下所示：

    
    
    {
        "bool": {
            "must":     { "match": "fox"         },
            "should":   { "match": "quick brown" },
            "must_not": { "match": "news"        }
        }
    }

#####Grouping

多个术语或子句可以用括号组合在一起，以形成子查询：

    
    
    (quick OR brown) AND fox

组可用于定位特定字段，或提升子查询的结果：

    
    
    status:(active OR pending) title:(full text search)^2

##### 保留字符

如果您需要使用任何在查询本身中充当运算符的字符(而不是运算符)，则应使用前导反斜杠对其进行转义。例如，要搜索"(1+1)=2"，您需要将查询编写为"\(1\+1\)\=2"。将 JSON 用于请求正文时，需要两个前面的反斜杠 ('\\');反斜杠是 JSON 字符串中的保留转义字符。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          query_string: {
            query: 'kimchy\\!',
            fields: [
              'user.id'
            ]
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "query" : {
        "query_string" : {
          "query" : "kimchy\\!",
          "fields"  : ["user.id"]
        }
      }
    }

保留字符为："+ - = &&||> < !( ) { } [ ] ^ " ~ * ? : \ /`

未能正确转义这些特殊字符可能会导致语法错误，从而阻止查询运行。

"<"和">"根本无法逃脱。防止它们尝试创建范围查询的唯一方法是将它们从查询中完全删除。

##### 空格和空查询

空格不被视为运算符。

如果查询字符串为空或仅包含空格，则查询将生成空结果集。

##### 避免对嵌套文档使用"query_string"查询

"query_string"搜索不会返回嵌套文档。要搜索嵌套文档，请使用"嵌套"查询。

##### 搜索多个字段

您可以使用"字段"参数对多个字段执行"query_string"搜索。

对多个字段运行"query_string"查询的想法是将每个查询词扩展为 OR 子句，如下所示：

    
    
    field1:query_term OR field2:query_term | ...

例如，以下查询

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            fields: [
              'content',
              'name'
            ],
            query: 'this AND that'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "fields": [
    	        "content",
    	        "name"
    	      ],
    	      "query": "this AND that"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "fields": [ "content", "name" ],
          "query": "this AND that"
        }
      }
    }

匹配相同的单词

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            query: '(content:this OR name:this) AND (content:that OR name:that)'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "query": "(content:this OR name:this) AND (content:that OR name:that)"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "query": "(content:this OR name:this) AND (content:that OR name:that)"
        }
      }
    }

由于多个查询是从单个搜索词生成的，因此使用带有"tie_breaker"的"dis_max"查询自动组合它们。例如(使用"^5"表示法将"名称"提升 5)：

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            fields: [
              'content',
              'name^5'
            ],
            query: 'this AND that OR thus',
            tie_breaker: 0
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "fields": [
    	        "content",
    	        "name^5"
    	      ],
    	      "query": "this AND that OR thus",
    	      "tie_breaker": 0
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string" : {
          "fields" : ["content", "name^5"],
          "query" : "this AND that OR thus",
          "tie_breaker" : 0
        }
      }
    }

简单的通配符也可用于搜索文档的特定内部元素。例如，如果我们有一个包含多个字段的"city"对象(或带有字段的内在对象)，我们可以自动搜索所有"city"字段：

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            fields: [
              'city.*'
            ],
            query: 'this AND that OR thus'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "fields": [
    	        "city.*"
    	      ],
    	      "query": "this AND that OR thus"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string" : {
          "fields" : ["city.*"],
          "query" : "this AND that OR thus"
        }
      }
    }

另一种选择是在查询字符串本身中提供通配符字段搜索(正确转义"*"符号)，例如："city.\*：something"：

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            query: 'city.\\*:(this AND that OR thus)'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "query": "city.\\*:(this AND that OR thus)"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string" : {
          "query" : "city.\\*:(this AND that OR thus)"
        }
      }
    }

由于"\"(反斜杠)是 json 字符串中的一个特殊字符，因此需要对其进行转义，因此上述"query_string"中的两个反斜杠。

fields 参数还可以包括基于模式的字段名称，允许自动扩展到相关字段(动态引入的字段包括)。例如：

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            fields: [
              'content',
              'name.*^5'
            ],
            query: 'this AND that OR thus'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "fields": [
    	        "content",
    	        "name.*^5"
    	      ],
    	      "query": "this AND that OR thus"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string" : {
          "fields" : ["content", "name.*^5"],
          "query" : "this AND that OR thus"
        }
      }
    }

##### 多个字段搜索的其他参数

对多个字段运行"query_string"查询时，支持以下附加参数。

`type`

    

(可选，字符串)确定查询如何匹配文档并对其进行评分。有效值为：

"best_fields"(默认)

     Finds documents which match any field and uses the highest [`_score`](query-filter-context.html#relevance-scores "Relevance scores") from any matching field. See [`best_fields`](query-dsl-multi-match-query.html#type-best-fields "best_fields"). 
`bool_prefix`

     Creates a `match_bool_prefix` query on each field and combines the `_score` from each field. See [`bool_prefix`](query-dsl-multi-match-query.html#type-bool-prefix "bool_prefix"). 
`cross_fields`

     Treats fields with the same `analyzer` as though they were one big field. Looks for each word in **any** field. See [`cross_fields`](query-dsl-multi-match-query.html#type-cross-fields "cross_fields"). 
`most_fields`

     Finds documents which match any field and combines the `_score` from each field. See [`most_fields`](query-dsl-multi-match-query.html#type-most-fields "most_fields"). 
`phrase`

     Runs a `match_phrase` query on each field and uses the `_score` from the best field. See [`phrase` and `phrase_prefix`](query-dsl-multi-match-query.html#type-phrase "phrase and phrase_prefix"). 
`phrase_prefix`

     Runs a `match_phrase_prefix` query on each field and uses the `_score` from the best field. See [`phrase` and `phrase_prefix`](query-dsl-multi-match-query.html#type-phrase "phrase and phrase_prefix"). 

注意：根据"类型"值，可以使用其他顶级"multi_match"参数。

#### 同义词和"query_string"查询

"query_string"查询支持使用thesynonym_graph令牌筛选器进行多术语同义词扩展。使用此筛选器时，分析器将为每个多术语同义词创建一个短语查询。例如，以下同义词："ny，New York"将产生：

'(纽约或("纽约"))"

也可以将多术语同义词与连词匹配：

    
    
    $params = [
        'body' => [
            'query' => [
                'query_string' => [
                    'default_field' => 'title',
                    'query' => 'ny city',
                    'auto_generate_synonyms_phrase_query' => false,
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "query_string": {
                    "default_field": "title",
                    "query": "ny city",
                    "auto_generate_synonyms_phrase_query": False,
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            default_field: 'title',
            query: 'ny city',
            auto_generate_synonyms_phrase_query: false
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "default_field": "title",
    	      "query": "ny city",
    	      "auto_generate_synonyms_phrase_query": false
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          query_string: {
            default_field: 'title',
            query: 'ny city',
            auto_generate_synonyms_phrase_query: false
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
       "query": {
           "query_string" : {
               "default_field": "title",
               "query" : "ny city",
               "auto_generate_synonyms_phrase_query" : false
           }
       }
    }

上面的示例创建了一个布尔查询：

"(纽约或(纽约和约克))城市"

将带有术语"ny"或连词"New AND York"的文档匹配。默认情况下，参数"auto_generate_synonyms_phrase_query"设置为"true"。

#### "minimum_should_match"的工作原理

"query_string"围绕每个运算符拆分查询，为整个输入创建一个布尔查询。可以使用"minimum_should_match"来控制生成的查询中应匹配的"should"子句数。

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            fields: [
              'title'
            ],
            query: 'this that thus',
            minimum_should_match: 2
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "fields": [
    	        "title"
    	      ],
    	      "query": "this that thus",
    	      "minimum_should_match": 2
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "fields": [
            "title"
          ],
          "query": "this that thus",
          "minimum_should_match": 2
        }
      }
    }

上面的示例创建了一个布尔查询：

'(标题：这个标题：那个标题：因此)~2'

将文档与单个字段"标题"中至少有两个术语"这个"、"那个"或"因此"匹配。

#### "minimum_should_match"如何用于多个字段

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            fields: [
              'title',
              'content'
            ],
            query: 'this that thus',
            minimum_should_match: 2
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "fields": [
    	        "title",
    	        "content"
    	      ],
    	      "query": "this that thus",
    	      "minimum_should_match": 2
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "fields": [
            "title",
            "content"
          ],
          "query": "this that thus",
          "minimum_should_match": 2
        }
      }
    }

上面的示例创建了一个布尔查询：

'((内容：此内容：该内容：因此) |(标题：这个标题：那个标题：因此))`

这将文档与"标题"和"内容"字段上的析取最大值匹配。此处无法应用"minimum_should_match"参数。

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            fields: [
              'title',
              'content'
            ],
            query: 'this OR that OR thus',
            minimum_should_match: 2
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "fields": [
    	        "title",
    	        "content"
    	      ],
    	      "query": "this OR that OR thus",
    	      "minimum_should_match": 2
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "fields": [
            "title",
            "content"
          ],
          "query": "this OR that OR thus",
          "minimum_should_match": 2
        }
      }
    }

添加显式运算符会强制将每个术语视为单独的子句。

上面的示例创建了一个布尔查询：

'((内容：这个 | 标题：这个) (内容：那个 | 标题：那个) (内容：因此 |标题：因此))~2'

这将匹配具有三个"应该"子句中至少两个的文档，每个子句都由每个项的字段上的析取最大值组成。

#### "minimum_should_match"如何用于跨字段搜索

"type"字段中的"cross_fields"值表示在分析输入时将具有相同分析器的字段分组在一起。

    
    
    response = client.search(
      body: {
        query: {
          query_string: {
            fields: [
              'title',
              'content'
            ],
            query: 'this OR that OR thus',
            type: 'cross_fields',
            minimum_should_match: 2
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "query_string": {
    	      "fields": [
    	        "title",
    	        "content"
    	      ],
    	      "query": "this OR that OR thus",
    	      "type": "cross_fields",
    	      "minimum_should_match": 2
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "query_string": {
          "fields": [
            "title",
            "content"
          ],
          "query": "this OR that OR thus",
          "type": "cross_fields",
          "minimum_should_match": 2
        }
      }
    }

上面的示例创建了一个布尔查询：

'(blended(terms：[field2：this， field1：this]) blended(terms：[field2：that，field1：that]) blended(terms：[field2：thus， field1：thus]))~2'

这将匹配具有三个每个术语混合查询中的至少两个的文档。

#### 允许昂贵的查询

查询字符串查询可以在内部转换为"前缀查询"，这意味着如果前缀查询被禁用，如此处所述，查询将不会执行，并且将引发异常。

[« Multi-match query](query-dsl-multi-match-query.md) [Simple query string
query »](query-dsl-simple-query-string-query.md)
