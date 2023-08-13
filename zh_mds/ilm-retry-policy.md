

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Remove policy from index API](ilm-remove-policy.md) [Get index lifecycle
management status API »](ilm-get-status.md)

## 重试策略执行接口

重试对 ERROR 步骤中的索引执行策略。

###Request

"开机自检<index>/_ilm/重试"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对所管理的索引具有"manage_ilm"权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

将策略设置回发生错误的步骤并执行该步骤。使用 ILM 解释 API 确定索引是否位于"错误"步骤中。

### 路径参数

`<index>`

     (Required, string) Identifier for the indices to retry in comma-separated format. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

以下示例重试"my-index-000001"的策略。

    
    
    POST my-index-000001/_ilm/retry

如果请求成功，您将收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Remove policy from index API](ilm-remove-policy.md) [Get index lifecycle
management status API »](ilm-get-status.md)
