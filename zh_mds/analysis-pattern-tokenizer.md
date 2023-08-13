

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Path hierarchy tokenizer](analysis-pathhierarchy-tokenizer.md) [Simple
pattern tokenizer »](analysis-simplepattern-tokenizer.md)

## 模式标记器

"模式"分词器使用正则表达式在与单词分隔符匹配时将文本拆分为术语，或者将匹配的文本捕获为术语。

默认模式为"\W+"，每当遇到非单词字符时，它就会拆分文本。

### 当心病态正则表达式

模式标记器使用 Java 正则表达式。

一个写得不好的正则表达式可能会运行得非常慢，甚至抛出 aStackOverflowError 并导致它运行的节点突然退出。

阅读更多关于病理正则表达式以及如何避免它们的信息。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'pattern',
        text: "The foo_bar_size's default is 5."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "pattern",
      "text": "The foo_bar_size's default is 5."
    }

上述句子将产生以下术语：

    
    
    [ The, foo_bar_size, s, default, is, 5 ]

###Configuration

"模式"标记器接受以下参数：

`pattern`

|

Java 正则表达式，默认为 '\W+'。   ---|---"旗帜"

|

Java 正则表达式标志。标志应该是管道分隔的，例如 '"CASE_INSENSITIVE|评论"'。   "组"

|

要提取为令牌的捕获组。默认为"-1"(拆分)。   ### 示例配置编辑

在此示例中，我们将"模式"分词器配置为在遇到逗号时将文本分解为标记：

    
    
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
                type: 'pattern',
                pattern: ','
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
        text: 'comma,separated,values'
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
              "type": "pattern",
              "pattern": ","
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "comma,separated,values"
    }

上面的示例生成以下术语：

    
    
    [ comma, separated, values ]

在下一个示例中，我们将"模式"分词器配置为捕获括在双引号中的值(忽略嵌入的转义引号"\"")。正则表达式本身如下所示：

    
    
    "((?:\\"|[^"]|\\")*)"

内容如下：

* 文字 '"' * 开始捕获：

    * A literal `\"` OR any character except `"`
    * Repeat until no more characters match 

* 文字结尾 '"'

当模式以 JSON 格式指定时，需要转义 '"' 和 '\' 字符，因此模式最终如下所示：

    
    
    \"((?:\\\\\"|[^\"]|\\\\\")+)\"
    
    
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
                type: 'pattern',
                pattern: '"((?:\\\"|[^"]|\\\")+)"',
                group: 1
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
        text: '"value", "value with embedded \" quote"'
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
              "type": "pattern",
              "pattern": "\"((?:\\\\\"|[^\"]|\\\\\")+)\"",
              "group": 1
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "\"value\", \"value with embedded \\\" quote\""
    }

上面的示例生成以下两个术语：

    
    
    [ value, value with embedded \" quote ]

[« Path hierarchy tokenizer](analysis-pathhierarchy-tokenizer.md) [Simple
pattern tokenizer »](analysis-simplepattern-tokenizer.md)
