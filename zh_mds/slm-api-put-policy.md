

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot lifecycle management APIs](snapshot-
lifecycle-management-api.md)

[« Snapshot lifecycle management APIs](snapshot-lifecycle-management-api.md)
[Get snapshot lifecycle policy API »](slm-api-get-policy.md)

## 创建或更新快照生命周期策略API

创建或更新快照生命周期策略。

###Request

'放置/_slm/策略/<snapshot-lifecycle-policy-id>"

###Prerequisites

如果启用了 Elasticsearch 安全功能，则任何包含的索引都必须具有"manage_slm"集群权限和"管理"索引权限才能使用此 API。有关更多信息，请参阅安全权限。

###Description

使用创建或更新快照生命周期策略 API 创建或更新快照生命周期策略。

如果策略已存在，则此请求将递增策略的版本。仅存储策略的最新版本。

### 路径参数

`<snapshot-lifecycle-policy-id>`

     (Required, string) ID for the snapshot lifecycle policy you want to create or update. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`config`

    

(必填，对象)策略创建的每个快照的配置。

"配置"的属性

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

`name`

     (Required, string) Name automatically assigned to each snapshot created by the policy. [Date math](api-conventions.html#api-date-math-index-names "Date math support in index and index alias names") is supported. To prevent conflicting snapshot names, a UUID is automatically appended to each snapshot name. 
`repository`

     (Required, string) Repository used to store snapshots created by this policy. This repository must exist prior to the policy's creation. You can create a repository using the [snapshot repository API](snapshot-restore.html "Snapshot and restore"). 

`retention`

    

(可选，对象)用于保留和删除策略创建的快照的保留规则。

"保留"的属性

`expire_after`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Time period after which a snapshot is considered expired and eligible for deletion. SLM deletes expired snapshots based on the [`slm.retention_schedule`](snapshot-settings.html#slm-retention-schedule). 
`max_count`

     (Optional, integer) Maximum number of snapshots to retain, even if the snapshots have not yet expired. If the number of snapshots in the repository exceeds this limit, the policy retains the most recent snapshots and deletes older snapshots. This limit only includes snapshots with a [`state`](get-snapshot-api.html#get-snapshot-api-response-state) of `SUCCESS`. 
`min_count`

     (Optional, integer) Minimum number of snapshots to retain, even if the snapshots have expired. 

`schedule`

     (Required, [Cron syntax](api-conventions.html#api-cron-expressions "Cron expressions")) Periodic or absolute schedule at which the policy creates snapshots. SLM applies `schedule` changes immediately. 

###Examples

创建"每日快照"生命周期策略：

    
    
    PUT /_slm/policy/daily-snapshots
    {
      "schedule": "0 30 1 * * ?", __"name": " <daily-snap-{now/d}>", __"repository": "my_repository", __"config": { __"indices": ["data-*", "important"], __"ignore_unavailable": false,
        "include_global_state": false
      },
      "retention": { __"expire_after": "30d", __"min_count": 5, __"max_count": 50 __}
    }

__

|

何时应拍摄快照，在本例中为每天凌晨 1：30 ---|--- __

|

每个快照的名称应指定 __

|

要在 __ 中拍摄快照的存储库

|

任何额外的快照配置 __

|

快照应包含的数据流和索引 __

|

可选保留配置 __

|

将快照保留 30 天 __

|

始终保留至少 5 个成功的快照，即使它们已超过 30 天 __

|

保留不超过 50 个成功的快照，即使它们不到 30 天 « 快照生命周期管理 API 获取快照生命周期策略 API »