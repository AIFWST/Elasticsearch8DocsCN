

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Uppercase token filter](analysis-uppercase-tokenfilter.md) [Word
delimiter graph token filter »](analysis-word-delimiter-graph-
tokenfilter.md)

## 单词分隔符标记筛选器

我们建议使用"word_delimiter_graph"而不是"word_delimiter"过滤器。

"word_delimiter"过滤器可能会生成无效的令牌图。请参阅"word_delimiter_graph"和"word_delimiter"之间的区别。

"word_delimiter"过滤器也使用 Lucene 的 WordDelimiterFilter，该过滤器被标记为已弃用。

在非字母数字字符处拆分标记。"word_delimiter"筛选器还根据一组规则执行可选的令牌规范化。默认情况下，筛选器使用以下规则：

* 将令牌拆分为非字母数字字符。筛选器使用这些字符作为分隔符。例如："超级杜珀"->"超级"、"骗子" * 从每个标记中删除前导或尾随分隔符。例如："XL---42+"自动编码器"->"XL"、"42"、"自动编码器" * 在字母大小写转换处拆分标记。例如："PowerShot" -> "Power"、"Shot" * 在字母数字转换处拆分标记。例如："XL500"->"XL"、"500" * 从每个标记的末尾删除英语所有格 (''s')。例如："尼尔的"->"尼尔"

"word_delimiter"过滤器旨在删除复杂标识符(例如产品 ID 或部件号)中的标点符号。对于这些用例，我们建议将"word_delimiter"过滤器与"关键字"分词器结合使用。

避免使用"word_delimiter"过滤器拆分带连字符的字词，例如"wi-fi"。由于用户经常搜索这些带有和不带连字符的字词，因此我们建议改用"synonym_graph"过滤器。

###Example

以下分析 API 请求使用"word_delimiter"筛选器使用筛选器的默认规则将"Neil's-Super-Duper-XL500--42+AutoCoder"拆分为规范化令牌：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        filter: [
          'word_delimiter'
        ],
        text: "Neil's-Super-Duper-XL500--42+AutoCoder"
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "keyword",
      "filter": [ "word_delimiter" ],
      "text": "Neil's-Super-Duper-XL500--42+AutoCoder"
    }

筛选器生成以下标记：

    
    
    [ Neil, Super, Duper, XL, 500, 42, Auto, Coder ]

### 添加到分析器

以下创建索引 API请求使用"word_delimiter"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'keyword',
                filter: [
                  'word_delimiter'
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
            "my_analyzer": {
              "tokenizer": "keyword",
              "filter": [ "word_delimiter" ]
            }
          }
        }
      }
    }

避免将"word_delimiter"筛选器与删除标点符号的分词器一起使用，例如"标准"分词器。这可能会阻止"word_delimiter"筛选器正确拆分令牌。它还会干扰过滤器的可配置参数，例如"catenate_all"或"preserve_original"。我们建议改用"关键字"或"空格"分词器。

### 可配置参数

`catenate_all`

    

(可选，布尔值)如果为"true"，则筛选器为由非字母分隔符分隔的字母数字字符链生成串联标记。例如： 'super-duper-xl-500' -> [ 'super'， **'superduperxl500'** ， 'duper'， 'xl'， '500' ]。默认为"假"。

当用于搜索分析时，串联令牌可能会导致"match_phrase"查询和其他依赖于令牌位置进行匹配的查询出现问题。如果计划使用这些查询，请避免将此参数设置为"true"。

`catenate_numbers`

    

(可选，布尔值)如果为"true"，则筛选器为由非字母分隔符分隔的数字字符链生成串联标记。例如："01-02-03" -> [ '01'， **'010203'** ， '02'， '03' ]。默认为"假"。

当用于搜索分析时，串联令牌可能会导致"match_phrase"查询和其他依赖于令牌位置进行匹配的查询出现问题。如果计划使用这些查询，请避免将此参数设置为"true"。

`catenate_words`

    

(可选，布尔值)如果为"true"，则筛选器为由非字母分隔符分隔的字母字符链生成串联标记。例如： 'super-duper-xl' -> [ 'super'， **'superduperxl'** ， 'duper'， 'xl' ]。默认为"假"。

当用于搜索分析时，串联令牌可能会导致"match_phrase"查询和其他依赖于令牌位置进行匹配的查询出现问题。如果计划使用这些查询，请避免将此参数设置为"true"。

`generate_number_parts`

     (Optional, Boolean) If `true`, the filter includes tokens consisting of only numeric characters in the output. If `false`, the filter excludes these tokens from the output. Defaults to `true`. 
