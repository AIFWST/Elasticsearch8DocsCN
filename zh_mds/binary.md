

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Arrays](array.md) [Boolean field type »](boolean.md)

## 二进制字段类型

"二进制"类型接受二进制值作为 aBase64 编码字符串。默认情况下，该字段不存储，并且不可搜索：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            name: {
              type: 'text'
            },
            blob: {
              type: 'binary'
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
        name: 'Some binary blob',
        blob: 'U29tZSBiaW5hcnkgYmxvYg=='
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "name": {
            "type": "text"
          },
          "blob": {
            "type": "binary"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "name": "Some binary blob",
      "blob": "U29tZSBiaW5hcnkgYmxvYg==" __}

__

|

Base64 编码的二进制值不得嵌入换行符"\n"。   ---|--- ### "二进制"字段的参数编辑

"二进制"字段接受以下参数：

"doc_values"

|

字段是否应以列步幅方式存储在磁盘上，以便以后可用于排序、聚合或脚本编写？接受"真"或"假"(默认值)。   ---|---"商店"

|

字段值是否应与"_source"字段分开存储和检索。接受"真"或"假"(默认值)。   « 数组布尔字段类型 »