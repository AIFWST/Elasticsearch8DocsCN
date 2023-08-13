

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `analyzer`](analyzer.md) [`copy_to` »](copy-to.md)

##'胁迫'

数据并不总是干净的。根据其生成方式，数字可能会在 JSON 正文中呈现为真正的 JSON 数字，例如"5"，但它也可能呈现为字符串，例如"5""。或者，应该为整数的数字可以呈现为浮点数，例如"5.0"，甚至"5.0""。

强制尝试清理脏值以适合字段的数据类型。例如：

* 字符串将被强制为数字。  * 整数值的浮点将被截断。

例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            number_one: {
              type: 'integer'
            },
            number_two: {
              type: 'integer',
              coerce: false
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
        number_one: '10'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        number_two: '10'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "number_one": {
            "type": "integer"
          },
          "number_two": {
            "type": "integer",
            "coerce": false
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "number_one": "10" __}
    
    PUT my-index-000001/_doc/2
    {
      "number_two": "10" __}

__

|

"number_one"字段将包含整数"10"。   ---|---    __

|

此文档将被拒绝，因为强制已禁用。   可以使用更新映射 API 在现有字段上更新"强制"设置值。

### 索引级默认值

可以在索引级别设置"index.mapping.coerce"设置，以在所有映射类型中全局禁用强制：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          "index.mapping.coerce": false
        },
        mappings: {
          properties: {
            number_one: {
              type: 'integer',
              coerce: true
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
        number_one: '10'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        number_two: '10'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "index.mapping.coerce": false
      },
      "mappings": {
        "properties": {
          "number_one": {
            "type": "integer",
            "coerce": true
          },
          "number_two": {
            "type": "integer"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    { "number_one": "10" } __PUT my-index-000001/_doc/2
    { "number_two": "10" } __

__

|

"number_one"字段会覆盖索引级别设置以启用强制。   ---|---    __

|

此文档将被拒绝，因为"number_two"字段继承了索引级强制设置。   « "分析仪" "copy_to" »