`generate_word_parts`

     (Optional, Boolean) If `true`, the filter includes tokens consisting of only alphabetical characters in the output. If `false`, the filter excludes these tokens from the output. Defaults to `true`. 
`preserve_original`

     (Optional, Boolean) If `true`, the filter includes the original version of any split tokens in the output. This original version includes non-alphanumeric delimiters. For example: `super-duper-xl-500` -> [ **`super-duper-xl-500`** , `super`, `duper`, `xl`, `500` ]. Defaults to `false`. 
`protected_words`

     (Optional, array of strings) Array of tokens the filter won't split. 
`protected_words_path`

    

(可选，字符串)包含筛选器不会拆分的令牌列表的文件的路径。

此路径必须是绝对路径或相对于"配置"位置的路径，并且文件必须采用 UTF-8 编码。文件中的每个标记必须用换行符分隔。

`split_on_case_change`

     (Optional, Boolean) If `true`, the filter splits tokens at letter case transitions. For example: `camelCase` -> [ `camel`, `Case` ]. Defaults to `true`. 
`split_on_numerics`

     (Optional, Boolean) If `true`, the filter splits tokens at letter-number transitions. For example: `j2se` -> [ `j`, `2`, `se` ]. Defaults to `true`. 
`stem_english_possessive`

     (Optional, Boolean) If `true`, the filter removes the English possessive (`'s`) from the end of each token. For example: `O'Neil's` -> [ `O`, `Neil` ]. Defaults to `true`. 
`type_table`

    

(可选，字符串数组)字符的自定义类型映射数组。这允许您将非字母数字字符映射为数字或字母数字以避免拆分这些字符。

例如，以下数组将加号 ('+') 和连字符 ('-') 映射为字母数字，这意味着它们不会被视为分隔符：

'[ "+ => ALPHA"， "- => ALPHA" ]'

支持的类型包括：

* "字母"(字母顺序)* "字母数字"(字母数字) * "数字"(数字) * "小写"(小写字母顺序)* "SUBWORD_DELIM"(非字母数字分隔符)* "大写"(大写字母顺序)

`type_table_path`

    

(可选，字符串)包含字符的自定义类型映射的文件的路径。这允许您将非字母数字字符映射为数字或字母数字，以避免拆分这些字符。

例如，此文件的内容可能包含以下内容：

    
    
    # Map the $, %, '.', and ',' characters to DIGIT
    # This might be useful for financial data.
    $ => DIGIT
    % => DIGIT
    . => DIGIT
    \\u002C => DIGIT
    
    # in some cases you might not want to split on ZWJ
    # this also tests the case where we need a bigger byte[]
    # see https://en.wikipedia.org/wiki/Zero-width_joiner
    \\u200D => ALPHANUM

支持的类型包括：

* "字母"(字母顺序)* "字母数字"(字母数字) * "数字"(数字) * "小写"(小写字母顺序)* "SUBWORD_DELIM"(非字母数字分隔符)* "大写"(大写字母顺序)

此文件路径必须是绝对路径或相对于"配置"位置的路径，并且该文件必须采用 UTF-8 编码。文件中的每个映射都必须用换行符分隔。

###Customize

若要自定义"word_delimiter"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建使用以下规则的"word_delimiter"筛选器：

* 将标记拆分为非字母数字字符，_连字符 ('-') 字符除外。  * 从每个标记中删除前导或尾随分隔符。  * 不要_在字母大小写转换处拆分标记。  * 不要在字母数字转换处拆分令牌。  * 从每个标记的末尾删除英文所有格 (''s')。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'keyword',
                filter: [
                  'my_custom_word_delimiter_filter'
                ]
              }
            },
            filter: {
              my_custom_word_delimiter_filter: {
                type: 'word_delimiter',
                type_table: [
                  '- => ALPHA'
                ],
                split_on_case_change: false,
                split_on_numerics: false,
                stem_english_possessive: true
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
              "filter": [ "my_custom_word_delimiter_filter" ]
            }
          },
          "filter": {
            "my_custom_word_delimiter_filter": {
              "type": "word_delimiter",
              "type_table": [ "- => ALPHA" ],
              "split_on_case_change": false,
              "split_on_numerics": false,
              "stem_english_possessive": true
            }
          }
        }
      }
    }

[« Uppercase token filter](analysis-uppercase-tokenfilter.md) [Word
delimiter graph token filter »](analysis-word-delimiter-graph-
tokenfilter.md)
