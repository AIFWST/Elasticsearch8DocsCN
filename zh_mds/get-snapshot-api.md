

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Create snapshot API](create-snapshot-api.md) [Get snapshot status API
»](get-snapshot-status-api.md)

## 获取快照接口

检索有关一个或多个快照的信息。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: 'my_snapshot'
    )
    puts response
    
    
    GET /_snapshot/my_repository/my_snapshot

###Request

"获取/_snapshot/<repository>/<snapshot>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"monitor_snapshot"、"create_snapshot"或"管理"集群权限才能使用此 API。

### 路径参数

`<repository>`

    

(必需，字符串)用于限制请求的快照存储库名称的逗号分隔列表。支持通配符 ('*') 表达式，包括将通配符与以 '-' 开头的排除模式组合在一起。

要获取有关集群中注册的所有快照存储库的信息，请省略此参数或使用"*"或"_all"。

`<snapshot>`

    

(必需，字符串)要检索的快照名称的逗号分隔列表。支持通配符 ('*') 表达式，包括将通配符与以 '-' 开头的排除模式组合在一起。

* 要获取有关已注册存储库中所有快照的信息，请使用通配符 ("*") 或"_all"。  * 要获取有关当前正在运行的任何快照的信息，请使用"_current"。

如果任何快照不可用，则在请求中使用"_all"将失败。将"ignore_unavailable"设置为"true"以仅返回可用的快照。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

`ignore_unavailable`

    

(可选，布尔值)如果为"false"，则请求将针对任何不可用的快照返回错误。默认为"假"。

如果为"true"，则请求将忽略不可用的快照，例如已损坏或暂时无法返回的快照。

`verbose`

     (Optional, Boolean) If `true`, returns additional information about each snapshot such as the version of Elasticsearch which took the snapshot, the start and end times of the snapshot, and the number of shards snapshotted. Defaults to `true`. If `false`, omits the additional information. 
`index_names`

     (Optional, Boolean) If `true`, returns the list of index names included in each snapshot in the response. Defaults to `true`. 
`index_details`

     (Optional, Boolean) If `true`, returns additional information about each index in the snapshot comprising the number of shards in the index, the total size of the index in bytes, and the maximum number of segments per shard in the index. Defaults to `false`, meaning that this information is omitted. 
`include_repository`

     (Optional, Boolean) If `true`, returns the repository name for each snapshot in the response. Defaults to `true`. 
`sort`

    

(可选，字符串)允许设置结果的排序顺序。默认为"start_time"，即按快照开始时间戳排序。

"排序"的有效值

`start_time`

     Sort snapshots by their start time stamp and break ties by snapshot name. 
`duration`

     Sort snapshots by their duration and break ties by snapshot name. 
`name`

     Sort snapshots by their name. 
`repository`

     Sort snapshots by their repository name and break ties by snapshot name. 
`index_count`

     Sort snapshots by the number of indices they contain and break ties by snapshot name. 
`shard_count`

     Sort snapshots by the number of shards they contain and break ties by snapshot name. 
`failed_shard_count`

     Sort snapshots by the number of shards that they failed to snapshot and break ties by snapshot name. 

`size`

     (Optional, integer) Maximum number of snapshots to return. Defaults to `0` which means return all that match the request without limit. 
`order`

     (Optional, string) Sort order. Valid values are `asc` for ascending and `desc` for descending order. Defaults to `asc`, meaning ascending order. 
`from_sort_value`

     (Optional, string) Value of the current sort column at which to start retrieval. Can either be a string snapshot- or repository name when sorting by snapshot or repository name, a millisecond time value or a number when sorting by index- or shard count. 
`after`

     (Optional, string) Offset identifier to start pagination from as returned by the `next` field in the response body. Using this parameter is mutually exclusive with using the `from_sort_value` parameter. 
`offset`

     (Optional, integer) Numeric offset to start pagination from based on the snapshots matching this request. Using a non-zero value for this parameter is mutually exclusive with using the `after` parameter. Defaults to `0`. 
