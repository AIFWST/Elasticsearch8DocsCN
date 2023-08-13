

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Multiplexer token filter](analysis-multiplexer-tokenfilter.md)
[Normalization token filters »](analysis-normalization-tokenfilter.md)

## N 元语法标记筛选器

从标记中形成指定长度的 n 元语法。

例如，您可以使用"ngram"标记筛选器将"fox"更改为"[ f，fo，o， ox， x ]"。

此过滤器使用 Lucene 的 NGramTokenFilter。

"ngram"筛选器类似于"edge_ngram"令牌筛选器。但是，"edge_ngram"仅输出从令牌开头开始的 n 元语法。

###Example

以下分析 API 请求使用"ngram"筛选器将"快速狐狸"转换为 1 个字符和 2 个字符的语法：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'ngram'
        ],
        text: 'Quick fox'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "standard",
      "filter": [ "ngram" ],
      "text": "Quick fox"
    }

筛选器生成以下标记：

    
    
    [ Q, Qu, u, ui, i, ic, c, ck, k, f, fo, o, ox, x ]

### 添加到分析器

以下创建索引 APIrequest 使用"ngram"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'ngram_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_ngram: {
                tokenizer: 'standard',
                filter: [
                  'ngram'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT ngram_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_ngram": {
              "tokenizer": "standard",
              "filter": [ "ngram" ]
            }
          }
        }
      }
    }

### 可配置参数

`max_gram`

     (Optional, integer) Maximum length of characters in a gram. Defaults to `2`. 
`min_gram`

     (Optional, integer) Minimum length of characters in a gram. Defaults to `1`. 
`preserve_original`

     (Optional, Boolean) Emits original token when set to `true`. Defaults to `false`. 

您可以使用"index.max_ngram_diff"索引级别设置来控制"max_gram"和"min_gram"值之间允许的最大差异。

###Customize

要自定义"ngram"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义的"ngram"筛选器，该筛选器在 3-5 个字符之间形成 n-gram。该请求还将"index.max_ngram_diff"设置增加到"2"。

    
    
    response = client.indices.create(
      index: 'ngram_custom_example',
      body: {
        settings: {
          index: {
            max_ngram_diff: 2
          },
          analysis: {
            analyzer: {
              default: {
                tokenizer: 'whitespace',
                filter: [
                  '3_5_grams'
                ]
              }
            },
            filter: {
              "3_5_grams": {
                type: 'ngram',
                min_gram: 3,
                max_gram: 5
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT ngram_custom_example
    {
      "settings": {
        "index": {
          "max_ngram_diff": 2
        },
        "analysis": {
          "analyzer": {
            "default": {
              "tokenizer": "whitespace",
              "filter": [ "3_5_grams" ]
            }
          },
          "filter": {
            "3_5_grams": {
              "type": "ngram",
              "min_gram": 3,
              "max_gram": 5
            }
          }
        }
      }
    }

[« Multiplexer token filter](analysis-multiplexer-tokenfilter.md)
[Normalization token filters »](analysis-normalization-tokenfilter.md)
