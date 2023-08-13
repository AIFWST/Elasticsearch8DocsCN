

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Behavioral Analytics APIs](behavioral-analytics-
apis.md)

[« List Analytics Collections](list-analytics-collection.md) [Compact and
aligned text (CAT) APIs »](cat.md)

## 将事件发布到分析集合

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

将事件发布到分析集合。

###Request

'POST _application/analytics//<collection_name>event/<event_type>'

### 路径参数

`<collection_name>`

     (Required, string) Analytics collection name you want to ingest event in. 
`<event_type>`

     (Required, string) Analytics event type. Can be one of `page_view`, `search`, `click`

###Prerequisites

需要"post_behavioral_analytics_event"群集权限。

### 响应码

`202`

     Event has been accepted and will be ingested. 
`404`

     Analytics Collection `<collection_name>` does not exists. 
`400`

     Occurs either when the event type is unknown or when event payload contains invalid data. 

###Examples

以下示例将"page_view"事件发送到名为"my_analytics_collection"的分析集合：

    
    
    POST _application/analytics/my_analytics_collection/event/page_view
    {
      "session": {
        "id": "1797ca95-91c9-4e2e-b1bd-9c38e6f386a9"
      },
      "user": {
        "id": "5f26f01a-bbee-4202-9298-81261067abbd"
      },
      "page": {
        "url": "https://www.elastic.co/"
      }
    }

[« List Analytics Collections](list-analytics-collection.md) [Compact and
aligned text (CAT) APIs »](cat.md)
