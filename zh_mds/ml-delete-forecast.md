

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Delete filters API](ml-delete-filter.md) [Delete anomaly detection jobs
API »](ml-delete-job.md)

## 删除预测接口

从机器学习作业中删除预测。

###Request

"删除_ml/anomaly_detectors/<job_id>/_forecast"

"删除_ml/anomaly_detectors/<job_id>/_forecast/<forecast_id>"

"删除_ml/anomaly_detectors/<job_id>/_forecast/_all"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

默认情况下，预测会保留 14 天。您可以使用预测作业 API 中的"expires_in"参数指定不同的保留期。删除预测 API 使您能够在一个或多个预测过期之前将其删除。

删除作业时，其关联的预测将被删除。

有关更多信息，请参阅预测未来。

### 路径参数

`<forecast_id>`

     (Optional, string) A comma-separated list of forecast identifiers. If you do not specify this optional parameter or if you specify `_all` or `*` the API deletes all forecasts from the job. 
`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 查询参数

`allow_no_forecasts`

     (Optional, Boolean) Specifies whether an error occurs when there are no forecasts. In particular, if this parameter is set to `false` and there are no forecasts associated with the job, attempts to delete all forecasts return an error. The default value is `true`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for the completion of the delete operation. When this period of time elapses, the API fails and returns an error. The default value is `30s`. 

###Examples

    
    
    response = client.ml.delete_forecast(
      job_id: 'total-requests',
      forecast_id: '_all'
    )
    puts response
    
    
    DELETE _ml/anomaly_detectors/total-requests/_forecast/_all

如果请求未遇到错误，您将收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Delete filters API](ml-delete-filter.md) [Delete anomaly detection jobs
API »](ml-delete-job.md)
