

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Character filters reference](analysis-
charfilters.md)

[« HTML strip character filter](analysis-htmlstrip-charfilter.md) [Pattern
replace character filter »](analysis-pattern-replace-charfilter.md)

## 映射字符筛选器

"映射"字符筛选器接受键和值的映射。每当遇到与键相同的字符串时，它都会将它们替换为与该键关联的值。

匹配是贪婪的;给定点上最长的模式匹配获胜。允许替换为空字符串。

"映射"过滤器使用 Lucene 的 MappingCharFilter。

###Example

以下分析 API 请求使用"映射"筛选器将印度教-阿拉伯数字 (٠١٢٣٤٥٦٧٨٩) 转换为阿拉伯-拉丁等效数字 (0123456789)，将文本"我的车牌是 ٢٥٠١٥"更改为"我的车牌是 25015"。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        char_filter: [
          {
            type: 'mapping',
            mappings: [
              '٠ => 0',
              '١ => 1',
              '٢ => 2',
              '٣ => 3',
              '٤ => 4',
              '٥ => 5',
              '٦ => 6',
              '٧ => 7',
              '٨ => 8',
              '٩ => 9'
            ]
          }
        ],
        text: 'My license plate is ٢٥٠١٥'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "keyword",
      "char_filter": [
        {
          "type": "mapping",
          "mappings": [
            "٠ => 0",
            "١ => 1",
            "٢ => 2",
            "٣ => 3",
            "٤ => 4",
            "٥ => 5",
            "٦ => 6",
            "٧ => 7",
            "٨ => 8",
            "٩ => 9"
          ]
        }
      ],
      "text": "My license plate is ٢٥٠١٥"
    }

筛选器生成以下文本：

    
    
    [ My license plate is 25015 ]

### 可配置参数

`mappings`

    

(必需*，字符串数组)映射数组，每个元素的形式为"键=>值"。

必须指定此参数或"mappings_path"参数。

`mappings_path`

    

(必填*，字符串)包含"键 => 值"映射的文件的路径。

此路径必须是绝对路径或相对于"配置"位置的路径，并且文件必须采用 UTF-8 编码。文件中的每个映射必须用换行符分隔。

必须指定此参数或"映射"参数。

### 自定义并添加到分析器

要自定义"映射"过滤器，请复制它以创建新的自定义字符过滤器的基础。您可以使用过滤器的可配置参数修改过滤器。

以下创建索引 APIrequest 使用自定义"映射"筛选器"my_mappings_char_filter"配置新的自定义分析器。

"my_mappings_char_filter"过滤器将":)"和":("表情替换为等效文本。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                char_filter: [
                  'my_mappings_char_filter'
                ]
              }
            },
            char_filter: {
              my_mappings_char_filter: {
                type: 'mapping',
                mappings: [
                  ':) => _happy_',
                  ':( => _sad_'
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
              "tokenizer": "standard",
              "char_filter": [
                "my_mappings_char_filter"
              ]
            }
          },
          "char_filter": {
            "my_mappings_char_filter": {
              "type": "mapping",
              "mappings": [
                ":) => _happy_",
                ":( => _sad_"
              ]
            }
          }
        }
      }
    }

以下分析 API 请求使用自定义"my_mappings_char_filter"将文本"我很高兴:("中的":("替换为"_sad_"。

    
    
    GET /my-index-000001/_analyze
    {
      "tokenizer": "keyword",
      "char_filter": [ "my_mappings_char_filter" ],
      "text": "I'm delighted about it :("
    }

筛选器生成以下文本：

    
    
    [ I'm delighted about it _sad_ ]

[« HTML strip character filter](analysis-htmlstrip-charfilter.md) [Pattern
replace character filter »](analysis-pattern-replace-charfilter.md)
