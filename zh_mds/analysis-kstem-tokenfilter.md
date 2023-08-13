

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Keyword repeat token filter](analysis-keyword-repeat-tokenfilter.md)
[Length token filter »](analysis-length-tokenfilter.md)

## KStem 令牌筛选器

为英语提供基于 KStem 的词干分析。"kstem"过滤器将算法词干与内置字典相结合。

"kstem"过滤器的词干往往不如其他英语词干过滤器(例如"porter_stem"过滤器)那么激进。

"kstem"过滤器等同于"词干"过滤器的"light_english"变体。

此过滤器使用 Lucene 的 KStemFilter。

###Example

以下分析 API 请求使用"kstem"过滤器将"狐狸快速跳跃"阻止为"狐狸快速跳跃"：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'kstem'
        ],
        text: 'the foxes jumping quickly'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "standard",
      "filter": [ "kstem" ],
      "text": "the foxes jumping quickly"
    }

筛选器生成以下标记：

    
    
    [ the, fox, jump, quick ]

### 添加到分析器

以下创建索引 API请求使用"kstem"筛选器来配置新的自定义分析器。

为了正常工作，"kstem"过滤器需要小写标记。若要确保令牌为小写，请在分析器配置中的"kstem"筛选器之前添加"小写"筛选器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'whitespace',
                filter: [
                  'lowercase',
                  'kstem'
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
              "tokenizer": "whitespace",
              "filter": [
                "lowercase",
                "kstem"
              ]
            }
          }
        }
      }
    }

[« Keyword repeat token filter](analysis-keyword-repeat-tokenfilter.md)
[Length token filter »](analysis-length-tokenfilter.md)
