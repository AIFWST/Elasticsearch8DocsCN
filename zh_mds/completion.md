

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Boolean field type](boolean.md) [Date field type »](date.md)

## 完成字段类型

要使用"完成"建议器，请将要从中生成建议的字段映射为类型"完成"。这将为字段值编制索引，以便快速完成。

    
    
    response = client.indices.create(
      index: 'music',
      body: {
        mappings: {
          properties: {
            suggest: {
              type: 'completion'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT music
    {
      "mappings": {
        "properties": {
          "suggest": {
            "type": "completion"
          }
        }
      }
    }

### "完成"字段的参数

"完成"字段接受以下参数：

"分析器"

|

要使用的索引分析器默认为"简单"。   ---|--- "search_analyzer"

|

要使用的搜索分析器默认为"分析器"值。   "preserve_separators"

|

保留分隔符，默认为"true"。如果禁用，您可以找到以"Foo Fighters"开头的领域，如果您建议使用"foof"。   "preserve_position_increments"

|

启用位置增量，默认为"true"。如果禁用并使用停用词分析器，您可以获得一个以"披头士"开头的字段，如果您建议使用"b"。**注意**：您也可以通过索引两个输入"披头士"和"披头士"来实现这一点，如果您能够丰富您的数据，则无需更改简单的分析器。   "max_input_length"

|

限制单个输入的长度，默认为"50"UTF-16 码位。此限制仅在索引时使用，以减少每个输入字符串的字符总数，以防止大量输入使底层数据结构膨胀。大多数用例不会受到默认值的影响，因为前缀补全很少超过前缀长度超过少数字符。   « 布尔字段类型 日期字段类型 »