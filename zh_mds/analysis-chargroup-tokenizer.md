

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Tokenizer reference](analysis-tokenizers.md) [Classic tokenizer
»](analysis-classic-tokenizer.md)

## 字符分组标记器

"char_group"分词器在遇到定义集中的字符时将文本分解为术语。它主要用于需要简单的自定义标记化的情况，并且使用"模式"标记器的开销是不可接受的。

###Configuration

"char_group"分词器接受一个参数：

`tokenize_on_chars`

|

包含要标记字符串的字符列表的列表。每当遇到此列表中的字符时，都会启动一个新令牌。这接受单个字符(例如"-")或字符组："空格"、"字母"、"数字"、"标点符号"、"符号"。   ---|--- "max_token_length"

|

最大令牌长度。如果看到超过此长度的令牌，则以"max_token_length"间隔拆分。默认为"255"。   ### 示例输出编辑

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: {
          type: 'char_group',
          tokenize_on_chars: [
            'whitespace',
            '-',
            "\n"
          ]
        },
        text: 'The QUICK brown-fox'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": {
        "type": "char_group",
        "tokenize_on_chars": [
          "whitespace",
          "-",
          "\n"
        ]
      },
      "text": "The QUICK brown-fox"
    }

returns

    
    
    {
      "tokens": [
        {
          "token": "The",
          "start_offset": 0,
          "end_offset": 3,
          "type": "word",
          "position": 0
        },
        {
          "token": "QUICK",
          "start_offset": 4,
          "end_offset": 9,
          "type": "word",
          "position": 1
        },
        {
          "token": "brown",
          "start_offset": 10,
          "end_offset": 15,
          "type": "word",
          "position": 2
        },
        {
          "token": "fox",
          "start_offset": 16,
          "end_offset": 19,
          "type": "word",
          "position": 3
        }
      ]
    }

[« Tokenizer reference](analysis-tokenizers.md) [Classic tokenizer
»](analysis-classic-tokenizer.md)
