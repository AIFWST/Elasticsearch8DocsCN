

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Stemmer override token filter](analysis-stemmer-override-tokenfilter.md)
[Synonym token filter »](analysis-synonym-tokenfilter.md)

## 停止令牌筛选器

从标记流中删除停用词。

如果未自定义，筛选器将默认删除以下英语停用词：

"a"、"an"、"and"、"are"、"as"、"at"、"be"、"but"、"by"、"for"、"if"、"in"、"is"、"it"、"no"、"not"、"of"、"on"、"or"、"such"、"that"、"the"、"then"、"there"、"this"、"they"、"this"、"they"、"this"、"to"、"was"、"will"、"with"

除英语外，"停止"过滤器还支持多种语言的预定义停用词列表。您还可以将自己的停用词指定为数组或文件。

"stop"过滤器使用Lucene的StopFilter。

###Example

以下分析 API 请求使用"停止"过滤器从"一只快速的狐狸跳过懒狗"中删除停用词"a"和"the"：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'stop'
        ],
        text: 'a quick fox jumps over the lazy dog'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "standard",
      "filter": [ "stop" ],
      "text": "a quick fox jumps over the lazy dog"
    }

筛选器生成以下标记：

    
    
    [ quick, fox, jumps, over, lazy, dog ]

### 添加到分析器

以下创建索引 APIrequest 使用"停止"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'whitespace',
                filter: [
                  'stop'
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
              "tokenizer": "whitespace",
              "filter": [ "stop" ]
            }
          }
        }
      }
    }

### 可配置参数

`stopwords`

    

(可选，字符串或字符串数组)语言值，例如"_阿拉伯语_"或"_泰语_"。默认为"_英语_"。

每个语言值对应于 Lucene 中预定义的非索引字列表。有关支持的语言值及其停用词，请参阅按语言列出的停用词。

也接受一系列停用词。

对于停用词的空列表，请使用"_none_"。

`stopwords_path`

    

(可选，字符串)包含要删除的非索引字列表的文件的路径。

此路径必须是绝对路径或相对于"配置"位置的路径，并且文件必须采用 UTF-8 编码。文件中的每个停用词必须用换行符分隔。

`ignore_case`

     (Optional, Boolean) If `true`, stop word matching is case insensitive. For example, if `true`, a stop word of `the` matches and removes `The`, `THE`, or `the`. Defaults to `false`. 
`remove_trailing`

    

(可选，布尔值)如果为"true"，则删除流的最后一个标记(如果它是停止词)。默认为"真"。

将筛选器与完成建议器一起使用时，此参数应为"false"。这将确保像"绿色a"这样的查询匹配并建议"青苹果"，同时仍然删除其他停用词。

###Customize

要自定义"停止"过滤器，请复制它以创建新的自定义令牌过滤器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个不区分大小写的自定义"stop"筛选器，该筛选器从"_English_"停用词列表中删除停用词：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              default: {
                tokenizer: 'whitespace',
                filter: [
                  'my_custom_stop_words_filter'
                ]
              }
            },
            filter: {
              my_custom_stop_words_filter: {
                type: 'stop',
                ignore_case: true
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
            "default": {
              "tokenizer": "whitespace",
              "filter": [ "my_custom_stop_words_filter" ]
            }
          },
          "filter": {
            "my_custom_stop_words_filter": {
              "type": "stop",
              "ignore_case": true
            }
          }
        }
      }
    }

您还可以指定自己的停用词列表。例如，以下请求创建一个不区分大小写的自定义"stop"筛选器，该筛选器仅删除停止词"and"、"is"和"the"：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              default: {
                tokenizer: 'whitespace',
                filter: [
                  'my_custom_stop_words_filter'
                ]
              }
            },
            filter: {
              my_custom_stop_words_filter: {
                type: 'stop',
                ignore_case: true,
                stopwords: [
                  'and',
                  'is',
                  'the'
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
            "default": {
              "tokenizer": "whitespace",
              "filter": [ "my_custom_stop_words_filter" ]
            }
          },
          "filter": {
            "my_custom_stop_words_filter": {
              "type": "stop",
              "ignore_case": true,
              "stopwords": [ "and", "is", "the" ]
            }
          }
        }
      }
    }

### 按语言分类停用词

以下列表包含"非索引字"参数支持的语言值，以及指向 Lucene 中预定义停用词的链接。

`_arabic_`

     [Arabic stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/ar/stopwords.txt)

`_armenian_`

     [Armenian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/hy/stopwords.txt)

`_basque_`

     [Basque stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/eu/stopwords.txt)

`_bengali_`

     [Bengali stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/bn/stopwords.txt)

"_巴西语_"(巴西葡萄牙语)

     [Brazilian Portuguese stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/br/stopwords.txt)

`_bulgarian_`

     [Bulgarian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/bg/stopwords.txt)

`_catalan_`

     [Catalan stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/ca/stopwords.txt)

"_cjk_"(中文、日文和韩文)

     [CJK stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/cjk/stopwords.txt)

`_czech_`

     [Czech stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/cz/stopwords.txt)

`_danish_`

     [Danish stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/danish_stop.txt)

`_dutch_`

     [Dutch stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/dutch_stop.txt)

`_english_`

     [English stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/java/org/apache/lucene/analysis/en/EnglishAnalyzer.java#L48)

`_estonian_`

     [Estonian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/et/stopwords.txt)

`_finnish_`

     [Finnish stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/finnish_stop.txt)

`_french_`

     [French stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/french_stop.txt)

`_galician_`

     [Galician stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/gl/stopwords.txt)

`_german_`

     [German stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/german_stop.txt)

`_greek_`

     [Greek stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/el/stopwords.txt)

`_hindi_`

     [Hindi stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/hi/stopwords.txt)

`_hungarian_`

     [Hungarian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/hungarian_stop.txt)

`_indonesian_`

     [Indonesian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/id/stopwords.txt)

`_irish_`

     [Irish stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/ga/stopwords.txt)

`_italian_`

     [Italian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/italian_stop.txt)

`_latvian_`

     [Latvian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/lv/stopwords.txt)

`_lithuanian_`

     [Lithuanian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/lt/stopwords.txt)

`_norwegian_`

     [Norwegian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/norwegian_stop.txt)

`_persian_`

     [Persian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/fa/stopwords.txt)

`_portuguese_`

     [Portuguese stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/portuguese_stop.txt)

`_romanian_`

     [Romanian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/ro/stopwords.txt)

`_russian_`

     [Russian stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/russian_stop.txt)

`_sorani_`

     [Sorani stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/ckb/stopwords.txt)

`_spanish_`

     [Spanish stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/spanish_stop.txt)

`_swedish_`

     [Swedish stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/snowball/swedish_stop.txt)

`_thai_`

     [Thai stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/th/stopwords.txt)

`_turkish_`

     [Turkish stop words](https://github.com/apache/lucene/blob/main/lucene/analysis/common/src/resources/org/apache/lucene/analysis/tr/stopwords.txt)

[« Stemmer override token filter](analysis-stemmer-override-tokenfilter.md)
[Synonym token filter »](analysis-synonym-tokenfilter.md)
