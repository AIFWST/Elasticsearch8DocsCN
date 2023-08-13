

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Estimate anomaly detection jobs model memory API](ml-estimate-model-
memory.md) [Forecast jobs API »](ml-forecast.md)

## 刷新作业API

强制作业处理任何缓冲数据。

###Request

"发布 _ml/anomaly_detectors/<job_id>/_flush"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

刷新作业 API 仅适用于使用发布数据 API 发送数据进行分析的情况。根据缓冲区的内容，它可能会额外计算新结果。

刷新和关闭操作类似，但是如果您希望发送更多数据进行分析，则刷新效率更高。刷新时，作业将保持打开状态，并可用于继续分析数据。关闭操作还会修剪模型状态并将其保存到磁盘，并且在分析进一步数据之前必须再次打开作业。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 查询参数

`advance_time`

     (string) Optional. Specifies to advance to a particular time value. Results are generated and the model is updated for data from the specified time interval. 
`calc_interim`

     (Boolean) Optional. If true, calculates the interim results for the most recent bucket or all buckets within the latency period. 
`end`

     (string) Optional. When used in conjunction with `calc_interim` and `start`, specifies the range of buckets on which to calculate interim results. 
`skip_time`

     (string) Optional. Specifies to skip to a particular time value. Results are not generated and the model is not updated for data from the specified time interval. 
`start`

     (string) Optional. When used in conjunction with `calc_interim`, specifies the range of buckets on which to calculate interim results. 

### 请求正文

您还可以在请求正文中指定查询参数(例如"advance_time"和"calc_interim")。

###Examples

    
    
    POST _ml/anomaly_detectors/low_request_rate/_flush
    {
      "calc_interim": true
    }

操作成功后，您会收到以下结果：

    
    
    {
      "flushed": true,
      "last_finalized_bucket_end": 1455234900000
    }

"last_finalized_bucket_end"提供已处理的最后一个存储桶末尾的时间戳(以毫秒为单位)。

如果要将作业刷新到特定时间戳，可以使用"advance_time"或"skip_time"参数。例如，要提前到 2018 年 1 月 1 日上午 11 点 GMT：

    
    
    POST _ml/anomaly_detectors/total-requests/_flush
    {
      "advance_time": "1514804400000"
    }

操作成功后，您会收到以下结果：

    
    
    {
      "flushed": true,
      "last_finalized_bucket_end": 1514804400000
    }

[« Estimate anomaly detection jobs model memory API](ml-estimate-model-
memory.md) [Forecast jobs API »](ml-forecast.md)
