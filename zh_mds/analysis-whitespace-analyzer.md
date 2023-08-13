

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Built-in analyzer reference](analysis-
analyzers.md)

[« Stop analyzer](analysis-stop-analyzer.md) [Tokenizer reference
»](analysis-tokenizers.md)

## 空格分析器

"空格"分析器在遇到空格字符时将文本分解为术语。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'whitespace',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "analyzer": "whitespace",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下术语：

    
    
    [ The, 2, QUICK, Brown-Foxes, jumped, over, the, lazy, dog's, bone. ]

###Configuration

"空格"分析器不可配置。

###Definition

它包括：

Tokenizer

    

*空格分词器

如果需要自定义"空白"分析器，则需要将其重新创建为"自定义"分析器并对其进行修改，通常通过添加令牌筛选器。这将重新创建内置的"空白"分析器，您可以将其用作进一步自定义的起点：

    
    
    response = client.indices.create(
      index: 'whitespace_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              rebuilt_whitespace: {
                tokenizer: 'whitespace',
                filter: []
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /whitespace_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "rebuilt_whitespace": {
              "tokenizer": "whitespace",
              "filter": [         __]
            }
          }
        }
      }
    }

__

|

您可以在此处添加任何令牌筛选器。   ---|--- « 停止分析器分词器参考»