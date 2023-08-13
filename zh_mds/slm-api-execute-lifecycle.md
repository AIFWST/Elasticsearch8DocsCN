

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot lifecycle management APIs](snapshot-
lifecycle-management-api.md)

[« Delete snapshot lifecycle policy API](slm-api-delete-policy.md) [Execute
snapshot retention policy API »](slm-api-execute-retention.md)

## 执行快照生命周期策略API

根据生命周期策略立即创建快照，无需等待计划时间。

###Request

"放置/_slm/策略/<snapshot-lifecycle-policy-id>/_execute"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"manage_slm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

手动应用快照策略以立即创建快照。快照策略通常根据其计划应用，但您可能希望在执行升级或其他维护之前手动执行策略。

### 路径参数

`<policy-id>`

     (Required, string) ID of the snapshot lifecycle policy to execute. 

###Examples

要根据"每日快照"策略拍摄即时快照，请执行以下操作：

    
    
    POST /_slm/policy/daily-snapshots/_execute

如果成功，此请求将返回生成的快照名称：

    
    
    {
      "snapshot_name": "daily-snap-2019.04.24-gwrqoo2xtea3q57vvg0uea"
    }

快照在后台拍摄。您可以使用快照 API 监控快照的状态。

要查看策略最新快照的状态，您可以使用 getsnapshot 生命周期策略 API。

[« Delete snapshot lifecycle policy API](slm-api-delete-policy.md) [Execute
snapshot retention policy API »](slm-api-execute-retention.md)
