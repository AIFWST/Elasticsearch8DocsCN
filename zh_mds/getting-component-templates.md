

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Get alias API](indices-get-alias.md) [Get field mapping API »](indices-
get-field-mapping.md)

## 获取组件模板接口

检索有关一个或多个组件模板的信息。

    
    
    response = client.cluster.get_component_template(
      name: 'template_1'
    )
    puts response
    
    
    GET /_component_template/template_1

###Request

"获取/_component_template/<component-template>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

### 路径参数

`<component-template>`

     (Optional, string) Comma-separated list of component template names used to limit the request. Wildcard (`*`) expressions are supported. 

### 查询参数

`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`include_defaults`

     (Optional, Boolean) Functionality in  [preview]  This functionality is in technical preview and may be changed or removed in a future release. Elastic will apply best effort to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.  . If `true`, return all default settings in the response. Defaults to `false`. 

###Examples

#### 使用通配符表达式获取组件模板

    
    
    response = client.cluster.get_component_template(
      name: 'temp*'
    )
    puts response
    
    
    GET /_component_template/temp*

#### 获取所有组件模板

    
    
    response = client.cluster.get_component_template
    puts response
    
    
    GET /_component_template

[« Get alias API](indices-get-alias.md) [Get field mapping API »](indices-
get-field-mapping.md)
