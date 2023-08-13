

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Common grams token filter](analysis-common-grams-tokenfilter.md) [Decimal
digit token filter »](analysis-decimal-digit-tokenfilter.md)

## 条件令牌筛选器

将一组令牌筛选器应用于与提供的谓词脚本中的条件匹配的令牌。

此过滤器使用 Lucene 的 ConditionalTokenFilter。

###Example

以下分析 API 请求使用"条件"筛选器来匹配"快速棕色狐狸"中少于 5 个字符的令牌。然后，它将"小写"过滤器应用于那些匹配的令牌，将它们转换为小写。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          {
            type: 'condition',
            filter: [
              'lowercase'
            ],
            script: {
              source: 'token.getTerm().length() < 5'
            }
          }
        ],
        text: 'THE QUICK BROWN FOX'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "standard",
      "filter": [
        {
          "type": "condition",
          "filter": [ "lowercase" ],
          "script": {
            "source": "token.getTerm().length() < 5"
          }
        }
      ],
      "text": "THE QUICK BROWN FOX"
    }

筛选器生成以下标记：

    
    
    [ the, QUICK, BROWN, fox ]

### 可配置参数

`filter`

    

(必需，令牌筛选器数组)令牌筛选器数组。如果令牌与"script"参数中的谓词脚本匹配，则这些筛选器将按提供的顺序应用于令牌。

这些筛选器可以包括在索引映射中定义的自定义令牌筛选器。

`script`

    

(必需，脚本对象)用于应用令牌筛选器的谓词脚本。如果令牌与此脚本匹配，则"filter"参数中的筛选器将应用于令牌。

有关有效参数，请参阅写入scripts__How。仅支持内联脚本。无痛脚本在分析谓词上下文中执行，并且需要"令牌"属性。

### 自定义并添加到分析器

要自定义"条件"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用自定义"条件"筛选器来配置新的自定义分析器。自定义"条件"筛选器与流中的第一个令牌匹配。然后，它使用"反向"筛选器反转该匹配令牌。

    
    
    response = client.indices.create(
      index: 'palindrome_list',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_reverse_first_token: {
                tokenizer: 'whitespace',
                filter: [
                  'reverse_first_token'
                ]
              }
            },
            filter: {
              reverse_first_token: {
                type: 'condition',
                filter: [
                  'reverse'
                ],
                script: {
                  source: 'token.getPosition() === 0'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /palindrome_list
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_reverse_first_token": {
              "tokenizer": "whitespace",
              "filter": [ "reverse_first_token" ]
            }
          },
          "filter": {
            "reverse_first_token": {
              "type": "condition",
              "filter": [ "reverse" ],
              "script": {
                "source": "token.getPosition() === 0"
              }
            }
          }
        }
      }
    }

[« Common grams token filter](analysis-common-grams-tokenfilter.md) [Decimal
digit token filter »](analysis-decimal-digit-tokenfilter.md)