`slm_policy_filter`

     (Optional, string) Filter snapshots by a comma-separated list of SLM policy names that snapshots belong to. Also accepts wildcards (`\*`) and combinations of wildcards followed by exclude patterns starting with `-`. For example, the pattern `*,-policy-a-\*` will return all snapshots except for those that were created by an SLM policy with a name starting with `policy-a-`. Note that the wildcard pattern `*` matches all snapshots created by an SLM policy but not those snapshots that were not created by an SLM policy. To include snapshots not created by an SLM policy you can use the special pattern `_none` that will match all snapshots without an SLM policy. 

"after"参数和"next"字段允许循环访问快照，并保证并发创建或删除快照的一致性。可以保证在迭代期间将看到迭代开始时存在且未同时删除的任何快照。在迭代期间可能会看到同时创建的快照。

使用 "verbose=false" 时，不支持参数 'size'、'order'、'after'、'from_sort_value'、'offset'、'slm_policy_filter' 和 'sort'，并且未定义带有 'verbose=false' 的请求的排序顺序。

### 响应正文

`snapshot`

     (string) Name of the snapshot. 
`uuid`

     (string) Universally unique identifier (UUID) of the snapshot. 
`version_id`

     (int) Build ID of the Elasticsearch version used to create the snapshot. 
`version`

     (float) Elasticsearch version used to create the snapshot. 
`indices`

     (array) List of indices included in the snapshot. 
`index_details`

    

(对象)快照中每个索引的详细信息，按索引名称键入。仅当设置了"？index_details"查询参数时才存在，并且仅包含在足够新的 Elasticsearch 版本中完全快照的索引的详细信息。

"index_details"的属性

`shard_count`

     (integer) Number of shards in this index. 
`size`

     (string) Total size of all shards in this index. Only present if the `?human` query paramter is set. 
`size_in_bytes`

     (long) Total size of all shards in this index, in bytes. 
`max_segments_per_shard`

     (integer) Maximum number of segments per shard in this index snapshot. 

`data_streams`

     (array of strings) List of [data streams](data-streams.html "Data streams") included in the snapshot. 
`include_global_state`

     (Boolean) Indicates whether the current cluster state is included in the snapshot. 

`feature_states`

    

(对象数组)快照中的功能状态。仅当快照包含一个或多个功能状态时才存在。

"features_states"对象的属性

`feature_name`

     (string) Name of the feature, as returned by the [get features API](get-features-api.html "Get Features API"). 
`indices`

     (array of strings) Indices in the feature state. 

`start_time`

     (string) Date timestamp of when the snapshot creation process started. 
`start_time_in_millis`

     (long) The time, in milliseconds, when the snapshot creation process started. 
`end_time`

     (string) Date timestamp of when the snapshot creation process ended. 
`end_time_in_millis`

     (long) The time, in milliseconds, when the snapshot creation process ended. 
`duration_in_millis`

     (long) How long, in milliseconds, it took to create the snapshot. 

`failures`

     (array) Lists any failures that occurred when creating the snapshot. 
`shards`

    

(对象)包含快照中的分片计数。

"分片"的属性

`total`

     (integer) Total number of shards included in the snapshot. 
`successful`

     (integer) Number of shards that were successfully included in the snapshot. 
`failed`

     (integer) Number of shards that failed to be included in the snapshot. 

`state`

    

(字符串)快照"状态"可以是以下值之一：

"状态"的值

`IN_PROGRESS`

     The snapshot is currently running. 
`SUCCESS`

     The snapshot finished and all shards were stored successfully. 
`FAILED`

     The snapshot finished with an error and failed to store any data. 
`PARTIAL`

     The global cluster state was stored, but data of at least one shard was not stored successfully. The [`failures`](get-snapshot-api.html#get-snapshot-api-response-failures) section of the response contains more detailed information about shards that were not processed correctly. 

`next`

     (string) If the request contained a size limit and there might be more results, a `next` field will be added to the response and can be used as the `after` query parameter to fetch additional results. 
`total`

     (integer) The total number of snapshots that match the request when ignoring size limit or `after` query parameter. 
`remaining`

     (integer) The number of remaining snapshots that were not returned due to size limits and that can be fetched by additional requests using the `next` field value. 

###Examples

以下请求返回"my_repository"存储库中"snapshot_2"的信息。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: 'snapshot_2'
    )
    puts response
    
    
    GET /_snapshot/my_repository/snapshot_2

