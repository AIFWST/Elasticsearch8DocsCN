

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Built-in analyzer reference](analysis-
analyzers.md)

[« Simple analyzer](analysis-simple-analyzer.md) [Stop analyzer »](analysis-
stop-analyzer.md)

## 标准分析器

"标准"分析器是默认分析器，如果未指定，则使用默认分析器。它提供基于语法的标记化(基于 Unicode 文本分割算法，如 Unicode 标准附件 #29 中指定)，适用于大多数语言。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'standard',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "analyzer": "standard",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下术语：

    
    
    [ the, 2, quick, brown, foxes, jumped, over, the, lazy, dog's, bone ]

###Configuration

"标准"分析器接受以下参数：

`max_token_length`

|

最大令牌长度。如果看到超过此长度的令牌，则以"max_token_length"间隔拆分。默认为"255"。   ---|---"停用词"

|

预定义的停用词列表，如"_English_"或包含停用词列表的数组。默认为"_none_"。   "stopwords_path"

|

包含停用词的文件的路径。   有关停用词配置的详细信息，请参阅停止标记筛选器。

### 配置示例

在此示例中，我们将"标准"分析器的"max_token_length"配置为 5(用于演示目的)，并使用预定义的英语停用词列表：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_english_analyzer: {
                type: 'standard',
                max_token_length: 5,
                stopwords: '_english_'
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
        analyzer: 'my_english_analyzer',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_english_analyzer": {
              "type": "standard",
              "max_token_length": 5,
              "stopwords": "_english_"
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_english_analyzer",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上面的示例生成以下术语：

    
    
    [ 2, quick, brown, foxes, jumpe, d, over, lazy, dog's, bone ]

###Definition

"标准"分析仪包括：

Tokenizer

    

* 标准分词器

令牌筛选器

    

* 小写令牌过滤器 * 停止令牌过滤器(默认禁用)

如果需要在配置参数之外自定义"标准"分析器，则需要将其重新创建为"自定义"分析器并对其进行修改，通常通过添加令牌筛选器。这将重新创建内置的"标准"分析器，您可以将其用作起点：

    
    
    response = client.indices.create(
      index: 'standard_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              rebuilt_standard: {
                tokenizer: 'standard',
                filter: [
                  'lowercase'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /standard_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "rebuilt_standard": {
              "tokenizer": "standard",
              "filter": [
                "lowercase"       __]
            }
          }
        }
      }
    }

__

|

您可以在"小写"之后添加任何令牌筛选器。   ---|--- « 简单的分析仪 停止分析仪 »