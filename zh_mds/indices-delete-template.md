

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Delete index API](indices-delete-index.md) [Delete index template API
»](indices-delete-template-v1.md)

## 删除索引模板接口

删除索引模板。

    
    
    response = client.indices.delete_index_template(
      name: 'my-index-template'
    )
    puts response
    
    
    DELETE /_index_template/my-index-template

###Request

"删除/_index_template/<index-template>"

提供的<index-template>模板可能包含多个以逗号分隔的模板名称。如果指定了多个模板名称，则没有通配符支持，提供的名称应与现有模板完全匹配。

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

###Description

使用删除索引模板 API 删除一个或多个索引模板。索引模板定义可自动应用于新索引的设置、映射和别名。

### 路径参数

`<index-template>`

     (Required, string) Comma-separated list of index template names used to limit the request. Wildcard (`*`) expressions are supported. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Delete index API](indices-delete-index.md) [Delete index template API
»](indices-delete-template-v1.md)
