

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Built-in analyzer reference](analysis-
analyzers.md)

[« Pattern analyzer](analysis-pattern-analyzer.md) [Standard analyzer
»](analysis-standard-analyzer.md)

## 简单分析器

"简单"分析器将文本分解为任何非字母字符(如数字、空格、连字符和撇号)的标记，丢弃非字母字符，并将大写更改为小写。

###Example

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'simple',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "analyzer": "simple",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

"简单"分析器分析句子并生成以下标记：

    
    
    [ the, quick, brown, foxes, jumped, over, the, lazy, dog, s, bone ]

###Definition

"简单"分析器由一个分词器定义：

Tokenizer

    

* 小写分词器

###Customize

若要自定义"简单"分析器，请复制它以创建自定义分析器的基础。可以根据需要修改此自定义分析器，通常通过添加令牌筛选器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_custom_simple_analyzer: {
                tokenizer: 'lowercase',
                filter: []
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
            "my_custom_simple_analyzer": {
              "tokenizer": "lowercase",
              "filter": [                          __]
            }
          }
        }
      }
    }

__

|

在此处添加令牌筛选器。   ---|--- « 模式分析仪 标准分析仪»