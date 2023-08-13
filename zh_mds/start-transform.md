

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Schedule now transform API](schedule-now-transform.md) [Stop transforms
API »](stop-transform.md)

## 启动转换接口

启动转换。

###Request

"发布_transform/<transform_id>/_start"

###Prerequisites

需要以下权限：

* 群集："manage_transform"("transform_admin"内置角色授予此权限)

###Description

启动转换时，它会创建目标索引(如果尚不存在)。"number_of_shards"设置为"1"，auto_expand_replicas"设置为"0-1"。

如果是透视转换，则从源索引和转换聚合中推断目标索引的映射定义。目标索引中的 if 字段派生自脚本(如"scripted_metric"或"bucket_script"聚合)，除非存在索引模板，否则转换将使用动态映射。

如果是最新转换，则不会推断映射定义;它使用动态映射。

若要使用显式映射，请在开始转换之前创建目标索引。或者，您可以创建索引模板，但它不会影响透视转换中推导的映射。

转换开始时，将进行一系列验证以确保其成功。如果在创建转换时延迟了验证，则启动转换时会发生验证，但权限检查除外。启用 Elasticsearch 安全功能后，转换会记住创建它的用户在创建时具有哪些角色，并使用这些相同的角色。如果这些角色对源索引和目标索引没有所需的特权，则转换在尝试未经授权的操作时将失败。

### 路径参数

`<transform_id>`

     (Required, string) Identifier for the transform. 

### 查询参数

`from`

     (Optional, string) Restricts the set of transformed entities to those changed after this time. Relative times like now-30d are supported. Only applicable for continuous transforms. 
`timeout`

     (Optional, time) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

    
    
    response = client.transform.start_transform(
      transform_id: 'ecommerce_transform'
    )
    puts response
    
    
    POST _transform/ecommerce_transform/_start

转换开始时，您会收到以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Schedule now transform API](schedule-now-transform.md) [Stop transforms
API »](stop-transform.md)
