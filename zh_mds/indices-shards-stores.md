

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Index segments API](indices-segments.md) [Index stats API »](indices-
stats.md)

## 索引分片存储接口

检索一个或多个索引中有关副本分片的存储信息。对于数据流，API 检索流的支持索引的存储信息。

    
    
    response = client.indices.shard_stores(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_shard_stores

###Request

"获取/<target>/_shard_stores"

"获取/_shard_stores"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"监控"或"管理"索引权限。

###Description

索引分片存储 API 返回以下信息：

* 每个副本分片所在的节点 * 每个副本分片的分配 ID * 每个副本分片的唯一 ID * 打开分片索引时遇到的任何错误或早期故障

默认情况下，API 仅返回未分配或具有一个或多个未分配副本分片的主分片的存储信息。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

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
`status`

    

(可选，字符串)用于限制请求的分片运行状况的逗号分隔列表。

有效值包括：

`green`

     The primary shard and all replica shards are assigned. 
`yellow`

     One or more replica shards are unassigned. 
`red`

     The primary shard is unassigned. 
`all`

     Return all shards, regardless of health status. 

默认为"黄色，红色"。

`max_concurrent_shard_requests`

    

(可选，整数)协调节点发送的最大并发分片级请求数。默认为"100"。较大的值可能会更快地响应面向多个分片的请求，但也可能对其他集群操作造成更大的影响。

###Examples

#### 获取特定数据流或索引的分片存储信息

    
    
    response = client.indices.shard_stores(
      index: 'test'
    )
    puts response
    
    
    GET /test/_shard_stores

#### 获取多个数据流和索引的分片存储信息

    
    
    response = client.indices.shard_stores(
      index: 'test1,test2'
    )
    puts response
    
    
    GET /test1,test2/_shard_stores

#### 获取所有数据流和索引的分片存储信息

    
    
    response = client.indices.shard_stores
    puts response
    
    
    GET /_shard_stores

#### 根据集群运行状况获取分片存储信息

您可以使用"状态"查询参数根据分片运行状况限制返回的信息。

以下请求仅返回分配的主分片和副本分片的信息。

    
    
    response = client.indices.shard_stores(
      status: 'green'
    )
    puts response
    
    
    GET /_shard_stores?status=green

API 返回以下响应：

    
    
    {
       "indices": {
           "my-index-000001": {
               "shards": {
                  "0": { __"stores": [ __{
                            "sPa3OgxLSYGvQ4oPs-Tajw": { __"name": "node_t0",
                                "ephemeral_id" : "9NlXRFGCT1m8tkvYCMK-8A",
                                "transport_address": "local[1]",
                                "external_id": "node_t0",
                                "attributes": {},
                                "roles": [...],
                                "version": "8.7.0"
                            },
                            "allocation_id": "2iNySv_OQVePRX-yaRH_lQ", __"allocation" : "primary|replica|unused" __"store_exception": ... __}
                    ]
                  }
               }
           }
       }
    }

__

|

键是存储信息 ---|--- __ 的相应分片 ID

|

分片 __ 的所有副本的存储信息列表

|

托管存储副本的节点信息，键是唯一节点 ID。   __

|

存储副本的分配 ID __

|

存储副本的状态，无论它是用作主副本、副本副本还是根本不使用 __

|

打开分片索引时或早期引擎故障时遇到的任何异常 « 索引段 API 索引统计信息 API »