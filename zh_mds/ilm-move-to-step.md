

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Delete lifecycle policy API](ilm-delete-lifecycle.md) [Remove policy from
index API »](ilm-remove-policy.md)

## 移动到生命周期步骤API

触发生命周期策略中特定步骤的执行。

###Request

"发布_ilm/移动/<index>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对所管理的索引具有"manage_ilm"权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

此操作可能会导致数据丢失。手动将索引移动到特定步骤中会执行该步骤，即使该步骤已执行。这是一个潜在的破坏性操作，应将其视为专家级 API。

手动将索引移动到指定步骤并执行该步骤。您必须在请求正文中指定当前步骤和要执行的步骤。

如果当前步骤与当前为索引执行的步骤不匹配，则请求将失败。这是为了防止索引从意外步骤移动到下一步。

指定索引将移动到的目标("next_step")时，"名称"或"操作"和"名称"字段都是可选的。如果仅指定了阶段，则索引将移动到目标阶段中第一个操作的第一步。如果指定了阶段和操作，则索引将移动到指定阶段中指定操作的第一步。只有在 ILM 策略中指定的操作才被视为有效，索引不能移动到不属于其策略的步骤。

### 路径参数

`<index>`

     (Required, string) Identifier for the index. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`current_step`

    

(必填，对象)

"current_step"的属性

`phase`

     (Required, string) The name of the current phase. Must match the phase as returned by the [explain](ilm-explain-lifecycle.html "Explain lifecycle API") API. 
`action`

     (Required, string) The name of the current action. Must match the action as returned by the [explain](ilm-explain-lifecycle.html "Explain lifecycle API") API. 
`name`

     (Required, string) The name of the current step. Must match the step as returned by the [explain](ilm-explain-lifecycle.html "Explain lifecycle API") API. If ILM encounters a problem while performing an action, it halts execution of the policy and transitions to the `ERROR` step. If you are trying to advance a policy after troubleshooting a failure, you specify this `ERROR` step as the current step. For more information, see [ILM error handling](index-lifecycle-error-handling.html "Troubleshooting index lifecycle management errors"). 

`next_step`

    

(必填，对象)

"next_step"的属性

`phase`

     (Required, string) The name of the phase that contains the action you want to perform or resume. 
`action`

     (Optional, string) The name action you want to perform or resume. Required if `name` used. 
`name`

     (Optional, string) The name of the step to move to and execute. Required if `action` used. 

###Examples

下面的示例将"my-index-000001"从初始步骤移动到"强制合并"步骤：

    
    
    POST _ilm/move/my-index-000001
    {
      "current_step": { __"phase": "new",
        "action": "complete",
        "name": "complete"
      },
      "next_step": { __"phase": "warm",
        "action": "forcemerge", __"name": "forcemerge" __}
    }

__

|

索引预计在 ---|--- __ 中的步骤

|

要执行的步骤 __

|

索引将移动到的可选操作 __

|

索引将移动到的可选步骤名称 如果请求成功，您将收到以下结果：

    
    
    {
      "acknowledged": true
    }

如果索引未处于"current_step"指定的"新建"阶段，则请求将失败。

以下示例将"my-index-000001"从热相的末尾推送到暖相的开始：

    
    
    POST _ilm/move/my-index-000001
    {
      "current_step": {
        "phase": "hot",
        "action": "complete",
        "name": "complete"
      },
      "next_step": {
        "phase": "warm"
      }
    }

[« Delete lifecycle policy API](ilm-delete-lifecycle.md) [Remove policy from
index API »](ilm-remove-policy.md)
