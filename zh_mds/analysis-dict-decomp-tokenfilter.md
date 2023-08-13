

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Delimited payload token filter](analysis-delimited-payload-
tokenfilter.md) [Edge n-gram token filter »](analysis-edgengram-
tokenfilter.md)

## 字典解复合器令牌筛选器

在大多数情况下，我们建议使用更快的"hyphenation_decompounder"令牌筛选器来代替此筛选器。但是，您可以使用"dictionary_decompounder"过滤器来检查单词列表的质量，然后再在"hyphenation_decompounder"过滤器中实现它。

使用指定的单词列表和暴力方法来查找复合词中的子词。如果找到，这些子字将包含在令牌输出中。

此过滤器使用Lucene的DictionaryCompoundWordTokenFilter，这是为日耳曼语言构建的。

###Example

以下分析 API 请求使用"dictionary_decompounder"过滤器在"Donaudampfschiff"中查找子词。然后，过滤器根据指定的单词列表检查这些子单词："Donau"、"dampf"、"meer"和"schiff"。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          {
            type: 'dictionary_decompounder',
            word_list: [
              'Donau',
              'dampf',
              'meer',
              'schiff'
            ]
          }
        ],
        text: 'Donaudampfschiff'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "standard",
      "filter": [
        {
          "type": "dictionary_decompounder",
          "word_list": ["Donau", "dampf", "meer", "schiff"]
        }
      ],
      "text": "Donaudampfschiff"
    }

筛选器生成以下标记：

    
    
    [ Donaudampfschiff, Donau, dampf, schiff ]

### 可配置参数

`word_list`

    

(必需*，字符串数组)要在令牌流中查找的子词列表。如果找到，则子字将包含在令牌输出中。

必须指定此参数或"word_list_path"。

`word_list_path`

    

(必填*，字符串)包含要在令牌流中查找的子字列表的文件的路径。如果找到，则子字将包含在令牌输出中。

此路径必须是绝对路径或相对于"配置"位置的路径，并且文件必须采用 UTF-8 编码。文件中的每个标记必须用换行符分隔。

必须指定此参数或"word_list"。

`max_subword_size`

     (Optional, integer) Maximum subword character length. Longer subword tokens are excluded from the output. Defaults to `15`. 
`min_subword_size`

     (Optional, integer) Minimum subword character length. Shorter subword tokens are excluded from the output. Defaults to `2`. 
`min_word_size`

     (Optional, integer) Minimum word character length. Shorter word tokens are excluded from the output. Defaults to `5`. 
`only_longest_match`

     (Optional, Boolean) If `true`, only include the longest matching subword. Defaults to `false`. 

### 自定义并添加到分析器

要自定义"dictionary_decompounder"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用自定义"dictionary_decompounder"筛选器来配置新的自定义分析器。

自定义"dictionary_decompounder"过滤器在"分析/example_word_list.txt"文件中查找子词。超过 22 个字符的子字将从令牌输出中排除。

    
    
    PUT dictionary_decompound_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_dictionary_decompound": {
              "tokenizer": "standard",
              "filter": [ "22_char_dictionary_decompound" ]
            }
          },
          "filter": {
            "22_char_dictionary_decompound": {
              "type": "dictionary_decompounder",
              "word_list_path": "analysis/example_word_list.txt",
              "max_subword_size": 22
            }
          }
        }
      }
    }

[« Delimited payload token filter](analysis-delimited-payload-
tokenfilter.md) [Edge n-gram token filter »](analysis-edgengram-
tokenfilter.md)
