

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« MinHash token filter](analysis-minhash-tokenfilter.md) [N-gram token
filter »](analysis-ngram-tokenfilter.md)

## 多路复用器令牌过滤器

类型为"multixer"的令牌筛选器将在同一位置发出多个令牌，令牌的每个版本都通过不同的筛选器运行。同一位置的相同输出令牌将被删除。

如果传入的令牌流具有重复的令牌，则多路复用器也将删除这些令牌

###Options

filters

|

要应用于传入令牌的令牌筛选器列表。这些可以是索引映射中其他位置定义的任何标记筛选器。可以使用逗号分隔的字符串链接筛选器，例如"小写，porter_stem"会将"小写"筛选器，然后将"porter_stem"筛选器应用于单个令牌。   ---|--- 在过滤器数组中声明时，带状疱疹或多字同义词标记过滤器将无法正常工作，因为它们在内部提前读取，而多路复用器不支持

preserve_original

     if `true` (the default) then emit the original token in addition to the filtered tokens 

### 设置示例

您可以像这样设置它：

    
    
    response = client.indices.create(
      index: 'multiplexer_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                filter: [
                  'my_multiplexer'
                ]
              }
            },
            filter: {
              my_multiplexer: {
                type: 'multiplexer',
                filters: [
                  'lowercase',
                  'lowercase, porter_stem'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /multiplexer_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "standard",
              "filter": [ "my_multiplexer" ]
            }
          },
          "filter": {
            "my_multiplexer": {
              "type": "multiplexer",
              "filters": [ "lowercase", "lowercase, porter_stem" ]
            }
          }
        }
      }
    }

并像这样测试它：

    
    
    response = client.indices.analyze(
      index: 'multiplexer_example',
      body: {
        analyzer: 'my_analyzer',
        text: 'Going HOME'
      }
    )
    puts response
    
    
    POST /multiplexer_example/_analyze
    {
      "analyzer" : "my_analyzer",
      "text" : "Going HOME"
    }

它会回应：

    
    
    {
      "tokens": [
        {
          "token": "Going",
          "start_offset": 0,
          "end_offset": 5,
          "type": "<ALPHANUM>",
          "position": 0
        },
        {
          "token": "going",
          "start_offset": 0,
          "end_offset": 5,
          "type": "<ALPHANUM>",
          "position": 0
        },
        {
          "token": "go",
          "start_offset": 0,
          "end_offset": 5,
          "type": "<ALPHANUM>",
          "position": 0
        },
        {
          "token": "HOME",
          "start_offset": 6,
          "end_offset": 10,
          "type": "<ALPHANUM>",
          "position": 1
        },
        {
          "token": "home",          __"start_offset": 6,
          "end_offset": 10,
          "type": " <ALPHANUM>",
          "position": 1
        }
      ]
    }

__

|

词干分析器还在位置 1 发出了一个令牌"home"，但由于它是此令牌的副本，因此已从令牌流中删除 ---|--- 同义词和synonym_graph筛选器使用其前面的分析链来解析和分析其同义词列表，如果该链包含在同一位置生成多个令牌的令牌筛选器，则会引发异常。如果要将同义词应用于包含多路复用器的令牌流，则应将同义词筛选器附加到每个相关的多路复用器筛选器列表中，而不是将其放在主令牌链定义中的多路复用器之后。

[« MinHash token filter](analysis-minhash-tokenfilter.md) [N-gram token
filter »](analysis-ngram-tokenfilter.md)
