

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Retry policy execution API](ilm-retry-policy.md) [Explain lifecycle API
»](ilm-explain-lifecycle.md)

## 获取索引生命周期管理状态API

检索当前索引生命周期管理 (ILM) 状态。

您可以使用启动 ILM 和停止 ILM API 来启动或停止 ILM。

###Request

"获取/_ilm/状态"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_ilm"或"read_ilm"或同时具有这两种集群权限才能使用此 API。有关详细信息，请参阅安全权限。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 响应正文

`operation_mode`

    

(字符串)ILM 的当前操作模式。

"operation_mode"的可能值

`RUNNING`

     ILM is running. 
`STOPPING`

     ILM is finishing sensitive actions, such as [shrink](ilm-shrink.html "Shrink"), that are in progress. When these actions finish, ILM will move to `STOPPED`. 
`STOPPED`

     ILM is not running. 

###Examples

以下示例获取 ILM 插件状态。

    
    
    response = client.ilm.get_status
    puts response
    
    
    GET _ilm/status

如果请求成功，响应正文将显示操作模式：

    
    
    {
      "operation_mode": "RUNNING"
    }

[« Retry policy execution API](ilm-retry-policy.md) [Explain lifecycle API
»](ilm-explain-lifecycle.md)
