

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Built-in analyzer reference](analysis-
analyzers.md)

[« Standard analyzer](analysis-standard-analyzer.md) [Whitespace analyzer
»](analysis-whitespace-analyzer.md)

## 停止分析器

"stop"分析器与"简单"分析器相同，但增加了对删除停用词的支持。它默认使用"_English_"停用词。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'stop',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "analyzer": "stop",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下术语：

    
    
    [ quick, brown, foxes, jumped, over, lazy, dog, s, bone ]

###Configuration

"停止"分析器接受以下参数：

`stopwords`

|

预定义的停用词列表，如"_English_"或包含停用词列表的数组。默认为"_英语_"。   ---|--- "stopwords_path"

|

包含停用词的文件的路径。此路径相对于 Elasticsearch 'config' 目录。   有关停用词配置的详细信息，请参阅停止标记筛选器。

### 配置示例

在此示例中，我们将"stop"分析器配置为使用指定的单词列表作为停用词：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_stop_analyzer: {
                type: 'stop',
                stopwords: [
                  'the',
                  'over'
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
        analyzer: 'my_stop_analyzer',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_stop_analyzer": {
              "type": "stop",
              "stopwords": ["the", "over"]
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_stop_analyzer",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上面的示例生成以下术语：

    
    
    [ quick, brown, foxes, jumped, lazy, dog, s, bone ]

###Definition

它包括：

Tokenizer

    

* 小写分词器

令牌筛选器

    

* 停止令牌过滤器

如果需要在配置参数之外自定义"停止"分析器，则需要将其重新创建为"自定义"分析器并对其进行修改，通常通过添加令牌过滤器。这将重新创建内置的"stop"分析器，您可以将其用作进一步自定义的起点：

    
    
    response = client.indices.create(
      index: 'stop_example',
      body: {
        settings: {
          analysis: {
            filter: {
              english_stop: {
                type: 'stop',
                stopwords: '_english_'
              }
            },
            analyzer: {
              rebuilt_stop: {
                tokenizer: 'lowercase',
                filter: [
                  'english_stop'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /stop_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "english_stop": {
              "type":       "stop",
              "stopwords":  "_english_" __}
          },
          "analyzer": {
            "rebuilt_stop": {
              "tokenizer": "lowercase",
              "filter": [
                "english_stop" __]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

您可以在"english_stop"之后添加任何令牌筛选器。   « 标准分析仪 空白分析仪»