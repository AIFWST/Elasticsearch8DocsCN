

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Term vectors API](docs-termvectors.md) [`?refresh` »](docs-refresh.md)

## 多术语向量API

使用单个请求检索多个术语向量。

    
    
    response = client.mtermvectors(
      body: {
        docs: [
          {
            _index: 'my-index-000001',
            _id: '2',
            term_statistics: true
          },
          {
            _index: 'my-index-000001',
            _id: '1',
            fields: [
              'message'
            ]
          }
        ]
      }
    )
    puts response
    
    
    POST /_mtermvectors
    {
       "docs": [
          {
             "_index": "my-index-000001",
             "_id": "2",
             "term_statistics": true
          },
          {
             "_index": "my-index-000001",
             "_id": "1",
             "fields": [
                "message"
             ]
          }
       ]
    }

###Request

"发布/_mtermvectors"

"发布/<index>/_mtermvectors"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对目标索引或索引别名具有"读取"索引权限。

###Description

您可以按索引和 ID 指定现有文档，也可以在请求正文中提供人工文档。可以在请求正文或请求 URI 中指定索引。

响应包含一个"docs"数组，其中包含所有获取的术语向量。每个元素都具有术语向量 API 提供的结构。

有关可包含在响应中的信息的详细信息，请参阅术语向量 API。

### 路径参数

`<index>`

     (Optional, string) Name of the index that contains the documents. 

### 查询参数

`fields`

    

(可选，字符串)要包含在统计信息中的字段的逗号分隔列表或通配符表达式。

用作默认列表，除非在"completion_fields"或"fielddata_fields"参数中提供了特定的字段列表。

`field_statistics`

     (Optional, Boolean) If `true`, the response includes the document count, sum of document frequencies, and sum of total term frequencies. Defaults to `true`. 
`<offsets>`

     (Optional, Boolean) If `true`, the response includes term offsets. Defaults to `true`. 
`payloads`

     (Optional, Boolean) If `true`, the response includes term payloads. Defaults to `true`. 
`positions`

     (Optional, Boolean) If `true`, the response includes term positions. Defaults to `true`. 
`preference`

     (Optional, string) Specifies the node or shard the operation should be performed on. Random by default. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`realtime`

     (Optional, Boolean) If `true`, the request is real-time as opposed to near-real-time. Defaults to `true`. See [Realtime](docs-get.html#realtime "Realtime"). 
`term_statistics`

     (Optional, Boolean) If `true`, the response includes term frequency and document frequency. Defaults to `false`. 
`version`

     (Optional, Boolean) If `true`, returns the document version as part of a hit. 
`version_type`

     (Optional, enum) Specific version type: `external`, `external_gte`. 

####Examples

如果在请求 URI 中指定索引，则无需为请求正文中的每个文档指定索引：

    
    
    response = client.mtermvectors(
      index: 'my-index-000001',
      body: {
        docs: [
          {
            _id: '2',
            fields: [
              'message'
            ],
            term_statistics: true
          },
          {
            _id: '1'
          }
        ]
      }
    )
    puts response
    
    
    POST /my-index-000001/_mtermvectors
    {
       "docs": [
          {
             "_id": "2",
             "fields": [
                "message"
             ],
             "term_statistics": true
          },
          {
             "_id": "1"
          }
       ]
    }

如果所有请求的文档都在同一索引中，并且参数相同，则可以使用以下简化语法：

    
    
    response = client.mtermvectors(
      index: 'my-index-000001',
      body: {
        ids: [
          '1',
          '2'
        ],
        parameters: {
          fields: [
            'message'
          ],
          term_statistics: true
        }
      }
    )
    puts response
    
    
    POST /my-index-000001/_mtermvectors
    {
      "ids": [ "1", "2" ],
      "parameters": {
        "fields": [
          "message"
        ],
        "term_statistics": true
      }
    }

#### 人工文档

您还可以使用"mtermvectors"为请求正文中提供的_artificial_documents生成术语向量。使用的映射由指定的"_index"确定。

    
    
    response = client.mtermvectors(
      body: {
        docs: [
          {
            _index: 'my-index-000001',
            doc: {
              message: 'test test test'
            }
          },
          {
            _index: 'my-index-000001',
            doc: {
              message: 'Another test ...'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST /_mtermvectors
    {
       "docs": [
          {
             "_index": "my-index-000001",
             "doc" : {
                "message" : "test test test"
             }
          },
          {
             "_index": "my-index-000001",
             "doc" : {
               "message" : "Another test ..."
             }
          }
       ]
    }

[« Term vectors API](docs-termvectors.md) [`?refresh` »](docs-refresh.md)
