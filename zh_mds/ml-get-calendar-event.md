

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get overall buckets API](ml-get-overall-buckets.md) [Get filters API
»](ml-get-filter.md)

## 获取定时事件接口

检索有关日历中计划事件的信息。

###Request

"获取_ml/日历/<calendar_id>/事件"

"获取_ml/日历/_all/事件"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

有关详细信息，请参阅日历和计划事件。

### 路径参数

`<calendar_id>`

    

(必需，字符串)唯一标识日历的字符串。

您可以使用逗号分隔的 id 列表或通配符表达式在单个 APIrequest 中获取多个日历的计划事件信息。您可以使用"_all"或"*"作为日历标识符来获取所有日历的预定事件信息。

### 查询参数

`end`

     (Optional, string) Specifies to get events with timestamps earlier than this time. 
`from`

     (Optional, integer) Skips the specified number of events. Defaults to `0`. 
`job_id`

     (Optional, string) Specifies to get events for a specific anomaly detection job identifier or job group. It must be used with a calendar identifier of `_all` or `*`. 
`size`

     (Optional, integer) Specifies the maximum number of events to obtain. Defaults to `100`. 
`start`

     (Optional, string) Specifies to get events with timestamps after this time. 

### 请求正文

您还可以在请求正文中指定查询参数;例外是"发件人"和"大小"，请改用"页面"：

`page`

     Properties of `page`

`from`

     (Optional, integer) Skips the specified number of events. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of events to obtain. Defaults to `100`. 

### 响应正文

API 返回一个计划事件资源数组，这些资源具有以下属性：

`calendar_id`

     (string) A string that uniquely identifies a calendar. 
`description`

     (string) A description of the scheduled event. 
`end_time`

     (date) The timestamp for the end of the scheduled event in milliseconds since the epoch or ISO 8601 format. 
`event_id`

     (string) An automatically-generated identifier for the scheduled event. 
`start_time`

     (date) The timestamp for the beginning of the scheduled event in milliseconds since the epoch or ISO 8601 format. 

###Examples

    
    
    response = client.ml.get_calendar_events(
      calendar_id: 'planned-outages'
    )
    puts response
    
    
    GET _ml/calendars/planned-outages/events

API 返回以下结果：

    
    
    {
      "count": 3,
      "events": [
        {
          "description": "event 1",
          "start_time": 1513641600000,
          "end_time": 1513728000000,
          "calendar_id": "planned-outages",
          "event_id": "LS8LJGEBMTCMA-qz49st"
        },
        {
          "description": "event 2",
          "start_time": 1513814400000,
          "end_time": 1513900800000,
          "calendar_id": "planned-outages",
          "event_id": "Li8LJGEBMTCMA-qz49st"
        },
        {
          "description": "event 3",
          "start_time": 1514160000000,
          "end_time": 1514246400000,
          "calendar_id": "planned-outages",
          "event_id": "Ly8LJGEBMTCMA-qz49st"
        }
      ]
    }

下面的示例检索在特定时间段内发生的计划事件：

    
    
    response = client.ml.get_calendar_events(
      calendar_id: 'planned-outages',
      start: 1_635_638_400_000,
      end: 1_635_724_800_000
    )
    puts response
    
    
    GET _ml/calendars/planned-outages/events?start=1635638400000&end=1635724800000

[« Get overall buckets API](ml-get-overall-buckets.md) [Get filters API
»](ml-get-filter.md)
