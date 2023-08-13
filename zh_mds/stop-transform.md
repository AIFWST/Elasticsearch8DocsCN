

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Start transform API](start-transform.md) [Update transform API »](update-
transform.md)

## 停止转换API

停止一个或多个转换。

###Request

"发布_transform/<transform_id>/_stop"

"发布_transform/<transform_id1>，<transform_id2>/_stop"

"发布_transform/_all/_stop"

###Prerequisites

需要"manage_transform"群集权限。此权限包含在"transform_admin"内置角色中。

### 路径参数

`<transform_id>`

     (Required, string) Identifier for the transform. To stop multiple transforms, use a comma-separated list or a wildcard expression. To stop all transforms, use `_all` or `*` as the identifier. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的转换。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时，它将返回成功的确认消息。当只有部分匹配时，API 会停止相应的转换。例如，如果请求包含"test-id1*，test-id2*"作为标识符，并且没有与"test-id2*"匹配的转换，则 API 仍会停止与"test-id1*"匹配的转换。

如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`force`

     (Optional, Boolean) Set to `true` to stop a failed transform or to forcefully stop a transform that did not respond to the initial stop request. 
`timeout`

     (Optional, time value) If `wait_for_completion=true`, the API blocks for (at maximum) the specified duration while waiting for the transform to stop. If more than `timeout` time has passed, the API throws a timeout exception. Even if a timeout exception is thrown, the stop request is still processing and eventually moves the transform to `STOPPED`. The timeout simply means the API call itself timed out while waiting for the status change. Defaults to `30s`. 
`wait_for_checkpoint`

     (Optional, Boolean) If set to `true`, the transform will not completely stop until the current checkpoint is completed. If set to `false`, the transform stops as soon as possible. Defaults to `false`. 
`wait_for_completion`

     (Optional, Boolean) If set to `true`, causes the API to block until the indexer state completely stops. If set to `false`, the API returns immediately and the indexer will be stopped asynchronously in the background. Defaults to `false`. 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

    
    
    response = client.transform.stop_transform(
      transform_id: 'ecommerce_transform'
    )
    puts response
    
    
    POST _transform/ecommerce_transform/_stop

转换停止时，您会收到以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Start transform API](start-transform.md) [Update transform API »](update-
transform.md)
