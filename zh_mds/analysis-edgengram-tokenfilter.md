

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Dictionary decompounder token filter](analysis-dict-decomp-
tokenfilter.md) [Elision token filter »](analysis-elision-tokenfilter.md)

## 边缘 n 元语法标记筛选器

从令牌的开头形成指定长度的 n 元语法。

例如，您可以使用"edge_ngram"令牌筛选器将"quick"更改为"qu"。

如果未自定义，筛选器默认创建 1 个字符的边缘 n-gram。

此过滤器使用 Lucene 的 EdgeNGramTokenFilter。

"edge_ngram"筛选器类似于"ngram"令牌筛选器。但是，"edge_ngram"仅输出从令牌开头开始的 n 元语法。这些边 n 元语法对于键入时搜索查询非常有用。

###Example

以下分析 API 请求使用"edge_ngram"筛选器将"快速棕色狐狸跳跃"转换为 1 个字符和 2 个字符的边缘 n 元语法：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          {
            type: 'edge_ngram',
            min_gram: 1,
            max_gram: 2
          }
        ],
        text: 'the quick brown fox jumps'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "standard",
      "filter": [
        { "type": "edge_ngram",
          "min_gram": 1,
          "max_gram": 2
        }
      ],
      "text": "the quick brown fox jumps"
    }

筛选器生成以下标记：

    
    
    [ t, th, q, qu, b, br, f, fo, j, ju ]

### 添加到分析器

以下创建索引 API请求使用"edge_ngram"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'edge_ngram_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_edge_ngram: {
                tokenizer: 'standard',
                filter: [
                  'edge_ngram'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT edge_ngram_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_edge_ngram": {
              "tokenizer": "standard",
              "filter": [ "edge_ngram" ]
            }
          }
        }
      }
    }

### 可配置参数

`max_gram`

    

(可选，整数)克的最大字符长度。对于自定义令牌筛选器，默认为"2"。对于内置的"edge_ngram"筛选器，默认为"1"。

请参阅"max_gram"参数的限制。

`min_gram`

     (Optional, integer) Minimum character length of a gram. Defaults to `1`. 
`preserve_original`

     (Optional, Boolean) Emits original token when set to `true`. Defaults to `false`. 
`side`

    

(可选，字符串)荒废的。指示是从"前面"还是"后面"截断令牌。默认为"正面"。

您可以在"edge_ngram"过滤器之前和之后使用"反向"令牌筛选器，而不是使用"back"值来实现相同的结果。

###Customize

要自定义"edge_ngram"筛选器，请复制它，为新的自定义令牌筛选器创建基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义"edge_ngram"筛选器，该筛选器在 3-5 个字符之间形成 n 元语法。

    
    
    response = client.indices.create(
      index: 'edge_ngram_custom_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              default: {
                tokenizer: 'whitespace',
                filter: [
                  '3_5_edgegrams'
                ]
              }
            },
            filter: {
              "3_5_edgegrams": {
                type: 'edge_ngram',
                min_gram: 3,
                max_gram: 5
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT edge_ngram_custom_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "default": {
              "tokenizer": "whitespace",
              "filter": [ "3_5_edgegrams" ]
            }
          },
          "filter": {
            "3_5_edgegrams": {
              "type": "edge_ngram",
              "min_gram": 3,
              "max_gram": 5
            }
          }
        }
      }
    }

### "max_gram"参数的限制

"edge_ngram"过滤器的"max_gram"值限制了令牌的字符长度。当"edge_ngram"筛选器与索引分析器一起使用时，这意味着长度超过"max_gram"长度的搜索词可能与任何索引词都不匹配。

例如，如果"max_gram"为"3"，则搜索"苹果"与索引字词"app"不匹配。

为此，您可以将"截断"筛选器与搜索分析器一起使用，以将搜索词缩短为"max_gram"字符长度。但是，这可能会返回不相关的结果。

例如，如果"max_gram"为"3"，搜索词被截断为三个字符，则搜索词"apple"将缩短为"app"。这意味着搜索"apple"会返回与"app"匹配的任何索引字词，例如"应用"、"贴靠"和"苹果"。

我们建议测试这两种方法，看看哪种方法最适合您的用例和所需的搜索体验。

[« Dictionary decompounder token filter](analysis-dict-decomp-
tokenfilter.md) [Elision token filter »](analysis-elision-tokenfilter.md)
