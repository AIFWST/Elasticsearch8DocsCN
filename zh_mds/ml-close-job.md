

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Add anomaly detection jobs to calendar API](ml-put-calendar-job.md)
[Create anomaly detection jobs API »](ml-put-job.md)

## 关闭异常检测作业API

关闭一个或多个异常情况检测作业。

###Request

"发布_ml/anomaly_detectors<job_id>//_close"

"发布 _ml/anomaly_detectors/<job_id>，<job_id>/_close"

"发布 _ml/anomaly_detectors/_all/_close"

###Prerequisites

* 需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

作业在其整个生命周期中可以多次打开和关闭。

已关闭的作业无法接收数据或执行分析操作，但您仍然可以浏览和导航结果。

如果关闭其数据馈送正在运行的异常情况检测作业，则请求首先会尝试停止数据馈送。此行为等效于使用与关闭作业请求相同的"超时"和"强制"参数调用 stopdatafeed。

关闭作业时，它会运行内务处理任务，例如修剪模型历史记录、刷新缓冲区、计算最终结果和保留模型快照。根据作业的大小，关闭可能需要几分钟，重新打开可能需要等效时间。

关闭后，作业在群集上的开销最小，但维护其元数据除外。因此，最佳做法是关闭不再需要处理数据的作业。

当具有指定结束日期的数据馈送停止时，它会自动关闭其关联的作业。

如果使用"force"查询参数，则请求返回时不执行关联的操作，例如刷新缓冲区和保留模型快照。因此，如果您希望作业在关闭作业 API 返回后处于不一致状态，请不要使用此参数。"force"查询参数应仅在作业已经失败的情况下使用，或者您对作业最近可能产生或将来可能产生的结果不感兴趣。

### 路径参数

`<job_id>`

    

(必需，字符串)异常情况检测作业的标识符。它可以是作业标识符、组名或通配符表达式。

您可以使用"_all"或指定"*"作为作业标识符来关闭所有作业。

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的作业。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时，它将返回一个空的"jobs"数组，当存在部分匹配时，它将返回结果的子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`force`

     (Optional, Boolean) Use to close a failed job, or to forcefully close a job which has not responded to its initial close request. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Controls the time to wait until a job has closed. The default value is 30 minutes. 

### 请求正文

您还可以在请求正文中指定查询参数(例如"allow_no_match"和"force")。

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

    
    
    response = client.ml.close_job(
      job_id: 'low_request_rate'
    )
    puts response
    
    
    POST _ml/anomaly_detectors/low_request_rate/_close

关闭作业后，您会收到以下结果：

    
    
    {
      "closed": true
    }

[« Add anomaly detection jobs to calendar API](ml-put-calendar-job.md)
[Create anomaly detection jobs API »](ml-put-job.md)
