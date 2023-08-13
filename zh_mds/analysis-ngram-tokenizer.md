

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Lowercase tokenizer](analysis-lowercase-tokenizer.md) [Path hierarchy
tokenizer »](analysis-pathhierarchy-tokenizer.md)

## N-gramtokenizer

"ngram"分词器首先在遇到指定字符列表之一时将文本分解为单词，然后发出指定长度的每个单词的 N 元语法。

N-gram就像一个在单词上移动的滑动窗口 - 指定长度的连续字符序列。它们对于查询不使用空格或具有长复合词的语言(如德语)非常有用。

### 示例输出

使用默认设置时，"ngram"分词器将初始文本视为单个标记，并生成最小长度为"1"和最大长度为"2"的 N 元语法：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'ngram',
        text: 'Quick Fox'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "ngram",
      "text": "Quick Fox"
    }

上述句子将产生以下术语：

    
    
    [ Q, Qu, u, ui, i, ic, c, ck, k, "k ", " ", " F", F, Fo, o, ox, x ]

###Configuration

"ngram"分词器接受以下参数：

`min_gram`

|

克中字符的最小长度。默认为"1"。   ---|--- "max_gram"

|

克中字符的最大长度。默认为"2"。   "token_chars"

|

应包含在标记中的字符类。Elasticsearch 将拆分不属于指定类的字符。默认为"[]"(保留所有字符)。

字符类可以是以下任何一种：

* "字母" - 例如"a"、"b"、"ï"或"京" * "数字"——例如"3"或"7" * "空格"——例如"""或"\n"* "标点符号"——例如"！"或""* "符号"——例如"$"或"√" * "自定义"——需要使用"custom_token_chars"设置设置的自定义字符。

"custom_token_chars"

|

应被视为令牌一部分的自定义字符。例如，将其设置为"+-_"将使分词器将加号、减号和下划线视为分号的一部分。   将"min_gram"和"max_gram"设置为相同的值通常是有意义的。长度越小，匹配的文档越多，但匹配的质量越低。长度越长，匹配越具体。三克(长度"3")是一个很好的起点。

索引级别设置"index.max_ngram_diff"控制"max_gram"和"min_gram"之间的最大允许差异。

### 配置示例

在此示例中，我们将"ngram"分词器配置为将字母和数字视为标记，并生成三元语法(长度为"3"的克)：

    
    
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
                type: 'ngram',
                min_gram: 3,
                max_gram: 3,
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
              "type": "ngram",
              "min_gram": 3,
              "max_gram": 3,
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

    
    
    [ Qui, uic, ick, Fox, oxe, xes ]

[« Lowercase tokenizer](analysis-lowercase-tokenizer.md) [Path hierarchy
tokenizer »](analysis-pathhierarchy-tokenizer.md)
