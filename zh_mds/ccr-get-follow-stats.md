

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Forget follower API](ccr-post-forget-follower.md) [Get follower info API
»](ccr-get-follow-info.md)

## 获取关注者统计信息API

获取关注者统计信息。

###Request

    
    
    GET /<index>/_ccr/stats

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对包含关注者索引的集群具有"监控"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 获取关注者统计信息。此 API 将返回有关与指定索引的每个分片关联的以下任务的分片级统计信息。

### 路径参数

`<index>`

     (Required, string) A comma-delimited list of index patterns. 

### 响应正文

`indices`

    

(阵列)关注者索引统计信息的数组。

"指数"的属性

`fatal_exception`

     (object) An object representing a fatal exception that cancelled the following task. In this situation, the following task must be resumed manually with the [resume follower API](ccr-post-resume-follow.html "Resume follower API"). 
`index`

     (string) The name of the follower index. 

`shards`

    

(阵列)分片级别的以下任务统计信息数组。

"分片"中对象的属性

`bytes_read`

    

(长)从领导者读取的传输字节总数。

这只是一个估计值，如果不考虑压缩(如果启用)。

`failed_read_requests`

     (long) The number of failed reads. 
`failed_write_requests`

     (long) The number of failed bulk write requests executed on the follower. 
`follower_aliases_version`

     (long) The index aliases version the follower is synced up to. 
`follower_global_checkpoint`

     (long) The current global checkpoint on the follower. The difference between the `leader_global_checkpoint` and the `follower_global_checkpoint` is an indication of how much the follower is lagging the leader. 
`follower_index`

     (string) The name of the follower index. 
`follower_mapping_version`

     (long) The mapping version the follower is synced up to. 
`follower_max_seq_no`

     (long) The current maximum sequence number on the follower. 
`follower_settings_version`

     (long) The index settings version the follower is synced up to. 
`last_requested_seq_no`

     (long) The starting sequence number of the last batch of operations requested from the leader. 
`leader_global_checkpoint`

     (long) The current global checkpoint on the leader known to the follower task. 
`leader_index`

     (string) The name of the index in the leader cluster being followed. 
`leader_max_seq_no`

     (long) The current maximum sequence number on the leader known to the follower task. 
`operations_read`

     (long) The total number of operations read from the leader. 
`operations_written`

     (long) The number of operations written on the follower. 
`outstanding_read_requests`

     (integer) The number of active read requests from the follower. 
`outstanding_write_requests`

     (integer) The number of active bulk write requests on the follower. 

`read_exceptions`

    

(阵列)表示失败读取的对象数组。

"read_exceptions"中对象的属性

`exception`

     (object) Represents the exception that caused the read to fail. 
`from_seq_no`

     (long) The starting sequence number of the batch requested from the leader. 
`retries`

     (integer) The number of times the batch has been retried. 

`remote_cluster`

     (string) The [remote cluster](remote-clusters.html "Remote clusters") containing the leader index. 
`shard_id`

     (integer) The numerical shard ID, with values from 0 to one less than the number of replicas. 
`successful_read_requests`

     (long) The number of successful fetches. 
`successful_write_requests`

     (long) The number of bulk write requests executed on the follower. 
`time_since_last_read_millis`

    

(长)自读取请求发送给领导者以来的毫秒数。

当追随者赶上领导者时，此数字将增加到配置的"read_poll_timeout"，此时将向领导者发送另一个读取请求。

`total_read_remote_exec_time_millis`

     (long) The total time reads spent executing on the remote cluster. 
`total_read_time_millis`

     (long) The total time reads were outstanding, measured from the time a read was sent to the leader to the time a reply was returned to the follower. 
`total_write_time_millis`

     (long) The total time spent writing on the follower. 
`write_buffer_operation_count`

     (integer) The number of write operations queued on the follower. 
`write_buffer_size_in_bytes`

     (long) The total number of bytes of operations currently queued for writing. 

###Examples

此示例检索关注者统计信息：

    
    
    GET /follower_index/_ccr/stats

API 返回以下结果：

    
    
    {
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

[« Forget follower API](ccr-post-forget-follower.md) [Get follower info API
»](ccr-get-follow-info.md)
