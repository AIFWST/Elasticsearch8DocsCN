

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« ASCII folding token filter](analysis-asciifolding-tokenfilter.md) [CJK
width token filter »](analysis-cjk-width-tokenfilter.md)

## 中日韩双元标记筛选器

用中日韩(中文、日文和韩文)代币形成双拼图。

此过滤器包含在 Elasticsearch 内置的 CJK 语言分析器中。它使用Lucene的CJKBigramFilter。

###Example

以下分析 API 请求演示了 CJK 双元语法令牌筛选器的工作原理。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'cjk_bigram'
        ],
        text: '東京都は、日本の首都であり'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "standard",
      "filter" : ["cjk_bigram"],
      "text" : "東京都は、日本の首都であり"
    }

筛选器生成以下标记：

    
    
    [ 東京, 京都, 都は, 日本, 本の, の首, 首都, 都で, であ, あり ]

### 添加到分析器

以下创建索引 API请求使用 CJK 双元标记筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'cjk_bigram_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_cjk_bigram: {
                tokenizer: 'standard',
                filter: [
                  'cjk_bigram'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /cjk_bigram_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_cjk_bigram": {
              "tokenizer": "standard",
              "filter": [ "cjk_bigram" ]
            }
          }
        }
      }
    }

### 可配置参数

`ignored_scripts`

    

(可选，字符脚本数组)要禁用双字母的字符脚本数组。可能的值：

* "汉" * "韩文" * "平假名" * "片假名"

所有非 CJK 输入均未经修改地传递。

`output_unigrams`

     (Optional, Boolean) If `true`, emit tokens in both bigram and [unigram](https://en.wikipedia.org/wiki/N-gram) form. If `false`, a CJK character is output in unigram form when it has no adjacent characters. Defaults to `false`. 

###Customize

若要自定义 CJK 双元语法令牌筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

    
    
    response = client.indices.create(
      index: 'cjk_bigram_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              han_bigrams: {
                tokenizer: 'standard',
                filter: [
                  'han_bigrams_filter'
                ]
              }
            },
            filter: {
              han_bigrams_filter: {
                type: 'cjk_bigram',
                ignored_scripts: [
                  'hangul',
                  'hiragana',
                  'katakana'
                ],
                output_unigrams: true
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /cjk_bigram_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "han_bigrams": {
              "tokenizer": "standard",
              "filter": [ "han_bigrams_filter" ]
            }
          },
          "filter": {
            "han_bigrams_filter": {
              "type": "cjk_bigram",
              "ignored_scripts": [
                "hangul",
                "hiragana",
                "katakana"
              ],
              "output_unigrams": true
            }
          }
        }
      }
    }

[« ASCII folding token filter](analysis-asciifolding-tokenfilter.md) [CJK
width token filter »](analysis-cjk-width-tokenfilter.md)
