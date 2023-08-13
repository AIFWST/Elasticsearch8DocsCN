

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Get follower info API](ccr-get-follow-info.md) [Delete auto-follow
pattern API »](ccr-delete-auto-follow-pattern.md)

## 创建自动关注模式API

创建自动跟随模式。

###Request

    
    
    PUT /_ccr/auto_follow/<auto_follow_pattern_name>
    {
      "remote_cluster" : "<remote_cluster>",
      "leader_index_patterns" :
      [
        "<leader_index_pattern>"
      ],
      "leader_index_exclusion_patterns":
      [
        "<leader_index_exclusion_pattern>"
      ],
      "follow_index_pattern" : "<follow_index_pattern>"
    }

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对领导者索引模式具有"读取"和"监控"索引权限。您还必须对包含追随者索引的集群具有"manage_ccr"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 针对请求正文中指定的远程群集创建一个新的自动跟踪模式命名集合。远程集群上新创建的索引与任何指定模式匹配将自动配置为追随者索引。在创建自动关注模式之前创建的远程群集上的索引不会自动跟踪，即使它们与模式匹配也是如此。

此 API 还可用于更新现有的自动关注模式。请注意，在更新自动关注模式之前自动配置的关注者索引将保持不变，即使它们与新模式不匹配。

### 路径参数

`<auto_follow_pattern_name>`

     (Required, string) The name of the collection of auto-follow patterns. 

### 请求正文

`remote_cluster`

     (Required, string) The [remote cluster](remote-clusters.html "Remote clusters") containing the leader indices to match against. 
`leader_index_patterns`

     (Optional, array) An array of simple index patterns to match against indices in the remote cluster specified by the `remote_cluster` field. 
`leader_index_exclusion_patterns`

     (Optional, array) An array of simple index patterns that can be used to exclude indices from being auto-followed. Indices in the remote cluster whose names are matching one or more `leader_index_patterns` and one or more `leader_index_exclusion_patterns` won't be followed. 
`follow_index_pattern`

     (Optional, string) The name of follower index. The template `{{leader_index}}` can be used to derive the name of the follower index from the name of the leader index. When following a data stream, the `follow_index_pattern` will be used for renaming not only the leader index, but also the data stream containing the leader index. For example, a data stream called `logs-mysql-default` with a backing index of `.ds-logs-mysql-default-2022-01-01-000001` and a `follow_index_pattern` of `{{leader_index}}_copy` will replicate the data stream as `logs-mysql-default_copy` and the backing index as `.ds-logs-mysql-default_copy-2022-01-01-000001`. 
`settings`

     (object) Settings to override from the leader index. Note that certain settings can not be overrode (e.g., `index.number_of_shards`). 

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

此示例创建一个名为"my_auto_follow_pattern"的自动跟随模式：

    
    
    PUT /_ccr/auto_follow/my_auto_follow_pattern
    {
      "remote_cluster" : "remote_cluster",
      "leader_index_patterns" :
      [
        "leader_index*"
      ],
      "follow_index_pattern" : "{{leader_index}}-follower",
      "settings": {
        "index.number_of_replicas": 0
      },
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

[« Get follower info API](ccr-get-follow-info.md) [Delete auto-follow
pattern API »](ccr-delete-auto-follow-pattern.md)
