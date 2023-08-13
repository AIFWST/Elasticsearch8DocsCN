

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Get index settings API](indices-get-settings.md) [Get index template API
»](indices-get-template-v1.md)

## 获取索引模板接口

返回有关一个或多个索引模板的信息。

    
    
    response = client.indices.get_index_template(
      name: 'template_1'
    )
    puts response
    
    
    GET /_index_template/template_1

###Request

"获取/_index_template/<index-template>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

### 路径参数

(可选，字符串)要返回的模板的名称。接受通配符表达式。如果省略，则返回所有模板。

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

#### 使用通配符表达式获取索引模板

    
    
    response = client.indices.get_index_template(
      name: 'temp*'
    )
    puts response
    
    
    GET /_index_template/temp*

#### 获取所有索引模板

    
    
    response = client.indices.get_index_template
    puts response
    
    
    GET /_index_template

[« Get index settings API](indices-get-settings.md) [Get index template API
»](indices-get-template-v1.md)
