

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Stemmer token filter](analysis-stemmer-tokenfilter.md) [Stop token filter
»](analysis-stop-tokenfilter.md)

## 词干分析器覆盖令牌过滤器

通过应用自定义映射来覆盖词干算法，然后保护这些术语不被词干分析器修改。必须放在任何词干过滤器之前。

规则是"token1[， ...， tokenN] => override"形式的映射。

设定 |描述 ---|--- "规则"

|

要使用的映射规则列表。   "rules_path"

|

映射列表的路径(相对于"配置"位置或绝对路径)。   下面是一个示例：

    
    
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
                  'custom_stems',
                  'porter_stem'
                ]
              }
            },
            filter: {
              custom_stems: {
                type: 'stemmer_override',
                rules_path: 'analysis/stemmer_override.txt'
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
              "filter": [ "lowercase", "custom_stems", "porter_stem" ]
            }
          },
          "filter": {
            "custom_stems": {
              "type": "stemmer_override",
              "rules_path": "analysis/stemmer_override.txt"
            }
          }
        }
      }
    }

文件如下所示的位置：

    
    
    running, runs => run
    
    stemmer => stemmer

您还可以以内联方式定义覆盖规则：

    
    
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
                  'custom_stems',
                  'porter_stem'
                ]
              }
            },
            filter: {
              custom_stems: {
                type: 'stemmer_override',
                rules: [
                  'running, runs => run',
                  'stemmer => stemmer'
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
              "tokenizer": "standard",
              "filter": [ "lowercase", "custom_stems", "porter_stem" ]
            }
          },
          "filter": {
            "custom_stems": {
              "type": "stemmer_override",
              "rules": [
                "running, runs => run",
                "stemmer => stemmer"
              ]
            }
          }
        }
      }
    }

[« Stemmer token filter](analysis-stemmer-tokenfilter.md) [Stop token filter
»](analysis-stop-tokenfilter.md)
