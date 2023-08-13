

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Phonetic token filter](analysis-phonetic-tokenfilter.md) [Predicate
script token filter »](analysis-predicatefilter-tokenfilter.md)

## 波特词干标记过滤器

基于波特词干算法为英语提供算法词干分析。

这个过滤器往往比其他英语词干过滤器(例如"kstem"过滤器)更积极地词干。

"porter_stem"过滤器等同于"词干"过滤器的"英语"变体。

"porter_stem"过滤器使用Lucene的PorterStemFilter。

###Example

以下分析 API 请求使用"porter_stem"过滤器将"狐狸快速跳跃"阻止为"狐狸快速跳跃"：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'porter_stem'
        ],
        text: 'the foxes jumping quickly'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "standard",
      "filter": [ "porter_stem" ],
      "text": "the foxes jumping quickly"
    }

筛选器生成以下标记：

    
    
    [ the, fox, jump, quickli ]

### 添加到分析器

以下创建索引 APIrequest 使用"porter_stem"筛选器来配置新的自定义分析器。

要正常工作，"porter_stem"筛选器需要小写标记。若要确保令牌为小写，请在分析器配置中的"porter_stem"筛选器之前添加"小写"筛选器。

    
    
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
                  'porter_stem'
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
                "porter_stem"
              ]
            }
          }
        }
      }
    }

[« Phonetic token filter](analysis-phonetic-tokenfilter.md) [Predicate
script token filter »](analysis-predicatefilter-tokenfilter.md)
