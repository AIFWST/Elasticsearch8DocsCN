

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Pause follower API](ccr-post-pause-follow.md) [Unfollow API »](ccr-post-
unfollow.md)

## 简历关注者API

恢复关注者索引。

###Request

    
    
    POST /<follower_index>/_ccr/resume_follow
    {
    }

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对关注者索引具有"写入"和"监控"索引权限。您必须具有领导者索引的"读取"和"监视"索引权限。您还必须对包含追随者索引的集群具有"manage_ccr"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 恢复已使用暂停追随者 API 显式暂停或由于执行而隐式暂停的追随者索引，该索引由于在跟踪期间失败而无法重试。当此 API 返回时，追随者索引将从领导者索引恢复获取操作。

### 路径参数

`<follower_index>`

     (Required, string) The name of the follower index. 

### 请求正文

`max_read_request_operation_count`

     (integer) The maximum number of operations to pull per read from the remote cluster. 
`max_outstanding_read_requests`

     (long) The maximum number of outstanding reads requests from the remote cluster. 
`max_read_request_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The maximum size in bytes of per read of a batch of operations pulled from the remote cluster. 
`max_write_request_operation_count`

     (integer) The maximum number of operations per bulk write request executed on the follower. 
`max_write_request_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The maximum total bytes of operations per bulk write request executed on the follower. 
`max_outstanding_write_requests`

     (integer) The maximum number of outstanding write requests on the follower. 
`max_write_buffer_count`

     (integer) The maximum number of operations that can be queued for writing. When this limit is reached, reads from the remote cluster will be deferred until the number of queued operations goes below the limit. 
`max_write_buffer_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The maximum total bytes of operations that can be queued for writing. When this limit is reached, reads from the remote cluster will be deferred until the total bytes of queued operations goes below the limit. 
`max_retry_delay`

     ([time value](api-conventions.html#time-units "Time units")) The maximum time to wait before retrying an operation that failed exceptionally. An exponential backoff strategy is employed when retrying. 
`read_poll_timeout`

     ([time value](api-conventions.html#time-units "Time units")) The maximum time to wait for new operations on the remote cluster when the follower index is synchronized with the leader index. When the timeout has elapsed, the poll for operations will return to the follower so that it can update some statistics. Then the follower will immediately attempt to read from the leader again. 

#### 默认值

以下信息 api 的以下输出描述了上述索引遵循请求参数的所有默认值：

    
    
    {
      "follower_indices" : [
        {
          "parameters" : {
            "max_read_request_operation_count" : 5120,
            "max_read_request_size" : "32mb",
            "max_outstanding_read_requests" : 12,
            "max_write_request_operation_count" : 5120,
            "max_write_request_size" : "9223372036854775807b",
            "max_outstanding_write_requests" : 9,
            "max_write_buffer_count" : 2147483647,
            "max_write_buffer_size" : "512mb",
            "max_retry_delay" : "500ms",
            "read_poll_timeout" : "1m"
          }
        }
      ]
    }

###Examples

此示例恢复名为"follower_index"的追随者索引：

    
    
    POST /follower_index/_ccr/resume_follow
    {
      "max_read_request_operation_count" : 1024,
      "max_outstanding_read_requests" : 16,
      "max_read_request_size" : "1024k",
      "max_write_request_operation_count" : 32768,
      "max_write_request_size" : "16k",
      "max_outstanding_write_requests" : 8,
      "max_write_buffer_count" : 512,
      "max_write_buffer_size" : "512k",
      "max_retry_delay" : "10s",
      "read_poll_timeout" : "30s"
    }

API 返回以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Pause follower API](ccr-post-pause-follow.md) [Unfollow API »](ccr-post-
unfollow.md)
