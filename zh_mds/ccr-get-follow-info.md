

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Get follower stats API](ccr-get-follow-stats.md) [Create auto-follow
pattern API »](ccr-put-auto-follow-pattern.md)

## 获取关注者信息API

检索有关所有关注者索引的信息。

###Request

    
    
    GET /<index>/_ccr/info

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 列出每个关注者索引的参数和状态。例如，结果包括追随者索引名称、领导者索引名称、复制选项以及追随者索引是处于活动状态还是已暂停。

### 路径参数

`<index>`

     (Required, string) A comma-delimited list of follower index patterns. 

### 响应正文

`follower_indices`

    

(阵列)关注者索引统计信息的数组。

"follower_indices"中对象的属性

`follower_index`

     (string) The name of the follower index. 
`leader_index`

     (string) The name of the index in the leader cluster that is followed. 

`parameters`

    

(对象)封装跨集群复制参数的对象。如果关注者索引的"状态"为"已暂停"，则省略此对象。

"参数"的属性

`max_outstanding_read_requests`

     (long) The maximum number of outstanding read requests from the remote cluster. 
`max_outstanding_write_requests`

     (integer) The maximum number of outstanding write requests on the follower. 
`max_read_request_operation_count`

     (integer) The maximum number of operations to pull per read from the remote cluster. 
`max_read_request_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The maximum size in bytes of per read of a batch of operations pulled from the remote cluster. 
`max_retry_delay`

     ([time value](api-conventions.html#time-units "Time units")) The maximum time to wait before retrying an operation that failed exceptionally. An exponential backoff strategy is employed when retrying. 
`max_write_buffer_count`

     (integer) The maximum number of operations that can be queued for writing. When this limit is reached, reads from the remote cluster are deferred until the number of queued operations goes below the limit. 
`max_write_buffer_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The maximum total bytes of operations that can be queued for writing. When this limit is reached, reads from the remote cluster are deferred until the total bytes of queued operations goes below the limit. 
`max_write_request_operation_count`

     (integer) The maximum number of operations per bulk write request executed on the follower. 
`max_write_request_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The maximum total bytes of operations per bulk write request executed on the follower. 
`read_poll_timeout`

     ([time value](api-conventions.html#time-units "Time units")) The maximum time to wait for new operations on the remote cluster when the follower index is synchronized with the leader index. When the timeout has elapsed, the poll for operations returns to the follower so that it can update some statistics, then the follower immediately attempts to read from the leader again. 

`remote_cluster`

     (string) The [remote cluster](remote-clusters.html "Remote clusters") that contains the leader index. 
`status`

     (string) Whether index following is `active` or `paused`. 

###Examples

此示例检索关注者信息：

    
    
    response = client.ccr.follow_info(
      index: 'follower_index'
    )
    puts response
    
    
    GET /follower_index/_ccr/info

如果追随者索引为"活动"，则 API 返回以下结果：

    
    
    {
      "follower_indices": [
        {
          "follower_index": "follower_index",
          "remote_cluster": "remote_cluster",
          "leader_index": "leader_index",
          "status": "active",
          "parameters": {
            "max_read_request_operation_count": 5120,
            "max_read_request_size": "32mb",
            "max_outstanding_read_requests": 12,
            "max_write_request_operation_count": 5120,
            "max_write_request_size": "9223372036854775807b",
            "max_outstanding_write_requests": 9,
            "max_write_buffer_count": 2147483647,
            "max_write_buffer_size": "512mb",
            "max_retry_delay": "500ms",
            "read_poll_timeout": "1m"
          }
        }
      ]
    }

如果关注者索引为"暂停"，API 将返回以下结果：

    
    
    {
      "follower_indices": [
        {
          "follower_index": "follower_index",
          "remote_cluster": "remote_cluster",
          "leader_index": "leader_index",
          "status": "paused"
        }
      ]
    }

[« Get follower stats API](ccr-get-follow-stats.md) [Create auto-follow
pattern API »](ccr-put-auto-follow-pattern.md)
