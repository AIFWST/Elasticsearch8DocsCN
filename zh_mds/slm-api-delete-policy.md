

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot lifecycle management APIs](snapshot-
lifecycle-management-api.md)

[« Get snapshot lifecycle policy API](slm-api-get-policy.md) [Execute
snapshot lifecycle policy API »](slm-api-execute-lifecycle.md)

## 删除快照生命周期策略API

删除现有的快照生命周期策略。

###Request

"删除/_slm/策略/<snapshot-lifecycle-policy-id>"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"manage_slm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

删除指定的生命周期策略定义。这可以防止将来拍摄任何快照，但不会取消正在进行的快照或删除以前拍摄的快照。

### 路径参数

`<policy-id>`

     (Required, string) ID of the snapshot lifecycle policy to delete. 

###Examples

    
    
    response = client.slm.delete_lifecycle(
      policy_id: 'daily-snapshots'
    )
    puts response
    
    
    DELETE /_slm/policy/daily-snapshots

[« Get snapshot lifecycle policy API](slm-api-get-policy.md) [Execute
snapshot lifecycle policy API »](slm-api-execute-lifecycle.md)
