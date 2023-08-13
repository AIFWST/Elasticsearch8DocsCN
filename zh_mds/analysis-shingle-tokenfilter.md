

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Reverse token filter](analysis-reverse-tokenfilter.md) [Snowball token
filter »](analysis-snowball-tokenfilter.md)

## 瓦状令牌过滤器

通过连接相邻的标记，将带状疱疹或单词 n 元语法添加到令牌流。默认情况下，"瓦"标记过滤器输出两个单词的带状疱疹和单字母。

例如，许多分词器将"懒狗"转换为"[ 懒惰的狗 ]"。您可以使用"瓦片"过滤器向此流中添加两个单词的带状疱疹："[the，懒惰，懒惰，懒惰的狗，狗]"。

带状疱疹通常用于帮助加快短语查询速度，例如"match_phrase"。我们建议您在相应的文本字段上使用"索引短语"映射参数，而不是使用"带状疱疹"过滤器创建带状疱疹。

此过滤器使用Lucene的瓦片过滤器。

###Example

以下分析 API 请求使用"瓦片"筛选器将两个字的带状疱疹添加到"快速棕色狐狸跳跃"的令牌流中：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'shingle'
        ],
        text: 'quick brown fox jumps'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [ "shingle" ],
      "text": "quick brown fox jumps"
    }

筛选器生成以下标记：

    
    
    [ quick, quick brown, brown, brown fox, fox, fox jumps, jumps ]

要生成 2-3 个单词的带状疱疹，请将以下参数添加到 analyzeAPI 请求中：

* "min_shingle_size"： "2" * "max_shingle_size"： "3"

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'shingle',
            min_shingle_size: 2,
            max_shingle_size: 3
          }
        ],
        text: 'quick brown fox jumps'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        {
          "type": "shingle",
          "min_shingle_size": 2,
          "max_shingle_size": 3
        }
      ],
      "text": "quick brown fox jumps"
    }

筛选器生成以下标记：

    
    
    [ quick, quick brown, quick brown fox, brown, brown fox, brown fox jumps, fox, fox jumps, jumps ]

若要仅在输出中包含带状疱疹，请在请求中添加"output_unigrams"参数"false"。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'shingle',
            min_shingle_size: 2,
            max_shingle_size: 3,
            output_unigrams: false
          }
        ],
        text: 'quick brown fox jumps'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        {
          "type": "shingle",
          "min_shingle_size": 2,
          "max_shingle_size": 3,
          "output_unigrams": false
        }
      ],
      "text": "quick brown fox jumps"
    }

筛选器生成以下标记：

    
    
    [ quick brown, quick brown fox, brown fox, brown fox jumps, fox jumps ]

### 添加到分析器

以下创建索引 APIrequest 使用"瓦"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              standard_shingle: {
                tokenizer: 'standard',
                filter: [
                  'shingle'
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
            "standard_shingle": {
              "tokenizer": "standard",
              "filter": [ "shingle" ]
            }
          }
        }
      }
    }

### 可配置参数

`max_shingle_size`

    

(可选，整数)创建带状疱疹时要连接的最大令牌数。默认为"2"。

此值不能小于"min_shingle_size"参数，该参数默认为"2"。此值与"min_shingle_size"参数之间的差异不能超过"index.max_shingle_diff"索引级设置，该设置默认为"3"。

`min_shingle_size`

    

(可选，整数)创建带状疱疹时要连接的最小令牌数。默认为"2"。

此值不能超过默认为"2"的"max_shingle_size"参数。"max_shingle_size"参数与此值之间的差异不能超过"index.max_shingle_diff"索引级别设置，该设置默认为"3"。

`output_unigrams`

     (Optional, Boolean) If `true`, the output includes the original input tokens. If `false`, the output only includes shingles; the original input tokens are removed. Defaults to `true`. 
`output_unigrams_if_no_shingles`

    

如果为"true"，则仅当未生成带状疱疹时，输出才包含原始输入标记;如果生产带状疱疹，则输出仅包括带状疱疹。默认为"假"。

如果 this 和 'output_unigrams' 参数都是 'true'，则仅使用 'output_unigrams' 参数。

`token_separator`

     (Optional, string) Separator used to concatenate adjacent tokens to form a shingle. Defaults to a space (`" "`). 
`filler_token`

    

(可选，字符串)带状疱疹中使用的字符串，用于替代不包含令牌的空位置。此填充令牌仅用于无瓦，而不是原始的 unigram。默认为下划线 ('_') 。

某些标记筛选器(例如"停止"筛选器)在删除位置增量大于 1 的非索引字时会创建空位置。

**Example**

在下面的分析 API 请求中，"stop"过滤器从"狐狸跳懒狗"中删除停用词"a"，创建一个空仓位。随后的"带状疱疹"过滤器将这个空位置替换为带状疱疹中的加号("+")。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'stop',
            stopwords: [
              'a'
            ]
          },
          {
            type: 'shingle',
            filler_token: '+'
          }
        ],
        text: 'fox jumps a lazy dog'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        {
          "type": "stop",
          "stopwords": [ "a" ]
        },
        {
          "type": "shingle",
          "filler_token": "+"
        }
      ],
      "text": "fox jumps a lazy dog"
    }

筛选器生成以下标记：

    
    
    [ fox, fox jumps, jumps, jumps +, + lazy, lazy, lazy dog, dog ]

###Customize

要自定义"瓦状疱疹"过滤器，请复制它以创建新的自定义令牌过滤器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用自定义"瓦"筛选器"my_shingle_filter"来配置新的自定义分析器。

"my_shingle_filter"过滤器使用"2"的"min_shingle_size"和"5"的"max_shingle_size"，这意味着它会产生 2-5 个单词的带状疱疹。过滤器还包括一个"假"的"output_unigrams"参数，这意味着输出中只包含带状疱疹。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              en: {
                tokenizer: 'standard',
                filter: [
                  'my_shingle_filter'
                ]
              }
            },
            filter: {
              my_shingle_filter: {
                type: 'shingle',
                min_shingle_size: 2,
                max_shingle_size: 5,
                output_unigrams: false
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
            "en": {
              "tokenizer": "standard",
              "filter": [ "my_shingle_filter" ]
            }
          },
          "filter": {
            "my_shingle_filter": {
              "type": "shingle",
              "min_shingle_size": 2,
              "max_shingle_size": 5,
              "output_unigrams": false
            }
          }
        }
      }
    }

[« Reverse token filter](analysis-reverse-tokenfilter.md) [Snowball token
filter »](analysis-snowball-tokenfilter.md)
