

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Forecast jobs API](ml-forecast.md) [Get calendars API »](ml-get-
calendar.md)

## 获取存储桶接口

检索一个或多个存储桶的异常情况检测作业结果。

###Request

"获取_ml/anomaly_detectors/<job_id>/结果/存储桶"

'获取_ml/anomaly_detectors/<job_id>/结果/桶/<timestamp>"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

获取存储桶 API 提供按时间顺序排列的记录视图，按存储桶分组。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 
`<timestamp>`

     (Optional, string) The timestamp of a single bucket result. If you do not specify this parameter, the API returns information about all buckets. 

### 查询参数

`anomaly_score`

     (Optional, double) Returns buckets with anomaly scores greater or equal than this value. Defaults to `0.0`. 
`desc`

     (Optional, Boolean) If true, the buckets are sorted in descending order. Defaults to `false`. 
`end`

     (Optional, string) Returns buckets with timestamps earlier than this time. Defaults to `-1`, which means it is unset and results are not limited to specific timestamps. 
`exclude_interim`

     (Optional, Boolean) If `true`, the output excludes interim results. Defaults to `false`, which means interim results are included. 
`expand`

     (Optional, Boolean) If true, the output includes anomaly records. Defaults to `false`. 
`from`

     (Optional, integer) Skips the specified number of buckets. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of buckets to obtain. Defaults to `100`. 
`sort`

     (Optional, string) Specifies the sort field for the requested buckets. By default, the buckets are sorted by the `timestamp` field. 
`start`

     (Optional, string) Returns buckets with timestamps after this time. Defaults to `-1`, which means it is unset and results are not limited to specific timestamps. 

### 请求正文

您还可以在请求正文中指定查询参数;例外是"发件人"和"大小"，请改用"页面"：

`page`

     Properties of `page`

`from`

     (Optional, integer) Skips the specified number of buckets. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of buckets to obtain. Defaults to `100`. 

### 响应正文

API 返回一个存储桶对象数组，这些对象具有以下属性：

`anomaly_score`

     (number) The maximum anomaly score, between 0-100, for any of the bucket influencers. This is an overall, rate-limited score for the job. All the anomaly records in the bucket contribute to this score. This value might be updated as new data is analyzed. 
`bucket_influencers`

    

(阵列)存储桶影响因素对象的数组。

"bucket_influencers"的属性

`anomaly_score`

     (number) A normalized score between 0-100, which is calculated for each bucket influencer. This score might be updated as newer data is analyzed. 
`bucket_span`

     (number) The length of the bucket in seconds. This value matches the `bucket_span` that is specified in the job. 
`influencer_field_name`

     (string) The field name of the influencer. 

`initial_anomaly_score`

     (number) The score between 0-100 for each bucket influencer. This score is the initial value that was calculated at the time the bucket was processed. 
`is_interim`

     (Boolean) If `true`, this is an interim result. In other words, the results are calculated based on partial input data. 
`job_id`

     (string) Identifier for the anomaly detection job. 
`probability`

     (number) The probability that the bucket has this behavior, in the range 0 to 1. This value can be held to a high precision of over 300 decimal places, so the `anomaly_score` is provided as a human-readable and friendly interpretation of this. 
`raw_anomaly_score`

     (number) Internal. 
`result_type`

     (string) Internal. This value is always set to `bucket_influencer`. 
`timestamp`

     (date) The start time of the bucket for which these results were calculated. 

`bucket_span`

     (number) The length of the bucket in seconds. This value matches the `bucket_span` that is specified in the job. 
`event_count`

     (number) The number of input data records processed in this bucket. 
`initial_anomaly_score`

     (number) The maximum `anomaly_score` for any of the bucket influencers. This is the initial value that was calculated at the time the bucket was processed. 
`is_interim`

     (Boolean) If `true`, this is an interim result. In other words, the results are calculated based on partial input data. 
`job_id`

     (string) Identifier for the anomaly detection job. 
`processing_time_ms`

     (number) The amount of time, in milliseconds, that it took to analyze the bucket contents and calculate results. 
`result_type`

     (string) Internal. This value is always set to `bucket`. 
`timestamp`

    

(日期)存储桶的开始时间。此时间戳唯一标识存储桶。

恰好在存储桶时间戳处发生的事件包含在存储桶的结果中。

###Examples

    
    
    response = client.ml.get_buckets(
      job_id: 'low_request_rate',
      body: {
        anomaly_score: 80,
        start: '1454530200001'
      }
    )
    puts response
    
    
    GET _ml/anomaly_detectors/low_request_rate/results/buckets
    {
      "anomaly_score": 80,
      "start": "1454530200001"
    }

在此示例中，API 返回与指定分数和时间限制匹配的单个结果：

    
    
    {
      "count" : 1,
      "buckets" : [
        {
          "job_id" : "low_request_rate",
          "timestamp" : 1578398400000,
          "anomaly_score" : 91.58505459594764,
          "bucket_span" : 3600,
          "initial_anomaly_score" : 91.58505459594764,
          "event_count" : 0,
          "is_interim" : false,
          "bucket_influencers" : [
            {
              "job_id" : "low_request_rate",
              "result_type" : "bucket_influencer",
              "influencer_field_name" : "bucket_time",
              "initial_anomaly_score" : 91.58505459594764,
              "anomaly_score" : 91.58505459594764,
              "raw_anomaly_score" : 0.5758246639716365,
              "probability" : 1.7340849573442696E-4,
              "timestamp" : 1578398400000,
              "bucket_span" : 3600,
              "is_interim" : false
            }
          ],
          "processing_time_ms" : 0,
          "result_type" : "bucket"
        }
      ]
    }

[« Forecast jobs API](ml-forecast.md) [Get calendars API »](ml-get-
calendar.md)
