

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Apostrophe token filter](analysis-apostrophe-tokenfilter.md) [CJK bigram
token filter »](analysis-cjk-bigram-tokenfilter.md)

## ASCII 折叠令牌筛选器

将不在基本拉丁语 Unicode 块中的字母、数字和符号字符(前 127 个 ASCII 字符)转换为其 ASCII 等效字符(如果存在)。例如，筛选器将"à"更改为"a"。

此过滤器使用 Lucene 的 ASCIIFoldingFilter。

###Example

以下分析 API 请求使用"asciifolding"过滤器删除"açaí à la carte"中的变音符号：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'asciifolding'
        ],
        text: 'açaí à la carte'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "standard",
      "filter" : ["asciifolding"],
      "text" : "açaí à la carte"
    }

筛选器生成以下标记：

    
    
    [ acai, a, la, carte ]

### 添加到分析器

以下创建索引 APIrequest 使用"腹入"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'asciifold_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_asciifolding: {
                tokenizer: 'standard',
                filter: [
                  'asciifolding'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /asciifold_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_asciifolding": {
              "tokenizer": "standard",
              "filter": [ "asciifolding" ]
            }
          }
        }
      }
    }

### 可配置参数

`preserve_original`

     (Optional, Boolean) If `true`, emit both original tokens and folded tokens. Defaults to `false`. 

###Customize

要自定义"腹腔折叠"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义的"腹闭"筛选器，并将"preserve_original"设置为 true：

    
    
    response = client.indices.create(
      index: 'asciifold_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_asciifolding: {
                tokenizer: 'standard',
                filter: [
                  'my_ascii_folding'
                ]
              }
            },
            filter: {
              my_ascii_folding: {
                type: 'asciifolding',
                preserve_original: true
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /asciifold_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_asciifolding": {
              "tokenizer": "standard",
              "filter": [ "my_ascii_folding" ]
            }
          },
          "filter": {
            "my_ascii_folding": {
              "type": "asciifolding",
              "preserve_original": true
            }
          }
        }
      }
    }

[« Apostrophe token filter](analysis-apostrophe-tokenfilter.md) [CJK bigram
token filter »](analysis-cjk-bigram-tokenfilter.md)
