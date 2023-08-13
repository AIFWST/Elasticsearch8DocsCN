

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Simple pattern tokenizer](analysis-simplepattern-tokenizer.md) [Standard
tokenizer »](analysis-standard-tokenizer.md)

## 简单的模式拆分令牌器

"simple_pattern_split"分词器使用正则表达式在模式匹配时将输入拆分为项。它支持的正则表达式功能集比"模式"分词器更受限制，但分词化通常更快。

此分词器不会从匹配项本身生成项。要使用同一受限正则表达式子集中的模式从匹配项生成项，请参阅"simple_pattern"分词器。

此分词器使用 Lucene 正则表达式。有关支持的功能和语法的说明，请参阅正则表达式语法。

默认模式是空字符串，它生成一个包含完整输入的术语。此分词器应始终配置非默认模式。

###Configuration

"simple_pattern_split"分词器接受以下参数：

`pattern`

|

Lucene 正则表达式，默认为空字符串。   ---|--- ### 示例配置编辑

本示例将"simple_pattern_split"分词器配置为在下划线上拆分输入文本。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'my_tokenizer'
              }
            },
            tokenizer: {
              my_tokenizer: {
                type: 'simple_pattern_split',
                pattern: '_'
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.analyze(
      index: 'my-index-000001',
      body: {
        analyzer: 'my_analyzer',
        text: 'an_underscored_phrase'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "my_tokenizer"
            }
          },
          "tokenizer": {
            "my_tokenizer": {
              "type": "simple_pattern_split",
              "pattern": "_"
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "an_underscored_phrase"
    }

上面的示例生成以下术语：

    
    
    [ an, underscored, phrase ]

[« Simple pattern tokenizer](analysis-simplepattern-tokenizer.md) [Standard
tokenizer »](analysis-standard-tokenizer.md)
