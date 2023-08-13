

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Behavioral Analytics APIs](behavioral-analytics-
apis.md)

[« Behavioral Analytics APIs](behavioral-analytics-apis.md) [Delete
Analytics Collection »](delete-analytics-collection.md)

## 放分析收藏

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

创建分析集合。

###Request

"放置_application/分析/<name>"

### 路径参数

`<name>`

     (Required, string) 

###Prerequisites

需要"manage_behavioral_analytics"群集权限。

### 响应码

`400`

     Analytics Collection `<name>` exists. 

###Examples

以下示例创建一个名为"my_analytics_collection"的新分析集合：

    
    
    PUT _application/analytics/my_analytics_collection

[« Behavioral Analytics APIs](behavioral-analytics-apis.md) [Delete
Analytics Collection »](delete-analytics-collection.md)
