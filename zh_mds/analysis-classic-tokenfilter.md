

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« CJK width token filter](analysis-cjk-width-tokenfilter.md) [Common grams
token filter »](analysis-common-grams-tokenfilter.md)

## 经典令牌筛选器

对"经典"分词器生成的术语执行可选的后处理。

此过滤器从单词末尾删除英语所有格 (''s)，并从首字母缩略词中删除点。它使用Lucene的ClassicFilter。

###Example

以下分析 API 请求演示了经典令牌筛选器的工作原理。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'classic',
        filter: [
          'classic'
        ],
        text: "The 2 Q.U.I.C.K. Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "classic",
      "filter" : ["classic"],
      "text" : "The 2 Q.U.I.C.K. Brown-Foxes jumped over the lazy dog's bone."
    }

筛选器生成以下标记：

    
    
    [ The, 2, QUICK, Brown, Foxes, jumped, over, the, lazy, dog, bone ]

### 添加到分析器

以下创建索引 APIrequest 使用经典令牌筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'classic_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              classic_analyzer: {
                tokenizer: 'classic',
                filter: [
                  'classic'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /classic_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "classic_analyzer": {
              "tokenizer": "classic",
              "filter": [ "classic" ]
            }
          }
        }
      }
    }

[« CJK width token filter](analysis-cjk-width-tokenfilter.md) [Common grams
token filter »](analysis-common-grams-tokenfilter.md)
