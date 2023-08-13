

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Keyword marker token filter](analysis-keyword-marker-tokenfilter.md)
[KStem token filter »](analysis-kstem-tokenfilter.md)

## 关键字重复标记筛选器

输出流中每个标记的关键字版本。这些关键字标记不进行词干提取。

"keyword_repeat"过滤器为关键字令牌分配"关键字"属性"true"。词干分析器令牌筛选器(例如"词干分析器"或"porter_stem")会跳过"关键字"属性为"true"的令牌。

您可以将"keyword_repeat"筛选器与词干分析器令牌筛选器结合使用，以输出流中每个令牌的词干和非词干版本。

要正常工作，必须在分析器配置中的任何词干器令牌过滤器之前列出"keyword_repeat"过滤器。

词干提取不会影响所有令牌。这意味着流可能包含相同位置的重复令牌，即使在词干提取后也是如此。

若要删除这些重复的令牌，请在分析器配置中的词干筛选器之后添加"remove_duplicates"筛选器。

"keyword_repeat"过滤器使用 Lucene 的 KeywordRepeatFilter。

###Example

以下分析 API 请求使用"keyword_repeat"过滤器输出"狐狸跑跳"中每个令牌的关键字和非关键字版本。

要返回这些令牌的"关键字"属性，分析 API 请求还包括以下参数：

* "解释"："真实" * "属性"："关键字"

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'keyword_repeat'
        ],
        text: 'fox running and jumping',
        explain: true,
        attributes: 'keyword'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        "keyword_repeat"
      ],
      "text": "fox running and jumping",
      "explain": true,
      "attributes": "keyword"
    }

API 返回以下响应。请注意，每个令牌的一个版本的"关键字"属性为"true"。

**Response**

    
    
    {
      "detail": {
        "custom_analyzer": true,
        "charfilters": [],
        "tokenizer": ...,
        "tokenfilters": [
          {
            "name": "keyword_repeat",
            "tokens": [
              {
                "token": "fox",
                "start_offset": 0,
                "end_offset": 3,
                "type": "word",
                "position": 0,
                "keyword": true
              },
              {
                "token": "fox",
                "start_offset": 0,
                "end_offset": 3,
                "type": "word",
                "position": 0,
                "keyword": false
              },
              {
                "token": "running",
                "start_offset": 4,
                "end_offset": 11,
                "type": "word",
                "position": 1,
                "keyword": true
              },
              {
                "token": "running",
                "start_offset": 4,
                "end_offset": 11,
                "type": "word",
                "position": 1,
                "keyword": false
              },
              {
                "token": "and",
                "start_offset": 12,
                "end_offset": 15,
                "type": "word",
                "position": 2,
                "keyword": true
              },
              {
                "token": "and",
                "start_offset": 12,
                "end_offset": 15,
                "type": "word",
                "position": 2,
                "keyword": false
              },
              {
                "token": "jumping",
                "start_offset": 16,
                "end_offset": 23,
                "type": "word",
                "position": 3,
                "keyword": true
              },
              {
                "token": "jumping",
                "start_offset": 16,
                "end_offset": 23,
                "type": "word",
                "position": 3,
                "keyword": false
              }
            ]
          }
        ]
      }
    }

要阻止非关键字令牌，请在上一个分析 API 请求中的"keyword_repeat"筛选器之后添加"词干分析器"筛选器。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'keyword_repeat',
          'stemmer'
        ],
        text: 'fox running and jumping',
        explain: true,
        attributes: 'keyword'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        "keyword_repeat",
        "stemmer"
      ],
      "text": "fox running and jumping",
      "explain": true,
      "attributes": "keyword"
    }

API 返回以下响应。请注意以下更改：

* "running"的非关键字版本被词干为"run"。  * "跳跃"的非关键字版本被删改为"跳转"。

