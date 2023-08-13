

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Shingle token filter](analysis-shingle-tokenfilter.md) [Stemmer token
filter »](analysis-stemmer-tokenfilter.md)

## 雪球令牌筛选器

使用 Snowball 生成的词干分析器对单词进行词干提取的筛选器。"language"参数使用以下可用值控制词干分析器："阿拉伯语"、"亚美尼亚语"、"巴斯克语"、"加泰罗尼亚语"、"丹麦语"、"荷兰语"、"英语"、"爱沙尼亚语"、"芬兰语"、"法语"、"德语"、"德语2"、"匈牙利语"、"意大利语"、"爱尔兰语"、"Kp"、"立陶宛语"、"洛文斯语"、"挪威语"、"波特语"、"葡萄牙语"、"罗马尼亚语"、"俄语"、"西班牙语"、"瑞典语"、"土耳其语"。

例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'my_snow'
                ]
              }
            },
            filter: {
              my_snow: {
                type: 'snowball',
                language: 'Lovins'
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
              "tokenizer": "standard",
              "filter": [ "lowercase", "my_snow" ]
            }
          },
          "filter": {
            "my_snow": {
              "type": "snowball",
              "language": "Lovins"
            }
          }
        }
      }
    }

[« Shingle token filter](analysis-shingle-tokenfilter.md) [Stemmer token
filter »](analysis-stemmer-tokenfilter.md)
