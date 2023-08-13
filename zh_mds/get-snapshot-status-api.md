

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Get snapshot API](get-snapshot-api.md) [Restore snapshot API »](restore-
snapshot-api.md)

## 获取快照状态API

检索参与快照的每个分片的当前状态的详细说明。

    
    
    response = client.snapshot.status
    puts response
    
    
    GET _snapshot/_status

###Request

"得到_snapshot/_status"

"得到_snapshot/<repository>/_status"

"得到_snapshot/<repository>/<snapshot>/_status"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"monitor_snapshot"、"create_snapshot"或"管理"集群权限才能使用此 API。

###Description

使用获取快照状态 API 获取有关参与快照的分片的详细信息。

如果省略 '' 请求<snapshot>路径参数，则请求仅检索当前正在运行的快照的信息。首选此用法。

如果需要，可以指定""<repository>和<snapshot>""来检索特定快照的信息，即使它们当前未运行。

使用 API 返回当前正在运行的快照以外的任何快照的状态可能会很昂贵。API 要求从存储库读取每个快照中的每个分片。例如，如果您有 100 个快照，每个快照包含 1000 个分片，则包含所有快照的 API 请求将需要 100000 次读取(100 个快照 * 1000 个分片)。

根据存储的延迟，此类请求可能需要很长时间才能返回结果。这些请求还会对机器资源征税，并且在使用云存储时会产生高昂的处理成本。

### 路径参数

`<repository>`

     (Optional, string) Snapshot repository name used to limit the request. Supports wildcards (`*`) if `<snapshot>` isn't specified. 
`<snapshot>`

     (Optional, string) Comma-separated list of snapshots to retrieve status for. Defaults to currently running snapshots. Wildcards (`*`) are not supported. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`ignore_unavailable`

    

(可选，布尔值)如果为"false"，则请求将针对任何不可用的快照返回错误。默认为"假"。

如果为"true"，则请求将忽略不可用的快照，例如已损坏或暂时无法返回的快照。

### 响应正文

`repository`

     (string) Name of the repository that includes the snapshot. 
`snapshot`

     (string) Name of the snapshot. 
`uuid`

     (string) Universally unique identifier (UUID) of the snapshot. 
`state`

    

(字符串)指示当前快照状态。

"状态"的值

`FAILED`

     The snapshot finished with an error and failed to store any data. 
`STARTED`

     The snapshot is currently running. 
