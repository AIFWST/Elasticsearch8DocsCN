

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Full text queries](full-text-queries.md)

[« Match phrase prefix query](query-dsl-match-query-phrase-prefix.md)
[Multi-match query »](query-dsl-multi-match-query.md)

## 组合字段

"combined_fields"查询支持搜索多个文本字段，就好像它们的内容已索引到一个组合字段中一样。查询采用以术语为中心的输入字符串视图：首先，它将查询字符串分析为单个术语，然后在任何字段中查找每个术语。当匹配项可以跨越多个文本字段(例如文章的"标题"、"摘要"和"正文")时，此查询特别有用：

    
    
    response = client.search(
      body: {
        query: {
          combined_fields: {
            query: 'database systems',
            fields: [
              'title',
              'abstract',
              'body'
            ],
            operator: 'and'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "combined_fields" : {
          "query":      "database systems",
          "fields":     [ "title", "abstract", "body"],
          "operator":   "and"
        }
      }
    }

"combined_fields"查询采用基于概率相关性框架：BM25 和 Beyond 中描述的简单 BM25F 公式的原则性评分方法。对匹配项进行评分时，查询将跨字段组合术语和集合统计信息，对每个匹配项进行评分，就像指定的字段已索引到单个组合字段中一样。这个评分是最好的尝试;"combined_fields"做出一些近似值，分数不会完全符合 BM25F 模型。

### 字段数限制

默认情况下，查询可以包含的子句数有限制。此限制由"index.query.bool.max_clause_count"设置定义，该设置默认为"4096"。对于组合字段查询，子句数的计算方法是字段数乘以字词数。

### 每字段提升

场提升根据组合场模型进行解释。例如，如果"title"字段的提升为 2，则计算分数时，标题中的每个术语在合成组合字段中出现两次。

    
    
    response = client.search(
      body: {
        query: {
          combined_fields: {
            query: 'distributed consensus',
            fields: [
              'title^2',
              'body'
            ]
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "combined_fields" : {
          "query" : "distributed consensus",
          "fields" : [ "title^2", "body" ] __}
      }
    }

__

|

可以使用插入符号 ('^') 表示法提升各个字段。   ---|--- "combined_fields"查询要求字段提升大于或等于 1.0。场提升允许为分数。

### combined_fields"的顶级参数

`fields`

     (Required, array of strings) List of fields to search. Field wildcard patterns are allowed. Only [`text`](text.html "Text type family") fields are supported, and they must all have the same search [`analyzer`](analyzer.html "analyzer"). 
`query`

    

(必需，字符串)要在提供的""中搜索的文本<fields>。

"combined_fields"查询在执行搜索之前分析提供的文本。

`auto_generate_synonyms_phrase_query`

    

(可选，布尔值)如果为"true"，则会自动为多术语同义词创建匹配短语查询。默认为"真"。

有关示例，请参阅在匹配查询中使用同义词。

`operator`

    

(可选，字符串)用于解释"query"值中的文本的布尔逻辑。有效值为：

"或"(默认)

     For example, a `query` value of `database systems` is interpreted as `database OR systems`. 
`and`

     For example, a `query` value of `database systems` is interpreted as `database AND systems`. 

`minimum_should_match`

    

(可选，字符串)要返回的文档必须匹配的最小子句数。有关有效值和更多信息，请参阅"minimum_should_match"参数。

`zero_terms_query`

    

(可选，字符串)指示如果"分析器"删除所有令牌(例如使用"停止"筛选器时)，是否不返回任何文档。有效值为：

"无"(默认)

     No documents are returned if the `analyzer` removes all tokens. 
`all`

     Returns all documents, similar to a [`match_all`](query-dsl-match-all-query.html "Match all query") query. 

有关示例，请参阅零字词查询。

#### 与"multi_match"查询的比较

"combined_fields"查询提供了一种跨多个"文本"字段进行匹配和评分的原则方法。为了支持这一点，它要求所有字段具有相同的搜索"分析器"。

如果您想要一个查询来处理不同类型的字段(如关键字或数字)，那么"multi_match"查询可能更适合。它支持文本和非文本字段，并接受不共享同一分析器的文本字段。

主要的"multi_match"模式"best_fields"和"most_fields"采用以字段为中心的查询视图。相比之下，"combined_fields"以术语为中心："运算符"和"minimum_should_match"按术语应用，而不是按字段应用。具体来说，像这样的查询

    
    
    response = client.search(
      body: {
        query: {
          combined_fields: {
            query: 'database systems',
            fields: [
              'title',
              'abstract'
            ],
            operator: 'and'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "combined_fields" : {
          "query":      "database systems",
          "fields":     [ "title", "abstract"],
          "operator":   "and"
        }
      }
    }

执行方式为：

    
    
    +(combined("database", fields:["title" "abstract"]))
    +(combined("systems", fields:["title", "abstract"]))

换句话说，每个术语必须至少存在于一个字段中，文档才能匹配。

"cross_fields"multi_match"模式也采用以术语为中心的方法，并应用"运算符"和"每个术语minimum_should_match"。与"cross_fields"相比，"combined_fields"的主要优势在于其基于BM25F算法的稳健且可解释的评分方法。

### 自定义相似性

"combined_fields"查询目前仅支持 BM25 相似性，这是默认值，除非配置了自定义相似性。也不允许每个字段有相似之处。在这两种情况下使用"combined_fields"都会导致错误。

[« Match phrase prefix query](query-dsl-match-query-phrase-prefix.md)
[Multi-match query »](query-dsl-multi-match-query.md)
