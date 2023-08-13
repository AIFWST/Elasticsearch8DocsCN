

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Get lifecycle policy API](ilm-get-lifecycle.md) [Move to lifecycle step
API »](ilm-move-to-step.md)

## 删除生命周期策略接口

删除索引生命周期策略。

###Request

"删除_ilm/策略/<policy_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_ilm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

删除指定的生命周期策略定义。您无法删除当前正在使用的策略。如果策略用于管理任何索引，则请求失败并返回错误。

### 路径参数

`<policy_id>`

     (Required, string) Identifier for the policy. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

以下示例删除"my_policy"：

    
    
    response = client.ilm.delete_lifecycle(
      policy: 'my_policy'
    )
    puts response
    
    
    DELETE _ilm/policy/my_policy

成功删除策略后，您会收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Get lifecycle policy API](ilm-get-lifecycle.md) [Move to lifecycle step
API »](ilm-move-to-step.md)
