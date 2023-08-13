

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Index lifecycle management APIs](index-lifecycle-management-api.md) [Get
lifecycle policy API »](ilm-get-lifecycle.md)

## 创建或更新生命周期策略API

创建或更新生命周期策略。有关策略组件的定义，请参阅索引生命周期。

###Request

"放_ilm/策略/<policy_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_ilm"集群权限才能使用此 API。您还必须对由"策略"管理的所有索引具有"管理"索引权限。ILM 以上次更新策略的用户身份执行操作。ILM 仅在上次策略更新时分配给用户的角色。

###Description

创建生命周期策略。如果指定的策略存在，则会替换该策略并递增策略版本。

仅存储策略的最新版本，无法还原到以前的版本。

### 路径参数

`<policy_id>`

     (Required, string) Identifier for the policy. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

以下示例创建一个名为"my_policy"的新策略。此外，您可以使用"_meta"参数向策略添加任意元数据，"_meta"参数是可选的，不会由Elasticsearch自动生成或使用。要取消设置"_meta"，请替换策略而不指定策略。要检查"_meta"，您可以使用获取生命周期策略 API。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          _meta: {
            description: 'used for nginx log',
            project: {
              name: 'myProject',
              department: 'myDepartment'
            }
          },
          phases: {
            warm: {
              min_age: '10d',
              actions: {
                forcemerge: {
                  max_num_segments: 1
                }
              }
            },
            delete: {
              min_age: '30d',
              actions: {
                delete: {}
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "_meta": {
          "description": "used for nginx log",
          "project": {
            "name": "myProject",
            "department": "myDepartment"
          }
        },
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
              "delete": {}
            }
          }
        }
      }
    }

如果请求成功，您将收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Index lifecycle management APIs](index-lifecycle-management-api.md) [Get
lifecycle policy API »](ilm-get-lifecycle.md)
