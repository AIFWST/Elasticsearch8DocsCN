

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md)

[« Pattern replace character filter](analysis-pattern-replace-charfilter.md)
[Index templates »](index-templates.md)

##Normalizers

规范化程序类似于分析器，只是它们只能发出单个令牌。因此，它们没有分词器，只接受可用字符筛选器和标记筛选器的子集。仅允许基于每个字符工作的筛选器。例如，允许使用小写过滤器，但不允许使用词干过滤器，后者需要从整体上查看关键字。当前可用于规范化程序的筛选器列表如下："arabic_normalization"、"腹水折叠"、"bengali_normalization"、"cjk_width"、"decimal_digit"、"省略"、"german_normalization"、"hindi_normalization"、"indic_normalization"、"小写"、"pattern_replace"、"persian_normalization"、"scandinavian_folding"、"serbian_normalization"、"sorani_normalization"、"修剪"、"大写"。

Elasticsearch附带了一个"小写"内置规范化器。对于其他形式的规范化，需要自定义配置。

### 自定义规范化程序

自定义规范化程序采用字符筛选器列表和标记筛选器列表。

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        settings: {
          analysis: {
            char_filter: {
              quote: {
                type: 'mapping',
                mappings: [
                  '« => "',
                  '» => "'
                ]
              }
            },
            normalizer: {
              my_normalizer: {
                type: 'custom',
                char_filter: [
                  'quote'
                ],
                filter: [
                  'lowercase',
                  'asciifolding'
                ]
              }
            }
          }
        },
        mappings: {
          properties: {
            foo: {
              type: 'keyword',
              normalizer: 'my_normalizer'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT index
    {
      "settings": {
        "analysis": {
          "char_filter": {
            "quote": {
              "type": "mapping",
              "mappings": [
                "« => \"",
                "» => \""
              ]
            }
          },
          "normalizer": {
            "my_normalizer": {
              "type": "custom",
              "char_filter": ["quote"],
              "filter": ["lowercase", "asciifolding"]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "foo": {
            "type": "keyword",
            "normalizer": "my_normalizer"
          }
        }
      }
    }

[« Pattern replace character filter](analysis-pattern-replace-charfilter.md)
[Index templates »](index-templates.md)
