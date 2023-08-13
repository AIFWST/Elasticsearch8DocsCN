

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Specialized queries](specialized-queries.md)

[« Distance feature query](query-dsl-distance-feature-query.md) [Percolate
query »](query-dsl-percolate-query.md)

## 更多类似这个查询

"更像此查询"查找"类似于"一组给定文档的文档。为此，MLT 选择这些输入文档的一组代表性术语，使用这些术语形成查询，执行查询并返回结果。用户控制输入文档、应如何选择术语以及如何形成查询。

最简单的用例包括请求类似于提供的一段文本的文档。在这里，我们要求所有在"标题"和"描述"字段中具有类似于"从前"的文本的电影，将所选术语的数量限制为 12。

    
    
    response = client.search(
      body: {
        query: {
          more_like_this: {
            fields: [
              'title',
              'description'
            ],
            like: 'Once upon a time',
            min_term_freq: 1,
            max_query_terms: 12
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "more_like_this" : {
          "fields" : ["title", "description"],
          "like" : "Once upon a time",
          "min_term_freq" : 1,
          "max_query_terms" : 12
        }
      }
    }

更复杂的用例包括将文本与索引中已存在的文档混合在一起。在这种情况下，指定文档的语法类似于 Multi GET API API"中使用的语法)。

    
    
    response = client.search(
      body: {
        query: {
          more_like_this: {
            fields: [
              'title',
              'description'
            ],
            like: [
              {
                _index: 'imdb',
                _id: '1'
              },
              {
                _index: 'imdb',
                _id: '2'
              },
              'and potentially some more text here as well'
            ],
            min_term_freq: 1,
            max_query_terms: 12
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "more_like_this": {
          "fields": [ "title", "description" ],
          "like": [
            {
              "_index": "imdb",
              "_id": "1"
            },
            {
              "_index": "imdb",
              "_id": "2"
            },
            "and potentially some more text here as well"
          ],
          "min_term_freq": 1,
          "max_query_terms": 12
        }
      }
    }

最后，用户可以混合一些文本，一组选定的文档，但也提供不一定存在于索引中的文档。为了提供索引中不存在的文档，语法类似于人工文档。

    
    
    response = client.search(
      body: {
        query: {
          more_like_this: {
            fields: [
              'name.first',
              'name.last'
            ],
            like: [
              {
                _index: 'marvel',
                doc: {
                  name: {
                    first: 'Ben',
                    last: 'Grimm'
                  },
                  _doc: "You got no idea what I'd... what I'd give to be invisible."
                }
              },
              {
                _index: 'marvel',
                _id: '2'
              }
            ],
            min_term_freq: 1,
            max_query_terms: 12
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "more_like_this": {
          "fields": [ "name.first", "name.last" ],
          "like": [
            {
              "_index": "marvel",
              "doc": {
                "name": {
                  "first": "Ben",
                  "last": "Grimm"
                },
                "_doc": "You got no idea what I'd... what I'd give to be invisible."
              }
            },
            {
              "_index": "marvel",
              "_id": "2"
            }
          ],
          "min_term_freq": 1,
          "max_query_terms": 12
        }
      }
    }

### 工作原理

假设我们想查找与给定输入文档类似的所有文档。显然，输入文档本身应该是该类型查询的最佳匹配项。根据Lucene评分公式，原因主要是由于tf-idf最高的条款。因此，具有最高 tf-idf 的输入文档的术语是该文档的良好代表，并且可以在析取查询(或"OR")中使用以检索类似的文档。MLT 查询只是从输入文档中提取文本，对其进行分析，通常在字段中使用相同的分析器，然后选择具有最高 tf-idf 的前 K 个术语以形成这些术语的析取查询。

执行 MLT 的字段必须已编制索引，并且类型为"文本"或"关键字"。此外，对文档使用"喜欢"时，必须启用"_source"，或者字段必须"存储"或存储"term_vector"。为了加快分析速度，它可以帮助在索引时存储术语向量。

例如，如果我们希望对"title"和"tags.raw"字段执行MLT，我们可以在索引时显式存储它们的"term_vector"。我们仍然可以对"描述"和"标签"字段执行 MLT，因为默认情况下启用"_source"，但这些字段的分析速度不会加快。

    
    
    response = client.indices.create(
      index: 'imdb',
      body: {
        mappings: {
          properties: {
            title: {
              type: 'text',
              term_vector: 'yes'
            },
            description: {
              type: 'text'
            },
            tags: {
              type: 'text',
              fields: {
                raw: {
                  type: 'text',
                  analyzer: 'keyword',
                  term_vector: 'yes'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /imdb
    {
      "mappings": {
        "properties": {
          "title": {
            "type": "text",
            "term_vector": "yes"
          },
          "description": {
            "type": "text"
          },
          "tags": {
            "type": "text",
            "fields": {
              "raw": {
                "type": "text",
                "analyzer": "keyword",
                "term_vector": "yes"
              }
            }
          }
        }
      }
    }

###Parameters

唯一必需的参数是"like"，所有其他参数都有合理的默认值。有三种类型的参数：一种用于指定文档输入，另一种用于术语选择和查询形成。

#### 文档输入参数

`like`

|

MLT 查询的唯一 **必需** 参数是 "like"，并遵循通用语法，用户可以在其中指定自由格式文本和/或单个或多个文档(请参阅上面的示例)。指定文档的语法类似于 Multi GET API API"使用的语法)。指定文档时，除非在每个文档请求中被覆盖，否则将从"字段"中获取文本。文本由分析器在现场进行分析，但也可以被覆盖。在字段中重写分析器的语法遵循与术语向量 API 的"per_field_analyzer"参数类似的语法。此外，为了提供不一定存在于索引中的文档，还支持人工文档。   ---|---"不像"

|

"unlike"参数与"like"结合使用，以便不选择在所选文档集中找到的术语。换句话说，我们可以要求提供文件"像："苹果"，但"不像："蛋糕碎树"。语法与"喜欢"相同。   "字段"

|

要从中获取和分析文本的字段列表。默认为"index.query.default_field"索引设置，其默认值为"*"。"*"值匹配符合术语级查询条件的所有字段，但元数据字段除外。   #### 术语选择参数编辑

`max_query_terms`

|

将选择的最大查询词数。增加此值可提高准确性，但会降低查询执行速度。默认为"25"。   ---|--- "min_term_freq"

|

最小术语频率，低于该频率将从输入文档中忽略术语。默认为"2"。   "min_doc_freq"

|

最低文档频率，低于该频率将从输入文档中忽略术语。默认为"5"。   "max_doc_freq"

|

输入文档中将忽略术语的最大文档频率。这对于忽略频繁的单词(如停用词)可能很有用。默认为无界("整数.MAX_VALUE"，即"2^31-1"或2147483647)。   "min_word_length"

|

将忽略术语的最小字长。默认为"0"。   "max_word_length"

|

将忽略术语的最大字长。默认值为无界 ('0')。   "stop_words"

|

一组停用词。此集合中的任何单词都被视为"无趣"并被忽略。如果分析器允许停用词，您可能希望告诉 MLT 明确忽略它们，因为出于文档相似性的目的，假设"停用词永远不会有趣"似乎是合理的。   "分析器"

|

用于分析自由格式文本的分析器。默认为与"字段"中的第一个字段关联的分析器。   #### 查询形成参数编辑

`minimum_should_match`

|

形成析取查询后，此参数控制必须匹配的项数。语法与最小应匹配相同。(默认为"30%")。   ---|--- "fail_on_unsupported_field"

|

控制如果任何指定的字段不属于受支持的类型("文本"或"关键字")，查询是否应失败(引发异常)。将此设置为 "false" 以忽略该字段并继续处理。默认为"true"。   "boost_terms"

|

形成的查询中的每个术语都可以通过其 tf-idf 分数进一步提高。这将设置使用此功能时要使用的提升因子。默认为已停用 ('0')。任何其他正值都会激活具有给定提升因子的项提升。   "包括"

|

指定输入文档是否也应包含在返回的搜索结果中。默认为"假"。   "提升"

|

设置整个查询的提升值。默认为"1.0"。   ###Alternativeedit

若要更好地控制类似文档的查询构造，值得考虑编写自定义客户端代码，以将示例文档中的选定术语组合到具有所需设置的布尔查询中。"more_like_this"中的逻辑从一段文本中选择"有趣"的单词也可以通过 TermVectors API 访问。例如，使用termvectors API，可以向用户提供在文档文本中找到的主题关键字选择，允许他们选择感兴趣的单词进行深入研究，而不是使用"more_like_this"使用的更"黑盒"的匹配方法。

[« Distance feature query](query-dsl-distance-feature-query.md) [Percolate
query »](query-dsl-percolate-query.md)