API 返回以下响应：

    
    
    {
      "snapshots": [
        {
          "snapshot": "snapshot_2",
          "uuid": "vdRctLCxSketdKb54xw67g",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.129Z",
          "start_time_in_millis": 1593093628850,
          "end_time": "2020-07-06T21:55:18.129Z",
          "end_time_in_millis": 1593094752018,
          "duration_in_millis": 0,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        }
      ],
      "total": 1,
      "remaining": 0
    }

以下请求返回"my_repository"存储库中前缀为"snapshot"的所有快照的信息，将响应大小限制为 2 并按快照名称排序。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: 'snapshot*',
      size: 2,
      sort: 'name'
    )
    puts response
    
    
    GET /_snapshot/my_repository/snapshot*?size=2&sort=name

API 返回以下响应：

    
    
    {
      "snapshots": [
        {
          "snapshot": "snapshot_1",
          "uuid": "dKb54xw67gvdRctLCxSket",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.129Z",
          "start_time_in_millis": 1593093628850,
          "end_time": "2020-07-06T21:55:18.129Z",
          "end_time_in_millis": 1593094752018,
          "duration_in_millis": 0,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        },
        {
          "snapshot": "snapshot_2",
          "uuid": "vdRctLCxSketdKb54xw67g",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.130Z",
          "start_time_in_millis": 1593093628851,
          "end_time": "2020-07-06T21:55:18.130Z",
          "end_time_in_millis": 1593094752019,
          "duration_in_millis": 1,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        }
      ],
      "next": "c25hcHNob3RfMixteV9yZXBvc2l0b3J5LHNuYXBzaG90XzI=",
      "total": 3,
      "remaining": 1
    }

然后，可以使用上一个响应中的"next"值作为"after"参数对剩余快照的后续请求。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: 'snapshot*',
      size: 2,
      sort: 'name',
      after: 'c25hcHNob3RfMixteV9yZXBvc2l0b3J5LHNuYXBzaG90XzI='
    )
    puts response
    
    
    GET /_snapshot/my_repository/snapshot*?size=2&sort=name&after=c25hcHNob3RfMixteV9yZXBvc2l0b3J5LHNuYXBzaG90XzI=

API 返回以下响应：

    
    
    {
      "snapshots": [
        {
          "snapshot": "snapshot_3",
          "uuid": "dRctdKb54xw67gvLCxSket",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.129Z",
          "start_time_in_millis": 1593093628850,
          "end_time": "2020-07-06T21:55:18.129Z",
          "end_time_in_millis": 1593094752018,
          "duration_in_millis": 0,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        }
      ],
      "total": 3,
      "remaining": 0
    }

或者，可以通过使用偏移值"2"跳过已看到的两个快照来检索相同的结果。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: 'snapshot*',
      size: 2,
      sort: 'name',
      offset: 2
    )
    puts response
    
    
    GET /_snapshot/my_repository/snapshot*?size=2&sort=name&offset=2

API 返回以下响应：

    
    
    {
      "snapshots": [
        {
          "snapshot": "snapshot_3",
          "uuid": "dRctdKb54xw67gvLCxSket",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.129Z",
          "start_time_in_millis": 1593093628850,
          "end_time": "2020-07-06T21:55:18.129Z",
          "end_time_in_millis": 1593094752018,
          "duration_in_millis": 0,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        }
      ],
      "total": 3,
      "remaining": 0
    }

以下请求返回"my_repository"存储库中前缀为"snapshot"的所有快照的信息，但名为"snapshot_3"的快照除外

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: 'snapshot*,-snapshot_3',
      sort: 'name'
    )
    puts response
    
    
    GET /_snapshot/my_repository/snapshot*,-snapshot_3?sort=name

