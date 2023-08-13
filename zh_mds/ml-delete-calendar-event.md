

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Delete datafeeds API](ml-delete-datafeed.md) [Delete filters API »](ml-
delete-filter.md)

## 从日历中删除事件API

从日历中删除计划事件。

###Request

"删除_ml/日历/<calendar_id>/事件/<event_id>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

此 API 从日历中删除单个事件。要删除所有计划事件并删除日历，请参阅删除日历 API。

### 路径参数

`<calendar_id>`

     (Required, string) A string that uniquely identifies a calendar. 
`<event_id>`

     (Required, string) Identifier for the scheduled event. You can obtain this identifier by using the [get calendar events API](ml-get-calendar-event.html "Get scheduled events API"). 

###Examples

    
    
    response = client.ml.delete_calendar_event(
      calendar_id: 'planned-outages',
      event_id: 'LS8LJGEBMTCMA-qz49st'
    )
    puts response
    
    
    DELETE _ml/calendars/planned-outages/events/LS8LJGEBMTCMA-qz49st

删除事件后，您会收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Delete datafeeds API](ml-delete-datafeed.md) [Delete filters API »](ml-
delete-filter.md)
