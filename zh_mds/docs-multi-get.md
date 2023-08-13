

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Update By Query API](docs-update-by-query.md) [Bulk API »](docs-
bulk.md)

## Multi get (mget)API

按 ID 检索多个 JSON 文档。

    
    
    response = client.mget(
      body: {
        docs: [
          {
            _index: 'my-index-000001',
            _id: '1'
          },
          {
            _index: 'my-index-000001',
            _id: '2'
          }
        ]
      }
    )
    puts response
    
    
    GET /_mget
    {
      "docs": [
        {
          "_index": "my-index-000001",
          "_id": "1"
        },
        {
          "_index": "my-index-000001",
          "_id": "2"
        }
      ]
    }

###Request

"获取/_mget"

"获取/<index>/_mget"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对目标索引或索引别名具有"读取"索引权限。

###Description

您可以使用"mget"从一个或多个索引中检索多个文档。如果在请求 URI 中指定索引，则只需在请求正文中指定文档 ID。

####Security

请参阅基于 URL 的访问控制。

#### 部分响应

为了确保快速响应，如果一个或多个分片失败，多获取 API 会响应并提供部分结果。有关更多信息，请参阅分片失败。

### 路径参数

`<index>`

     (Optional, string) Name of the index to retrieve documents from when `ids` are specified, or when a document in the `docs` array does not specify an index. 

### 查询参数

`preference`

     (Optional, string) Specifies the node or shard the operation should be performed on. Random by default. 
