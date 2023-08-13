

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Machine learning anomaly detection APIs](ml-ad-apis.md) [Add anomaly
detection jobs to calendar API »](ml-put-calendar-job.md)

## 将事件添加到日历API

在日历中发布计划的事件。

###Request

"发布_ml/日历/<calendar_id>/事件"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

此 API 接受计划事件的列表，每个事件必须具有开始时间、结束时间和说明。

### 路径参数

`<calendar_id>`

     (Required, string) A string that uniquely identifies a calendar. 

### 请求正文

`events`

    

(必需，阵列)多个计划事件的列表。事件的开始和结束时间可以指定为自纪元以来的整数毫秒，也可以指定为 ISO 8601 格式的字符串。

事件的属性

`description`

     (Optional, string) A description of the scheduled event. 
`end_time`

     (Required, date) The timestamp for the end of the scheduled event in milliseconds since the epoch or ISO 8601 format. 
`start_time`

     (Required, date) The timestamp for the beginning of the scheduled event in milliseconds since the epoch or ISO 8601 format. 

###Examples

    
    
    response = client.ml.post_calendar_events(
      calendar_id: 'planned-outages',
      body: {
        events: [
          {
            description: 'event 1',
            start_time: 1_513_641_600_000,
            end_time: 1_513_728_000_000
          },
          {
            description: 'event 2',
            start_time: 1_513_814_400_000,
            end_time: 1_513_900_800_000
          },
          {
            description: 'event 3',
            start_time: 1_514_160_000_000,
            end_time: 1_514_246_400_000
          }
        ]
      }
    )
    puts response
    
    
    POST _ml/calendars/planned-outages/events
    {
      "events" : [
        {"description": "event 1", "start_time": 1513641600000, "end_time": 1513728000000},
        {"description": "event 2", "start_time": 1513814400000, "end_time": 1513900800000},
        {"description": "event 3", "start_time": 1514160000000, "end_time": 1514246400000}
      ]
    }

API 返回以下结果：

    
    
    {
      "events": [
        {
          "description": "event 1",
          "start_time": 1513641600000,
          "end_time": 1513728000000,
          "calendar_id": "planned-outages"
        },
        {
          "description": "event 2",
          "start_time": 1513814400000,
          "end_time": 1513900800000,
          "calendar_id": "planned-outages"
        },
        {
          "description": "event 3",
          "start_time": 1514160000000,
          "end_time": 1514246400000,
          "calendar_id": "planned-outages"
        }
      ]
    }

[« Machine learning anomaly detection APIs](ml-ad-apis.md) [Add anomaly
detection jobs to calendar API »](ml-put-calendar-job.md)
