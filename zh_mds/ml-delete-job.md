

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Delete forecasts API](ml-delete-forecast.md) [Delete anomaly detection
jobs from calendar API »](ml-delete-calendar-job.md)

## 删除异常检测作业API

删除现有的异常情况检测作业。

###Request

"删除_ml/anomaly_detectors<job_id>/"

###Prerequisites

* 需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。  * 在删除作业之前，必须将其关闭(除非指定"force"参数)。请参阅关闭作业。

###Description

将删除所有作业配置、模型状态和结果。

删除异常情况检测作业只能通过此 API 完成。不要使用 Elasticsearchdelete 文档 API 直接从".ml-*"索引中删除作业。启用 Elasticsearch 安全功能后，请确保不会通过 '.ml-*' 索引向任何人授予"写入"权限。

目前无法使用通配符或逗号分隔列表删除多个作业。

如果删除具有数据馈送的作业，则请求首先尝试删除该数据馈送。此行为等效于使用与删除作业请求相同的"超时"和"强制"参数调用删除数据馈送。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 查询参数

`force`

     (Optional, Boolean) Use to forcefully delete an opened job; this method is quicker than closing and deleting the job. 
`wait_for_completion`

     (Optional, Boolean) Specifies whether the request should return immediately or wait until the job deletion completes. Defaults to `true`. 
`delete_user_annotations`

     (Optional, Boolean) Specifies whether annotations that have been added by the user should be deleted along with any auto-generated annotations when the job is reset. Defaults to `false`. 

###Examples

    
    
    response = client.ml.delete_job(
      job_id: 'total-requests'
    )
    puts response
    
    
    DELETE _ml/anomaly_detectors/total-requests

删除作业后，您会收到以下结果：

    
    
    {
      "acknowledged": true
    }

在下一个示例中，我们异步删除"总请求数"作业：

    
    
    response = client.ml.delete_job(
      job_id: 'total-requests',
      wait_for_completion: false
    )
    puts response
    
    
    DELETE _ml/anomaly_detectors/total-requests?wait_for_completion=false

当"wait_for_completion"设置为"false"时，响应包含作业删除任务的 id：

    
    
    {
      "task": "oTUltX4IQMOUUVeiohTt8A:39"
    }

[« Delete forecasts API](ml-delete-forecast.md) [Delete anomaly detection
jobs from calendar API »](ml-delete-calendar-job.md)
