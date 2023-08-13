

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« Range query](query-dsl-range-query.md) [Term query »](query-dsl-term-
query.md)

## 正则表达式查询

返回包含与正则表达式匹配的术语的文档。

正则表达式是一种使用占位符字符(称为运算符)匹配数据模式的方法。有关"正则表达式"查询支持的运算符列表，请参阅正则表达式语法。

### 示例请求

以下搜索返回文档，其中"user.id"字段包含以"k"开头并以"y"结尾的任何术语。".*"运算符匹配任何长度的任何字符，包括任何字符。匹配的术语可以包括"ky"、"kay"和"kimchy"。

    
    
    response = client.search(
      body: {
        query: {
          regexp: {
            "user.id": {
              value: 'k.*y',
              flags: 'ALL',
              case_insensitive: true,
              max_determinized_states: 10_000,
              rewrite: 'constant_score'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "regexp": {
          "user.id": {
            "value": "k.*y",
            "flags": "ALL",
            "case_insensitive": true,
            "max_determinized_states": 10000,
            "rewrite": "constant_score"
          }
        }
      }
    }

### "正则表达式"的顶级参数

`<field>`

     (Required, object) Field you wish to search. 

### 参数 '<field>'

`value`

    

(必需，字符串)您希望在提供的 '' 中找到的术语的正则表达式<field>。有关支持的运算符的列表，请参阅正则表达式语法。

默认情况下，正则表达式限制为 1，000 个字符。您可以使用"index.max_regex_length"设置更改此限制。

"regexp"查询的性能可能因提供的正则表达式而异。若要提高性能，请避免使用不带前缀或后缀的通配符模式，例如".*"或".*？+"。

`flags`

     (Optional, string) Enables optional operators for the regular expression. For valid values and more information, see [Regular expression syntax](regexp-syntax.html#regexp-optional-operators "Optional operators"). 
`case_insensitive` [7.10.0]  Added in 7.10.0.

     (Optional, Boolean) Allows case insensitive matching of the regular expression value with the indexed field values when set to true. Default is false which means the case sensitivity of matching depends on the underlying field's mapping. 
`max_determinized_states`

    

(可选，整数)查询所需的最大自动机状态数。默认值为"10000"。

Elasticsearch在内部使用Apache Lucene来解析正则表达式。Lucene 将每个正则表达式转换为包含许多确定状态的无限自动机。

您可以使用此参数来防止该转换无意中消耗过多资源。您可能需要增加此限制才能运行复杂的正则表达式。

`rewrite`

     (Optional, string) Method used to rewrite the query. For valid values and more information, see the [`rewrite` parameter](query-dsl-multi-term-rewrite.html "rewrite parameter"). 

###Notes

#### 允许昂贵的查询

如果"search.allow_expensive_queries"设置为 false，则不会执行正则表达式查询。

[« Range query](query-dsl-range-query.md) [Term query »](query-dsl-term-
query.md)
