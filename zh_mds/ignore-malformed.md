

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `ignore_above`](ignore-above.md) [`index` »](mapping-index.md)

##'ignore_malformed'

有时，您无法控制收到的数据。一个用户可以发送一个"登录"字段，即"日期"，另一个用户发送一个作为电子邮件地址的"登录"字段。

默认情况下，尝试将错误的数据类型索引到字段中会引发异常，并拒绝整个文档。"ignore_malformed"参数(如果设置为"true")允许忽略异常。格式错误的字段未编制索引，但文档中的其他字段将正常处理。

例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            number_one: {
              type: 'integer',
              ignore_malformed: true
            },
            number_two: {
              type: 'integer'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        text: 'Some text value',
        number_one: 'foo'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        text: 'Some text value',
        number_two: 'foo'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "number_one": {
            "type": "integer",
            "ignore_malformed": true
          },
          "number_two": {
            "type": "integer"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "text":       "Some text value",
      "number_one": "foo" __}
    
    PUT my-index-000001/_doc/2
    {
      "text":       "Some text value",
      "number_two": "foo" __}

__

|

本文档将为"文本"字段编制索引，但不为"number_one"字段编制索引。   ---|---    __

|

此文档将被拒绝，因为"number_two"不允许格式错误的值。   以下映射类型目前支持"ignore_malformed"设置：

数值的

     `long`, `integer`, `short`, `byte`, `double`, `float`, `half_float`, `scaled_float`
[Boolean](boolean.html "Boolean field type")

     `boolean`
[Date](date.html "Date field type")

     `date`
[Date nanoseconds](date_nanos.html "Date nanoseconds field type")

     `date_nanos`
[Geopoint](geo-point.html "Geopoint field type")

     `geo_point` for lat/lon points 
[Geoshape](geo-shape.html "Geoshape field type")

     `geo_shape` for complex shapes like polygons 
[IP](ip.html "IP field type")

     `ip` for IPv4 and IPv6 addresses 

可以使用更新映射 API 在现有字段上更新"ignore_malformed"设置值。

### 索引级默认值

可以在索引级别设置"index.mapping.ignore_malformed"设置，以在所有允许的映射类型中全局忽略格式错误的内容。如果在索引级别设置，则不支持该设置的映射类型将忽略它。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          "index.mapping.ignore_malformed": true
        },
        mappings: {
          properties: {
            number_one: {
              type: 'byte'
            },
            number_two: {
              type: 'integer',
              ignore_malformed: false
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "index.mapping.ignore_malformed": true __},
      "mappings": {
        "properties": {
          "number_one": { __"type": "byte"
          },
          "number_two": {
            "type": "integer",
            "ignore_malformed": false __}
        }
      }
    }

__

|

"number_one"字段继承索引级设置。   ---|---    __

|

"number_two"字段会覆盖索引级别设置以关闭"ignore_malformed"。   ### 处理格式错误的字段编辑

当"ignore_malformed"打开索引时，格式错误的字段将被静默忽略。建议尽可能保留包含格式错误的字段的文档数，否则对此字段的查询将变得毫无意义。Elasticsearch 通过在特殊的"_ignored"字段上使用"存在"、"术语"或"术语"查询，可以轻松检查有多少文档具有格式错误的字段。

### JSONObjects 的限制

不能将"ignore_malformed"与以下数据类型一起使用：

* 嵌套数据类型 * 对象数据类型 * 范围数据类型

您也不能使用"ignore_malformed"来忽略提交到错误数据类型字段的 JSON 对象。JSON 对象是用大括号"{}"括起来的任何数据，包括映射到嵌套、对象和范围数据类型的数据。

如果您将 JSON 对象提交到不受支持的字段，Elasticsearch 将返回错误并拒绝整个文档，而不管"ignore_malformed"设置如何。

[« `ignore_above`](ignore-above.md) [`index` »](mapping-index.md)
