

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Built-in analyzer reference](analysis-
analyzers.md)

[« Language analyzers](analysis-lang-analyzer.md) [Simple analyzer
»](analysis-simple-analyzer.md)

## 模式分析器

"模式"分析器使用正则表达式将文本拆分为术语。正则表达式应匹配 **令牌分隔符** 而不是标记本身。正则表达式默认为"\W+"(或所有非单词字符)。

### 当心病态正则表达式

模式分析器使用 Java 正则表达式。

一个写得不好的正则表达式可能会运行得非常慢，甚至抛出 aStackOverflowError 并导致它运行的节点突然退出。

阅读更多关于病理正则表达式以及如何避免它们的信息。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'pattern',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "analyzer": "pattern",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下术语：

    
    
    [ the, 2, quick, brown, foxes, jumped, over, the, lazy, dog, s, bone ]

###Configuration

"模式"分析器接受以下参数：

`pattern`

|

Java 正则表达式，默认为 '\W+'。   ---|---"旗帜"

|

Java 正则表达式标志。标志应该是管道分隔的，例如 '"CASE_INSENSITIVE|评论"'。   "小写"

|

术语是否应小写。默认为"真"。   "停用词"

|

预定义的停用词列表，如"_English_"或包含停用词列表的数组。默认为"_none_"。   "stopwords_path"

|

包含停用词的文件的路径。   有关停用词配置的详细信息，请参阅停止标记筛选器。

### 配置示例

在此示例中，我们将"模式"分析器配置为在非单词字符或下划线 ('\W|_') 上拆分电子邮件地址，并将结果小写：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_email_analyzer: {
                type: 'pattern',
                pattern: '\\W|_',
                lowercase: true
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
        analyzer: 'my_email_analyzer',
        text: 'John_Smith@foo-bar.com'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_email_analyzer": {
              "type":      "pattern",
              "pattern":   "\\W|_", __"lowercase": true
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_email_analyzer",
      "text": "John_Smith@foo-bar.com"
    }

__

|

将模式指定为 JSON 字符串时，需要对模式中的反斜杠进行转义。   ---|--- 上面的示例生成以下术语：

    
    
    [ john, smith, foo, bar, com ]

#### 骆驼案例标记器

以下更复杂的示例将驼峰大小写文本拆分为标记：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              camel: {
                type: 'pattern',
                pattern: '([^\\p{L}\\d]+)|(?<=\\D)(?=\\d)|(?<=\\d)(?=\\D)|(?<=[\\p{L}&&[^\\p{Lu}]])(?=\\p{Lu})|(?<=\\p{Lu})(?=\\p{Lu}[\\p{L}&&[^\\p{Lu}]])'
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
        analyzer: 'camel',
        text: 'MooseX::FTPClass2_beta'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "camel": {
              "type": "pattern",
              "pattern": "([^\\p{L}\\d]+)|(?<=\\D)(?=\\d)|(?<=\\d)(?=\\D)|(?<=[\\p{L}&&[^\\p{Lu}]])(?=\\p{Lu})|(?<=\\p{Lu})(?=\\p{Lu}[\\p{L}&&[^\\p{Lu}]])"
            }
          }
        }
      }
    }
    
    GET my-index-000001/_analyze
    {
      "analyzer": "camel",
      "text": "MooseX::FTPClass2_beta"
    }

上面的示例生成以下术语：

    
    
    [ moose, x, ftp, class, 2, beta ]

上面的正则表达式更容易理解为：

    
    
      ([^\p{L}\d]+)                 # swallow non letters and numbers,
    | (?<=\D)(?=\d)                 # or non-number followed by number,
    | (?<=\d)(?=\D)                 # or number followed by non-number,
    | (?<=[ \p{L} && [^\p{Lu}]])    # or lower case
      (?=\p{Lu})                    #   followed by upper case,
    | (?<=\p{Lu})                   # or upper case
      (?=\p{Lu}                     #   followed by upper case
        [\p{L}&&[^\p{Lu}]]          #   then lower case
      )

###Definition

"模式"分析器包括：

Tokenizer

    

* 模式标记器

令牌筛选器

    

* 小写令牌过滤器 * 停止令牌过滤器(默认禁用)

如果需要在配置参数之外自定义"模式"分析器，则需要将其重新创建为"自定义"分析器并对其进行修改，通常通过添加令牌筛选器。这将重新创建内置的"模式"分析器，您可以将其用作进一步自定义的起点：

    
    
    response = client.indices.create(
      index: 'pattern_example',
      body: {
        settings: {
          analysis: {
            tokenizer: {
              split_on_non_word: {
                type: 'pattern',
                pattern: '\\W+'
              }
            },
            analyzer: {
              rebuilt_pattern: {
                tokenizer: 'split_on_non_word',
                filter: [
                  'lowercase'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /pattern_example
    {
      "settings": {
        "analysis": {
          "tokenizer": {
            "split_on_non_word": {
              "type":       "pattern",
              "pattern":    "\\W+" __}
          },
          "analyzer": {
            "rebuilt_pattern": {
              "tokenizer": "split_on_non_word",
              "filter": [
                "lowercase" __]
            }
          }
        }
      }
    }

__

|

默认模式是"\W+"，它会在非单词字符上拆分，这是您要更改它的地方。   ---|---    __

|

您可以在"小写"之后添加其他令牌筛选器。   « 语言分析器简单分析器»