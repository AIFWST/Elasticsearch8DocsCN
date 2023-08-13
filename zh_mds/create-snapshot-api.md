

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Clone snapshot API](clone-snapshot-api.md) [Get snapshot API »](get-
snapshot-api.md)

## 创建快照接口

拍摄集群或指定数据流和索引的快照。

    
    
    response = client.snapshot.create(
      repository: 'my_repository',
      snapshot: 'my_snapshot'
    )
    puts response
    
    
    PUT /_snapshot/my_repository/my_snapshot

###Request

"放 /_snapshot/<repository><snapshot>/"

"发布/_snapshot/<repository><snapshot>/"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"create_snapshot"或"管理"集群权限才能使用此 API。

### 路径参数

`<repository>`

     (Required, string) Name of the snapshot repository. 
`<snapshot>`

     (Required, string) Name of the snapshot. Supports [date math](api-conventions.html#api-date-math-index-names "Date math support in index and index alias names"). Must be unique within the snapshot repository. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`wait_for_completion`

     (Optional, Boolean) If `true`, the request returns a response when the snapshot is complete. If `false`, the request returns a response when the snapshot initializes. Defaults to `false`. 

### 请求正文

`expand_wildcards`

    

(可选，字符串)确定"索引"参数中的通配符模式如何匹配数据流和索引。支持逗号分隔的值，例如"打开，隐藏"。默认为"全部"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open indices and data streams. 
`closed`

     Match closed indices and data streams. 
`hidden`

     Match hidden data streams and indices. Must be combined with `open`, `closed`, or both. 
`none`

     Don't expand wildcard patterns. 

`ignore_unavailable`

     (Optional, Boolean) If `false`, the snapshot fails if any data stream or index in `indices` is missing. If `true`, the snapshot ignores missing data streams and indices. Defaults to `false`. 
`include_global_state`

    

(可选，布尔值)如果为"true"，则在快照中包含群集状态。默认为"真"。群集状态包括：

* 持久群集设置 * 索引模板 * 旧索引模板 * 引入管道 * ILM 策略 * 对于 7.12.0 之后拍摄的快照，功能状态

`indices`

    

(可选，字符串或字符串数组)要包含在快照中的数据流和索引的逗号分隔列表。支持多目标语法。默认为空数组 ('[]')，其中包括所有常规数据流和常规索引。要排除所有数据流和索引，请使用"-*"。

不能使用此参数在快照中包含或排除系统索引或系统数据流。请改用"feature_states"。

`feature_states`

    

(可选，字符串数组)要包含在快照中的功能状态。若要获取可能值及其说明的列表，请使用获取功能 API。

如果"include_global_state"为"true"，则快照默认包含所有功能状态。如果"include_global_state"为"false"，则快照默认包含无功能状态。

请注意，指定空数组将导致默认行为。要排除所有功能状态，而不考虑"include_global_state"值，请指定一个仅包含值"none"("["none"]")的数组。

`metadata`

     (Optional, object) Attaches arbitrary metadata to the snapshot, such as a record of who took the snapshot, why it was taken, or any other useful data. Metadata must be less than 1024 bytes. 

`partial`

    

(可选，布尔值)如果为"false"，则当快照中包含的一个或多个索引没有所有可用的主分片时，整个快照将失败。默认为"假"。

如果为"true"，则允许拍摄具有不可用分片的索引的部分快照。

###Examples

以下请求拍摄"index_1"和"index_2"的快照。

    
    
    response = client.snapshot.create(
      repository: 'my_repository',
      snapshot: 'snapshot_2',
      wait_for_completion: true,
      body: {
        indices: 'index_1,index_2',
        ignore_unavailable: true,
        include_global_state: false,
        metadata: {
          taken_by: 'user123',
          taken_because: 'backup before upgrading'
        }
      }
    )
    puts response
    
    
    PUT /_snapshot/my_repository/snapshot_2?wait_for_completion=true
    {
      "indices": "index_1,index_2",
      "ignore_unavailable": true,
      "include_global_state": false,
      "metadata": {
        "taken_by": "user123",
        "taken_because": "backup before upgrading"
      }
    }

API 返回以下响应：

    
    
    {
      "snapshot": {
        "snapshot": "snapshot_2",
        "uuid": "vdRctLCxSketdKb54xw67g",
        "repository": "my_repository",
        "version_id": <version_id>,
        "version": <version>,
        "indices": [],
        "data_streams": [],
        "feature_states": [],
        "include_global_state": false,
        "metadata": {
          "taken_by": "user123",
          "taken_because": "backup before upgrading"
        },
        "state": "SUCCESS",
        "start_time": "2020-06-25T14:00:28.850Z",
        "start_time_in_millis": 1593093628850,
        "end_time": "2020-06-25T14:00:28.850Z",
        "end_time_in_millis": 1593094752018,
        "duration_in_millis": 0,
        "failures": [],
        "shards": {
          "total": 0,
          "failed": 0,
          "successful": 0
        }
      }
    }

[« Clone snapshot API](clone-snapshot-api.md) [Get snapshot API »](get-
snapshot-api.md)
