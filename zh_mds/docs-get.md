

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Index API](docs-index_.md) [Delete API »](docs-delete.md)

## 获取接口

从索引中检索指定的 JSON 文档。

    
    
    response = client.get(
      index: 'my-index-000001',
      id: 0
    )
    puts response
    
    
    GET my-index-000001/_doc/0

###Request

"获取<index>/_doc/<_id>"

"头<index>/_doc/<_id>"

"获取<index>/_source/<_id>"

"头<index>/_source/<_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对目标索引或索引别名具有"读取"索引权限。

###Description

使用 GET 从特定索引中检索文档及其源字段或存储字段。使用 HEAD 验证文档是否存在。可以使用"_source"资源仅检索文档源或验证其是否存在。

#####Realtime

默认情况下，get API 是实时的，不受索引刷新率的影响(当数据对搜索可见时)。如果请求存储字段(请参阅 'stored_fields' 参数)并且文档已更新但尚未刷新，get API 必须解析和分析源以提取存储的字段。为了禁用实时GET，可以将"实时"参数设置为"false"。

##### 源过滤

默认情况下，get 操作返回"_source"字段的内容，除非您使用了"stored_fields"参数或禁用了"_source"字段。您可以使用"_source"参数关闭"_source"检索：

    
    
    response = client.get(
      index: 'my-index-000001',
      id: 0,
      _source: false
    )
    puts response
    
    
    GET my-index-000001/_doc/0?_source=false

如果只需要"_source"中的一个或两个字段，请使用"_source_includes"或"_source_excludes"参数来包含或过滤掉的特定字段。这对于部分检索可以节省网络开销的大型文档特别有用。这两个参数都采用逗号分隔的字段列表或通配符表达式。例：

    
    
    response = client.get(
      index: 'my-index-000001',
      id: 0,
      _source_includes: '*.id',
      _source_excludes: 'entities'
    )
    puts response
    
    
    GET my-index-000001/_doc/0?_source_includes=*.id&_source_excludes=entities

如果只想指定包含，则可以使用较短的表示法：

    
    
    response = client.get(
      index: 'my-index-000001',
      id: 0,
      _source: '*.id'
    )
    puts response
    
    
    GET my-index-000001/_doc/0?_source=*.id

#####Routing

如果在编制索引期间使用传送，则还需要指定传送值以检索文档。例如：

    
    
    response = client.get(
      index: 'my-index-000001',
      id: 2,
      routing: 'user1'
    )
    puts response
    
    
    GET my-index-000001/_doc/2?routing=user1

此请求获取 ID 为"2"的文档，但它是根据用户路由的。如果未指定正确的工艺路线，则不会读取文档。

#####Preference

控制要在其上执行 get 请求的分片副本的"首选项"。默认情况下，操作在分片副本之间随机化。

"首选项"可以设置为：

`_local`

     The operation will prefer to be executed on a local allocated shard if possible. 
Custom (string) value

     A custom value will be used to guarantee that the same shards will be used for the same custom value. This can help with "jumping values" when hitting different shards in different refresh states. A sample value can be something like the web session id, or the user name. 

#####Refresh

可以将"refresh"参数设置为"true"，以便在获取操作之前刷新相关分片并使其可搜索。应将其设置为"true"，然后再仔细考虑并验证这不会对系统造成沉重的负载(并减慢索引速度)。

#####Distributed

get 操作被哈希到特定的分片 id 中。然后，它被重定向到该分片 id 中的一个副本并返回结果。副本是该分片身份组中的主分片及其副本。这意味着我们拥有的副本越多，GET扩展就越好。

##### 版本控制支持

仅当文档的当前版本等于指定的版本时，才能使用"version"参数检索文档。

在内部，Elasticsearch 已将旧文档标记为已删除，并添加了全新的文档。文档的旧版本不会立即消失，尽管您将无法访问它。Elasticsearch 会在后台清理已删除的文档，同时继续索引更多数据。

### 路径参数

`<index>`

     (Required, string) Name of the index that contains the document. 
`<_id>`

     (Required, string) Unique identifier of the document. 

### 查询参数

`preference`

     (Optional, string) Specifies the node or shard the operation should be performed on. Random by default. 
