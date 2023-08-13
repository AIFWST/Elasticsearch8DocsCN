

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Configure text analysis](configure-text-
analysis.md)

[« Configuring built-in analyzers](configuring-analyzers.md) [Specify an
analyzer »](specify-analyzer.md)

## 创建自定义分析器

当内置分析器不能满足您的需求时，您可以创建一个"自定义"分析器，该分析器使用以下各项的适当组合：

* 零个或多个字符过滤器 * 一个分词器 * 零个或多个令牌过滤器。

###Configuration

"自定义"分析器接受以下参数：

`type`

|

分析器类型。接受内置分析器类型。对于自定义分析器，请使用"自定义"或省略此参数。   ---|--- "分词器"

|

内置或自定义的分词器。(必填) "char_filter"

|

内置或自定义字符筛选器的可选数组。   "过滤器"

|

内置或自定义令牌筛选器的可选数组。   "position_increment_gap"

|

在索引文本值数组时，Elasticsearch 在一个值的最后一个术语和下一个值的第一个术语之间插入一个假的"间隙"，以确保短语查询与来自不同数组元素的两个术语不匹配。默认为"100"。请参阅"position_increment_gap"了解更多信息。   ### 示例配置编辑

下面是一个组合以下内容的示例：

字符过滤器

    

* HTML 条形字符过滤器

Tokenizer

    

* 标准分词器

令牌筛选器

    

* 小写令牌过滤器 * ASCII 折叠令牌过滤器

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_custom_analyzer: {
                type: 'custom',
                tokenizer: 'standard',
                char_filter: [
                  'html_strip'
                ],
                filter: [
                  'lowercase',
                  'asciifolding'
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
        analyzer: 'my_custom_analyzer',
        text: 'Is this déjà vu</b>?'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_custom_analyzer": {
              "type": "custom", __"tokenizer": "standard",
              "char_filter": [
                "html_strip"
              ],
              "filter": [
                "lowercase",
                "asciifolding"
              ]
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_custom_analyzer",
      "text": "Is this <b>déjà vu</b>?"
    }

__

|

对于"自定义"分析器，请使用"自定义"的"类型"或省略"类型"参数。   ---|--- 上面的示例生成以下术语：

    
    
    [ is, this, deja, vu ]

前面的示例使用分词器、标记筛选器和字符筛选器及其默认配置，但可以创建每个版本的配置版本并在自定义分析器中使用它们。

下面是一个更复杂的示例，它结合了以下内容：

字符过滤器

    

* 映射字符过滤器，配置为将":)"替换为"_happy_"，将":("替换为"_sad_"

Tokenizer

    

* 模式分词器，配置为拆分标点字符

令牌筛选器

    

* 小写令牌过滤器 * 停止令牌过滤器，配置为使用预定义的英语停用词列表

下面是一个示例：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_custom_analyzer: {
                char_filter: [
                  'emoticons'
                ],
                tokenizer: 'punctuation',
                filter: [
                  'lowercase',
                  'english_stop'
                ]
              }
            },
            tokenizer: {
              punctuation: {
                type: 'pattern',
                pattern: '[ .,!?]'
              }
            },
            char_filter: {
              emoticons: {
                type: 'mapping',
                mappings: [
                  ':) => _happy_',
                  ':( => _sad_'
                ]
              }
            },
            filter: {
              english_stop: {
                type: 'stop',
                stopwords: '_english_'
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
        analyzer: 'my_custom_analyzer',
        text: "I'm a :) person, and you?"
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_custom_analyzer": { __"char_filter": [
                "emoticons"
              ],
              "tokenizer": "punctuation",
              "filter": [
                "lowercase",
                "english_stop"
              ]
            }
          },
          "tokenizer": {
            "punctuation": { __"type": "pattern",
              "pattern": "[ .,!?]"
            }
          },
          "char_filter": {
            "emoticons": { __"type": "mapping",
              "mappings": [
                ":) = > _happy_",
                ":( => _sad_"
              ]
            }
          },
          "filter": {
            "english_stop": { __"type": "stop",
              "stopwords": "_english_"
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_custom_analyzer",
      "text": "I'm a :) person, and you?"
    }

__

|

为索引分配一个默认的自定义分析器"my_custom_analyzer"。此分析器使用稍后在请求中定义的自定义分词器、字符筛选器和标记筛选器。此分析器还省略了"类型"参数。   ---|---    __

|

定义自定义"标点符号"分词器。   __

|

定义自定义"表情符号"字符筛选器。   __

|

定义自定义"english_stop"令牌筛选器。   上面的示例生成以下术语：

    
    
    [ i'm, _happy_, person, you ]

[« Configuring built-in analyzers](configuring-analyzers.md) [Specify an
analyzer »](specify-analyzer.md)
