

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot lifecycle management APIs](snapshot-
lifecycle-management-api.md)

[« Start snapshot lifecycle management API](slm-api-start.md) [SQL APIs
»](sql-apis.md)

## 停止快照生命周期管理API

关闭快照生命周期管理 (SLM)。

###Request

"开机自检/_slm/停止"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"manage_slm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

停止所有快照生命周期管理 (SLM) 操作并停止 SLM插件。当您在集群上执行维护并且需要阻止 SLM 对数据流或索引执行任何操作时，这非常有用。停止 SLM 不会停止正在进行的任何快照。即使 SLM 已停止，您也可以使用执行快照生命周期策略手动触发快照。

API 会在请求被确认后立即返回响应，但插件可能会继续运行，直到正在进行的操作完成并且可以安全地停止。

使用获取快照生命周期管理状态查看 SLM 是否正在运行。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

    
    
    POST _slm/stop

[« Start snapshot lifecycle management API](slm-api-start.md) [SQL APIs
»](sql-apis.md)
