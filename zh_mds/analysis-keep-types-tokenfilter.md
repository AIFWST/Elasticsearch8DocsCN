

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Hyphenation decompounder token filter](analysis-hyp-decomp-
tokenfilter.md) [Keep words token filter »](analysis-keep-words-
tokenfilter.md)

## 保留类型标记筛选器

保留或删除特定类型的令牌。例如，您可以使用此过滤器通过仅保留"<ALPHANUM>(字母数字)标记"将"3 只快速狐狸"更改为"快速狐狸"。

### 令牌类型

令牌类型由分词器在将字符转换为令牌时设置。令牌类型在令牌化器之间可能有所不同。

例如，"标准"标记器可以生成各种令牌类型，包括"、"<ALPHANUM><HANGUL>"和<NUM>""。更简单的分析器，如"小写"标记器，仅生成"单词"标记类型。

某些令牌筛选器还可以添加令牌类型。例如，"同义词"筛选器可以添加<SYNONYM>""令牌类型。

某些分词器不支持此分词筛选器，例如关键字、simple_pattern和simple_pattern_split分词器，因为它们不支持设置令牌类型属性。

此筛选器使用 Lucene 的类型令牌筛选器。

### 包含示例

以下分析 API 请求使用"keep_types"筛选器仅保留"<NUM>1 只快狐 2 只懒狗"中的""(数字)令牌。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          {
            type: 'keep_types',
            types: [
              '<NUM>'
            ]
          }
        ],
        text: '1 quick fox 2 lazy dogs'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "standard",
      "filter": [
        {
          "type": "keep_types",
          "types": [ "<NUM>" ]
        }
      ],
      "text": "1 quick fox 2 lazy dogs"
    }

筛选器生成以下标记：

    
    
    [ 1, 2 ]

### 排除示例

以下分析 API 请求使用"keep_types"筛选器从"<NUM>1 只快速狐狸 2 只懒狗"中删除""令牌。请注意，"模式"参数设置为"排除"。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          {
            type: 'keep_types',
            types: [
              '<NUM>'
            ],
            mode: 'exclude'
          }
        ],
        text: '1 quick fox 2 lazy dogs'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "standard",
      "filter": [
        {
          "type": "keep_types",
          "types": [ "<NUM>" ],
          "mode": "exclude"
        }
      ],
      "text": "1 quick fox 2 lazy dogs"
    }

筛选器生成以下标记：

    
    
    [ quick, fox, lazy, dogs ]

### 可配置参数

`types`

     (Required, array of strings) List of token types to keep or remove. 
`mode`

    

(可选，字符串)指示是保留还是删除指定的标记类型。有效值为：

`include`

     (Default) Keep only the specified token types. 
`exclude`

     Remove the specified token types. 

### 自定义并添加到分析器

要自定义"keep_types"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用自定义"keep_types"筛选器来配置新的自定义分析器。自定义"keep_types"筛选器仅保留<ALPHANUM>"(字母数字)标记。

    
    
    response = client.indices.create(
      index: 'keep_types_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                filter: [
                  'extract_alpha'
                ]
              }
            },
            filter: {
              extract_alpha: {
                type: 'keep_types',
                types: [
                  '<ALPHANUM>'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT keep_types_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "standard",
              "filter": [ "extract_alpha" ]
            }
          },
          "filter": {
            "extract_alpha": {
              "type": "keep_types",
              "types": [ "<ALPHANUM>" ]
            }
          }
        }
      }
    }

[« Hyphenation decompounder token filter](analysis-hyp-decomp-
tokenfilter.md) [Keep words token filter »](analysis-keep-words-
tokenfilter.md)
