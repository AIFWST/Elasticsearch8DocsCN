

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Numeric field types](number.md) [Percolator field type
»](percolator.md)

## 对象字段类型

JSON 文档本质上是分层的：文档可能包含内部对象，而内部对象又可能包含内部对象本身：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        region: 'US',
        manager: {
          age: 30,
          name: {
            first: 'John',
            last: 'Smith'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    { __"region": "US",
      "manager": { __"age":     30,
        "name": { __"first": "John",
          "last":  "Smith"
        }
      }
    }

__

|

外部文档也是一个 JSON 对象。   ---|---    __

|

它包含一个名为"管理器"的内部对象。   __

|

它又包含一个名为"name"的内部对象。   在内部，本文档被索引为键值对的简单平面列表，如下所示：

    
    
    {
      "region":             "US",
      "manager.age":        30,
      "manager.name.first": "John",
      "manager.name.last":  "Smith"
    }

上述文档的显式映射可能如下所示：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            region: {
              type: 'keyword'
            },
            manager: {
              properties: {
                age: {
                  type: 'integer'
                },
                name: {
                  properties: {
                    first: {
                      type: 'text'
                    },
                    last: {
                      type: 'text'
                    }
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": { __"region": {
            "type": "keyword"
          },
          "manager": { __"properties": {
              "age":  { "type": "integer" },
              "name": { __"properties": {
                  "first": { "type": "text" },
                  "last":  { "type": "text" }
                }
              }
            }
          }
        }
      }
    }

__

|

顶级映射定义中的属性。   ---|---    __

|

"经理"字段是内部的"对象"字段。   __

|

"manager.name"字段是"经理"字段中的内部"对象"字段。   您不需要将字段"type"显式设置为"对象"，因为这是默认值。

### "对象"字段的参数

"对象"字段接受以下参数：

"动态"

|

是否应将新的"属性"动态添加到现有对象中。接受"真"(默认值)、"运行时"、"假"和"严格"。   ---|---"已启用"

|

是为对象字段提供的 JSON 值是应该解析和索引("true"，默认值)还是完全忽略("false")。   "子对象"

|

对象是否可以保存子对象("true"，默认值)或不能保存子对象("false")。如果不是，名称中带有点的子字段将被视为叶子，否则它们的字段名称将扩展到其相应的对象结构。   "属性"

|

对象中的字段，可以是任何数据类型，包括"对象"。可以将新属性添加到现有对象。   如果需要索引对象数组而不是单个对象，请先读取嵌套。

[« Numeric field types](number.md) [Percolator field type
»](percolator.md)