**Response**

    
    
    {
      "detail": {
        "custom_analyzer": true,
        "charfilters": [],
        "tokenizer": ...,
        "tokenfilters": [
          {
            "name": "keyword_repeat",
            "tokens": ...
          },
          {
            "name": "stemmer",
            "tokens": [
              {
                "token": "fox",
                "start_offset": 0,
                "end_offset": 3,
                "type": "word",
                "position": 0,
                "keyword": true
              },
              {
                "token": "fox",
                "start_offset": 0,
                "end_offset": 3,
                "type": "word",
                "position": 0,
                "keyword": false
              },
              {
                "token": "running",
                "start_offset": 4,
                "end_offset": 11,
                "type": "word",
                "position": 1,
                "keyword": true
              },
              {
                "token": "run",
                "start_offset": 4,
                "end_offset": 11,
                "type": "word",
                "position": 1,
                "keyword": false
              },
              {
                "token": "and",
                "start_offset": 12,
                "end_offset": 15,
                "type": "word",
                "position": 2,
                "keyword": true
              },
              {
                "token": "and",
                "start_offset": 12,
                "end_offset": 15,
                "type": "word",
                "position": 2,
                "keyword": false
              },
              {
                "token": "jumping",
                "start_offset": 16,
                "end_offset": 23,
                "type": "word",
                "position": 3,
                "keyword": true
              },
              {
                "token": "jump",
                "start_offset": 16,
                "end_offset": 23,
                "type": "word",
                "position": 3,
                "keyword": false
              }
            ]
          }
        ]
      }
    }

但是，"fox"和"and"的关键字和非关键字版本是相同的，并且处于相同的位置。

若要删除这些重复的令牌，请在分析 API 请求中的"词干分析器"之后添加"remove_duplicates"筛选器。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'keyword_repeat',
          'stemmer',
          'remove_duplicates'
        ],
        text: 'fox running and jumping',
        explain: true,
        attributes: 'keyword'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        "keyword_repeat",
        "stemmer",
        "remove_duplicates"
      ],
      "text": "fox running and jumping",
      "explain": true,
      "attributes": "keyword"
    }

API 返回以下响应。请注意，"fox"和"and"的重复标记已被删除。

**Response**

    
    
    {
      "detail": {
        "custom_analyzer": true,
        "charfilters": [],
        "tokenizer": ...,
        "tokenfilters": [
          {
            "name": "keyword_repeat",
            "tokens": ...
          },
          {
            "name": "stemmer",
            "tokens": ...
          },
          {
            "name": "remove_duplicates",
            "tokens": [
              {
                "token": "fox",
                "start_offset": 0,
                "end_offset": 3,
                "type": "word",
                "position": 0,
                "keyword": true
              },
              {
                "token": "running",
                "start_offset": 4,
                "end_offset": 11,
                "type": "word",
                "position": 1,
                "keyword": true
              },
              {
                "token": "run",
                "start_offset": 4,
                "end_offset": 11,
                "type": "word",
                "position": 1,
                "keyword": false
              },
              {
                "token": "and",
                "start_offset": 12,
                "end_offset": 15,
                "type": "word",
                "position": 2,
                "keyword": true
              },
              {
                "token": "jumping",
                "start_offset": 16,
                "end_offset": 23,
                "type": "word",
                "position": 3,
                "keyword": true
              },
              {
                "token": "jump",
                "start_offset": 16,
                "end_offset": 23,
                "type": "word",
                "position": 3,
                "keyword": false
              }
            ]
          }
        ]
      }
    }

### 添加到分析器

以下创建索引 APIrequest 使用"keyword_repeat"筛选器来配置新的自定义分析器。

此自定义分析器使用"keyword_repeat"和"porter_stem"筛选器为流中的每个令牌创建带词干和无词干的版本。然后，"remove_duplicates"筛选器从流中删除任何重复的令牌。

    
    
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
                  'porter_stem',
                  'remove_duplicates'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_custom_analyzer": {
              "tokenizer": "standard",
              "filter": [
                "keyword_repeat",
                "porter_stem",
                "remove_duplicates"
              ]
            }
          }
        }
      }
    }

[« Keyword marker token filter](analysis-keyword-marker-tokenfilter.md)
[KStem token filter »](analysis-kstem-tokenfilter.md)