`realtime`

     (Optional, Boolean) If `true`, the request is real-time as opposed to near-real-time. Defaults to `true`. See [Realtime](docs-get.html#realtime "Realtime"). 
`refresh`

     (Optional, Boolean) If `true`, the request refreshes relevant shards before retrieving documents. Defaults to `false`. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`stored_fields`

     (Optional, Boolean) If `true`, retrieves the document fields stored in the index rather than the document `_source`. Defaults to `false`. 
`_source`

     (Optional, string) True or false to return the `_source` field or not, or a list of fields to return. 
`_source_excludes`

    

(可选，字符串)要从响应中排除的源字段的逗号分隔列表。

您还可以使用此参数从"_source_includes"查询参数中指定的子集中排除字段。

如果"_source"参数为"false"，则忽略此参数。

`_source_includes`

    

(可选，字符串)要包含在响应中的源字段的逗号分隔列表。

如果指定此参数，则仅返回这些源字段。您可以使用"_source_excludes"查询参数从此子集中排除字段。

如果"_source"参数为"false"，则忽略此参数。

### 请求正文

`docs`

    

(可选，数组)要检索的文档。如果未在请求 URI 中指定索引，则为必需。您可以为每个文档指定以下属性：

`_id`

     (Required, string) The unique document ID. 
`_index`

     (Optional, string) The index that contains the document. Required if no index is specified in the request URI. 
`routing`

     (Optional, string) The key for the primary shard the document resides on. Required if routing is used during indexing. 
`_source`

    

(可选，布尔值)如果为"false"，则排除所有"_source"字段。默认为"true"。

`source_include`

     (Optional, array) The fields to extract and return from the `_source` field. 
`source_exclude`

     (Optional, array) The fields to exclude from the returned `_source` field. 

`_stored_fields`

     (Optional, array) The stored fields you want to retrieve. 

`ids`

     (Optional, array) The IDs of the documents you want to retrieve. Allowed when the index is specified in the request URI. 

### 响应正文

响应包括一个"docs"数组，该数组包含请求中指定的顺序的文档。返回文档的结构类似于获取 API 返回的结构。如果获取特定文档失败，则会包含错误来代替文档。

###Examples

#### 按 ID 获取文档

如果在请求 URI 中指定索引，则请求正文中只需要文档 ID：

    
    
    response = client.mget(
      index: 'my-index-000001',
      body: {
        docs: [
          {
            _id: '1'
          },
          {
            _id: '2'
          }
        ]
      }
    )
    puts response
    
    
    GET /my-index-000001/_mget
    {
      "docs": [
        {
          "_id": "1"
        },
        {
          "_id": "2"
        }
      ]
    }

您可以使用"ids"元素来简化请求：

    
    
    response = client.mget(
      index: 'my-index-000001',
      body: {
        ids: [
          '1',
          '2'
        ]
      }
    )
    puts response
    
    
    GET /my-index-000001/_mget
    {
      "ids" : ["1", "2"]
    }

#### 筛选源字段

默认情况下，为每个文档(如果存储)返回"_source"字段。使用"_source"和"_source_include"或"source_exclude"属性来过滤为特定文档返回的字段。您可以在请求 URI 中包含"_source"、"_source_includes"和"_source_excludes"查询参数，以指定在没有每个文档指令时使用的默认值。

例如，以下请求将文档 1 的"_source"设置为 false 以完全排除源，从文档 2 中检索"field3"和"field4"，并从文档 3 中检索"user"字段，但过滤掉"user.location"字段。

    
    
    response = client.mget(
      body: {
        docs: [
          {
            _index: 'test',
            _id: '1',
            _source: false
          },
          {
            _index: 'test',
            _id: '2',
            _source: [
              'field3',
              'field4'
            ]
          },
          {
            _index: 'test',
            _id: '3',
            _source: {
              include: [
                'user'
              ],
              exclude: [
                'user.location'
              ]
            }
          }
        ]
      }
    )
    puts response
    
    
    GET /_mget
    {
      "docs": [
        {
          "_index": "test",
          "_id": "1",
          "_source": false
        },
        {
          "_index": "test",
          "_id": "2",
          "_source": [ "field3", "field4" ]
        },
        {
          "_index": "test",
          "_id": "3",
          "_source": {
            "include": [ "user" ],
            "exclude": [ "user.location" ]
          }
        }
      ]
    }

#### 获取存储字段

使用"stored_fields"属性指定要检索的存储字段集。任何未存储的请求字段都将被忽略。您可以在请求 URI 中包含"stored_fields"查询参数，以指定在没有每个文档指令时使用的默认值。

例如，以下请求从文档 1 中检索"field1"和"field2"，从文档 2 中检索"field3"和"field4"：

    
    
    response = client.mget(
      body: {
        docs: [
          {
            _index: 'test',
            _id: '1',
            stored_fields: [
              'field1',
              'field2'
            ]
          },
          {
            _index: 'test',
            _id: '2',
            stored_fields: [
              'field3',
              'field4'
            ]
          }
        ]
      }
    )
    puts response
    
    
    GET /_mget
    {
      "docs": [
        {
          "_index": "test",
          "_id": "1",
          "stored_fields": [ "field1", "field2" ]
        },
        {
          "_index": "test",
          "_id": "2",
          "stored_fields": [ "field3", "field4" ]
        }
      ]
    }

默认情况下，以下请求从所有文档中检索"field1"和"field2"。为文档 1 返回这些默认字段，但覆盖以返回文档 2 的"field3"和"field4"。

    
    
    response = client.mget(
      index: 'test',
      stored_fields: 'field1,field2',
      body: {
        docs: [
          {
            _id: '1'
          },
          {
            _id: '2',
            stored_fields: [
              'field3',
              'field4'
            ]
          }
        ]
      }
    )
    puts response
    
    
    GET /test/_mget?stored_fields=field1,field2
    {
      "docs": [
        {
          "_id": "1"
        },
        {
          "_id": "2",
          "stored_fields": [ "field3", "field4" ]
        }
      ]
    }

#### 指定文档传送

如果在编制索引期间使用传送，则需要指定传送值以检索文档。例如，以下请求从与路由密钥"key1"对应的分片中获取"test/_doc/2"，并从与路由密钥"key2"对应的分片中获取"test/_doc/1"。

    
    
    response = client.mget(
      routing: 'key1',
      body: {
        docs: [
          {
            _index: 'test',
            _id: '1',
            routing: 'key2'
          },
          {
            _index: 'test',
            _id: '2'
          }
        ]
      }
    )
    puts response
    
    
    GET /_mget?routing=key1
    {
      "docs": [
        {
          "_index": "test",
          "_id": "1",
          "routing": "key2"
        },
        {
          "_index": "test",
          "_id": "2"
        }
      ]
    }

[« Update By Query API](docs-update-by-query.md) [Bulk API »](docs-
bulk.md)
