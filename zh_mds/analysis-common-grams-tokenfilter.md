

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Classic token filter](analysis-classic-tokenfilter.md) [Conditional token
filter »](analysis-condition-tokenfilter.md)

## 常用克标记筛选器

为一组指定的常用词生成双字母。

例如，可以将"is"和"the"指定为常用词。然后，此筛选器将标记"[the， quick， fox， is， brown]"转换为"[the， the_quick， quick，fox， fox_is， is， is_brown， brown]"。

当您不想完全忽略常用词时，可以使用"common_grams"过滤器代替停止标记过滤器。

此过滤器使用 Lucene 的 CommonGramsFilter。

###Example

以下分析 API 请求为"is"和"the"创建双字母：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'common_grams',
            common_words: [
              'is',
              'the'
            ]
          }
        ],
        text: 'the quick fox is brown'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "whitespace",
      "filter" : [
        {
          "type": "common_grams",
          "common_words": ["is", "the"]
        }
      ],
      "text" : "the quick fox is brown"
    }

筛选器生成以下标记：

    
    
    [ the, the_quick, quick, fox, fox_is, is, is_brown, brown ]

### 添加到分析器

以下创建索引 APIrequest 使用"common_grams"筛选器来配置新的自定义分析器：

    
    
    response = client.indices.create(
      index: 'common_grams_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              index_grams: {
                tokenizer: 'whitespace',
                filter: [
                  'common_grams'
                ]
              }
            },
            filter: {
              common_grams: {
                type: 'common_grams',
                common_words: [
                  'a',
                  'is',
                  'the'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /common_grams_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "index_grams": {
              "tokenizer": "whitespace",
              "filter": [ "common_grams" ]
            }
          },
          "filter": {
            "common_grams": {
              "type": "common_grams",
              "common_words": [ "a", "is", "the" ]
            }
          }
        }
      }
    }

### 可配置参数

`common_words`

    

(必需*，字符串数组)令牌列表。筛选器为这些令牌生成二进制图。

此参数或"common_words_path"参数是必需的。

`common_words_path`

    

(必填*，字符串)包含令牌列表的文件的路径。筛选器为这些令牌生成双字母。

此路径必须是绝对路径或相对于"配置"位置的路径。该文件必须采用 UTF-8 编码。文件中的每个标记必须用换行符分隔。

此参数或"common_words"参数是必需的。

`ignore_case`

     (Optional, Boolean) If `true`, matches for common words matching are case-insensitive. Defaults to `false`. 
`query_mode`

    

(可选，布尔值)如果为"true"，则筛选器从输出中排除以下标记：

* 常用词的统一字母 * 术语的统一字母，后跟常用词

默认为"假"。建议为搜索分析器启用此参数。

例如，您可以启用此参数并指定"is"和"the"作为常用词。此筛选器将标记"[the， quick， fox， is， brown]"转换为"[the_quick， quick， fox_is， is_brown，]"。

###Customize

要自定义"common_grams"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义"common_grams"筛选器，并将"ignore_case"和"query_mode"设置为"true"：

    
    
    response = client.indices.create(
      index: 'common_grams_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              index_grams: {
                tokenizer: 'whitespace',
                filter: [
                  'common_grams_query'
                ]
              }
            },
            filter: {
              common_grams_query: {
                type: 'common_grams',
                common_words: [
                  'a',
                  'is',
                  'the'
                ],
                ignore_case: true,
                query_mode: true
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /common_grams_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "index_grams": {
              "tokenizer": "whitespace",
              "filter": [ "common_grams_query" ]
            }
          },
          "filter": {
            "common_grams_query": {
              "type": "common_grams",
              "common_words": [ "a", "is", "the" ],
              "ignore_case": true,
              "query_mode": true
            }
          }
        }
      }
    }

[« Classic token filter](analysis-classic-tokenfilter.md) [Conditional token
filter »](analysis-condition-tokenfilter.md)
