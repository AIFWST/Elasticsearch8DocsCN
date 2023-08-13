

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot lifecycle management APIs](snapshot-
lifecycle-management-api.md)

[« Execute snapshot lifecycle policy API](slm-api-execute-lifecycle.md) [Get
snapshot lifecycle management status API »](slm-api-get-status.md)

## 执行快照保留策略API

根据策略的保留规则删除过期的任何快照。

###Request

"发布/_slm/_execute_retention"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"manage_slm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

手动应用保留策略以强制立即删除过期的快照。保留策略通常根据其计划应用。

###Examples

要强制删除过期快照，请执行以下操作：

    
    
    response = client.slm.execute_retention
    puts response
    
    
    POST /_slm/_execute_retention

保留在后台异步运行。

[« Execute snapshot lifecycle policy API](slm-api-execute-lifecycle.md) [Get
snapshot lifecycle management status API »](slm-api-get-status.md)
