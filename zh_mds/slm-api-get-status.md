

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot lifecycle management APIs](snapshot-
lifecycle-management-api.md)

[« Execute snapshot retention policy API](slm-api-execute-retention.md) [Get
snapshot lifecycle stats API »](slm-api-get-stats.md)

## 获取快照生命周期管理状态API

检索快照生命周期管理 (SLM) 的状态。

###Request

"获取/_slm/状态"

###Description

返回 SLM 插件的状态。响应中的"operation_mode"字段显示以下三种状态之一："正在运行"、"正在停止"或"已停止"。使用停止和启动 API 停止并重新启动 SLM 插件。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"manage_slm"或"read_slm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Examples

    
    
    response = client.slm.get_status
    puts response
    
    
    GET _slm/status

API 返回以下结果：

    
    
    {
      "operation_mode": "RUNNING"
    }

[« Execute snapshot retention policy API](slm-api-execute-retention.md) [Get
snapshot lifecycle stats API »](slm-api-get-stats.md)
