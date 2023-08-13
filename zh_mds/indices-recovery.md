

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Import dangling index API](dangling-index-import.md) [Index segments API
»](indices-segments.md)

## 索引恢复接口

返回有关一个或多个索引的正在进行的和已完成的分片恢复的信息。对于数据流，API 返回流的支持索引的信息。

    
    
    response = client.indices.recovery(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_recovery

###Request

"获取/<target>/_recovery"

"获取/_recovery"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"监控"或"管理"索引权限。

###Description

使用索引恢复 API 获取有关正在进行的和已完成的分片恢复的信息。

分片恢复是初始化分片副本的过程，例如从快照恢复主分片或从主分片同步副本分片。分片恢复完成后，恢复的分片可用于搜索和索引。

恢复在以下过程中自动发生：

* 节点启动。这种类型的恢复称为本地存储恢复。  * 主分片复制。  * 将分片重新定位到同一集群中的不同节点。  * 快照还原操作。  * 克隆、收缩或拆分操作。

索引恢复 API 仅报告有关群集中当前存在的已完成恢复的存储分页副本的信息。它仅报告每个分片副本的上次恢复，不报告有关早期恢复的历史信息，也不报告有关不再存在的分片副本的恢复的信息。这意味着，如果分片副本完成了恢复，然后 Elasticsearch 将其重新定位到不同的节点上，则有关原始恢复的信息将不会显示在恢复 API 中。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`active_only`

     (Optional, Boolean) If `true`, the response only includes ongoing shard recoveries. Defaults to `false`. 
`detailed`

     (Optional, Boolean) If `true`, the response includes detailed information about shard recoveries. Defaults to `false`. 
`index`

     (Optional, string) Comma-separated list or wildcard expression of index names used to limit the request. 

### 响应正文

`id`

     (Integer) ID of the shard. 
`type`

    

(字符串)分片的恢复源。返回的值包括：

`EMPTY_STORE`

     An empty store. Indicates a new primary shard or the forced allocation of an empty primary shard using the [cluster reroute API](cluster-reroute.html "Cluster reroute API"). 
`EXISTING_STORE`

     The store of an existing primary shard. Indicates recovery is related to node startup or the allocation of an existing primary shard. 
`LOCAL_SHARDS`

     Shards of another index on the same node. Indicates recovery is related to a [clone](indices-clone-index.html "Clone index API"), [shrink](indices-shrink-index.html "Shrink index API"), or [split](indices-split-index.html "Split index API") operation. 
`PEER`

     A primary shard on another node. Indicates recovery is related to shard replication. 
`SNAPSHOT`

     A snapshot. Indicates recovery is related to a [snapshot restore](snapshots-restore-snapshot.html "Restore a snapshot") operation. 

`STAGE`

    

(字符串)恢复阶段。返回的值可以包括：

`INIT`

     Recovery has not started. 
`INDEX`

     Reading index metadata and copying bytes from source to destination. 
`VERIFY_INDEX`

     Verifying the integrity of the index. 
`TRANSLOG`

     Replaying transaction log. 
`FINALIZE`

     Cleanup. 
`DONE`

     Complete. 

`primary`

     (Boolean) If `true`, the shard is a primary shard. 
`start_time`

     (String) Timestamp of recovery start. 
`stop_time`

     (String) Timestamp of recovery finish. 
`total_time_in_millis`

     (String) Total time to recover shard in milliseconds. 
`source`

    

(对象)恢复源。这可能包括：

* 如果从快照恢复，则为存储库说明 * 源节点的描述

`target`

     (Object) Destination node. 
`index`

     (Object) Statistics about physical index recovery. 
`translog`

     (Object) Statistics about translog recovery. 
`start`

     (Object) Statistics about time to open and start the index. 

###Examples

#### 获取多个数据流和索引的恢复信息

    
    
    response = client.indices.recovery(
      index: 'index1,index2',
      human: true
    )
    puts response
    
    
    GET index1,index2/_recovery?human

#### 获取集群中所有数据流和索引的分段信息

    
    
    response = client.indices.recovery(
      human: true
    )
    puts response
    
    
    GET /_recovery?human

API 返回以下响应：

    
    
    {
      "index1" : {
        "shards" : [ {
          "id" : 0,
          "type" : "SNAPSHOT",
          "stage" : "INDEX",
          "primary" : true,
          "start_time" : "2014-02-24T12:15:59.716",
          "start_time_in_millis": 1393244159716,
          "stop_time" : "0s",
          "stop_time_in_millis" : 0,
          "total_time" : "2.9m",
          "total_time_in_millis" : 175576,
          "source" : {
            "repository" : "my_repository",
            "snapshot" : "my_snapshot",
            "index" : "index1",
            "version" : "{version}",
            "restoreUUID": "PDh1ZAOaRbiGIVtCvZOMww"
          },
          "target" : {
            "id" : "ryqJ5lO5S4-lSFbGntkEkg",
            "host" : "my.fqdn",
            "transport_address" : "my.fqdn",
            "ip" : "10.0.1.7",
            "name" : "my_es_node"
          },
          "index" : {
            "size" : {
              "total" : "75.4mb",
              "total_in_bytes" : 79063092,
              "reused" : "0b",
              "reused_in_bytes" : 0,
              "recovered" : "65.7mb",
              "recovered_in_bytes" : 68891939,
              "recovered_from_snapshot" : "0b",
              "recovered_from_snapshot_in_bytes" : 0,
              "percent" : "87.1%"
            },
            "files" : {
              "total" : 73,
              "reused" : 0,
              "recovered" : 69,
              "percent" : "94.5%"
            },
            "total_time" : "0s",
            "total_time_in_millis" : 0,
            "source_throttle_time" : "0s",
            "source_throttle_time_in_millis" : 0,
            "target_throttle_time" : "0s",
            "target_throttle_time_in_millis" : 0
          },
          "translog" : {
            "recovered" : 0,
            "total" : 0,
            "percent" : "100.0%",
            "total_on_start" : 0,
            "total_time" : "0s",
            "total_time_in_millis" : 0
          },
          "verify_index" : {
            "check_index_time" : "0s",
            "check_index_time_in_millis" : 0,
            "total_time" : "0s",
            "total_time_in_millis" : 0
          }
        } ]
      }
    }

此响应包括有关恢复单个分片的单个索引的信息。恢复源是快照存储库，恢复目标是"my_es_node"节点。

响应还包括恢复的文件和字节数和百分比。

#### 获取详细的恢复信息

要获取恢复中的物理文件列表，请将"详细"查询参数设置为"true"。

    
    
    response = client.indices.recovery(
      human: true,
      detailed: true
    )
    puts response
    
    
    GET _recovery?human&detailed=true

API 返回以下响应：

    
    
    {
      "index1" : {
        "shards" : [ {
          "id" : 0,
          "type" : "STORE",
          "stage" : "DONE",
          "primary" : true,
          "start_time" : "2014-02-24T12:38:06.349",
          "start_time_in_millis" : "1393245486349",
          "stop_time" : "2014-02-24T12:38:08.464",
          "stop_time_in_millis" : "1393245488464",
          "total_time" : "2.1s",
          "total_time_in_millis" : 2115,
          "source" : {
            "id" : "RGMdRc-yQWWKIBM4DGvwqQ",
            "host" : "my.fqdn",
            "transport_address" : "my.fqdn",
            "ip" : "10.0.1.7",
            "name" : "my_es_node"
          },
          "target" : {
            "id" : "RGMdRc-yQWWKIBM4DGvwqQ",
            "host" : "my.fqdn",
            "transport_address" : "my.fqdn",
            "ip" : "10.0.1.7",
            "name" : "my_es_node"
          },
          "index" : {
            "size" : {
              "total" : "24.7mb",
              "total_in_bytes" : 26001617,
              "reused" : "24.7mb",
              "reused_in_bytes" : 26001617,
              "recovered" : "0b",
              "recovered_in_bytes" : 0,
              "recovered_from_snapshot" : "0b",
              "recovered_from_snapshot_in_bytes" : 0,
              "percent" : "100.0%"
            },
            "files" : {
              "total" : 26,
              "reused" : 26,
              "recovered" : 0,
              "percent" : "100.0%",
              "details" : [ {
                "name" : "segments.gen",
                "length" : 20,
                "recovered" : 20
              }, {
                "name" : "_0.cfs",
                "length" : 135306,
                "recovered" : 135306,
                "recovered_from_snapshot": 0
              }, {
                "name" : "segments_2",
                "length" : 251,
                "recovered" : 251,
                "recovered_from_snapshot": 0
              }
              ]
            },
            "total_time" : "2ms",
            "total_time_in_millis" : 2,
            "source_throttle_time" : "0s",
            "source_throttle_time_in_millis" : 0,
            "target_throttle_time" : "0s",
            "target_throttle_time_in_millis" : 0
          },
          "translog" : {
            "recovered" : 71,
            "total" : 0,
            "percent" : "100.0%",
            "total_on_start" : 0,
            "total_time" : "2.0s",
            "total_time_in_millis" : 2025
          },
          "verify_index" : {
            "check_index_time" : 0,
            "check_index_time_in_millis" : 0,
            "total_time" : "88ms",
            "total_time_in_millis" : 88
          }
        } ]
      }
    }

响应包括已恢复的任何物理文件及其大小的列表。

响应还包括各个恢复阶段的计时(以毫秒为单位)：

* 索引检索 * 事务日志重播 * 索引开始时间

此响应指示恢复已"完成"。所有恢复(无论是正在进行的还是完整的)都保持群集状态，并可能随时报告。

若要仅返回有关正在进行的恢复的信息，请将"active_only"查询参数设置为"true"。

[« Import dangling index API](dangling-index-import.md) [Index segments API
»](indices-segments.md)
