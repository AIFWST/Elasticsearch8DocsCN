

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« Terms set query](query-dsl-terms-set-query.md) [Text expansion query
»](query-dsl-text-expansion-query.md)

## 通配符查询

返回包含与通配符模式匹配的术语的文档。

通配符是匹配一个或多个字符的占位符。例如，"*"通配符匹配零个或多个字符。您可以将通配符运算符与其他字符组合以创建通配符模式。

### 示例请求

以下搜索返回文档，其中"user.id"字段包含以"ki"开头并以"y"结尾的术语。这些匹配的术语可以包括"kiy"、"kity"或"kimchy"。

    
    
    response = client.search(
      body: {
        query: {
          wildcard: {
            "user.id": {
              value: 'ki*y',
              boost: 1,
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
        "wildcard": {
          "user.id": {
            "value": "ki*y",
            "boost": 1.0,
            "rewrite": "constant_score"
          }
        }
      }
    }

### "通配符"的顶级参数

`<field>`

     (Required, object) Field you wish to search. 

### 参数 '<field>'

`boost`

    

(可选，浮动)用于减少或增加查询的相关性分数的浮点数。默认为"1.0"。

您可以使用"boost"参数来调整包含两个或多个查询的搜索的相关性分数。

提升值相对于默认值"1.0"。介于"0"和"1.0"之间的提升值会降低相关性分数。大于"1.0"的值会增加相关性分数。

"case_insensitive" [7.10.0] 在 7.10.0 中添加。

     (Optional, Boolean) Allows case insensitive matching of the pattern with the indexed field values when set to true. Default is false which means the case sensitivity of matching depends on the underlying field's mapping. 
`rewrite`

     (Optional, string) Method used to rewrite the query. For valid values and more information, see the [`rewrite` parameter](query-dsl-multi-term-rewrite.html "rewrite parameter"). 
`value`

    

(必需，字符串)您希望在提供的"'"中找到的术语的通配符模式<field>。

此参数支持两个通配符运算符：

* '？'，匹配任何单个字符 * '*'，可以匹配零个或多个字符，包括空字符

避免以"*"或"？"开头模式。这可能会增加查找匹配字词所需的迭代次数，并降低搜索性能。

`wildcard`

     (Required, string) An alias for the `value` parameter. If you specify both `value` and `wildcard`, the query uses the last one in the request body. 

###Notes

#### 允许昂贵的查询

如果"search.allow_expensive_queries"设置为 false，则不会执行通配符查询。

[« Terms set query](query-dsl-terms-set-query.md) [Text expansion query
»](query-dsl-text-expansion-query.md)
