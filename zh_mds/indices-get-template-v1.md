

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Get index template API ](indices-get-template.md) [Get mapping API
»](indices-get-mapping.md)

## 获取索引模板API

本文档介绍旧版索引模板，这些模板已弃用，将由 Elasticsearch 7.8 中引入的可组合模板取代。有关可组合模板的信息，请参阅索引模板。

检索有关一个或多个索引模板的信息。

    
    
    response = client.indices.get_template(
      name: 'template_1'
    )
    puts response
    
    
    GET /_template/template_1

###Request

"获取/_template/<index-template>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

### 路径参数

`<index-template>`

    

(必需，字符串)用于限制请求的索引模板名称的逗号分隔列表。支持通配符 ('*') 表达式。

若要返回所有索引模板，请省略此参数或使用值"_all"或"*"。

### 查询参数

`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

#### 获取多个索引模板

    
    
    response = client.indices.get_template(
      name: 'template_1,template_2'
    )
    puts response
    
    
    GET /_template/template_1,template_2

#### 使用通配符表达式获取索引模板

    
    
    response = client.indices.get_template(
      name: 'temp*'
    )
    puts response
    
    
    GET /_template/temp*

#### 获取所有索引模板

    
    
    response = client.indices.get_template
    puts response
    
    
    GET /_template

[« Get index template API ](indices-get-template.md) [Get mapping API
»](indices-get-mapping.md)
