

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Character group tokenizer](analysis-chargroup-tokenizer.md) [Edge n-gram
tokenizer »](analysis-edgengram-tokenizer.md)

## 经典标记器

"经典"分词器是一种基于语法的分词器，适用于英语文档。此分词器具有启发式方法，用于特殊处理首字母缩略词、公司名称、电子邮件地址和互联网主机名。但是，这些规则并不总是有效，并且分词器不适用于英语以外的大多数语言：

*它最多拆分标点字符的单词，删除标点符号。但是，不跟空格的点被视为标记的一部分。  * 它会用连字符拆分单词，除非令牌中有数字，在这种情况下，整个标记将被解释为产品编号，并且不会拆分。  *它将电子邮件地址和互联网主机名识别为一个令牌。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'classic',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "classic",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下术语：

    
    
    [ The, 2, QUICK, Brown, Foxes, jumped, over, the, lazy, dog's, bone ]

###Configuration

"经典"分词器接受以下参数：

`max_token_length`

|

最大令牌长度。如果看到超过此长度的令牌，则以"max_token_length"间隔拆分。默认为"255"。   ---|--- ### 示例配置编辑

在此示例中，我们将"经典"分词器配置为"max_token_length"为 5(用于演示目的)：

    
    
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
                type: 'classic',
                max_token_length: 5
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
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
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
              "type": "classic",
              "max_token_length": 5
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上面的示例生成以下术语：

    
    
    [ The, 2, QUICK, Brown, Foxes, jumpe, d, over, the, lazy, dog's, bone ]

[« Character group tokenizer](analysis-chargroup-tokenizer.md) [Edge n-gram
tokenizer »](analysis-edgengram-tokenizer.md)
