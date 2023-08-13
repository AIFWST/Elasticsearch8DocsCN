

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot lifecycle management APIs](snapshot-
lifecycle-management-api.md)

[« Get snapshot lifecycle stats API](slm-api-get-stats.md) [Stop snapshot
lifecycle management API »](slm-api-stop.md)

## 启动快照生命周期管理API

启用快照生命周期管理 (SLM)。

###Request

"开机自检/_slm/开始"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"manage_slm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

如果 SLM 插件未运行，则启动它。SLM 在形成集群时自动启动。仅当使用"停止快照生命周期管理"已停止 SLM 时，才需要手动启动 SLM。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

启动 SLM 插件：

    
    
    POST _slm/start

如果成功，此请求将返回：

    
    
    {
      "acknowledged": true
    }

[« Get snapshot lifecycle stats API](slm-api-get-stats.md) [Stop snapshot
lifecycle management API »](slm-api-stop.md)
