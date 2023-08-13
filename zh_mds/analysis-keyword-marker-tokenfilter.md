

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Keep words token filter](analysis-keep-words-tokenfilter.md) [Keyword
repeat token filter »](analysis-keyword-repeat-tokenfilter.md)

## 关键字标记令牌筛选器

将指定的标记标记为不带词干的关键字。

"keyword_marker"过滤器为指定的令牌分配"true"的"关键字"属性。词干分析器令牌筛选器(例如"词干分析器"或"porter_stem")会跳过"关键字"属性为"true"的令牌。

若要正常工作，必须在分析器配置中的任何词干标记筛选器之前列出"keyword_marker"筛选器。

"keyword_marker"过滤器使用Lucene的KeywordMarkerFilter。

###Example

若要查看"keyword_marker"筛选器的工作原理，首先需要生成包含词干标记的令牌流。

以下分析 API 请求使用"词干"过滤器为"狐狸奔跑和跳跃"创建词干标记。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'stemmer'
        ],
        text: 'fox running and jumping'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [ "stemmer" ],
      "text": "fox running and jumping"
    }

该请求生成以下令牌。请注意，"running"被词干为"run"，"jumping"被词干为"jump"。

    
    
    [ fox, run, and, jump ]

为防止"跳转"被词干提取，请在上一个分析 API 请求中的"词干分析器"过滤器之前添加"keyword_marker"过滤器。在"keyword_marker"过滤器的"关键字"参数中指定"跳转"。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'keyword_marker',
            keywords: [
              'jumping'
            ]
          },
          'stemmer'
        ],
        text: 'fox running and jumping'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        {
          "type": "keyword_marker",
          "keywords": [ "jumping" ]
        },
        "stemmer"
      ],
      "text": "fox running and jumping"
    }

该请求生成以下令牌。"跑步"仍然被词干为"跑"，但"跳跃"不是词干。

    
    
    [ fox, run, and, jumping ]

要查看这些令牌的"关键字"属性，请将以下参数添加到分析 API 请求：

* "解释"："真实" * "属性"："关键字"

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'keyword_marker',
            keywords: [
              'jumping'
            ]
          },
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
        {
          "type": "keyword_marker",
          "keywords": [ "jumping" ]
        },
        "stemmer"
      ],
      "text": "fox running and jumping",
      "explain": true,
      "attributes": "keyword"
    }

API 返回以下响应。请注意，"跳跃"标记的"关键字"属性为"true"。

    
    
    {
      "detail": {
        "custom_analyzer": true,
        "charfilters": [],
        "tokenizer": {
          "name": "whitespace",
          "tokens": [
            {
              "token": "fox",
              "start_offset": 0,
              "end_offset": 3,
              "type": "word",
              "position": 0
            },
            {
              "token": "running",
              "start_offset": 4,
              "end_offset": 11,
              "type": "word",
              "position": 1
            },
            {
              "token": "and",
              "start_offset": 12,
              "end_offset": 15,
              "type": "word",
              "position": 2
            },
            {
              "token": "jumping",
              "start_offset": 16,
              "end_offset": 23,
              "type": "word",
              "position": 3
            }
          ]
        },
        "tokenfilters": [
          {
            "name": "__anonymous__keyword_marker",
            "tokens": [
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
                "keyword": false
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
              }
            ]
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
                "keyword": false
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
                "keyword": false
              },
              {
                "token": "jumping",
                "start_offset": 16,
                "end_offset": 23,
                "type": "word",
                "position": 3,
                "keyword": true
              }
            ]
          }
        ]
      }
    }

### 可配置参数

`ignore_case`

     (Optional, Boolean) If `true`, matching for the `keywords` and `keywords_path` parameters ignores letter case. Defaults to `false`. 
`keywords`

    

(必需*，字符串数组)关键字数组。与这些关键字匹配的令牌不会被词干提取。

必须指定此参数"keywords_path"或"keywords_pattern"。不能指定此参数和"keywords_pattern"。

`keywords_path`

    

(必填*，字符串)包含关键字列表的文件的路径。与这些关键字匹配的标记不进行词干提取。

此路径必须是绝对路径或相对于"配置"位置的路径，并且文件必须采用 UTF-8 编码。文件中的每个单词必须用换行符分隔。

必须指定此参数"关键字"或"keywords_pattern"。不能指定此参数和"keywords_pattern"。

`keywords_pattern`

    

(必填*，字符串)Java 正则表达式用于匹配令牌。与此表达式匹配的标记将标记为关键字，而不是词干。

必须指定此参数、"关键字"或"keywords_path"。您不能指定此参数和"关键字"或"keywords_pattern"。

写得不好的正则表达式会导致 Elasticsearch 运行缓慢或导致堆栈溢出错误，从而导致正在运行的节点突然退出。

### 自定义并添加到分析器

要自定义"keyword_marker"筛选器，请复制它，为新的自定义令牌筛选器创建基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用自定义"keyword_marker"筛选器和"porter_stem"筛选器来配置新的自定义分析器。

自定义"keyword_marker"筛选器将"分析/example_word_list.txt"文件中指定的标记标记为关键字。"porter_stem"过滤器不会阻止这些令牌。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_custom_analyzer: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'my_custom_keyword_marker_filter',
                  'porter_stem'
                ]
              }
            },
            filter: {
              my_custom_keyword_marker_filter: {
                type: 'keyword_marker',
                keywords_path: 'analysis/example_word_list.txt'
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
              "type": "custom",
              "tokenizer": "standard",
              "filter": [
                "my_custom_keyword_marker_filter",
                "porter_stem"
              ]
            }
          },
          "filter": {
            "my_custom_keyword_marker_filter": {
              "type": "keyword_marker",
              "keywords_path": "analysis/example_word_list.txt"
            }
          }
        }
      }
    }

[« Keep words token filter](analysis-keep-words-tokenfilter.md) [Keyword
repeat token filter »](analysis-keyword-repeat-tokenfilter.md)