`PARTIAL`

     The global cluster state was stored, but data of at least one shard was not stored successfully. The [`failures`](get-snapshot-api.html#get-snapshot-api-response-failures) section of the response contains more detailed information about shards that were not processed correctly. 
`SUCCESS`

     The snapshot finished and all shards were stored successfully. 

`include_global_state`

     (Boolean) Indicates whether the current cluster state is included in the snapshot. 

`shards_stats`

    

(对象)包含快照中的分片计数。

"shards_stats"的属性

`initializing`

     (integer) Number of shards that are still initializing. 
`started`

     (integer) Number of shards that have started but are not finalized. 
`finalizing`

     (integer) Number of shards that are finalizing but are not done. 
`done`

     (integer) Number of shards that initialized, started, and finalized successfully. 
`failed`

     (integer) Number of shards that failed to be included in the snapshot. 
`total`

     (integer) Total number of shards included in the snapshot. 

`stats`

    

(对象)提供有关快照中包含的文件的数量 ("file_count") 和大小 ("size_in_bytes") 的详细信息。

"统计"的属性

`incremental`

    

(对象)仍需要作为增量快照的一部分复制的文件的数量和大小。

对于已完成的快照，此属性指示存储库中尚不存在且作为增量快照的一部分复制的文件的数量和大小。

`processed`

     (object) Number and size of files that have already been uploaded to the snapshot. After a file is uploaded, the processed `file_count` and `size_in_bytes` are incremented in `stats`. 
`total`

     (object) Total number and size of files that are referenced by the snapshot. 

`start_time_in_millis`

     (long) The time, in milliseconds, when the snapshot creation process started. 

`time_in_millis`

     (long) The total time, in milliseconds, that it took for the snapshot process to complete. 

`<index>`

    

(对象列表)包含有关快照中包含的索引的信息的对象列表。

""的属性<index>

`shards_stats`

     (object) See [`shards_stats`](get-snapshot-status-api.html#get-snapshot-status-shards-stats). 
`stats`

     (object) See [`stats`](get-snapshot-status-api.html#get-snapshot-status-stats). 
`shards`

    

(对象列表)包含有关包含快照的分片的信息的对象列表。

"分片"的属性

`stage`

    

(字符串)指示包含快照的分片的当前状态。

"舞台"的属性

`DONE`

     Number of shards in the snapshot that were successfully stored in the repository. 
`FAILURE`

     Number of shards in the snapshot that were not successfully stored in the repository. 
`FINALIZE`

     Number of shards in the snapshot that are in the finalizing stage of being stored in the repository. 
`INIT`

     Number of shards in the snapshot that are in the initializing stage of being stored in the repository. 
`STARTED`

     Number of shards in the snapshot that are in the started stage of being stored in the repository. 

`stats`

     (object) See [`stats`](get-snapshot-status-api.html#get-snapshot-status-stats). 
`total`

     (object) Total number and size of files that are referenced by the snapshot. 
`start_time_in_millis`

     (long) See [`start_time_in_millis`](get-snapshot-status-api.html#get-snapshot-status-start-time). 
`time_in_millis`

     (long) See [`time_in_millis`](get-snapshot-status-api.html#get-snapshot-status-total-time). 

###Example

以下请求返回"my_repository"存储库中"snapshot_2"的详细状态信息。此响应包括获取快照 API 以外的其他信息，例如分片状态和文件统计信息。

    
    
    response = client.snapshot.status(
      repository: 'my_repository',
      snapshot: 'snapshot_2'
    )
    puts response
    
    
    GET _snapshot/my_repository/snapshot_2/_status
    
    
    {
      "snapshots" : [
        {
          "snapshot" : "snapshot_2",
          "repository" : "my_repository",
          "uuid" : "lNeQD1SvTQCqqJUMQSwmGg",
          "state" : "SUCCESS",
          "include_global_state" : false,
          "shards_stats" : {
            "initializing" : 0,
            "started" : 0,
            "finalizing" : 0,
            "done" : 1,
            "failed" : 0,
            "total" : 1
          },
          "stats" : {
            "incremental" : {
              "file_count" : 3,
              "size_in_bytes" : 5969
            },
            "total" : {
              "file_count" : 4,
              "size_in_bytes" : 6024
            },
            "start_time_in_millis" : 1594829326691,
            "time_in_millis" : 205
          },
          "indices" : {
            "index_1" : {
              "shards_stats" : {
                "initializing" : 0,
                "started" : 0,
                "finalizing" : 0,
                "done" : 1,
                "failed" : 0,
                "total" : 1
              },
              "stats" : {
                "incremental" : {
                  "file_count" : 3,
                  "size_in_bytes" : 5969
                },
                "total" : {
                  "file_count" : 4,
                  "size_in_bytes" : 6024
                },
                "start_time_in_millis" : 1594829326896,
                "time_in_millis" : 0
              },
              "shards" : {
                "0" : {
                  "stage" : "DONE",
                  "stats" : {
                    "incremental" : {
                      "file_count" : 3,
                      "size_in_bytes" : 5969
                    },
                    "total" : {
                      "file_count" : 4,
                      "size_in_bytes" : 6024
                    },
                    "start_time_in_millis" : 1594829326896,
                    "time_in_millis" : 0
                  }
                }
              }
            }
          }
        }
      ]
    }

[« Get snapshot API](get-snapshot-api.md) [Restore snapshot API »](restore-
snapshot-api.md)
