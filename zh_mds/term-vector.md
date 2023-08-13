

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `subobjects`](subobjects.md) [Mapping limit settings »](mapping-settings-
limit.md)

##'term_vector'

项向量包含有关分析过程生成的项的信息，包括：

* 术语列表。  * 每个术语的位置(或顺序)。  * 开始和结束字符偏移量将术语映射到原始字符串中的原点。  * 有效负载(如果可用) — 与每个术语位置关联的用户定义的二进制数据。

可以存储这些术语向量，以便可以为特定文档检索它们。

"term_vector"设置接受：

`no`

|

不存储任何术语向量。(默认值)---|---"是"

|

仅存储字段中的术语。   "with_positions"

|

存储术语和位置。   "with_offsets"

|

存储术语和字符偏移量。   "with_positions_offsets"

|

存储术语、位置和字符偏移量。   "with_positions_payloads"

|

存储术语、位置和有效负载。   "with_positions_offsets_payloads"

|

存储项、位置、偏移和有效负载。   快速矢量荧光笔需要"with_positions_offsets"。术语向量 API 可以检索存储的任何内容。

设置"with_positions_offsets"将使字段索引的大小加倍。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            text: {
              type: 'text',
              term_vector: 'with_positions_offsets'
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
        text: 'Quick brown fox'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            text: 'brown fox'
          }
        },
        highlight: {
          fields: {
            text: {}
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "text": {
            "type":        "text",
            "term_vector": "with_positions_offsets"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "text": "Quick brown fox"
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "text": "brown fox"
        }
      },
      "highlight": {
        "fields": {
          "text": {} __}
      }
    }

__

|

默认情况下，快速矢量荧光笔将用于"文本"字段，因为启用了术语矢量。   ---|--- « '子对象' 映射限制设置 »