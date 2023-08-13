

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Configure text analysis](configure-text-
analysis.md)

[« Configure text analysis](configure-text-analysis.md) [Configuring built-
in analyzers »](configuring-analyzers.md)

## 测试分析器

"分析"API 是查看分析器生成的术语的宝贵工具。可以在请求中内联指定内置分析器：

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'whitespace',
        text: 'The quick brown fox.'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "analyzer": "whitespace",
      "text":     "The quick brown fox."
    }

API 返回以下响应：

    
    
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
          "token": "quick",
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
          "token": "fox.",
          "start_offset": 16,
          "end_offset": 20,
          "type": "word",
          "position": 3
        }
      ]
    }

您还可以测试以下各项的组合：

* 一个分词器 * 零个或多个令牌过滤器 * 零个或多个字符过滤器

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'lowercase',
          'asciifolding'
        ],
        text: 'Is this déja vu?'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "standard",
      "filter":  [ "lowercase", "asciifolding" ],
      "text":      "Is this déja vu?"
    }

API 返回以下响应：

    
    
    {
      "tokens": [
        {
          "token": "is",
          "start_offset": 0,
          "end_offset": 2,
          "type": "<ALPHANUM>",
          "position": 0
        },
        {
          "token": "this",
          "start_offset": 3,
          "end_offset": 7,
          "type": "<ALPHANUM>",
          "position": 1
        },
        {
          "token": "deja",
          "start_offset": 8,
          "end_offset": 12,
          "type": "<ALPHANUM>",
          "position": 2
        },
        {
          "token": "vu",
          "start_offset": 13,
          "end_offset": 15,
          "type": "<ALPHANUM>",
          "position": 3
        }
      ]
    }

**位置和字符偏移**

从"分析"API 的输出中可以看出，分析器不仅将单词转换为术语，还记录每个术语_positions_of顺序或相对(用于短语查询或单词邻近查询)，以及原始文本中每个术语的开始和结束_character offsets_(用于突出显示搜索片段)。

或者，在特定索引上运行"分析"API 时，可以参考"自定义"分析器：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              std_folded: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'asciifolding'
                ]
              }
            }
          }
        },
        mappings: {
          properties: {
            my_text: {
              type: 'text',
              analyzer: 'std_folded'
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.analyze(
      index: 'my-index-000001',
      body: {
        analyzer: 'std_folded',
        text: 'Is this déjà vu?'
      }
    )
    puts response
    
    response = client.indices.analyze(
      index: 'my-index-000001',
      body: {
        field: 'my_text',
        text: 'Is this déjà vu?'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "std_folded": { __"type": "custom",
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "asciifolding"
              ]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "my_text": {
            "type": "text",
            "analyzer": "std_folded" __}
        }
      }
    }
    
    GET my-index-000001/_analyze __{
      "analyzer": "std_folded", __"text":     "Is this déjà vu?"
    }
    
    GET my-index-000001/_analyze __{
      "field": "my_text", __"text":  "Is this déjà vu?"
    }

API 返回以下响应：

    
    
    {
      "tokens": [
        {
          "token": "is",
          "start_offset": 0,
          "end_offset": 2,
          "type": "<ALPHANUM>",
          "position": 0
        },
        {
          "token": "this",
          "start_offset": 3,
          "end_offset": 7,
          "type": "<ALPHANUM>",
          "position": 1
        },
        {
          "token": "deja",
          "start_offset": 8,
          "end_offset": 12,
          "type": "<ALPHANUM>",
          "position": 2
        },
        {
          "token": "vu",
          "start_offset": 13,
          "end_offset": 15,
          "type": "<ALPHANUM>",
          "position": 3
        }
      ]
    }

__

|

定义一个名为"std_folded"的"自定义"分析器。   ---|---    __

|

字段"my_text"使用"std_folded"分析器。   __

|

若要引用此分析器，"分析"API 必须指定索引名称。   __

|

按名称引用分析器。   __

|

请参阅字段"my_text"使用的分析器。   « 配置文本分析 配置内置分析器 »