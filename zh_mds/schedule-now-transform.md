

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Reset transform API](reset-transform.md) [Start transform API »](start-
transform.md)

## 立即计划转换 API

即时运行转换以处理数据。

###Request

"发布_transform/<transform_id>/_schedule_now"

###Prerequisites

* 需要"manage_transform"群集权限。此权限包含在"transform_admin"内置角色中。

###Description

运行此 API 时，将立即启动下一个检查点的处理，而无需等待配置的"频率"间隔。API 立即返回，数据处理在后台进行。随后，转换将以"现在 + 频率"再次处理，除非在此期间再次调用 API。

### 路径参数

`<transform_id>`

     (Required, string) Identifier for the transform. 

### 查询参数

`timeout`

     (Optional, time) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

    
    
    response = client.transform.schedule_now_transform(
      transform_id: 'ecommerce_transform'
    )
    puts response
    
    
    POST _transform/ecommerce_transform/_schedule_now

现在计划转换时，您会收到以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Reset transform API](reset-transform.md) [Start transform API »](start-
transform.md)
