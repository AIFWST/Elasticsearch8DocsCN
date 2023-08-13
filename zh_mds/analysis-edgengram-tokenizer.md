

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Classic tokenizer](analysis-classic-tokenizer.md) [Keyword tokenizer
»](analysis-keyword-tokenizer.md)

## 边缘 n-gramtokenizer

"edge_ngram"分词器首先在遇到指定字符列表之一时将文本分解为单词，然后发出每个单词的 N 元语法，其中 N 元语法的开头锚定到单词的开头。

边缘 N 元语法对于_search即type_查询非常有用。

当您需要_search type_具有广为人知的顺序的文本(例如电影或歌曲标题)时，完成建议器是比边缘 N 元语法更有效的选择。边缘 N 元语法在尝试自动完成可以按任何顺序出现的单词时具有优势。

### 示例输出

使用默认设置，"edge_ngram"分词器将初始文本视为单个标记，并生成最小长度为"1"和最大长度为"2"的 N 元语法：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'edge_ngram',
        text: 'Quick Fox'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "edge_ngram",
      "text": "Quick Fox"
    }

上述句子将产生以下术语：

    
    
    [ Q, Qu ]

这些默认的克长几乎完全没用。您需要在使用前配置"edge_ngram"。

###Configuration

"edge_ngram"分词器接受以下参数：

`min_gram`

     Minimum length of characters in a gram. Defaults to `1`. 
`max_gram`

    

克中字符的最大长度。默认为"2"。

请参阅"max_gram"参数的限制。

`token_chars`

    

应包含在标记中的字符类。Elasticsearch 将拆分不属于指定类的字符。默认为"[]"(保留所有字符)。

字符类可以是以下任何一种：

* "字母" - 例如"a"、"b"、"ï"或"京" * "数字"——例如"3"或"7" * "空格"——例如"""或"\n"* "标点符号"——例如"！"或""* "符号"——例如"$"或"√" * "自定义"——需要使用"custom_token_chars"设置设置的自定义字符。

`custom_token_chars`

     Custom characters that should be treated as part of a token. For example, setting this to `+-_` will make the tokenizer treat the plus, minus and underscore sign as part of a token. 

### "max_gram"参数的限制

"edge_ngram"分词器的"max_gram"值限制了代币的字符长度。当"edge_ngram"分词器与索引分析器一起使用时，这意味着长度超过"max_gram"长度的搜索词可能与任何索引词都不匹配。

例如，如果"max_gram"为"3"，则搜索"苹果"与索引字词"app"不匹配。

为此，您可以将"截断"标记筛选器与搜索分析器一起使用，以将搜索词缩短为"max_gram"字符长度。但是，这可能会返回不相关的结果。

例如，如果"max_gram"为"3"，搜索词被截断为三个字符，则搜索词"apple"将缩短为"app"。这意味着搜索"apple"会返回与"app"匹配的任何索引字词，例如"apply"、"approxine"和"apple"。

我们建议测试这两种方法，看看哪种方法最适合您的用例和所需的搜索体验。

### 配置示例

在此示例中，我们将"edge_ngram"分词器配置为将字母和数字视为标记，并生成最小长度为"2"和最大长度为"10"的克：

    
    
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
                type: 'edge_ngram',
                min_gram: 2,
                max_gram: 10,
                token_chars: [
                  'letter',
                  'digit'
                ]
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
        text: '2 Quick Foxes.'
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
              "type": "edge_ngram",
              "min_gram": 2,
              "max_gram": 10,
              "token_chars": [
                "letter",
                "digit"
              ]
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "2 Quick Foxes."
    }

上面的示例生成以下术语：

    
    
    [ Qu, Qui, Quic, Quick, Fo, Fox, Foxe, Foxes ]

通常，我们建议在索引时和搜索时使用相同的"分析器"。对于"edge_ngram"分词器，建议是不同的。只有在索引时使用"edge_ngram"标记器才有意义，以确保部分单词可用于索引中的匹配。在搜索时，只需搜索用户输入的术语，例如："Quick Fo"。

下面是如何为即type__search设置字段的示例。

请注意，索引分析器的"max_gram"值为"10"，这会将索引术语限制为 10 个字符。搜索词不会被截断，这意味着超过 10 个字符的搜索词可能与任何索引词都不匹配。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              autocomplete: {
                tokenizer: 'autocomplete',
                filter: [
                  'lowercase'
                ]
              },
              autocomplete_search: {
                tokenizer: 'lowercase'
              }
            },
            tokenizer: {
              autocomplete: {
                type: 'edge_ngram',
                min_gram: 2,
                max_gram: 10,
                token_chars: [
                  'letter'
                ]
              }
            }
          }
        },
        mappings: {
          properties: {
            title: {
              type: 'text',
              analyzer: 'autocomplete',
              search_analyzer: 'autocomplete_search'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        title: 'Quick Foxes'
      }
    )
    puts response
    
    response = client.indices.refresh(
      index: 'my-index-000001'
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            title: {
              query: 'Quick Fo',
              operator: 'and'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "autocomplete": {
              "tokenizer": "autocomplete",
              "filter": [
                "lowercase"
              ]
            },
            "autocomplete_search": {
              "tokenizer": "lowercase"
            }
          },
          "tokenizer": {
            "autocomplete": {
              "type": "edge_ngram",
              "min_gram": 2,
              "max_gram": 10,
              "token_chars": [
                "letter"
              ]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "title": {
            "type": "text",
            "analyzer": "autocomplete",
            "search_analyzer": "autocomplete_search"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "title": "Quick Foxes" __}
    
    POST my-index-000001/_refresh
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "title": {
            "query": "Quick Fo", __"operator": "and"
          }
        }
      }
    }

__

|

"自动完成"分析器索引术语"[qu， qui， quic， quick， fo， fox，foxe， foxes]"。   ---|---    __

|

"autocomplete_search"分析器搜索术语"quick， fo]"，这两个术语都出现在索引中。   [« 经典分词器 关键字分词器»