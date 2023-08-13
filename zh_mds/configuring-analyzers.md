

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Configure text analysis](configure-text-
analysis.md)

[« Test an analyzer](test-analyzer.md) [Create a custom analyzer
»](analysis-custom-analyzer.md)

## 配置内置分析器

内置分析器无需任何配置即可直接使用。但是，其中一些支持配置选项来更改其行为。例如，可以将"标准"分析器配置为支持非索引字列表：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              std_english: {
                type: 'standard',
                stopwords: '_english_'
              }
            }
          }
        },
        mappings: {
          properties: {
            my_text: {
              type: 'text',
              analyzer: 'standard',
              fields: {
                english: {
                  type: 'text',
                  analyzer: 'std_english'
                }
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
        field: 'my_text',
        text: 'The old brown cow'
      }
    )
    puts response
    
    response = client.indices.analyze(
      index: 'my-index-000001',
      body: {
        field: 'my_text.english',
        text: 'The old brown cow'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "std_english": { __"type":      "standard",
              "stopwords": "_english_"
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "my_text": {
            "type":     "text",
            "analyzer": "standard", __"fields": {
              "english": {
                "type":     "text",
                "analyzer": "std_english" __}
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "field": "my_text", __"text": "The old brown cow"
    }
    
    POST my-index-000001/_analyze
    {
      "field": "my_text.english", __"text": "The old brown cow"
    }

__

|

我们将"std_english"分析器定义为基于"标准"分析器，但配置为删除预定义的英语停用词列表。   ---|---    __

|

"my_text"字段直接使用"标准"分析器，无需任何配置。不会从此字段中删除任何停用词。结果术语是："[ 的，旧的，棕色的，牛的]" __

|

"my_text.english"字段使用"std_english"分析器，因此英语非索引字将被删除。生成的术语是："老的、棕色的、牛的]' [« 测试分析器 创建自定义分析器»