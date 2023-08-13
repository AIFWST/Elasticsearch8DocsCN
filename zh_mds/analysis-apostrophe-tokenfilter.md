

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Token filter reference](analysis-tokenfilters.md) [ASCII folding token
filter »](analysis-asciifolding-tokenfilter.md)

## 撇号标记过滤器

去除撇号后的所有字符，包括撇号本身。

此过滤器包含在 Elasticsearch 的内置土耳其语分析器中。它使用Lucene的ApostropheFilter，这是为土耳其语构建的。

###Example

以下分析 API 请求演示了撇号标记筛选器的工作原理。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'apostrophe'
        ],
        text: "Istanbul'a veya Istanbul'dan"
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "standard",
      "filter" : ["apostrophe"],
      "text" : "Istanbul'a veya Istanbul'dan"
    }

筛选器生成以下标记：

    
    
    [ Istanbul, veya, Istanbul ]

### 添加到分析器

以下创建索引 API请求使用撇号标记筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'apostrophe_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_apostrophe: {
                tokenizer: 'standard',
                filter: [
                  'apostrophe'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /apostrophe_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_apostrophe": {
              "tokenizer": "standard",
              "filter": [ "apostrophe" ]
            }
          }
        }
      }
    }

[« Token filter reference](analysis-tokenfilters.md) [ASCII folding token
filter »](analysis-asciifolding-tokenfilter.md)