API 返回以下响应：

    
    
    {
      "snapshots": [
        {
          "snapshot": "snapshot_1",
          "uuid": "dKb54xw67gvdRctLCxSket",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.129Z",
          "start_time_in_millis": 1593093628850,
          "end_time": "2020-07-06T21:55:18.129Z",
          "end_time_in_millis": 1593094752018,
          "duration_in_millis": 0,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        },
        {
          "snapshot": "snapshot_2",
          "uuid": "vdRctLCxSketdKb54xw67g",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.130Z",
          "start_time_in_millis": 1593093628851,
          "end_time": "2020-07-06T21:55:18.130Z",
          "end_time_in_millis": 1593094752019,
          "duration_in_millis": 1,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        }
      ],
      "total": 2,
      "remaining": 0
    }

以下请求返回按默认升序按快照名称排序时"snapshot_2"之后的所有快照的信息。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: '*',
      sort: 'name',
      from_sort_value: 'snapshot_2'
    )
    puts response
    
    
    GET /_snapshot/my_repository/*?sort=name&from_sort_value=snapshot_2

API 返回以下响应：

    
    
    {
      "snapshots": [
        {
          "snapshot": "snapshot_2",
          "uuid": "vdRctLCxSketdKb54xw67g",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.130Z",
          "start_time_in_millis": 1593093628851,
          "end_time": "2020-07-06T21:55:18.130Z",
          "end_time_in_millis": 1593094752019,
          "duration_in_millis": 1,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        },
        {
          "snapshot": "snapshot_3",
          "uuid": "dRctdKb54xw67gvLCxSket",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.129Z",
          "start_time_in_millis": 1593093628850,
          "end_time": "2020-07-06T21:55:18.129Z",
          "end_time_in_millis": 1593094752018,
          "duration_in_millis": 0,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        }
      ],
      "total": 2,
      "remaining": 0
    }

以下请求返回名称以"snapshot_"开头且在时间戳"1577833200000"(2020 年 1 月 1 日)当天或之后开始的所有快照的信息，当按快照开始时间按默认升序排序时。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: 'snapshot_*',
      sort: 'start_time',
      from_sort_value: 1_577_833_200_000
    )
    puts response
    
    
    GET /_snapshot/my_repository/snapshot_*?sort=start_time&from_sort_value=1577833200000

API 返回以下响应：

    
    
    {
      "snapshots": [
        {
          "snapshot": "snapshot_1",
          "uuid": "dKb54xw67gvdRctLCxSket",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.128Z",
          "start_time_in_millis": 1593093628849,
          "end_time": "2020-07-06T21:55:18.129Z",
          "end_time_in_millis": 1593093628850,
          "duration_in_millis": 1,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        },
        {
          "snapshot": "snapshot_2",
          "uuid": "vdRctLCxSketdKb54xw67g",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.130Z",
          "start_time_in_millis": 1593093628851,
          "end_time": "2020-07-06T21:55:18.130Z",
          "end_time_in_millis": 1593093628851,
          "duration_in_millis": 0,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        },
        {
          "snapshot": "snapshot_3",
          "uuid": "dRctdKb54xw67gvLCxSket",
          "repository": "my_repository",
          "version_id": <version_id>,
          "version": <version>,
          "indices": [],
          "data_streams": [],
          "feature_states": [],
          "include_global_state": true,
          "state": "SUCCESS",
          "start_time": "2020-07-06T21:55:18.131Z",
          "start_time_in_millis": 1593093628852,
          "end_time": "2020-07-06T21:55:18.135Z",
          "end_time_in_millis": 1593093628856,
          "duration_in_millis": 4,
          "failures": [],
          "shards": {
            "total": 0,
            "failed": 0,
            "successful": 0
          }
        }
      ],
      "total": 3,
      "remaining": 0
    }

[« Create snapshot API](create-snapshot-api.md) [Get snapshot status API
»](get-snapshot-status-api.md)
