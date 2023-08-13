

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `coerce`](coerce.md) [`doc_values` »](doc-values.md)

##'copy_to'

"copy_to"参数允许您将多个字段的值复制到组字段中，然后可以将其作为单个字段进行查询。

如果您经常搜索多个字段，则可以通过使用"copy_to"搜索较少的字段来提高搜索速度。请参阅搜索尽可能少的字段。

例如，可以将"first_name"和"last_name"字段复制到"full_name"字段，如下所示：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            first_name: {
              type: 'text',
              copy_to: 'full_name'
            },
            last_name: {
              type: 'text',
              copy_to: 'full_name'
            },
            full_name: {
              type: 'text'
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
        first_name: 'John',
        last_name: 'Smith'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            full_name: {
              query: 'John Smith',
              operator: 'and'
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
          "first_name": {
            "type": "text",
            "copy_to": "full_name" __},
          "last_name": {
            "type": "text",
            "copy_to": "full_name" __},
          "full_name": {
            "type": "text"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "first_name": "John",
      "last_name": "Smith"
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "full_name": { __"query": "John Smith",
            "operator": "and"
          }
        }
      }
    }

__

|

"first_name"和"last_name"字段的值将复制到"full_name"字段。   ---|---    __

|

"first_name"和"last_name"字段仍可分别查询名字和姓氏，但"full_name"字段可以同时查询名字和姓氏。   一些要点：

* 复制的是字段 _value_，而不是项(分析过程的结果)。  * 原始的"_source"字段不会被修改以显示复制的值。  * 相同的值可以复制到多个字段，其中 '"copy_to"： "field_1"、"field_2" ]' * 您不能通过中间字段递归复制，例如"field_1"上的"copy_to"到"field_2"和"field_2"到"field_3"上的"copy_to"，期望索引到"field_1"将以"field_3"结束，而是直接使用copy_to到原始字段中的多个字段。  * 如果索引映射中不存在目标字段，则通常的 [动态映射行为适用。默认情况下，将"dynamic"设置为"true"时，不存在的目标字段将动态添加到索引映射中。如果"dynamic"设置为"false"，则不会将目标字段添加到索引映射中，并且不会复制该值。如果"动态"设置为"严格"，则复制到不存在的字段将导致错误。

"copy_to"对于值采用对象形式的字段类型(例如"date_range")不受支持

[« `coerce`](coerce.md) [`doc_values` »](doc-values.md)
