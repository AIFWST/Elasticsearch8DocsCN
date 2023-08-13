

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Create transform API](put-transform.md) [Get transforms API »](get-
transform.md)

## 删除转换接口

删除现有转换。

###Request

"删除_transform/<transform_id>"

###Prerequisites

* 需要"manage_transform"群集权限。此权限包含在"transform_admin"内置角色中。  * 必须先停止转换，然后才能删除转换。

### 路径参数

`<transform_id>`

     (Required, string) Identifier for the transform. 

### 查询参数

`force`

     (Optional, Boolean) When `true`, the transform is deleted regardless of its current state. The default value is `false`, meaning that the transform must be `stopped` before it can be deleted. 
`delete_dest_index`

     (Optional, Boolean) When `true`, the destination index is deleted together with the transform. The default value is `false`, meaning that the destination index will not be deleted. 
`timeout`

     (Optional, time) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

    
    
    response = client.transform.delete_transform(
      transform_id: 'ecommerce_transform'
    )
    puts response
    
    
    DELETE _transform/ecommerce_transform

删除转换后，会收到以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Create transform API](put-transform.md) [Get transforms API »](get-
transform.md)
