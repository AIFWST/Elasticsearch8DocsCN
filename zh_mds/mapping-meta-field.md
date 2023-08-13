

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Metadata fields](mapping-fields.md)

[« `_index` field](mapping-index-field.md) [`_routing` field »](mapping-
routing-field.md)

## '_meta'字段

映射类型可以具有与之关联的自定义元数据。Elasticsearch 根本不使用它们，但可用于存储特定于应用程序的元数据，例如文档所属的类：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          _meta: {
            class: 'MyApp::User',
            version: {
              min: '1.0',
              max: '1.3'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "_meta": { __"class": "MyApp::User",
          "version": {
            "min": "1.0",
            "max": "1.3"
          }
        }
      }
    }

__

|

可以使用GET映射API检索此"_meta"信息。   ---|--- 可以使用 updatemapping API 在现有类型上更新"_meta"字段：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        _meta: {
          class: 'MyApp2::User3',
          version: {
            min: '1.3',
            max: '1.5'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_mapping
    {
      "_meta": {
        "class": "MyApp2::User3",
        "version": {
          "min": "1.3",
          "max": "1.5"
        }
      }
    }

[« `_index` field](mapping-index-field.md) [`_routing` field »](mapping-
routing-field.md)
