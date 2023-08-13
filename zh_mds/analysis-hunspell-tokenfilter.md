

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Flatten graph token filter](analysis-flatten-graph-tokenfilter.md)
[Hyphenation decompounder token filter »](analysis-hyp-decomp-
tokenfilter.md)

## Hunspell tokenfilter

提供基于提供的 Hunspelldictionary 的字典词干分析。"hunspell"过滤器需要配置一个或多个特定于语言的 Hunspell 词典。

此过滤器使用 Lucene 的 HunspellStemFilter。

如果可用，我们建议在使用"hunspell"令牌过滤器之前尝试使用适用于您的语言的算法词干分析器。在实践中，算法词干分析器通常优于字典词干分析器。请参阅词干词干。

### 配置拼写词典

Hunspell词典存储在文件系统上的专用"hunspell"目录中并检测："<$ES_PATH_CONF>/hunspell"。每个词典都应该有自己的目录，以其关联的语言和区域设置命名(例如，"pt_BR"、"en_GB")。此字典目录应包含单个".aff"和一个或多个".dic"文件，所有这些文件都将自动拾取。例如，以下目录布局将定义"en_US"字典：

    
    
    - config
        |-- hunspell
        |    |-- en_US
        |    |    |-- en_US.dic
        |    |    |-- en_US.aff

每个字典都可以配置一个设置：

`ignore_case`

    

(静态，布尔值)如果为 true，则字典匹配将不区分大小写。默认为"假"。

可以使用"indices.analysis.hunspell.dictionary.ignore_case"在"elasticsearch.yml"中全局配置此设置。

要为特定区域设置配置设置，请使用"index.analysis.hunspell.dictionary"。<locale>.ignore_case"设置(例如，对于"en_US"(美式英语)区域设置，设置为"indices.analysis.hunspell.dictionary.en_US.ignore_case")。

您还可以在包含这些设置的字典目录下添加一个"settings.yml"文件。这将覆盖"elasticsearch.yml"中定义的任何其他"ignore_case"设置。

###Example

以下分析 API 请求使用"hunspell"过滤器将"狐狸快速跳跃"阻止为"狐狸快速跳跃"。

该请求指定了"en_US"区域设置，这意味着"<$ES_PATH_CONF>/hunspell/en_US"目录中的".aff"和".dic"文件用于Hunspell字典。

    
    
    GET /_analyze
    {
      "tokenizer": "standard",
      "filter": [
        {
          "type": "hunspell",
          "locale": "en_US"
        }
      ],
      "text": "the foxes jumping quickly"
    }

筛选器生成以下标记：

    
    
    [ the, fox, jump, quick ]

### 可配置参数

`dictionary`

    

(可选，字符串或字符串数组)一个或多个用于Hunspell词典的".dic"文件(例如，"en_US.dic，my_custom.dic")。

默认情况下，"hunspell"过滤器使用<locale>使用"lang"，"language"或"locale"参数指定的"<$ES_PATH_CONF>/hunspell/"目录中的所有".dic"文件。

`dedup`

     (Optional, Boolean) If `true`, duplicate tokens are removed from the filter's output. Defaults to `true`. 
`lang`

    

(必填*，字符串)"区域设置"参数的别名。

如果未指定此参数，则需要"语言"或"区域设置"参数。

`language`

    

(必填*，字符串)"区域设置"参数的别名。

如果未指定此参数，则需要"lang"或"区域设置"参数。

`locale`

    

(必填*，字符串)用于指定 Hunspell 词典的".aff"和".dic"文件的区域设置目录。请参阅配置拼写词典。

如果未指定此参数，则需要"lang"或"language"参数。

`longest_only`

     (Optional, Boolean) If `true`, only the longest stemmed version of each token is included in the output. If `false`, all stemmed versions of the token are included. Defaults to `false`. 

### 自定义并添加到分析器

要自定义"hunspell"过滤器，请复制它以创建新的自定义令牌过滤器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用自定义"hunspell"筛选器"my_en_US_dict_stemmer"来配置新的自定义分析器。

"my_en_US_dict_stemmer"过滤器使用"en_US"的"区域设置"，这意味着使用"<$ES_PATH_CONF>/hunspell/en_US"目录中的".aff"和".dic"文件。过滤器还包括一个"假"的"dedup"参数，这意味着从字典中添加的重复标记不会从过滤器的输出中删除。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              en: {
                tokenizer: 'standard',
                filter: [
                  'my_en_US_dict_stemmer'
                ]
              }
            },
            filter: {
              "my_en_US_dict_stemmer": {
                type: 'hunspell',
                locale: 'en_US',
                dedup: false
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
              "filter": [ "my_en_US_dict_stemmer" ]
            }
          },
          "filter": {
            "my_en_US_dict_stemmer": {
              "type": "hunspell",
              "locale": "en_US",
              "dedup": false
            }
          }
        }
      }
    }

###Settings

除了"ignore_case"设置之外，您还可以使用"elasticsearch.yml"为"hunspell"过滤器配置以下全局设置：

`indices.analysis.hunspell.dictionary.lazy`

     (Static, Boolean) If `true`, the loading of Hunspell dictionaries is deferred until a dictionary is used. If `false`, the dictionary directory is checked for dictionaries when the node starts, and any dictionaries are automatically loaded. Defaults to `false`. 

[« Flatten graph token filter](analysis-flatten-graph-tokenfilter.md)
[Hyphenation decompounder token filter »](analysis-hyp-decomp-
tokenfilter.md)
