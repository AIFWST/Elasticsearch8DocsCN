

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« CJK bigram token filter](analysis-cjk-bigram-tokenfilter.md) [Classic
token filter »](analysis-classic-tokenfilter.md)

## 中日韩宽度标记筛选器

规范化 CJK(中文、日语和韩语)字符的宽度差异如下：

* 将全角 ASCII 字符变体折叠为等效的基本拉丁字符 * 将半角片假名字符变体折叠为等效的假名字符

此过滤器包含在 Elasticsearch 内置的 CJK 语言分析器中。它使用Lucene的CJKWidthFilter。

此令牌筛选器可以被视为 NFKC/NFKD Unicodenormalization 的子集。请参阅"分析-icu"插件以获得完整的规范化支持。

###Example

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'cjk_width'
        ],
        text: 'ｼｰｻｲﾄﾞﾗｲﾅｰ'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer" : "standard",
      "filter" : ["cjk_width"],
      "text" : "ｼｰｻｲﾄﾞﾗｲﾅｰ"
    }

筛选器生成以下令牌：

    
    
    シーサイドライナー

### 添加到分析器

以下创建索引 API请求使用 CJK 宽度令牌筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'cjk_width_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_cjk_width: {
                tokenizer: 'standard',
                filter: [
                  'cjk_width'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /cjk_width_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_cjk_width": {
              "tokenizer": "standard",
              "filter": [ "cjk_width" ]
            }
          }
        }
      }
    }

[« CJK bigram token filter](analysis-cjk-bigram-tokenfilter.md) [Classic
token filter »](analysis-classic-tokenfilter.md)