`realtime`

     (Optional, Boolean) If `true`, the request is real-time as opposed to near-real-time. Defaults to `true`. See [Realtime](docs-get.html#realtime "Realtime"). 
`refresh`

     (Optional, Boolean) If `true`, the request refreshes the relevant shard before retrieving the document. Defaults to `false`. 
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

`version`

     (Optional, integer) Explicit version number for concurrency control. The specified version must match the current version of the document for the request to succeed. 
`version_type`

     (Optional, enum) Specific version type: `external`, `external_gte`. 

### 响应正文

`_index`

     The name of the index the document belongs to. 
`_id`

     The unique identifier for the document. 
`_version`

     The document version. Incremented each time the document is updated. 
`_seq_no`

     The sequence number assigned to the document for the indexing operation. Sequence numbers are used to ensure an older version of a document doesn’t overwrite a newer version. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`_primary_term`

     The primary term assigned to the document for the indexing operation. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`found`

     Indicates whether the document exists: `true` or `false`. 
`_routing`

     The explicit routing, if set. 
__source_

     If `found` is `true`, contains the document data formatted in JSON. Excluded if the `_source` parameter is set to `false` or the `stored_fields` parameter is set to `true`. 
__fields_

     If the `stored_fields` parameter is set to `true` and `found` is `true`, contains the document fields stored in the index. 

###Examples

从"my-index-000001"索引中检索带有"_id"0 的 JSON 文档：

    
    
    response = client.get(
      index: 'my-index-000001',
      id: 0
    )
    puts response
    
    
    GET my-index-000001/_doc/0

API 返回以下结果：

    
    
    {
      "_index": "my-index-000001",
      "_id": "0",
      "_version": 1,
      "_seq_no": 0,
      "_primary_term": 1,
      "found": true,
      "_source": {
        "@timestamp": "2099-11-15T14:12:12",
        "http": {
          "request": {
            "method": "get"
          },
          "response": {
            "status_code": 200,
            "bytes": 1070000
          },
          "version": "1.1"
        },
        "source": {
          "ip": "127.0.0.1"
        },
        "message": "GET /search HTTP/1.1 200 1070000",
        "user": {
          "id": "kimchy"
        }
      }
    }

检查是否存在带有"_id"0 的文档：

    
    
    response = client.exists(
      index: 'my-index-000001',
      id: 0
    )
    puts response
    
    
    HEAD my-index-000001/_doc/0

如果文档存在，Elasticsearch 返回状态代码"200 - 正常"，如果不存在，则返回状态代码"404 - 未找到"。

##### 仅获取源字段

使用"<index>/_source<id>/"资源仅获取文档的"_source"字段。例如：

    
    
    response = client.get_source(
      index: 'my-index-000001',
      id: 1
    )
    puts response
    
    
    GET my-index-000001/_source/1

您可以使用源筛选参数来控制返回"_source"的哪些部分：

    
    
    response = client.get_source(
      index: 'my-index-000001',
      id: 1,
      _source_includes: '*.id',
      _source_excludes: 'entities'
    )
    puts response
    
    
    GET my-index-000001/_source/1/?_source_includes=*.id&_source_excludes=entities

您可以将 HEAD 与"_source"端点一起使用，以有效地测试文档_source是否存在。如果在映射中禁用文档的源，则文档的源不可用。

    
    
    response = client.exists_source(
      index: 'my-index-000001',
      id: 1
    )
    puts response
    
    
    HEAD my-index-000001/_source/1

##### 获取存储字段

使用"stored_fields"参数指定要检索的存储字段集。任何未存储的请求字段都将被忽略。例如，请考虑以下映射：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            counter: {
              type: 'integer',
              store: false
            },
            tags: {
              type: 'keyword',
              store: true
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
              "counter": {
                 "type": "integer",
                 "store": false
              },
              "tags": {
                 "type": "keyword",
                 "store": true
              }
           }
       }
    }

现在我们可以添加一个文档：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        counter: 1,
        tags: [
          'production'
        ]
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "counter": 1,
      "tags": [ "production" ]
    }

然后尝试检索它：

    
    
    response = client.get(
      index: 'my-index-000001',
      id: 1,
      stored_fields: 'tags,counter'
    )
    puts response
    
    
    GET my-index-000001/_doc/1?stored_fields=tags,counter

API 返回以下结果：

    
    
    {
       "_index": "my-index-000001",
       "_id": "1",
       "_version": 1,
       "_seq_no" : 22,
       "_primary_term" : 1,
       "found": true,
       "fields": {
          "tags": [
             "production"
          ]
       }
    }

从文档本身获取的字段值始终以数组形式返回。由于不存储"计数器"字段，因此 get 请求会忽略它。

您还可以检索元数据字段，例如"_routing"字段：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      routing: 'user1',
      body: {
        counter: 1,
        tags: [
          'env2'
        ]
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/2?routing=user1
    {
      "counter" : 1,
      "tags" : ["env2"]
    }
    
    
    response = client.get(
      index: 'my-index-000001',
      id: 2,
      routing: 'user1',
      stored_fields: 'tags,counter'
    )
    puts response
    
    
    GET my-index-000001/_doc/2?routing=user1&stored_fields=tags,counter

API 返回以下结果：

    
    
    {
       "_index": "my-index-000001",
       "_id": "2",
       "_version": 1,
       "_seq_no" : 13,
       "_primary_term" : 1,
       "_routing": "user1",
       "found": true,
       "fields": {
          "tags": [
             "env2"
          ]
       }
    }

只能使用"stored_field"选项检索叶字段。无法返回对象字段 - 如果指定，请求将失败。

[« Index API](docs-index_.md) [Delete API »](docs-delete.md)
