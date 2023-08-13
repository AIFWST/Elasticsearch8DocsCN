

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Word delimiter token filter](analysis-word-delimiter-tokenfilter.md)
[Character filters reference »](analysis-charfilters.md)

## 单词分隔符图标记筛选器

在非字母数字字符处拆分标记。"word_delimiter_graph"筛选器还根据一组规则执行可选的令牌规范化。默认情况下，筛选器使用以下规则：

* 将令牌拆分为非字母数字字符。筛选器使用这些字符作为分隔符。例如："超级杜珀"->"超级"、"骗子" * 从每个标记中删除前导或尾随分隔符。例如："XL---42+"自动编码器"->"XL"、"42"、"自动编码器" * 在字母大小写转换处拆分标记。例如："PowerShot" -> "Power"、"Shot" * 在字母数字转换处拆分标记。例如："XL500"->"XL"、"500" * 从每个标记的末尾删除英语所有格 (''s')。例如："尼尔的"->"尼尔"

"word_delimiter_graph"过滤器使用 Lucene 的 WordDelimiterGraphFilter。

"word_delimiter_graph"过滤器旨在从复杂的标识符(例如产品 ID 或部件号)中删除标点符号。对于这些用例，我们建议将"word_delimiter_graph"过滤器与"关键字"分词器一起使用。

避免使用"word_delimiter_graph"过滤器拆分带连字符的单词，例如"wi-fi"。由于用户经常搜索这些带有和不带连字符的字词，因此我们建议改用"synonym_graph"过滤器。

###Example

以下分析 API 请求使用"word_delimiter_graph"筛选器使用筛选器的默认规则将"Neil's-Super-Duper-XL500--42+AutoCoder"拆分为规范化令牌：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        filter: [
          'word_delimiter_graph'
        ],
        text: "Neil's-Super-Duper-XL500--42+AutoCoder"
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "keyword",
      "filter": [ "word_delimiter_graph" ],
      "text": "Neil's-Super-Duper-XL500--42+AutoCoder"
    }

筛选器生成以下标记：

    
    
    [ Neil, Super, Duper, XL, 500, 42, Auto, Coder ]

### 添加到分析器

以下创建索引 APIrequest 使用"word_delimiter_graph"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'keyword',
                filter: [
                  'word_delimiter_graph'
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
              "filter": [ "word_delimiter_graph" ]
            }
          }
        }
      }
    }

避免将"word_delimiter_graph"筛选器与删除标点符号的分词器一起使用，例如"标准"分词器。这可能会阻止"word_delimiter_graph"过滤器正确拆分令牌。它还会干扰过滤器的可配置参数，例如"catenate_all"或"preserve_original"。我们建议改用"关键字"或"空格"标记器。

### 可配置参数

`adjust_offsets`

    

(可选，布尔值)如果为"true"，则筛选器将调整拆分或级联令牌的偏移量，以更好地反映它们在令牌流中的实际位置。默认为"真"。

如果分析器使用筛选器(例如"trim"筛选器)更改令牌长度而不更改其偏移量，请将"adjust_offsets"设置为"false"。否则，"word_delimiter_graph"筛选器可能会生成具有非法偏移量的令牌。

`catenate_all`

    

(可选，布尔值)如果为"true"，则筛选器为由非字母分隔符分隔的字母数字字符链生成串联标记。例如： 'super-duper-xl-500' -> [ **'super-duperxl500'** ， 'super'， 'duper'， 'xl'， '500' ]。默认为"假"。

将此参数设置为"true"会生成索引不支持的多位置令牌。

如果此参数为"true"，请避免在索引分析器中使用此筛选器，或在此筛选器之后使用"flatten_graph"筛选器，以使令牌流适合索引。

当用于搜索分析时，串联令牌可能会导致"match_phrase"查询和其他依赖于令牌位置进行匹配的查询出现问题。如果计划使用这些查询，请避免将此参数设置为"true"。

`catenate_numbers`

    

(可选，布尔值)如果为"true"，则筛选器为由非字母分隔符分隔的数字字符链生成串联标记。例如："01-02-03" -> [ **'010203'** ， '01'， '02'， '03' ]。默认为"假"。

将此参数设置为"true"会生成索引不支持的多位置令牌。

如果此参数为"true"，请避免在索引分析器中使用此筛选器，或在此筛选器之后使用"flatten_graph"筛选器，以使令牌流适合索引。

当用于搜索分析时，串联令牌可能会导致"match_phrase"查询和其他依赖于令牌位置进行匹配的查询出现问题。如果计划使用这些查询，请避免将此参数设置为"true"。

