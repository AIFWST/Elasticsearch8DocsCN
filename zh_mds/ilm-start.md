

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Explain lifecycle API](ilm-explain-lifecycle.md) [Stop index lifecycle
management API »](ilm-stop.md)

## 启动索引生命周期管理API

启动索引生命周期管理 (ILM) 插件。

###Request

"开机自检/_ilm/开始"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_ilm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

启动 ILM 插件(如果当前已停止)。ILM 在群集形成时自动启动。仅当已使用停止 ILM API 停止 ILM 时，才需要重新启动 ILM。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

以下示例启动 ILM 插件。

    
    
    response = client.ilm.start
    puts response
    
    
    POST _ilm/start

如果请求成功，您将收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Explain lifecycle API](ilm-explain-lifecycle.md) [Stop index lifecycle
management API »](ilm-stop.md)
