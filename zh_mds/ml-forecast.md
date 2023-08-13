

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Flush jobs API](ml-flush-job.md) [Get buckets API »](ml-get-bucket.md)

## 预测作业API

使用时间序列的历史行为预测其未来行为。

###Request

"发布_ml/anomaly_detectors/<job_id>/_forecast"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

您可以基于异常情况检测作业创建预测作业，以推断未来行为。请参阅预测未来和预测限制以了解更多信息。

您可以使用删除预测 API 删除预测。

* 执行人口分析的工作不支持预测;如果尝试为配置中包含"over_field_name"属性的作业创建预测，则会发生错误。  * 创建预测时，作业必须处于打开状态。否则，将发生错误。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 查询参数

`duration`

     (Optional, [time units](api-conventions.html#time-units "Time units")) A period of time that indicates how far into the future to forecast. For example, `30d` corresponds to 30 days. The default value is 1 day. The forecast starts at the last record that was processed. 
`expires_in`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The period of time that forecast results are retained. After a forecast expires, the results are deleted. The default value is 14 days. If set to a value of `0`, the forecast is never automatically deleted. 
`max_model_memory`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) The maximum memory the forecast can use. If the forecast needs to use more than the provided amount, it will spool to disk. Default is 20mb, maximum is 500mb and minimum is 1mb. If set to 40% or more of the job's configured memory limit, it is automatically reduced to below that amount. 

### 请求正文

您还可以在请求正文中指定查询参数(例如"持续时间"和"expires_in")。

###Examples

    
    
    POST _ml/anomaly_detectors/low_request_rate/_forecast
    {
      "duration": "10d"
    }

创建预测后，您将收到以下结果：

    
    
    {
      "acknowledged": true,
      "forecast_id": "wkCWa2IB2lF8nSE_TzZo"
    }

随后，您可以在 Kibana 中的**单一指标查看器** 中查看预测。

[« Flush jobs API](ml-flush-job.md) [Get buckets API »](ml-get-bucket.md)
