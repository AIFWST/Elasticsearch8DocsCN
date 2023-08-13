

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Render search template API](render-search-template-api.md) [Suggesters
»](search-suggesters.md)

## 搜索分片接口

返回将对其执行搜索请求的索引和分片。

    
    
    response = client.search_shards(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_search_shards

###Request

"获取/<target>/_search_shards"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"view_index_metadata"或"管理"索引权限。

###Description

搜索分片 api 返回将对其执行搜索请求的索引和分片。这可以为使用路由和分片首选项解决问题或规划优化提供有用的反馈。使用过滤后的别名时，过滤器将作为"索引"部分的一部分返回。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to search. Supports wildcards (`*`). To search all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的索引类型。如果请求可以以数据流为目标，则此参数确定通配符表达式是否与隐藏的数据流匹配。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open, non-hidden indices. Also matches any non-hidden data stream. 
`closed`

     Match closed, non-hidden indices. Also matches any non-hidden data stream. Data streams cannot be closed. 
`hidden`

     Match hidden data streams and hidden indices. Must be combined with `open`, `closed`, or both. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`preference`

     (Optional, string) Specifies the node or shard the operation should be performed on. Random by default. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 

###Examples

    
    
    response = client.search_shards(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_search_shards

API 返回以下结果：

    
    
    {
      "nodes": ...,
      "indices" : {
        "my-index-000001": { }
      },
      "shards": [
        [
          {
            "index": "my-index-000001",
            "node": "JklnKbD7Tyqi9TP3_Q_tBg",
            "relocating_node": null,
            "primary": true,
            "shard": 0,
            "state": "STARTED",
            "allocation_id": {"id":"0TvkCyF7TAmM1wHP4a42-A"},
            "relocation_failure_info" : {
              "failed_attempts" : 0
            }
          }
        ],
        [
          {
            "index": "my-index-000001",
            "node": "JklnKbD7Tyqi9TP3_Q_tBg",
            "relocating_node": null,
            "primary": true,
            "shard": 1,
            "state": "STARTED",
            "allocation_id": {"id":"fMju3hd1QHWmWrIgFnI4Ww"},
            "relocation_failure_info" : {
              "failed_attempts" : 0
            }
          }
        ],
        [
          {
            "index": "my-index-000001",
            "node": "JklnKbD7Tyqi9TP3_Q_tBg",
            "relocating_node": null,
            "primary": true,
            "shard": 2,
            "state": "STARTED",
            "allocation_id": {"id":"Nwl0wbMBTHCWjEEbGYGapg"},
            "relocation_failure_info" : {
              "failed_attempts" : 0
            }
          }
        ],
        [
          {
            "index": "my-index-000001",
            "node": "JklnKbD7Tyqi9TP3_Q_tBg",
            "relocating_node": null,
            "primary": true,
            "shard": 3,
            "state": "STARTED",
            "allocation_id": {"id":"bU_KLGJISbW0RejwnwDPKw"},
            "relocation_failure_info" : {
              "failed_attempts" : 0
            }
          }
        ],
        [
          {
            "index": "my-index-000001",
            "node": "JklnKbD7Tyqi9TP3_Q_tBg",
            "relocating_node": null,
            "primary": true,
            "shard": 4,
            "state": "STARTED",
            "allocation_id": {"id":"DMs7_giNSwmdqVukF7UydA"},
            "relocation_failure_info" : {
              "failed_attempts" : 0
            }
          }
        ]
      ]
    }

指定相同的请求，这次使用路由值：

    
    
    response = client.search_shards(
      index: 'my-index-000001',
      routing: 'foo,bar'
    )
    puts response
    
    
    GET /my-index-000001/_search_shards?routing=foo,bar

API 返回以下结果：

    
    
    {
      "nodes": ...,
      "indices" : {
          "my-index-000001": { }
      },
      "shards": [
        [
          {
            "index": "my-index-000001",
            "node": "JklnKbD7Tyqi9TP3_Q_tBg",
            "relocating_node": null,
            "primary": true,
            "shard": 2,
            "state": "STARTED",
            "allocation_id": {"id":"fMju3hd1QHWmWrIgFnI4Ww"},
            "relocation_failure_info" : {
              "failed_attempts" : 0
            }
          }
        ],
        [
          {
            "index": "my-index-000001",
            "node": "JklnKbD7Tyqi9TP3_Q_tBg",
            "relocating_node": null,
            "primary": true,
            "shard": 3,
            "state": "STARTED",
            "allocation_id": {"id":"0TvkCyF7TAmM1wHP4a42-A"},
            "relocation_failure_info" : {
              "failed_attempts" : 0
            }
          }
        ]
      ]
    }

由于指定的路由值，仅对两个分片执行搜索。

[« Render search template API](render-search-template-api.md) [Suggesters
»](search-suggesters.md)
