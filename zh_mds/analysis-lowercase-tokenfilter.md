

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Limit token count token filter](analysis-limit-token-count-
tokenfilter.md) [MinHash token filter »](analysis-minhash-tokenfilter.md)

## 小写标记筛选器

将令牌文本更改为小写。例如，您可以使用"小写"过滤器将"懒惰的DoG"更改为"懒惰的狗"。

除了默认过滤器之外，"小写"标记过滤器还提供对 Lucene 特定于语言的小写过滤器的希腊语、爱尔兰语和土耳其语的访问。

###Example

以下分析 API 请求使用默认的"小写"筛选器将"快速 FoX 跳转"更改为小写：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'lowercase'
        ],
        text: 'THE Quick FoX JUMPs'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer" : "standard",
      "filter" : ["lowercase"],
      "text" : "THE Quick FoX JUMPs"
    }

筛选器生成以下标记：

    
    
    [ the, quick, fox, jumps ]

### 添加到分析器

以下创建索引 APIrequest 使用"小写"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'lowercase_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_lowercase: {
                tokenizer: 'whitespace',
                filter: [
                  'lowercase'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT lowercase_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_lowercase": {
              "tokenizer": "whitespace",
              "filter": [ "lowercase" ]
            }
          }
        }
      }
    }

### 可配置参数

`language`

    

(可选，字符串)要使用的特定于语言的小写标记筛选器。有效值包括：

`greek`

     Uses Lucene's [GreekLowerCaseFilter](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/el/GreekLowerCaseFilter.html)
`irish`

     Uses Lucene's [IrishLowerCaseFilter](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/ga/IrishLowerCaseFilter.html)
`turkish`

     Uses Lucene's [TurkishLowerCaseFilter](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/tr/TurkishLowerCaseFilter.html)

如果未指定，则默认为 Lucene 的 LowerCaseFilter。

###Customize

若要自定义"小写"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求为希腊语创建自定义"小写"过滤器：

    
    
    response = client.indices.create(
      index: 'custom_lowercase_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              greek_lowercase_example: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'greek_lowercase'
                ]
              }
            },
            filter: {
              greek_lowercase: {
                type: 'lowercase',
                language: 'greek'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT custom_lowercase_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "greek_lowercase_example": {
              "type": "custom",
              "tokenizer": "standard",
              "filter": ["greek_lowercase"]
            }
          },
          "filter": {
            "greek_lowercase": {
              "type": "lowercase",
              "language": "greek"
            }
          }
        }
      }
    }

[« Limit token count token filter](analysis-limit-token-count-
tokenfilter.md) [MinHash token filter »](analysis-minhash-tokenfilter.md)
