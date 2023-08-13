

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Create or update lifecycle policy API](ilm-put-lifecycle.md) [Delete
lifecycle policy API »](ilm-delete-lifecycle.md)

## 获取生命周期策略接口

检索生命周期策略。

###Request

"获取_ilm/策略"

"获取_ilm/策略/<policy_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_ilm"或"read_ilm"或同时具有这两种集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

返回指定的策略定义。包括策略版本和上次修改日期。如果未指定策略，则返回所有定义的策略。

### 路径参数

`<policy_id>`

     (Optional, string) Identifier for the policy. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

以下示例检索"my_policy"：

    
    
    response = client.ilm.get_lifecycle(
      policy: 'my_policy'
    )
    puts response
    
    
    GET _ilm/policy/my_policy

如果请求成功，则响应正文包含策略定义：

    
    
    {
      "my_policy": {
        "version": 1, __"modified_date": 82392349, __"policy": {
          "phases": {
            "warm": {
              "min_age": "10d",
              "actions": {
                "forcemerge": {
                  "max_num_segments": 1
                }
              }
            },
            "delete": {
              "min_age": "30d",
              "actions": {
                "delete": {
                  "delete_searchable_snapshot": true
                }
              }
            }
          }
        },
        "in_use_by" : { __"indices" : [],
          "data_streams" : [],
          "composable_templates" : []
        }
      }
    }

__

|

每当策略更新时，策略版本都会递增 ---|--- __

|

上次修改此策略的时间 __

|

哪些索引、数据流或模板当前使用此策略 « 创建或更新生命周期策略 API 删除生命周期策略 API »