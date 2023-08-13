

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot lifecycle management APIs](snapshot-
lifecycle-management-api.md)

[« Create or update snapshot lifecycle policy API](slm-api-put-policy.md)
[Delete snapshot lifecycle policy API »](slm-api-delete-policy.md)

## 获取快照生命周期策略API

检索一个或多个快照生命周期策略定义以及有关最新快照尝试的信息。

###Request

"获取_slm/策略/<policy-id>"

"获取_slm/策略"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"manage_slm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

返回指定的策略定义以及有关最近成功和失败的快照创建尝试的信息。如果未指定策略，则返回所有定义的策略。

### 路径参数

`<policy-id>`

     (Optional, string) Comma-separated list of snapshot lifecycle policy IDs. 

###Examples

#### 获取特定策略

获取"每日快照"策略：

    
    
    response = client.slm.get_lifecycle(
      policy_id: 'daily-snapshots',
      human: true
    )
    puts response
    
    
    GET _slm/policy/daily-snapshots?human

此请求返回以下响应：

    
    
    {
      "daily-snapshots": {
        "version": 1,                                 __"modified_date": "2099-05-06T01:30:00.000Z", __"modified_date_millis": 4081757400000,
        "policy" : {
          "schedule": "0 30 1 * * ?",
          "name": " <daily-snap-{now/d}>",
          "repository": "my_repository",
          "config": {
            "indices": ["data-*", "important"],
            "ignore_unavailable": false,
            "include_global_state": false
          },
          "retention": {
            "expire_after": "30d",
            "min_count": 5,
            "max_count": 50
          }
        },
        "stats": {
          "policy": "daily-snapshots",
          "snapshots_taken": 0,
          "snapshots_failed": 0,
          "snapshots_deleted": 0,
          "snapshot_deletion_failures": 0
        },
        "next_execution": "2099-05-07T01:30:00.000Z", __"next_execution_millis": 4081843800000
      }
    }

__

|

快照策略的版本，仅存储最新版本，并在更新策略时递增 ---|--- __

|

上次修改此策略的时间。   __

|

下次执行此策略时。   #### 获取所有策略编辑

    
    
    response = client.slm.get_lifecycle
    puts response
    
    
    GET _slm/policy

[« Create or update snapshot lifecycle policy API](slm-api-put-policy.md)
[Delete snapshot lifecycle policy API »](slm-api-delete-policy.md)
