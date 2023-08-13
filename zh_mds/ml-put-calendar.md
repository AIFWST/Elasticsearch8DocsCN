

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Create anomaly detection jobs API](ml-put-job.md) [Create datafeeds API
»](ml-put-datafeed.md)

## 创建日历接口

实例化日历。

###Request

"放_ml/日历/<calendar_id>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

有关详细信息，请参阅日历和计划事件。

### 路径参数

`<calendar_id>`

     (Required, string) A string that uniquely identifies a calendar. 

### 请求正文

`description`

     (Optional, string) A description of the calendar. 

###Examples

    
    
    response = client.ml.put_calendar(
      calendar_id: 'planned-outages'
    )
    puts response
    
    
    PUT _ml/calendars/planned-outages

创建日历后，您会收到以下结果：

    
    
    {
      "calendar_id": "planned-outages",
      "job_ids": []
    }

[« Create anomaly detection jobs API](ml-put-job.md) [Create datafeeds API
»](ml-put-datafeed.md)
