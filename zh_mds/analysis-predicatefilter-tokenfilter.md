

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Porter stem token filter](analysis-porterstem-tokenfilter.md) [Remove
duplicates token filter »](analysis-remove-duplicates-tokenfilter.md)

## 谓词脚本标记筛选器

删除与提供的谓词脚本不匹配的令牌。过滤器仅支持内联无痛脚本。脚本在分析谓词上下文中计算。

###Example

以下分析 API 请求使用"predicate_token_filter"筛选器仅输出"狐狸跳懒狗"中长度超过三个字符的令牌。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'predicate_token_filter',
            script: {
              source: "\n          token.term.length() > 3\n        "
            }
          }
        ],
        text: 'the fox jumps the lazy dog'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        {
          "type": "predicate_token_filter",
          "script": {
            "source": """
              token.term.length() > 3
            """
          }
        }
      ],
      "text": "the fox jumps the lazy dog"
    }

筛选器生成以下令牌。

    
    
    [ jumps, lazy ]

API 响应包含每个输出令牌的位置和偏移量。请注意，"predicate_token_filter"过滤器不会更改令牌的原始位置或偏移量。

**Response**

    
    
    {
      "tokens" : [
        {
          "token" : "jumps",
          "start_offset" : 8,
          "end_offset" : 13,
          "type" : "word",
          "position" : 2
        },
        {
          "token" : "lazy",
          "start_offset" : 18,
          "end_offset" : 22,
          "type" : "word",
          "position" : 4
        }
      ]
    }

### 可配置参数

`script`

    

(必需，脚本对象)包含用于筛选传入令牌的条件的脚本。只有与此脚本匹配的令牌才会包含在输出中。

此参数仅支持内联无痛脚本。脚本在分析谓词上下文中计算。

### 自定义并添加到分析器

要自定义"predicate_token_filter"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

以下创建索引 APIrequest 使用自定义"predicate_token_filter"筛选器"my_script_filter"配置新的自定义分析器。

"my_script_filter"过滤器会删除除"ALPHANUM"以外的任何类型的令牌。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                filter: [
                  'my_script_filter'
                ]
              }
            },
            filter: {
              my_script_filter: {
                type: 'predicate_token_filter',
                script: {
                  source: "\n              token.type.contains(\"ALPHANUM\")\n            "
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "standard",
              "filter": [
                "my_script_filter"
              ]
            }
          },
          "filter": {
            "my_script_filter": {
              "type": "predicate_token_filter",
              "script": {
                "source": """
                  token.type.contains("ALPHANUM")
                """
              }
            }
          }
        }
      }
    }

[« Porter stem token filter](analysis-porterstem-tokenfilter.md) [Remove
duplicates token filter »](analysis-remove-duplicates-tokenfilter.md)
