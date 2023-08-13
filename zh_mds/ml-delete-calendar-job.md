

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Delete anomaly detection jobs API](ml-delete-job.md) [Delete model
snapshots API »](ml-delete-snapshot.md)

## 从日历 API 中删除异常检测作业

从日历中删除异常情况检测作业。

###Request

"删除_ml/日历/<calendar_id>/作业/<job_id>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

### 路径参数

`<calendar_id>`

     (Required, string) A string that uniquely identifies a calendar. 
`<job_id>`

     (Required, string) An identifier for the anomaly detection jobs. It can be a job identifier, a group name, or a comma-separated list of jobs or groups. 

###Examples

    
    
    response = client.ml.delete_calendar_job(
      calendar_id: 'planned-outages',
      job_id: 'total-requests'
    )
    puts response
    
    
    DELETE _ml/calendars/planned-outages/jobs/total-requests

从日历中删除作业后，您会收到以下结果：

    
    
    {
       "calendar_id": "planned-outages",
       "job_ids": []
    }

[« Delete anomaly detection jobs API](ml-delete-job.md) [Delete model
snapshots API »](ml-delete-snapshot.md)
