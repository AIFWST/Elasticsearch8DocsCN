

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search Application APIs](search-application-apis.md)

[« List Search Applications](list-search-applications.md) [Search
Application Search »](search-application-search.md)

## 删除搜索应用程序

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

删除搜索应用程序及其关联的别名。附加到搜索应用程序的索引不会被删除。

###Request

"删除_application/search_application<name>/"

###Prerequisites

需要"manage_search_application"群集权限。还需要对搜索应用程序中包含的所有索引的管理权限。

### 路径参数

`<name>`

     (Required, string) 

### 响应码

`400`

     The `name` was not provided. 
`404` (Missing resources)

     No Search Application matching `name` could be found. 

###Examples

以下示例删除名为"my-app"的搜索应用程序：

    
    
    DELETE _application/search_application/my-app/

[« List Search Applications](list-search-applications.md) [Search
Application Search »](search-application-search.md)
