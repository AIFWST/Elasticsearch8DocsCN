

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index lifecycle management APIs](index-lifecycle-
management-api.md)

[« Move to lifecycle step API](ilm-move-to-step.md) [Retry policy execution
API »](ilm-retry-policy.md)

## 从索引 API 中删除策略

从索引或数据流的支持索引中删除分配的生命周期策略。

###Request

"发布<target>/_ilm/删除"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对所管理的索引具有"manage_ilm"权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

对于索引，删除生命周期策略 API 会删除分配的生命周期策略并停止管理指定的索引。

对于数据流，API 会从流的支持索引中删除任何分配的生命周期策略，并停止管理索引。

### 路径参数

`<target>`

     (Required, string) Comma-separated list of data streams, indices, and aliases to target. Supports wildcards (`*`). To target all data streams and indices, use `*` or `_all`. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

以下示例从"my-index-000001"中删除分配的策略。

    
    
    response = client.ilm.remove_policy(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST my-index-000001/_ilm/remove

如果请求成功，您将收到以下结果：

    
    
    {
      "has_failures" : false,
      "failed_indexes" : []
    }

[« Move to lifecycle step API](ilm-move-to-step.md) [Retry policy execution
API »](ilm-retry-policy.md)
