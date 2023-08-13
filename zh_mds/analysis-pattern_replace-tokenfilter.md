

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Pattern capture token filter](analysis-pattern-capture-tokenfilter.md)
[Phonetic token filter »](analysis-phonetic-tokenfilter.md)

## 模式替换令牌筛选器

使用正则表达式匹配和替换标记子字符串。

"pattern_replace"过滤器使用Java的正则表达式语法。默认情况下，筛选器将匹配的子字符串替换为空子字符串('""')。替换子字符串可以使用 Java 的"$g"语法从原始标记文本中引用捕获组。

编写不佳的正则表达式可能会运行缓慢或返回 aStackOverflowError，从而导致运行表达式的节点突然退出。

阅读更多关于病理正则表达式以及如何避免它们的信息。

此过滤器使用 Lucene 的 PatternReplaceFilter。

###Example

以下分析 API 请求使用"pattern_replace"筛选器将"watch"附加到"狐狸跳懒狗"中的子字符串"狗"前面。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'pattern_replace',
            pattern: '(dog)',
            replacement: 'watch$1'
          }
        ],
        text: 'foxes jump lazy dogs'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        {
          "type": "pattern_replace",
          "pattern": "(dog)",
          "replacement": "watch$1"
        }
      ],
      "text": "foxes jump lazy dogs"
    }

筛选器生成以下令牌。

    
    
    [ foxes, jump, lazy, watchdogs ]

### 可配置参数

`all`

     (Optional, Boolean) If `true`, all substrings matching the `pattern` parameter's regular expression are replaced. If `false`, the filter replaces only the first matching substring in each token. Defaults to `true`. 
`pattern`

     (Required, string) Regular expression, written in [Java's regular expression syntax](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html). The filter replaces token substrings matching this pattern with the substring in the `replacement` parameter. 
`replacement`

     (Optional, string) Replacement substring. Defaults to an empty substring (`""`). 

### 自定义并添加到分析器

要自定义"pattern_replace"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

以下创建索引 APIrequest 使用自定义"pattern_replace"筛选器"my_pattern_replace_filter"配置新的自定义分析器。

"my_pattern_replace_filter"过滤器使用正则表达式"[£|€]"来匹配并删除货币符号"£"和"€"。过滤器的"all"参数为"false"，这意味着仅删除每个标记中的第一个匹配符号。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'keyword',
                filter: [
                  'my_pattern_replace_filter'
                ]
              }
            },
            filter: {
              my_pattern_replace_filter: {
                type: 'pattern_replace',
                pattern: '[£|€]',
                replacement: '',
                all: false
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
              "tokenizer": "keyword",
              "filter": [
                "my_pattern_replace_filter"
              ]
            }
          },
          "filter": {
            "my_pattern_replace_filter": {
              "type": "pattern_replace",
              "pattern": "[£|€]",
              "replacement": "",
              "all": false
            }
          }
        }
      }
    }

[« Pattern capture token filter](analysis-pattern-capture-tokenfilter.md)
[Phonetic token filter »](analysis-phonetic-tokenfilter.md)
