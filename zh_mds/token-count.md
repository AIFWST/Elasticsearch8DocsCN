

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Text type family](text.md) [Unsigned long field type »](unsigned-
long.md)

## 令牌计数字段类型

类型为"token_count"的字段实际上是一个"整数"字段，它接受字符串值，分析它们，然后索引字符串中的标记数。

例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            name: {
              type: 'text',
              fields: {
                length: {
                  type: 'token_count',
                  analyzer: 'standard'
                }
              }
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
        name: 'John Smith'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        name: 'Rachel Alice Williams'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          term: {
            "name.length": 3
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "name": { __"type": "text",
            "fields": {
              "length": { __"type":     "token_count",
                "analyzer": "standard"
              }
            }
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    { "name": "John Smith" }
    
    PUT my-index-000001/_doc/2
    { "name": "Rachel Alice Williams" }
    
    GET my-index-000001/_search
    {
      "query": {
        "term": {
          "name.length": 3 __}
      }
    }

__

|

"名称"字段是使用默认"标准"分析器的"文本"字段。   ---|---    __

|

"name.length"字段是一个"token_count"多字段，它将索引"name"字段中的令牌数量。   __

|

此查询仅匹配包含"Rachel Alice Williams"的文档，因为它包含三个令牌。   ### "token_count"字段的参数编辑

"token_count"字段接受以下参数：

"分析器"

|

应该用于分析字符串值的分析器。必填。为获得最佳性能，请使用不带令牌筛选器的分析器。   ---|--- "enable_position_increments"

|

指示是否应计算位置增量。如果不想计算分析器筛选器删除的令牌(如"停止")，请设置为"false"。默认为"true"。   "doc_values"

|

字段是否应以列步幅方式存储在磁盘上，以便以后可用于排序、聚合或脚本编写？接受"真"(默认值)或"假"。   "索引"

|

该字段是否应可搜索？接受"真"(默认值)和"假"。   "null_value"

|

接受与字段相同"类型"的数值，该数值将替换为任何显式的"null"值。默认为"null"，表示该字段被视为缺失。   "商店"

|

字段值是否应与"_source"字段分开存储和检索。接受"真"或"假"(默认值)。   « 文本类型系列无符号长字段类型 »