

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Cross-cluster replication APIs](ccr-apis.md) [Create follower API »](ccr-
put-follow.md)

## 获取跨集群复制统计信息API

获取跨集群复制统计信息。

###Request

    
    
    GET /_ccr/stats

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对包含关注者索引的集群具有"监控"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 获取跨集群复制统计信息。此 API 将返回与跨集群复制相关的所有统计信息。特别是，此 API 返回有关自动关注的统计信息，并返回与 getfollower 统计信息 API 中相同的分片级统计信息。

### 响应正文

`auto_follow_stats`

    

(对象)表示自动关注协调器的统计信息的对象。

"auto_follow_stats"的属性

`number_of_failed_follow_indices`

     (long) The number of indices that the auto-follow coordinator failed to automatically follow. The causes of recent failures are captured in the logs of the elected master node and in the `auto_follow_stats.recent_auto_follow_errors` field. 
`number_of_failed_remote_cluster_state_requests`

     (long) The number of times that the auto-follow coordinator failed to retrieve the cluster state from a remote cluster registered in a collection of auto-follow patterns. 
`number_of_successful_follow_indices`

     (long) The number of indices that the auto-follow coordinator successfully followed. 
`recent_auto_follow_errors`

     (array) An array of objects representing failures by the auto-follow coordinator. 

`follow_stats`

     (object) An object representing shard-level stats for follower indices; refer to the details of the response in the [get follower stats API](ccr-get-follow-stats.html "Get follower stats API"). 

###Examples

此示例检索跨集群复制统计信息：

    
    
    GET /_ccr/stats

API 返回以下结果：

    
    
    {
      "auto_follow_stats" : {
        "number_of_failed_follow_indices" : 0,
        "number_of_failed_remote_cluster_state_requests" : 0,
        "number_of_successful_follow_indices" : 1,
        "recent_auto_follow_errors" : [],
        "auto_followed_clusters" : []
      },
      "follow_stats" : {
        "indices" : [
          {
            "index" : "follower_index",
            "shards" : [
              {
                "remote_cluster" : "remote_cluster",
                "leader_index" : "leader_index",
                "follower_index" : "follower_index",
                "shard_id" : 0,
                "leader_global_checkpoint" : 1024,
                "leader_max_seq_no" : 1536,
                "follower_global_checkpoint" : 768,
                "follower_max_seq_no" : 896,
                "last_requested_seq_no" : 897,
                "outstanding_read_requests" : 8,
                "outstanding_write_requests" : 2,
                "write_buffer_operation_count" : 64,
                "follower_mapping_version" : 4,
                "follower_settings_version" : 2,
                "follower_aliases_version" : 8,
                "total_read_time_millis" : 32768,
                "total_read_remote_exec_time_millis" : 16384,
                "successful_read_requests" : 32,
                "failed_read_requests" : 0,
                "operations_read" : 896,
                "bytes_read" : 32768,
                "total_write_time_millis" : 16384,
                "write_buffer_size_in_bytes" : 1536,
                "successful_write_requests" : 16,
                "failed_write_requests" : 0,
                "operations_written" : 832,
                "read_exceptions" : [ ],
                "time_since_last_read_millis" : 8
              }
            ]
          }
        ]
      }
    }

[« Cross-cluster replication APIs](ccr-apis.md) [Create follower API »](ccr-
put-follow.md)
