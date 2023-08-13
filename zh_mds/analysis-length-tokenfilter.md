

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« KStem token filter](analysis-kstem-tokenfilter.md) [Limit token count
token filter »](analysis-limit-token-count-tokenfilter.md)

## 长度标记筛选器

删除短于或长于指定字符长度的标记。例如，您可以使用"长度"过滤器排除短于 2 个字符的令牌和长度超过 5 个字符的标记。

此过滤器使用 Lucene 的 LengthFilter。

"长度"过滤器会删除整个令牌。如果您希望将令牌缩短到特定长度，请使用"截断"过滤器。

###Example

以下分析 API 请求使用"长度"筛选器删除长度超过 4 个字符的令牌：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'length',
            min: 0,
            max: 4
          }
        ],
        text: 'the quick brown fox jumps over the lazy dog'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        {
          "type": "length",
          "min": 0,
          "max": 4
        }
      ],
      "text": "the quick brown fox jumps over the lazy dog"
    }

筛选器生成以下标记：

    
    
    [ the, fox, over, the, lazy, dog ]

### 添加到分析器

以下创建索引 APIrequest 使用"长度"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'length_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_length: {
                tokenizer: 'standard',
                filter: [
                  'length'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT length_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_length": {
              "tokenizer": "standard",
              "filter": [ "length" ]
            }
          }
        }
      }
    }

### 可配置参数

`min`

     (Optional, integer) Minimum character length of a token. Shorter tokens are excluded from the output. Defaults to `0`. 
`max`

     (Optional, integer) Maximum character length of a token. Longer tokens are excluded from the output. Defaults to `Integer.MAX_VALUE`, which is `2^31-1` or `2147483647`. 

###Customize

要自定义"长度"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义"长度"筛选器，用于删除短于 2 个字符的令牌和长度超过 10 个字符的标记：

    
    
    response = client.indices.create(
      index: 'length_custom_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              "whitespace_length_2_to_10_char": {
                tokenizer: 'whitespace',
                filter: [
                  'length_2_to_10_char'
                ]
              }
            },
            filter: {
              "length_2_to_10_char": {
                type: 'length',
                min: 2,
                max: 10
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT length_custom_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_length_2_to_10_char": {
              "tokenizer": "whitespace",
              "filter": [ "length_2_to_10_char" ]
            }
          },
          "filter": {
            "length_2_to_10_char": {
              "type": "length",
              "min": 2,
              "max": 10
            }
          }
        }
      }
    }

[« KStem token filter](analysis-kstem-tokenfilter.md) [Limit token count
token filter »](analysis-limit-token-count-tokenfilter.md)
