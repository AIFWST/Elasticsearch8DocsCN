

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Character filters reference](analysis-
charfilters.md)

[« Character filters reference](analysis-charfilters.md) [Mapping character
filter »](analysis-mapping-charfilter.md)

## HTML 条带字符过滤器

从文本中去除 HTML 元素，并用其解码值替换 HTML 实体(例如，将"&amp;"替换为"&amp;")。

"html_strip"过滤器使用Lucene的HTMLStripCharFilter。

###Example

以下分析 API 请求使用"html_strip"筛选器更改文本"<p>我很高兴！<b></b></p>'\n我太高兴了！\n'。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        char_filter: [
          'html_strip'
        ],
        text: 'I&apos;m so happy</b>!</p>'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "keyword",
      "char_filter": [
        "html_strip"
      ],
      "text": "<p>I&apos;m so <b>happy</b>!</p>"
    }

筛选器生成以下文本：

    
    
    [ \nI'm so happy!\n ]

### 添加到分析器

以下创建索引 APIrequest 使用"html_strip"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'keyword',
                char_filter: [
                  'html_strip'
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
            "my_analyzer": {
              "tokenizer": "keyword",
              "char_filter": [
                "html_strip"
              ]
            }
          }
        }
      }
    }

### 可配置参数

`escaped_tags`

     (Optional, array of strings) Array of HTML elements without enclosing angle brackets (`< >`). The filter skips these HTML elements when stripping HTML from the text. For example, a value of `[ "p" ]` skips the `<p>` HTML element. 

###Customize

要自定义"html_strip"过滤器，请复制它以创建新的自定义字符过滤器的基础。您可以使用过滤器的可配置参数修改过滤器。

以下创建索引 APIrequest 使用自定义"html_strip"筛选器"my_custom_html_strip_char_filter"配置新的自定义分析器。

"my_custom_html_strip_char_filter"过滤器跳过"HTML 元素"的删除<b>。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'keyword',
                char_filter: [
                  'my_custom_html_strip_char_filter'
                ]
              }
            },
            char_filter: {
              my_custom_html_strip_char_filter: {
                type: 'html_strip',
                escaped_tags: [
                  'b'
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
            "my_analyzer": {
              "tokenizer": "keyword",
              "char_filter": [
                "my_custom_html_strip_char_filter"
              ]
            }
          },
          "char_filter": {
            "my_custom_html_strip_char_filter": {
              "type": "html_strip",
              "escaped_tags": [
                "b"
              ]
            }
          }
        }
      }
    }

[« Character filters reference](analysis-charfilters.md) [Mapping character
filter »](analysis-mapping-charfilter.md)
