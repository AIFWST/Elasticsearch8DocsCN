

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Preview transform API](preview-transform.md) [Schedule now transform API
»](schedule-now-transform.md)

## 重置转换接口

重置转换。

###Request

"发布_transform/<transform_id>/_reset"

###Prerequisites

* 需要"manage_transform"群集权限。此权限包含在"transform_admin"内置角色中。

###Description

必须先停止转换，然后才能重置转换;或者，使用"强制"查询参数。

如果重置转换，则会删除所有检查点、状态和目标索引(如果它是由转换创建的)。转换将更新为最新格式，就像使用了更新转换 API 一样。转换已准备好重新开始，就像刚刚创建一样。

### 路径参数

`<transform_id>`

     (Required, string) Identifier for the transform. 

### 查询参数

`force`

     (Optional, Boolean) If this value is `true`, the transform is reset regardless of its current state. If it's false, the transform must be `stopped` before it can be reset. The default value is `false`
`timeout`

     (Optional, time) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

    
    
    response = client.transform.reset_transform(
      transform_id: 'ecommerce_transform'
    )
    puts response
    
    
    POST _transform/ecommerce_transform/_reset

重置转换时，您会收到以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Preview transform API](preview-transform.md) [Schedule now transform API
»](schedule-now-transform.md)
