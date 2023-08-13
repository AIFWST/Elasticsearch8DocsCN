

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Behavioral Analytics APIs](behavioral-analytics-
apis.md)

[« Delete Analytics Collection](delete-analytics-collection.md) [Post Event
to an Analytics Collection »](post-analytics-collection-event.md)

## 列表分析集合

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

返回有关分析集合的信息。

###Request

"获取_application/分析/<criteria>"

###Prerequisites

需要"manage_behavioral_analytics"群集权限。

### 路径参数

`<criteria>`

     (optional, string) Criteria is used to find a matching analytics collection. This could be the name of the collection or a pattern to match multiple. If not specified, will return all analytics collections. 

### 响应码

`404`

     Criteria does not match any Analytics Collections. 

### 响应码

###Examples

以下示例列出了所有已配置的分析集合：

    
    
    GET _application/analytics/

示例响应：

    
    
    {
      "my_analytics_collection": {
          "event_data_stream": {
              "name": "behavioral_analytics-events-my_analytics_collection"
          }
      },
      "my_analytics_collection2": {
          "event_data_stream": {
              "name": "behavioral_analytics-events-my_analytics_collection2"
          }
      }
    }

以下示例返回与"my_analytics_collection"匹配的分析集合：

    
    
    GET _application/analytics/my_analytics_collection

示例响应：

    
    
    {
      "my_analytics_collection": {
          "event_data_stream": {
              "name": "behavioral_analytics-events-my_analytics_collection"
          }
      }
    }

以下示例返回所有以"my"为前缀的分析集合：

    
    
    GET _application/analytics/my*

示例响应：

    
    
    {
      "my_analytics_collection": {
          "event_data_stream": {
              "name": "behavioral_analytics-events-my_analytics_collection"
          }
      },
      "my_analytics_collection2": {
          "event_data_stream": {
              "name": "behavioral_analytics-events-my_analytics_collection2"
          }
      }
    }

[« Delete Analytics Collection](delete-analytics-collection.md) [Post Event
to an Analytics Collection »](post-analytics-collection-event.md)
