

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Create or update index template API](indices-templates-v1.md) [Delete
dangling index API »](dangling-index-delete.md)

## 删除组件模板接口

删除现有组件模板。

    
    
    response = client.cluster.delete_component_template(
      name: 'template_1'
    )
    puts response
    
    
    DELETE _component_template/template_1

提供的<component-template>模板可能包含多个模板名称，以逗号分隔。如果指定了多个模板名称，则没有通配符支持，提供的名称应与现有组件模板完全匹配。

###Request

"删除/_component_template/<component-template>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

###Description

使用删除组件模板 API 删除一个或多个组件模板 组件模板是用于构造指定索引映射、设置和别名的索引模板的构建基块。

### 路径参数

`<component-template>`

     (Required, string) Comma-separated list or wildcard expression of component template names used to limit the request. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Create or update index template API](indices-templates-v1.md) [Delete
dangling index API »](dangling-index-delete.md)
