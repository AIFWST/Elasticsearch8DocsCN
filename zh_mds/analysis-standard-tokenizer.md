

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Simple pattern split tokenizer](analysis-simplepatternsplit-tokenizer.md)
[Thai tokenizer »](analysis-thai-tokenizer.md)

## 标准标记器

"标准"分词器提供基于语法的分词(基于 Unicode 文本分割算法，如 Unicode 标准附录 #29 中指定)，适用于大多数语言。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "standard",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下术语：

    
    
    [ The, 2, QUICK, Brown, Foxes, jumped, over, the, lazy, dog's, bone ]

###Configuration

"标准"分词器接受以下参数：

`max_token_length`

|

最大令牌长度。如果看到超过此长度的令牌，则以"max_token_length"间隔拆分。默认为"255"。   ---|--- ### 示例配置编辑

在此示例中，我们将"标准"分词器配置为"max_token_length"为 5(用于演示目的)：

    
    
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
                type: 'standard',
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
              "type": "standard",
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

[« Simple pattern split tokenizer](analysis-simplepatternsplit-tokenizer.md)
[Thai tokenizer »](analysis-thai-tokenizer.md)
