

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Character filters reference](analysis-
charfilters.md)

[« Mapping character filter](analysis-mapping-charfilter.md) [Normalizers
»](analysis-normalizers.md)

## 模式替换字符过滤器

"pattern_replace"字符筛选器使用正则表达式来匹配应替换为指定替换字符串的字符。放置字符串可以引用正则表达式中的捕获组。

### 当心病态正则表达式

模式替换字符过滤器使用 Java 正则表达式。

一个写得不好的正则表达式可能会运行得非常慢，甚至抛出 aStackOverflowError 并导致它运行的节点突然退出。

阅读更多关于病理正则表达式以及如何避免它们的信息。

###Configuration

"pattern_replace"字符筛选器接受以下参数：

`pattern`

|

Java 正则表达式。必填。   ---|---"替换"

|

替换字符串，可以使用"$1"引用捕获组。"$9"语法，如此处所述。   "旗帜"

|

Java 正则表达式标志。标志应该是管道分隔的，例如 '"CASE_INSENSITIVE|评论"'。   ### 示例配置编辑

在此示例中，我们配置"pattern_replace"字符过滤器，以将数字中任何嵌入的破折号替换为下划线，即"123-456-789"->"123_456_789"：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                char_filter: [
                  'my_char_filter'
                ]
              }
            },
            char_filter: {
              my_char_filter: {
                type: 'pattern_replace',
                pattern: '(\\d+)-(?=\\d)',
                replacement: '$1_'
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
        text: 'My credit card is 123-456-789'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "standard",
              "char_filter": [
                "my_char_filter"
              ]
            }
          },
          "char_filter": {
            "my_char_filter": {
              "type": "pattern_replace",
              "pattern": "(\\d+)-(?=\\d)",
              "replacement": "$1_"
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "My credit card is 123-456-789"
    }

上面的示例生成以下术语：

    
    
    [ My, credit, card, is, 123_456_789 ]

使用更改原始文本长度的替换字符串将用于搜索目的，但会导致不正确的突出显示，如以下示例所示。

本示例在遇到后跟大写字母(即"fooBarBaz"->"foo Bar Baz")时插入一个空格，允许单独查询驼峰大小写单词：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                char_filter: [
                  'my_char_filter'
                ],
                filter: [
                  'lowercase'
                ]
              }
            },
            char_filter: {
              my_char_filter: {
                type: 'pattern_replace',
                pattern: '(?<=\\p{Lower})(?=\\p{Upper})',
                replacement: ' '
              }
            }
          }
        },
        mappings: {
          properties: {
            text: {
              type: 'text',
              analyzer: 'my_analyzer'
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
        text: 'The fooBarBaz method'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "standard",
              "char_filter": [
                "my_char_filter"
              ],
              "filter": [
                "lowercase"
              ]
            }
          },
          "char_filter": {
            "my_char_filter": {
              "type": "pattern_replace",
              "pattern": "(?<=\\p{Lower})(?=\\p{Upper})",
              "replacement": " "
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "text": {
            "type": "text",
            "analyzer": "my_analyzer"
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "The fooBarBaz method"
    }

以上返回以下术语：

    
    
    [ the, foo, bar, baz, method ]

查询"bar"将正确找到文档，但在结果上突出显示会产生不正确的突出显示，因为我们的字符过滤器更改了原始文本的长度：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        text: 'The fooBarBaz method'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            text: 'bar'
          }
        },
        highlight: {
          fields: {
            text: {}
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?refresh
    {
      "text": "The fooBarBaz method"
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "text": "bar"
        }
      },
      "highlight": {
        "fields": {
          "text": {}
        }
      }
    }

上面的输出是：

    
    
    {
      "timed_out": false,
      "took": $body.took,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.2876821,
        "hits": [
          {
            "_index": "my-index-000001",
            "_id": "1",
            "_score": 0.2876821,
            "_source": {
              "text": "The fooBarBaz method"
            },
            "highlight": {
              "text": [
                "The foo<em>Ba</em>rBaz method" __]
            }
          }
        ]
      }
    }

__

|

请注意不正确的突出显示。   ---|--- « 映射字符过滤器规范化器»