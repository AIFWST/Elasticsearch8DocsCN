

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Edge n-gram token filter](analysis-edgengram-tokenfilter.md) [Fingerprint
token filter »](analysis-fingerprint-tokenfilter.md)

## Elision 令牌筛选器

从标记的开头删除指定的省略号。例如，您可以使用此过滤器将"l'avion"更改为"avion"。

如果未自定义，筛选器将默认删除以下法语省略号：

'l'， 'm'， 't'， 'qu'， 'n'， 's'， 'j'， 'd'， 'c'， 'jusqu'， 'quoiqu'， 'lorsqu'， 'puisqu''

此过滤器的自定义版本包含在 Elasticsearch 的几个内置语言分析器中：

*加泰罗尼亚语分析仪 *法语分析仪 *爱尔兰分析仪 *意大利语分析仪

此过滤器使用 Lucene 的 ElisionFilter。

###Example

以下分析 API 请求使用"elision"过滤器从"j'examine près du wharf"中删除"j"：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'elision'
        ],
        text: 'j’examine près du wharf'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer" : "standard",
      "filter" : ["elision"],
      "text" : "j’examine près du wharf"
    }

筛选器生成以下标记：

    
    
    [ examine, près, du, wharf ]

### 添加到分析器

以下创建索引 APIrequest 使用"elision"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'elision_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_elision: {
                tokenizer: 'whitespace',
                filter: [
                  'elision'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /elision_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_elision": {
              "tokenizer": "whitespace",
              "filter": [ "elision" ]
            }
          }
        }
      }
    }

### 可配置参数

`articles`

    

(必需*，字符串数组)要删除的省略列表。

要删除，省略号必须位于标记的开头，紧跟撇号。省略号和撇号都被删除了。

对于自定义"elision"筛选器，必须指定此参数或"articles_path"。

`articles_path`

    

(必填*，字符串)包含要删除的省略符列表的文件的路径。

此路径必须是绝对路径或相对于"配置"位置的路径，并且文件必须采用 UTF-8 编码。文件中的每个省略号必须用换行符分隔。

要删除，省略号必须位于标记的开头，紧跟撇号。省略号和撇号都被删除了。

对于自定义"省略"筛选器，必须指定此参数或"文章"。

`articles_case`

     (Optional, Boolean) If `true`, elision matching is case insensitive. If `false`, elision matching is case sensitive. Defaults to `false`. 

###Customize

若要自定义"elision"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个不区分大小写的自定义"elision"筛选器，该筛选器删除"l"、"m"、"t"、"qu"、"n"、"s"和"j"省略：

    
    
    response = client.indices.create(
      index: 'elision_case_insensitive_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              default: {
                tokenizer: 'whitespace',
                filter: [
                  'elision_case_insensitive'
                ]
              }
            },
            filter: {
              elision_case_insensitive: {
                type: 'elision',
                articles: [
                  'l',
                  'm',
                  't',
                  'qu',
                  'n',
                  's',
                  'j'
                ],
                articles_case: true
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /elision_case_insensitive_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "default": {
              "tokenizer": "whitespace",
              "filter": [ "elision_case_insensitive" ]
            }
          },
          "filter": {
            "elision_case_insensitive": {
              "type": "elision",
              "articles": [ "l", "m", "t", "qu", "n", "s", "j" ],
              "articles_case": true
            }
          }
        }
      }
    }

[« Edge n-gram token filter](analysis-edgengram-tokenfilter.md) [Fingerprint
token filter »](analysis-fingerprint-tokenfilter.md)
