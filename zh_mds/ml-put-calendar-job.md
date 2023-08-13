

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Add events to calendar API](ml-post-calendar-event.md) [Close anomaly
detection jobs API »](ml-close-job.md)

## 将异常检测作业添加到日历 API

将异常情况检测作业添加到日历。

###Request

'把_ml/日历/<calendar_id>/工作/<job_id>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

### 路径参数

`<calendar_id>`

     (Required, string) A string that uniquely identifies a calendar. 
`<job_id>`

     (Required, string) An identifier for the anomaly detection jobs. It can be a job identifier, a group name, or a comma-separated list of jobs or groups. 

###Examples

    
    
    response = client.ml.put_calendar_job(
      calendar_id: 'planned-outages',
      job_id: 'total-requests'
    )
    puts response
    
    
    PUT _ml/calendars/planned-outages/jobs/total-requests

API 返回以下结果：

    
    
    {
      "calendar_id": "planned-outages",
      "job_ids": [
        "total-requests"
      ]
    }

[« Add events to calendar API](ml-post-calendar-event.md) [Close anomaly
detection jobs API »](ml-close-job.md)
