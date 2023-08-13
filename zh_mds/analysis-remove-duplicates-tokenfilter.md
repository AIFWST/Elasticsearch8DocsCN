

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Predicate script token filter](analysis-predicatefilter-tokenfilter.md)
[Reverse token filter »](analysis-reverse-tokenfilter.md)

## 删除重复的令牌筛选器

删除同一位置的重复令牌。

"remove_duplicates"过滤器使用 Lucene 的 RemoveDuplicatesTokenFilter。

###Example

要查看"remove_duplicates"过滤器的工作原理，您首先需要生成包含相同位置重复令牌的令牌流。

以下分析 API 请求使用"keyword_repeat"和"词干分析器"筛选器为"跳狗"创建词干和非词干标记。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'keyword_repeat',
          'stemmer'
        ],
        text: 'jumping dog'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        "keyword_repeat",
        "stemmer"
      ],
      "text": "jumping dog"
    }

API 返回以下响应。请注意，位置"1"中的"狗"标记是重复的。

    
    
    {
      "tokens": [
        {
          "token": "jumping",
          "start_offset": 0,
          "end_offset": 7,
          "type": "word",
          "position": 0
        },
        {
          "token": "jump",
          "start_offset": 0,
          "end_offset": 7,
          "type": "word",
          "position": 0
        },
        {
          "token": "dog",
          "start_offset": 8,
          "end_offset": 11,
          "type": "word",
          "position": 1
        },
        {
          "token": "dog",
          "start_offset": 8,
          "end_offset": 11,
          "type": "word",
          "position": 1
        }
      ]
    }

若要删除其中一个重复的"狗"令牌，请将"remove_duplicates"筛选器添加到上一个分析 API 请求。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'keyword_repeat',
          'stemmer',
          'remove_duplicates'
        ],
        text: 'jumping dog'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        "keyword_repeat",
        "stemmer",
        "remove_duplicates"
      ],
      "text": "jumping dog"
    }

API 返回以下响应。现在只有一个"狗"令牌位置"1"。

    
    
    {
      "tokens": [
        {
          "token": "jumping",
          "start_offset": 0,
          "end_offset": 7,
          "type": "word",
          "position": 0
        },
        {
          "token": "jump",
          "start_offset": 0,
          "end_offset": 7,
          "type": "word",
          "position": 0
        },
        {
          "token": "dog",
          "start_offset": 8,
          "end_offset": 11,
          "type": "word",
          "position": 1
        }
      ]
    }

### 添加到分析器

以下创建索引 APIrequest 使用"remove_duplicates"筛选器来配置新的自定义分析器。

此自定义分析器使用"keyword_repeat"和"词干分析器"筛选器创建流中每个令牌的词干和非词干版本。然后，"remove_duplicates"筛选器将删除相同位置中的任何重复令牌。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_custom_analyzer: {
                tokenizer: 'standard',
                filter: [
                  'keyword_repeat',
                  'stemmer',
                  'remove_duplicates'
                ]
              }
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
            "my_custom_analyzer": {
              "tokenizer": "standard",
              "filter": [
                "keyword_repeat",
                "stemmer",
                "remove_duplicates"
              ]
            }
          }
        }
      }
    }

[« Predicate script token filter](analysis-predicatefilter-tokenfilter.md)
[Reverse token filter »](analysis-reverse-tokenfilter.md)
