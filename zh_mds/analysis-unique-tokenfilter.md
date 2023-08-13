

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Truncate token filter](analysis-truncate-tokenfilter.md) [Uppercase token
filter »](analysis-uppercase-tokenfilter.md)

## 唯一令牌筛选器

从流中删除重复的令牌。例如，您可以使用"唯一"过滤器将"懒惰的懒狗"更改为"懒惰的狗"。

如果"only_on_same_position"参数设置为"true"，则"唯一"筛选器仅删除同一position__in重复标记。

当"only_on_same_position"为"true"时，"唯一"过滤器的工作方式与"remove_duplicates"过滤器相同。

###Example

以下分析 API 请求使用"唯一"过滤器从"快速狐狸跳懒狐"中删除重复的令牌：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'unique'
        ],
        text: 'the quick fox jumps the lazy fox'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer" : "whitespace",
      "filter" : ["unique"],
      "text" : "the quick fox jumps the lazy fox"
    }

筛选器删除"the"和"fox"的重复标记，生成以下输出：

    
    
    [ the, quick, fox, jumps, lazy ]

### 添加到分析器

以下创建索引 APIrequest 使用"唯一"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'custom_unique_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_truncate: {
                tokenizer: 'standard',
                filter: [
                  'unique'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT custom_unique_example
    {
      "settings" : {
        "analysis" : {
          "analyzer" : {
            "standard_truncate" : {
            "tokenizer" : "standard",
            "filter" : ["unique"]
            }
          }
        }
      }
    }

### 可配置参数

`only_on_same_position`

     (Optional, Boolean) If `true`, only remove duplicate tokens in the same position. Defaults to `false`. 

###Customize

若要自定义"唯一"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义"唯一"筛选器，并将"only_on_same_position"设置为"true"。

    
    
    response = client.indices.create(
      index: 'letter_unique_pos_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              letter_unique_pos: {
                tokenizer: 'letter',
                filter: [
                  'unique_pos'
                ]
              }
            },
            filter: {
              unique_pos: {
                type: 'unique',
                only_on_same_position: true
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT letter_unique_pos_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "letter_unique_pos": {
              "tokenizer": "letter",
              "filter": [ "unique_pos" ]
            }
          },
          "filter": {
            "unique_pos": {
              "type": "unique",
              "only_on_same_position": true
            }
          }
        }
      }
    }

[« Truncate token filter](analysis-truncate-tokenfilter.md) [Uppercase token
filter »](analysis-uppercase-tokenfilter.md)
