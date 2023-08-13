

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Start index lifecycle management API](ilm-start.md) [Migrate to data
tiers routing API »](ilm-migrate-to-data-tiers.md)

## 停止索引生命周期管理API

停止索引生命周期管理 (ILM) 插件。

###Request

"发布/_ilm/停止"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_ilm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

停止所有生命周期管理操作并停止 ILM 插件。当您在集群上执行维护并且需要阻止 ILM 对索引执行任何操作时，这非常有用。

一旦确认停止请求，API 就会返回，但插件可能会继续运行，直到正在进行的操作完成并且可以安全地停止插件。使用获取 ILM 状态 API 查看 ILM 是否正在运行。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

下面的示例停止 ILM 插件。

    
    
    response = client.ilm.stop
    puts response
    
    
    POST _ilm/stop

如果请求未遇到错误，您将收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Start index lifecycle management API](ilm-start.md) [Migrate to data
tiers routing API »](ilm-migrate-to-data-tiers.md)
