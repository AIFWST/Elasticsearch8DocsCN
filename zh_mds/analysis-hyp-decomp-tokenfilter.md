

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Hunspell token filter](analysis-hunspell-tokenfilter.md) [Keep types
token filter »](analysis-keep-types-tokenfilter.md)

## 连字解复合器令牌筛选器

使用基于 XML 的断字模式查找复合词中的潜在子词。然后根据指定的单词列表检查这些子单词。不在列表中的子字将从令牌输出中排除。

此过滤器使用 Lucene 的 HyphenationCompoundWordTokenFilter，它是为日耳曼语言构建的。

###Example

以下分析 API 请求使用"hyphenation_decompounder"筛选器根据"分析/hyphenation_patterns.xml"文件中的德语连字模式查找"Kaffeetasse"中的子词。然后，过滤器根据指定单词的列表检查这些子单词："kaffee"、"zucker"和"tasse"。

    
    
    GET _analyze
    {
      "tokenizer": "standard",
      "filter": [
        {
          "type": "hyphenation_decompounder",
          "hyphenation_patterns_path": "analysis/hyphenation_patterns.xml",
          "word_list": ["Kaffee", "zucker", "tasse"]
        }
      ],
      "text": "Kaffeetasse"
    }

筛选器生成以下标记：

    
    
    [ Kaffeetasse, Kaffee, tasse ]

### 可配置参数

`hyphenation_patterns_path`

    

(必需，字符串)Apache FOP(格式化对象处理器)XML 断字模式文件的路径。

此路径必须是绝对路径或相对于"配置"位置的路径。仅支持 FOP v1.2 兼容文件。

例如，FOP XML 断字模式文件，请参阅：

* 用于格式化对象的对象 (OFFO) Sourceforge 项目 * offo-hyphenation_v1.2.zip 直接下载(不支持 v2.0 及以上连字模式文件)

`word_list`

    

(必需*，字符串数组)子词列表。使用断字模式找到但不在此列表中的子字将从标记输出中排除。

您可以使用"dictionary_decompounder"过滤器在实施单词列表之前测试单词列表的质量。

必须指定此参数或"word_list_path"。

`word_list_path`

    

(必填*，字符串)包含子单词列表的文件的路径。使用断字模式找到但不在此列表中的子字将从令牌输出中排除。

此路径必须是绝对路径或相对于"配置"位置的路径，并且文件必须采用 UTF-8 编码。文件中的每个标记必须用换行符分隔。

您可以使用"dictionary_decompounder"过滤器在实施单词列表之前测试单词列表的质量。

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

要自定义"hyphenation_decompounder"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用自定义"hyphenation_decompounder"筛选器来配置新的自定义分析器。

自定义"hyphenation_decompounder"过滤器根据"分析/hyphenation_patterns.xml"文件中的连字模式查找子词。然后，过滤器根据"分析/example_word_list.txt"文件中指定的单词列表检查这些子单词。超过 22 个字符的子字将从令牌输出中排除。

    
    
    PUT hyphenation_decompound_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "standard_hyphenation_decompound": {
              "tokenizer": "standard",
              "filter": [ "22_char_hyphenation_decompound" ]
            }
          },
          "filter": {
            "22_char_hyphenation_decompound": {
              "type": "hyphenation_decompounder",
              "word_list_path": "analysis/example_word_list.txt",
              "hyphenation_patterns_path": "analysis/hyphenation_patterns.xml",
              "max_subword_size": 22
            }
          }
        }
      }
    }

[« Hunspell token filter](analysis-hunspell-tokenfilter.md) [Keep types
token filter »](analysis-keep-types-tokenfilter.md)