`catenate_words`

    

(可选，布尔值)如果为"true"，则筛选器为由非字母分隔符分隔的字母字符链生成串联标记。例如： 'super-duper-xl' -> [ **'superduperxl'** ， 'super'， 'duper'， 'xl' ]。默认为"假"。

将此参数设置为"true"会生成索引不支持的多位置令牌。

如果此参数为"true"，请避免在索引分析器中使用此筛选器，或在此筛选器之后使用"flatten_graph"筛选器，以使令牌流适合索引。

当用于搜索分析时，串联令牌可能会导致"match_phrase"查询和其他依赖于令牌位置进行匹配的查询出现问题。如果计划使用这些查询，请避免将此参数设置为"true"。

`generate_number_parts`

     (Optional, Boolean) If `true`, the filter includes tokens consisting of only numeric characters in the output. If `false`, the filter excludes these tokens from the output. Defaults to `true`. 
`generate_word_parts`

     (Optional, Boolean) If `true`, the filter includes tokens consisting of only alphabetical characters in the output. If `false`, the filter excludes these tokens from the output. Defaults to `true`. 
`ignore_keywords`

     (Optional, Boolean) If `true`, the filter skips tokens with a `keyword` attribute of `true`. Defaults to `false`. 

`preserve_original`

    

(可选，布尔值)如果为"true"，则筛选器在输出中包含任意拆分令牌的原始版本。此原始版本包括非字母数字分隔符。例如："超级骗子-xl-500" -> [ **'超级骗子-xl-500'** ，'超级'， '骗子'， 'xl'， '500' ]。默认为"假"。

将此参数设置为"true"会生成索引不支持的多位置令牌。

如果此参数为"true"，请避免在索引分析器中使用此筛选器，或在此筛选器之后使用"flatten_graph"筛选器，以使令牌流适合索引。

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

要自定义"word_delimiter_graph"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个使用以下规则的"word_delimiter_graph"筛选器：

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
                  'my_custom_word_delimiter_graph_filter'
                ]
              }
            },
            filter: {
              my_custom_word_delimiter_graph_filter: {
                type: 'word_delimiter_graph',
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
              "filter": [ "my_custom_word_delimiter_graph_filter" ]
            }
          },
          "filter": {
            "my_custom_word_delimiter_graph_filter": {
              "type": "word_delimiter_graph",
              "type_table": [ "- => ALPHA" ],
              "split_on_case_change": false,
              "split_on_numerics": false,
              "stem_english_possessive": true
            }
          }
        }
      }
    }

### "word_delimiter_graph"和"word_delimiter"之间的区别

当以下任何参数为"true"时，"word_delimiter_graph"和"word_delimiter"过滤器都会生成跨越多个位置的令牌：

* "catenate_all" * "catenate_numbers" * "catenate_words" * "preserve_original"

但是，只有"word_delimiter_graph"过滤器会分配多位置令牌的"位置长度"属性，该属性指示令牌跨越的位置数。这可确保"word_delimiter_graph"过滤器始终生成有效令牌图。

"word_delimiter"过滤器不会为多位置令牌分配"位置长度"属性。这意味着它会为流(包括这些令牌)生成无效的图形。

虽然索引不支持包含多位置令牌的令牌图，但查询(如"match_phrase"查询)可以使用这些图从单个查询字符串生成多个子查询。

要查看"word_delimiter"和"word_delimiter_graph"筛选器生成的令牌图有何不同，请查看以下示例。

**Example**

**基本令牌图**

当以下参数为"false"时，"word_delimiter"和"word_delimiter_graph"都会为"PowerShot2000"生成以下标记图：

* "catenate_all" * "catenate_numbers" * "catenate_words" * "preserve_original"

此图不包含多位置令牌。所有代币仅跨越一个头寸。

！令牌图基本

**带有多位置令牌的"word_delimiter_graph"图形**

当"catenate_words"为"true"时，"word_delimiter_graph"筛选器会为"PowerShot2000"生成以下令牌图。

此图正确指示串联的"PowerShot"令牌跨越两个位置。

！令牌图形 WDG

**带有多位置令牌的"word_delimiter"图形**

当"catenate_words"为"true"时，"word_delimiter"筛选器会为"PowerShot2000"生成以下令牌图。

请注意，串联的"PowerShot"令牌应跨越两个位置，但在令牌图中仅跨越一个位置，使其无效。

！令牌图形 WD

[« Word delimiter token filter](analysis-word-delimiter-tokenfilter.md)
[Character filters reference »](analysis-charfilters.md)
