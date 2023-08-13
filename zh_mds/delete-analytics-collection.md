

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Behavioral Analytics APIs](behavioral-analytics-
apis.md)

[« Put Analytics Collection](put-analytics-collection.md) [List Analytics
Collections »](list-analytics-collection.md)

## 删除分析集合

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

删除分析集合及其关联的数据流。

###Request

"删除_application/分析/<name>"

###Prerequisites

需要"manage_behavioral_analytics"群集权限。

### 路径参数

`<name>`

     (Required, string) 

### 响应码

`400`

     The `name` was not provided. 
`404` (Missing resources)

     No Analytics Collection matching `name` could be found. 

###Examples

以下示例删除名为"my_analytics_collection"的分析集合：

    
    
    DELETE _application/analytics/my_analytics_collection/

[« Put Analytics Collection](put-analytics-collection.md) [List Analytics
Collections »](list-analytics-collection.md)
