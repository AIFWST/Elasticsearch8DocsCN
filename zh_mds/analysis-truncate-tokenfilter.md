

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Trim token filter](analysis-trim-tokenfilter.md) [Unique token filter
»](analysis-unique-tokenfilter.md)

## 截断令牌筛选器

截断超过指定字符限制的令牌。此限制默认为"10"，但可以使用"length"参数进行自定义。

例如，您可以使用"截断"过滤器将所有标记缩短为"3"个字符或更少，将"跳跃狐狸"更改为"巨型狐狸"。

此筛选器使用 Lucene 的 TruncateTokenFilter。

###Example

以下分析 API 请求使用"截断"筛选器来缩短"五年一度的盛会"中超过 10 个字符的令牌：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'truncate'
        ],
        text: 'the quinquennial extravaganza carried on'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer" : "whitespace",
      "filter" : ["truncate"],
      "text" : "the quinquennial extravaganza carried on"
    }

筛选器生成以下标记：

    
    
    [ the, quinquenni, extravagan, carried, on ]

### 添加到分析器

以下创建索引 APIrequest 使用"截断"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'custom_truncate_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_truncate: {
                tokenizer: 'standard',
                filter: [
                  'truncate'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT custom_truncate_example
    {
      "settings" : {
        "analysis" : {
          "analyzer" : {
            "standard_truncate" : {
            "tokenizer" : "standard",
            "filter" : ["truncate"]
            }
          }
        }
      }
    }

### 可配置参数

`length`

     (Optional, integer) Character limit for each token. Tokens exceeding this limit are truncated. Defaults to `10`. 

###Customize

若要自定义"截断"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义"截断"筛选器"5_char_trunc"，该筛选器将令牌缩短为"5"或更少字符的"长度"：

    
    
    response = client.indices.create(
      index: '5_char_words_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              "lowercase_5_char": {
                tokenizer: 'lowercase',
                filter: [
                  '5_char_trunc'
                ]
              }
            },
            filter: {
              "5_char_trunc": {
                type: 'truncate',
                length: 5
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT 5_char_words_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "lowercase_5_char": {
              "tokenizer": "lowercase",
              "filter": [ "5_char_trunc" ]
            }
          },
          "filter": {
            "5_char_trunc": {
              "type": "truncate",
              "length": 5
            }
          }
        }
      }
    }

[« Trim token filter](analysis-trim-tokenfilter.md) [Unique token filter
»](analysis-unique-tokenfilter.md)
