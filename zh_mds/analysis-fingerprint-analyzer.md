

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Built-in analyzer reference](analysis-
analyzers.md)

[« Built-in analyzer reference](analysis-analyzers.md) [Keyword analyzer
»](analysis-keyword-analyzer.md)

## 指纹分析仪

"指纹"分析器实现了OpenRefine项目用来协助聚类的指纹算法。

输入文本为小写，规范化以删除扩展字符，排序，重复数据删除并连接成单个标记。如果配置了非索引字列表，则非索引字也将被删除。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        analyzer: 'fingerprint',
        text: 'Yes yes, Gödel said this sentence is consistent and.'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "analyzer": "fingerprint",
      "text": "Yes yes, Gödel said this sentence is consistent and."
    }

上述句子将产生以下单一术语：

    
    
    [ and consistent godel is said sentence this yes ]

###Configuration

"指纹"分析器接受以下参数：

`separator`

|

用于连接术语的字符。默认为空格。   ---|--- "max_output_size"

|

要发出的最大令牌大小。默认为"255"。大于此大小的令牌将被丢弃。   "停用词"

|

预定义的停用词列表，如"_English_"或包含停用词列表的数组。默认为"_none_"。   "stopwords_path"

|

包含停用词的文件的路径。   有关停用词配置的详细信息，请参阅停止标记筛选器。

### 配置示例

在此示例中，我们将"指纹"分析器配置为使用预定义的英语停用词列表：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_fingerprint_analyzer: {
                type: 'fingerprint',
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
        analyzer: 'my_fingerprint_analyzer',
        text: 'Yes yes, Gödel said this sentence is consistent and.'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_fingerprint_analyzer": {
              "type": "fingerprint",
              "stopwords": "_english_"
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_fingerprint_analyzer",
      "text": "Yes yes, Gödel said this sentence is consistent and."
    }

上面的示例生成以下术语：

    
    
    [ consistent godel said sentence yes ]

###Definition

"指纹"标记器包括：

Tokenizer

    

* 标准分词器

令牌筛选器(按顺序)

    

* 小写令牌过滤器 * ASCII 折叠 * 停止令牌过滤器(默认禁用) * 指纹

如果您需要自定义配置参数之外的"指纹"分析器，则需要将其重新创建为"自定义"分析器并对其进行修改，通常通过添加令牌过滤器。这将重新创建内置的"指纹"分析器，您可以将其用作进一步自定义的起点：

    
    
    response = client.indices.create(
      index: 'fingerprint_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              rebuilt_fingerprint: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'asciifolding',
                  'fingerprint'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /fingerprint_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "rebuilt_fingerprint": {
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "asciifolding",
                "fingerprint"
              ]
            }
          }
        }
      }
    }

[« Built-in analyzer reference](analysis-analyzers.md) [Keyword analyzer
»](analysis-keyword-analyzer.md)
