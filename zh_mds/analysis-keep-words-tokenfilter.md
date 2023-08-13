

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Keep types token filter](analysis-keep-types-tokenfilter.md) [Keyword
marker token filter »](analysis-keyword-marker-tokenfilter.md)

## 保留单词标记筛选器

仅保留指定单词列表中包含的标记。

此过滤器使用 Lucene 的 KeepWordFilter。

要从令牌流中删除单词列表，请使用"停止"过滤器。

###Example

以下分析 API 请求使用"保留"筛选器仅保留"快速狐狸跳过懒狗"中的"狐狸"和"狗"令牌。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          {
            type: 'keep',
            keep_words: [
              'dog',
              'elephant',
              'fox'
            ]
          }
        ],
        text: 'the quick fox jumps over the lazy dog'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "whitespace",
      "filter": [
        {
          "type": "keep",
          "keep_words": [ "dog", "elephant", "fox" ]
        }
      ],
      "text": "the quick fox jumps over the lazy dog"
    }

筛选器生成以下标记：

    
    
    [ fox, dog ]

### 可配置参数

`keep_words`

    

(必需*，字符串数组)要保留的单词列表。只有与此列表中的单词匹配的标记才会包含在输出中。

必须指定此参数或"keep_words_path"。

`keep_words_path`

    

(必需*，字符串数组)包含要保留的单词列表的文件的路径。只有与此列表中的单词匹配的标记才会包含在输出中。

此路径必须是绝对路径或相对于"配置"位置的路径，并且文件必须采用 UTF-8 编码。文件中的每个单词必须用换行符分隔。

必须指定此参数或"keep_words"。

`keep_words_case`

     (Optional, Boolean) If `true`, lowercase all keep words. Defaults to `false`. 

### 自定义并添加到分析器

要自定义"保留"过滤器，请复制它以创建新的自定义令牌过滤器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用自定义"保留"筛选器来配置两个新的自定义分析器：

* "standard_keep_word_array"，使用带有内联保留字数组的自定义"保留"过滤器 * "standard_keep_word_file"，使用带有保留字数文件的客户"保留"过滤器

    
    
    PUT keep_words_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_keep_word_array": {
              "tokenizer": "standard",
              "filter": [ "keep_word_array" ]
            },
            "standard_keep_word_file": {
              "tokenizer": "standard",
              "filter": [ "keep_word_file" ]
            }
          },
          "filter": {
            "keep_word_array": {
              "type": "keep",
              "keep_words": [ "one", "two", "three" ]
            },
            "keep_word_file": {
              "type": "keep",
              "keep_words_path": "analysis/example_word_list.txt"
            }
          }
        }
      }
    }

[« Keep types token filter](analysis-keep-types-tokenfilter.md) [Keyword
marker token filter »](analysis-keyword-marker-tokenfilter.md)
