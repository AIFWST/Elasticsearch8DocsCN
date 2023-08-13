

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Built-in analyzer reference](analysis-
analyzers.md)

[« Fingerprint analyzer](analysis-fingerprint-analyzer.md) [Language
analyzers »](analysis-lang-analyzer.md)

## 关键字分析器

"关键字"分析器是一个"noop"分析器，它将整个输入字符串作为单个标记返回。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'keyword',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "analyzer": "keyword",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下单一术语：

    
    
    [ The 2 QUICK Brown-Foxes jumped over the lazy dog's bone. ]

###Configuration

"关键字"分析器不可配置。

###Definition

"关键字"分析器包括：

Tokenizer

    

*关键字分词器

如果需要自定义"关键字"分析器，则需要将其重新创建为"自定义"分析器并对其进行修改，通常通过添加令牌筛选器。通常，当您想要不拆分为标记的字符串时，您应该首选关键字类型，但为了以防万一，这将重新创建内置的"关键字"分析器，您可以将其用作进一步自定义的起点：

    
    
    response = client.indices.create(
      index: 'keyword_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              rebuilt_keyword: {
                tokenizer: 'keyword',
                filter: []
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /keyword_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "rebuilt_keyword": {
              "tokenizer": "keyword",
              "filter": [         __]
            }
          }
        }
      }
    }

__

|

您可以在此处添加任何令牌筛选器。   ---|--- « 指纹分析仪 语言分析仪 »