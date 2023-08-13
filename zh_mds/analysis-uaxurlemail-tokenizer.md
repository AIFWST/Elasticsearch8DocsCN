

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Thai tokenizer](analysis-thai-tokenizer.md) [Whitespace tokenizer
»](analysis-whitespace-tokenizer.md)

## UAX 网址电子邮件标记器

"uax_url_email"分词器与"标准"分词器类似，只是它将 URL 和电子邮件地址识别为单个分词。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'uax_url_email',
        text: 'Email me at john.smith@global-international.com'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "uax_url_email",
      "text": "Email me at john.smith@global-international.com"
    }

上述句子将产生以下术语：

    
    
    [ Email, me, at, john.smith@global-international.com ]

而"标准"分词器将产生：

    
    
    [ Email, me, at, john.smith, global, international.com ]

###Configuration

"uax_url_email"分词器接受以下参数：

`max_token_length`

|

最大令牌长度。如果看到超过此长度的令牌，则以"max_token_length"间隔拆分。默认为"255"。   ---|--- ### 示例配置编辑

在此示例中，我们将"uax_url_email"分词器配置为"max_token_length"为 5(用于演示目的)：

    
    
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
                type: 'uax_url_email',
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
        text: 'john.smith@global-international.com'
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
              "type": "uax_url_email",
              "max_token_length": 5
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "john.smith@global-international.com"
    }

上面的示例生成以下术语：

    
    
    [ john, smith, globa, l, inter, natio, nal.c, om ]

[« Thai tokenizer](analysis-thai-tokenizer.md) [Whitespace tokenizer
»](analysis-whitespace-tokenizer.md)
