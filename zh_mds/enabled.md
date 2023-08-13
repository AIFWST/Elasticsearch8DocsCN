

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `eager_global_ordinals`](eager-global-ordinals.md) [`format` »](mapping-
date-format.md)

##'已启用'

Elasticsearch 尝试索引您为其提供的所有字段，但有时您希望只存储字段而不对其进行索引。例如，假设您正在使用Elasticsearch作为Web会话存储。您可能希望为会话 ID 和上次更新时间编制索引，但不需要对会话数据本身进行查询或运行聚合。

"启用"设置只能应用于顶级映射定义和"对象"字段，导致 Elasticsearch 完全跳过字段内容的解析。JSON仍然可以从"_source"字段中检索，但不能以任何其他方式搜索或存储：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            user_id: {
              type: 'keyword'
            },
            last_updated: {
              type: 'date'
            },
            session_data: {
              type: 'object',
              enabled: false
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'session_1',
      body: {
        user_id: 'kimchy',
        session_data: {
          arbitrary_object: {
            some_array: [
              'foo',
              'bar',
              {
                baz: 2
              }
            ]
          }
        },
        last_updated: '2015-12-06T18:20:22'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'session_2',
      body: {
        user_id: 'jpountz',
        session_data: 'none',
        last_updated: '2015-12-06T18:22:13'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "user_id": {
            "type":  "keyword"
          },
          "last_updated": {
            "type": "date"
          },
          "session_data": { __"type": "object",
            "enabled": false
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/session_1
    {
      "user_id": "kimchy",
      "session_data": { __"arbitrary_object": {
          "some_array": [ "foo", "bar", { "baz": 2 } ]
        }
      },
      "last_updated": "2015-12-06T18:20:22"
    }
    
    PUT my-index-000001/_doc/session_2
    {
      "user_id": "jpountz",
      "session_data": "none", __"last_updated": "2015-12-06T18:22:13"
    }

__

|

"session_data"字段已禁用。   ---|---    __

|

任何任意数据都可以传递到"session_data"字段，因为它将被完全忽略。   __

|

"session_data"还将忽略不是 JSON 对象的值。   整个映射也可能被禁用，在这种情况下，文档存储在"_source"字段中，这意味着它可以被检索，但无论如何都不会索引其内容：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          enabled: false
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'session_1',
      body: {
        user_id: 'kimchy',
        session_data: {
          arbitrary_object: {
            some_array: [
              'foo',
              'bar',
              {
                baz: 2
              }
            ]
          }
        },
        last_updated: '2015-12-06T18:20:22'
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 'session_1'
    )
    puts response
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "enabled": false __}
    }
    
    PUT my-index-000001/_doc/session_1
    {
      "user_id": "kimchy",
      "session_data": {
        "arbitrary_object": {
          "some_array": [ "foo", "bar", { "baz": 2 } ]
        }
      },
      "last_updated": "2015-12-06T18:20:22"
    }
    
    GET my-index-000001/_doc/session_1 __GET my-index-000001/_mapping __

__

|

整个映射被禁用。   ---|---    __

|

可以检索文档。   __

|

检查映射显示未添加任何字段。   现有字段和顶级映射定义的"已启用"设置无法更新。

请注意，由于 Elasticsearch 完全跳过了字段内容的解析，因此可以将非对象数据添加到禁用的字段中：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            session_data: {
              type: 'object',
              enabled: false
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'session_1',
      body: {
        session_data: 'foo bar'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "session_data": {
            "type": "object",
            "enabled": false
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/session_1
    {
      "session_data": "foo bar" __}

__

|

即使"session_data"包含非对象数据，文档也会成功添加。   ---|--- « 'eager_global_ordinals' '格式' »