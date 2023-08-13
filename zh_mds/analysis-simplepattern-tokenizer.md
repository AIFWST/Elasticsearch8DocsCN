

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Pattern tokenizer](analysis-pattern-tokenizer.md) [Simple pattern split
tokenizer »](analysis-simplepatternsplit-tokenizer.md)

## 简单的模式标记器

"simple_pattern"分词器使用正则表达式将匹配文本捕获为术语。它支持的正则表达式功能集比"模式"分词器更受限制，但分词化通常更快。

此分词器不支持在模式匹配上拆分输入，与"模式"分词器不同。要使用相同的受限正则表达式子集拆分模式匹配，请参阅"simple_pattern_split"分词器。

此分词器使用 Lucene 正则表达式。有关支持的功能和语法的说明，请参阅正则表达式语法。

默认模式是空字符串，它不生成任何术语。此标记器应始终使用非默认模式进行配置。

###Configuration

"simple_pattern"分词器接受以下参数：

`pattern`

|

Lucene 正则表达式，默认为空字符串。   ---|--- ### 示例配置编辑

此示例将"simple_pattern"分词器配置为生成三位数字的术语

    
    
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
                type: 'simple_pattern',
                pattern: '[0123456789]{3}'
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
        text: 'fd-786-335-514-x'
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
              "type": "simple_pattern",
              "pattern": "[0123456789]{3}"
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "fd-786-335-514-x"
    }

上面的示例生成以下术语：

    
    
    [ 786, 335, 514 ]

[« Pattern tokenizer](analysis-pattern-tokenizer.md) [Simple pattern split
tokenizer »](analysis-simplepatternsplit-tokenizer.md)
