

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Unique token filter](analysis-unique-tokenfilter.md) [Word delimiter
token filter »](analysis-word-delimiter-tokenfilter.md)

## 大写标记筛选器

将令牌文本更改为大写。例如，您可以使用"大写"过滤器将"懒惰的DoG"更改为"懒惰的狗"。

此过滤器使用 Lucene 的 UpperCaseFilter。

根据语言的不同，一个大写字符可以映射到多个小写字符。使用"大写"过滤器可能会导致丢失花大小写字符信息。

为避免这种损失，但仍具有一致的字母大小写，请改用"小写"过滤器。

###Example

以下分析 API 请求使用默认的"大写"筛选器将"快速 FoX 跳转"更改为大写：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'uppercase'
        ],
        text: 'the Quick FoX JUMPs'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer" : "standard",
      "filter" : ["uppercase"],
      "text" : "the Quick FoX JUMPs"
    }

筛选器生成以下标记：

    
    
    [ THE, QUICK, FOX, JUMPS ]

### 添加到分析器

以下创建索引 APIrequest 使用"大写"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'uppercase_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_uppercase: {
                tokenizer: 'whitespace',
                filter: [
                  'uppercase'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT uppercase_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_uppercase": {
              "tokenizer": "whitespace",
              "filter": [ "uppercase" ]
            }
          }
        }
      }
    }

[« Unique token filter](analysis-unique-tokenfilter.md) [Word delimiter
token filter »](analysis-word-delimiter-tokenfilter.md)
