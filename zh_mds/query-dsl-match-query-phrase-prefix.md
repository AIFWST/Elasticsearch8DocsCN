

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Full text queries](full-text-queries.md)

[« Match phrase query](query-dsl-match-query-phrase.md) [Combined fields
»](query-dsl-combined-fields-query.md)

## 匹配短语前缀查询

返回包含所提供文本的单词的文档，按提供的顺序返回。所提供文本的最后一个术语被视为前缀，与以该术语开头的任何单词匹配。

### 示例请求

以下搜索返回在"邮件"字段中包含以"快速棕色 f"开头的短语的文档。

此搜索将匹配"快速棕色狐狸"或"两只快速棕色雪貂"的"消息"值，但不匹配"狐狸快速和棕色"。

    
    
    response = client.search(
      body: {
        query: {
          match_phrase_prefix: {
            message: {
              query: 'quick brown f'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "match_phrase_prefix": {
          "message": {
            "query": "quick brown f"
          }
        }
      }
    }

### match_phrase_prefix"的顶级参数

`<field>`

     (Required, object) Field you wish to search. 

### 参数 '<field>'

`query`

    

(必需，字符串)您希望在提供的""中找到的文本<field>。

"match_phrase_prefix"查询在执行搜索之前将任何提供的文本分析为标记。此文本的最后一个术语被视为前缀，与以该术语开头的任何单词匹配。

`analyzer`

     (Optional, string) [Analyzer](analysis.html "Text analysis") used to convert text in the `query` value into tokens. Defaults to the [index-time analyzer](specify-analyzer.html#specify-index-time-analyzer "How Elasticsearch determines the index analyzer") mapped for the `<field>`. If no analyzer is mapped, the index's default analyzer is used. 
`max_expansions`

     (Optional, integer) Maximum number of terms to which the last provided term of the `query` value will expand. Defaults to `50`. 
`slop`

     (Optional, integer) Maximum number of positions allowed between matching tokens. Defaults to `0`. Transposed terms have a slop of `2`. 
`zero_terms_query`

    

(可选，字符串)指示如果"分析器"删除所有令牌(例如使用"停止"筛选器时)，是否不返回任何文档。有效值为：

"无"(默认)

     No documents are returned if the `analyzer` removes all tokens. 
`all`

     Returns all documents, similar to a [`match_all`](query-dsl-match-all-query.html "Match all query") query. 

###Notes

#### 使用匹配短语前缀查询进行搜索自动完成

虽然易于设置，但使用"match_phrase_prefix"查询进行搜索自动完成有时会产生令人困惑的结果。

例如，考虑查询字符串"快速棕色 f"。此查询的工作原理是从"quick"和"brown"创建一个短语查询(即术语"quick"必须存在，并且后面必须跟着术语"brown")。然后，它会查看排序术语字典以查找以"f"开头的前 50 个术语，并将这些术语添加到短语查询中。

问题是前50个术语可能不包括术语"狐狸"，因此找不到短语"快速棕色狐狸"。这通常不是问题，因为用户将继续键入更多字母，直到出现他们正在寻找的单词。

有关_search即type_的更好解决方案，请参阅完成建议器和"search_as_you_type"字段类型。

[« Match phrase query](query-dsl-match-query-phrase.md) [Combined fields
»](query-dsl-combined-fields-query.md)
