

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Index stats API](indices-stats.md) [List dangling indices API
»](dangling-indices-list.md)

## 索引模板存在API

本文档是关于遗留索引模板的，这些模板已被弃用，将被 Elasticsearch 7.8 中引入的可组合模板所取代。有关可组合模板的信息，请参阅索引模板。

检查旧索引模板是否存在。

    
    
    response = client.indices.exists_template(
      name: 'template_1'
    )
    puts response
    
    
    HEAD /_template/template_1

###Request

"头/_template/<index-template>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

###Description

使用索引模板存在 API 来确定是否存在一个或多个索引模板。

索引模板定义可自动应用于新索引的设置、映射和别名。

### 路径参数

`<index-template>`

     (Required, string) Comma-separated list of index template names used to limit the request. Wildcard (`*`) expressions are supported. 

### 查询参数

`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 响应码

`200`

     Indicates all specified index templates exist. 
`404`

     Indicates one or more specified index templates **do not** exist. 

[« Index stats API](indices-stats.md) [List dangling indices API
»](dangling-indices-list.md)
