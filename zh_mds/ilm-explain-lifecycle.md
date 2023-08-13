

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Get index lifecycle management status API](ilm-get-status.md) [Start
index lifecycle management API »](ilm-start.md)

## 解释生命周期接口

检索一个或多个索引的当前生命周期状态。对于数据流，API 检索流的支持索引的当前生命周期状态。

###Request

"获取<target>/_ilm/解释"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对所管理的索引具有"view_index_metadata"或"manage_ilm"或两者兼而有之的权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

检索有关索引的当前生命周期状态的信息，例如当前执行的阶段、操作和步骤。显示索引进入每个索引的时间、运行阶段的定义以及有关任何故障的信息。

### 路径参数

`<target>`

     (Required, string) Comma-separated list of data streams, indices, and aliases to target. Supports wildcards (`*`).To target all data streams and indices, use `*` or `_all`. 

### 查询参数

`only_managed`

     (Optional, Boolean) Filters the returned indices to only indices that are managed by ILM. 
`only_errors`

     (Optional, Boolean) Filters the returned indices to only indices that are managed by ILM and are in an error state, either due to an encountering an error while executing the policy, or attempting to use a policy that does not exist. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

以下示例检索"my-index-000001"的生命周期状态：

    
    
    response = client.ilm.explain_lifecycle(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET my-index-000001/_ilm/explain

当 ILM 首次接管索引的管理时，"解释"表示索引已管理并处于"新"阶段：

    
    
    {
      "indices": {
        "my-index-000001": {
          "index": "my-index-000001",
          "index_creation_date_millis": 1538475653281,  __"time_since_index_creation": "15s", __"managed": true, __"policy": "my_policy", __"lifecycle_date_millis": 1538475653281, __"age": "15s", __"phase": "new",
          "phase_time_millis": 1538475653317, __"action": "complete"
          "action_time_millis": 1538475653317, __"step": "complete",
          "step_time_millis": 1538475653317 __}
      }
    }

__

|

创建索引时，此时间戳用于确定何时滚动更新---|--- __

|

自创建索引以来的时间(用于计算何时通过"max_age"滚动更新索引)__

|

显示索引是否由 ILM 管理。如果索引不是由 ILM 管理的，则不会显示其他字段 __

|

ILM 用于此索引的策略的名称 __

|

用于"min_age"__ 的时间戳

|

指数的年龄(用于计算何时进入下一阶段)__

|

当指数进入当前阶段__

|

当索引进入当前操作 __

|

当索引进入当前步骤时 在索引上运行策略后，响应将包括显示当前阶段定义的"phase_execution"对象。在当前阶段完成之前，对基础策略的更改不会影响此索引。

    
    
    {
      "indices": {
        "test-000069": {
          "index": "test-000069",
          "index_creation_date_millis": 1538475653281,
          "time_since_index_creation": "25.14s",
          "managed": true,
          "policy": "my_lifecycle3",
          "lifecycle_date_millis": 1538475653281,
          "lifecycle_date": "2018-10-15T13:45:21.981Z",
          "age": "25.14s",
          "phase": "hot",
          "phase_time_millis": 1538475653317,
          "phase_time": "2018-10-15T13:45:22.577Z",
          "action": "rollover",
          "action_time_millis": 1538475653317,
          "action_time": "2018-10-15T13:45:22.577Z",
          "step": "attempt-rollover",
          "step_time_millis": 1538475653317,
          "step_time": "2018-10-15T13:45:22.577Z",
          "phase_execution": {
            "policy": "my_lifecycle3",
            "phase_definition": { __"min_age": "0ms",
              "actions": {
                "rollover": {
                  "max_age": "30s"
                }
              }
            },
            "version": 3, __"modified_date": "2018-10-15T13:21:41.576Z", __"modified_date_in_millis": 1539609701576 __}
        }
      }
    }

__

|

索引进入此阶段时从指定策略加载的 JSON 阶段定义 ---|--- __

|

加载的策略的版本 __

|

上次修改加载的策略的日期 __

|

上次修改加载的策略的纪元时间 如果 ILM 正在等待某个步骤完成，则响应将包括正在对索引执行的步骤的状态信息。

    
    
    {
      "indices": {
        "test-000020": {
          "index": "test-000020",
          "index_creation_date_millis": 1538475653281,
          "time_since_index_creation": "4.12m",
          "managed": true,
          "policy": "my_lifecycle3",
          "lifecycle_date_millis": 1538475653281,
          "lifecycle_date": "2018-10-15T13:45:21.981Z",
          "age": "4.12m",
          "phase": "warm",
          "phase_time_millis": 1538475653317,
          "phase_time": "2018-10-15T13:45:22.577Z",
          "action": "allocate",
          "action_time_millis": 1538475653317,
          "action_time": "2018-10-15T13:45:22.577Z",
          "step": "check-allocation",
          "step_time_millis": 1538475653317,
          "step_time": "2018-10-15T13:45:22.577Z",
          "step_info": { __"message": "Waiting for all shard copies to be active",
            "shards_left_to_allocate": -1,
            "all_shards_active": false,
            "number_of_replicas": 2
          },
          "phase_execution": {
            "policy": "my_lifecycle3",
            "phase_definition": {
              "min_age": "0ms",
              "actions": {
                "allocate": {
                  "number_of_replicas": 2,
                  "include": {
                    "box_type": "warm"
                  },
                  "exclude": {},
                  "require": {}
                },
                "forcemerge": {
                  "max_num_segments": 1
                }
              }
            },
            "version": 2,
            "modified_date": "2018-10-15T13:20:02.489Z",
            "modified_date_in_millis": 1539609602489
          }
        }
      }
    }

__

|

正在进行的步骤的状态。   ---|--- 如果索引位于 ERROR 步骤中，则在执行策略中的步骤时出现问题，您需要采取措施使索引继续执行下一步。在某些情况下，某些步骤可以安全地自动重试。为了帮助您诊断问题，解释响应显示失败的步骤、提供有关错误信息的步骤信息，以及有关为失败步骤执行的重试尝试的信息(如果是这种情况)。

    
    
    {
      "indices": {
        "test-000056": {
          "index": "test-000056",
          "index_creation_date_millis": 1538475653281,
          "time_since_index_creation": "50.1d",
          "managed": true,
          "policy": "my_lifecycle3",
          "lifecycle_date_millis": 1538475653281,
          "lifecycle_date": "2018-10-15T13:45:21.981Z",
          "age": "50.1d",
          "phase": "hot",
          "phase_time_millis": 1538475653317,
          "phase_time": "2018-10-15T13:45:22.577Z",
          "action": "rollover",
          "action_time_millis": 1538475653317,
          "action_time": "2018-10-15T13:45:22.577Z",
          "step": "ERROR",
          "step_time_millis": 1538475653317,
          "step_time": "2018-10-15T13:45:22.577Z",
          "failed_step": "check-rollover-ready", __"is_auto_retryable_error": true, __"failed_step_retry_count": 1, __"step_info": { __"type": "cluster_block_exception",
            "reason": "index [test-000057/H7lF9n36Rzqa-KfKcnGQMg] blocked by: [FORBIDDEN/5/index read-only (api)",
            "index_uuid": "H7lF9n36Rzqa-KfKcnGQMg",
            "index": "test-000057"
          },
          "phase_execution": {
            "policy": "my_lifecycle3",
            "phase_definition": {
              "min_age": "0ms",
              "actions": {
                "rollover": {
                  "max_age": "30s"
                }
              }
            },
            "version": 3,
            "modified_date": "2018-10-15T13:21:41.576Z",
            "modified_date_in_millis": 1539609701576
          }
        }
      }
    }

__

|

导致错误的步骤 ---|--- __

|

指示重试失败的步骤是否可以克服错误。如果为真，ILM 将自动重试失败的步骤。   __

|

显示尝试自动重试以执行失败步骤的次数。   __

|

出了什么问题 « 获取索引生命周期管理状态 API 启动索引生命周期管理 API »