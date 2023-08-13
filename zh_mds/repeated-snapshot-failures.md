

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Multiple deployments writing to the same snapshot repository](add-
repository.md) [Troubleshooting discovery »](discovery-troubleshooting.md)

## 解决重复的快照策略失败问题

重复的快照失败通常表示部署存在问题。自动快照的持续故障可能会使部署在数据丢失或中断的情况下没有恢复选项。

Elasticsearch 在执行自动快照时跟踪重复失败的次数。如果自动快照失败的次数过多而未成功执行，运行状况 API 将报告警告。报告警告之前的重复失败次数由"slm.health.failed_snapshot_warn_threshold"设置控制。

如果自动快照生命周期管理策略执行反复失败，请按照以下步骤获取有关问题的详细信息：

弹性搜索服务 自我管理

为了检查失败的快照生命周期管理策略的状态我们需要转到 Kibana 并检索快照生命周期策略信息。

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 检索快照生命周期管理策略：获取_slm/策略/<affected-policy-name>

响应将如下所示：

    
        {
      "affected-policy-name": { __"version": 1,
        "modified_date": "2099-05-06T01:30:00.000Z",
        "modified_date_millis": 4081757400000,
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
        "last_success" : {
          "snapshot_name" : "daily-snap-2099.05.30-tme_ivjqswgkpryvnao2lg",
          "start_time" : 4083782400000,
          "time" : 4083782400000
        },
        "last_failure" : { __"snapshot_name" : "daily-snap-2099.06.16-ywe-kgh5rfqfrpnchvsujq",
          "time" : 4085251200000, __"details" : """{"type":"snapshot_exception","reason":"[daily-snap-2099.06.16-ywe-kgh5rfqfrpnchvsujq] failed to create snapshot successfully, 5 out of 149 total shards failed"}""" __},
        "stats": {
          "policy": "daily-snapshots",
          "snapshots_taken": 0,
          "snapshots_failed": 0,
          "snapshots_deleted": 0,
          "snapshot_deletion_failures": 0
        },
        "next_execution": "2099-06-17T01:30:00.000Z",
        "next_execution_millis": 4085343000000
      }
    }

__

|

受影响的快照生命周期策略。   ---|---    __

|

有关策略上次失败的信息。   __

|

发生故障的时间(以毫秒为单位)。使用"human=true"请求参数查看格式化的时间戳。   __

|

包含快照失败原因的错误详细信息。   快照可能由于各种原因而失败。如果失败是由于配置错误造成的，请参阅自动快照正在使用的存储库的文档。如果您使用的是此类部署，请参阅有关在ECE中管理存储库的指南。

一种常见的故障情况是存储库损坏。当多个 Elasticsearch 实例写入同一存储库位置时，最常发生这种情况。有一个单独的故障排除指南可以解决此问题。

如果快照由于其他原因而失败，请在快照执行期间检查所选主节点上的日志以获取更多信息。

检索快照生命周期管理策略：

    
    
    GET _slm/policy/<affected-policy-name>

响应将如下所示：

    
    
    {
      "affected-policy-name": { __"version": 1,
        "modified_date": "2099-05-06T01:30:00.000Z",
        "modified_date_millis": 4081757400000,
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
        "last_success" : {
          "snapshot_name" : "daily-snap-2099.05.30-tme_ivjqswgkpryvnao2lg",
          "start_time" : 4083782400000,
          "time" : 4083782400000
        },
        "last_failure" : { __"snapshot_name" : "daily-snap-2099.06.16-ywe-kgh5rfqfrpnchvsujq",
          "time" : 4085251200000, __"details" : """{"type":"snapshot_exception","reason":"[daily-snap-2099.06.16-ywe-kgh5rfqfrpnchvsujq] failed to create snapshot successfully, 5 out of 149 total shards failed"}""" __},
        "stats": {
          "policy": "daily-snapshots",
          "snapshots_taken": 0,
          "snapshots_failed": 0,
          "snapshots_deleted": 0,
          "snapshot_deletion_failures": 0
        },
        "next_execution": "2099-06-17T01:30:00.000Z",
        "next_execution_millis": 4085343000000
      }
    }

__

|

受影响的快照生命周期策略。   ---|---    __

|

有关策略上次失败的信息。   __

|

发生故障的时间(以毫秒为单位)。使用"human=true"请求参数查看格式化的时间戳。   __

|

包含快照失败原因的错误详细信息。   快照可能由于各种原因而失败。如果失败是由于配置错误造成的，请参阅自动快照正在使用的存储库的文档。

一种常见的故障情况是存储库损坏。当多个 Elasticsearch 实例写入同一存储库位置时，最常发生这种情况。有一个单独的故障排除指南可以解决此问题。

如果快照由于其他原因而失败，请在快照执行期间检查所选主节点上的日志以获取更多信息。

[« Multiple deployments writing to the same snapshot repository](add-
repository.md) [Troubleshooting discovery »](discovery-troubleshooting.md)
