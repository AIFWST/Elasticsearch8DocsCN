

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Length token filter](analysis-length-tokenfilter.md) [Lowercase token
filter »](analysis-lowercase-tokenfilter.md)

## 限制令牌计数令牌筛选器

限制输出令牌的数量。"限制"筛选器通常用于根据令牌计数限制文档字段值的大小。

默认情况下，"limit"筛选器仅保留流中的第一个令牌。例如，筛选器可以将令牌流"[ 一、二、三 ]"更改为"[一]"。

此过滤器使用 Lucene 的 LimitTokenCountFilter。

    
    
     If you want to limit the size of field values based on
    _character length_, use the <<ignore-above,`ignore_above`>> mapping parameter.

### 可配置参数

`max_token_count`

     (Optional, integer) Maximum number of tokens to keep. Once this limit is reached, any remaining tokens are excluded from the output. Defaults to `1`. 
`consume_all_tokens`

     (Optional, Boolean) If `true`, the `limit` filter exhausts the token stream, even if the `max_token_count` has already been reached. Defaults to `false`. 

###Example

以下分析 API 请求使用"限制"过滤器仅保留"快速狐狸跳跃过懒狗"中的前两个令牌：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          {
            type: 'limit',
            max_token_count: 2
          }
        ],
        text: 'quick fox jumps over lazy dog'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "standard",
        "filter": [
        {
          "type": "limit",
          "max_token_count": 2
        }
      ],
      "text": "quick fox jumps over lazy dog"
    }

筛选器生成以下标记：

    
    
    [ quick, fox ]

### 添加到分析器

以下创建索引 APIrequest 使用"限制"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'limit_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_one_token_limit: {
                tokenizer: 'standard',
                filter: [
                  'limit'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT limit_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_one_token_limit": {
              "tokenizer": "standard",
              "filter": [ "limit" ]
            }
          }
        }
      }
    }

###Customize

要自定义"限制"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义"limit"筛选器，该筛选器仅保留流的前五个令牌：

    
    
    response = client.indices.create(
      index: 'custom_limit_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_five_token_limit: {
                tokenizer: 'whitespace',
                filter: [
                  'five_token_limit'
                ]
              }
            },
            filter: {
              five_token_limit: {
                type: 'limit',
                max_token_count: 5
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT custom_limit_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_five_token_limit": {
              "tokenizer": "whitespace",
              "filter": [ "five_token_limit" ]
            }
          },
          "filter": {
            "five_token_limit": {
              "type": "limit",
              "max_token_count": 5
            }
          }
        }
      }
    }

[« Length token filter](analysis-length-tokenfilter.md) [Lowercase token
filter »](analysis-lowercase-tokenfilter.md)
