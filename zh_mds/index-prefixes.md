

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `index_phrases`](index-phrases.md) [`meta` »](mapping-field-meta.md)

##'index_prefixes'

"index_prefixes"参数支持对术语前缀编制索引，以加快前缀搜索速度。它接受以下可选设置：

`min_chars`

|

要编制索引的最小前缀长度。必须大于 0，默认为 2。该值包含。   ---|--- "max_chars"

|

要编制索引的最大前缀长度。必须小于 20，默认为 5。该值包含。   此示例使用默认前缀长度设置创建一个文本字段：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            body_text: {
              type: 'text',
              index_prefixes: {}
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "body_text": {
            "type": "text",
            "index_prefixes": { }    __}
        }
      }
    }

__

|

空设置对象将使用默认的"min_chars"和"max_chars"设置 ---|--- 此示例使用自定义前缀长度设置：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            full_name: {
              type: 'text',
              index_prefixes: {
                min_chars: 1,
                max_chars: 10
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
        "properties": {
          "full_name": {
            "type": "text",
            "index_prefixes": {
              "min_chars" : 1,
              "max_chars" : 10
            }
          }
        }
      }
    }

[« `index_phrases`](index-phrases.md) [`meta` »](mapping-field-meta.md)
