

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Data stream APIs](data-stream-apis.md)

[« Promote data stream API](promote-data-stream-api.md) [Downsample index
API »](indices-downsample-data-stream.md)

## 修改数据流API

在单个原子操作中执行一个或多个数据流修改操作。

    
    
    POST _data_stream/_modify
    {
      "actions": [
        {
          "remove_backing_index": {
            "data_stream": "my-logs",
            "index": ".ds-my-logs-2099.01.01-000001"
          }
        },
        {
          "add_backing_index": {
            "data_stream": "my-logs",
            "index": "index-to-add"
          }
        }
      ]
    }

###Request

"发布/_data_stream/_modify"

### 请求正文

`actions`

    

(必需，对象数组)要执行的操作。

"操作"对象的属性

`<action>`

    

(必填，对象)关键是操作类型。至少需要一个操作。

有效的<action>""键

`add_backing_index`

     Adds an existing index as a backing index for a data stream. The index is hidden as part of this operation. 

使用"add_backing_index"操作添加索引可能会导致不正确的数据流行为。这应被视为专家级 API。

`remove_backing_index`

     Removes a backing index from a data stream. The index is unhidden as part of this operation. A data stream's write index cannot be removed. 

对象正文包含操作的选项。

""的属性<action>

`data_stream`

     (Required*, string) Data stream targeted by the action. 
`index`

     (Required*, string) Index for the action. 

[« Promote data stream API](promote-data-stream-api.md) [Downsample index
API »](indices-downsample-data-stream.md)
