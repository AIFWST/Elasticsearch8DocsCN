

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get records API](ml-get-record.md) [Post data to jobs API »](ml-post-
data.md)

## 打开异常检测作业API

打开一个或多个异常情况检测作业。

###Request

'POST _ml/anomaly_detectors/{job_id}/_open'

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

必须打开异常情况检测作业，才能准备好接收和分析数据。它可以在其整个生命周期中多次打开和关闭。

当您打开新作业时，它从一个空模型开始。

打开现有作业时，将自动加载最新的模型状态。一旦收到新数据，作业已准备好从中断的位置继续其分析。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 查询参数

`timeout`

     (Optional, time) Controls the time to wait until a job has opened. The default value is 30 minutes. 

### 请求正文

您还可以在请求正文中指定"超时"查询参数。

### 响应正文

`node`

     (string) The ID of the node that the job was opened on. If the job is allowed to open lazily and has not yet been assigned to a node, this value is an empty string. 
`opened`

     (Boolean) For a successful response, this value is always `true`. On failure, an exception is returned instead. 

###Examples

    
    
    POST _ml/anomaly_detectors/low_request_rate/_open
    {
      "timeout": "35m"
    }

作业打开时，您会收到以下结果：

    
    
    {
      "opened" : true,
      "node" : "node-1"
    }

[« Get records API](ml-get-record.md) [Post data to jobs API »](ml-post-
data.md)
