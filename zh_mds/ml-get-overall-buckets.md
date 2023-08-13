

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get anomaly detection job model snapshot upgrade statistics API](ml-get-
job-model-snapshot-upgrade-stats.md) [Get scheduled events API »](ml-get-
calendar-event.md)

## 获取整体存储桶API

检索汇总多个异常情况检测作业的存储桶结果的总体存储桶结果。

###Request

"获取_ml/anomaly_detectors/<job_id>/结果/overall_buckets"

'获取_ml/anomaly_detectors<job_id>/，<job_id>/结果/overall_buckets"

"获取_ml/anomaly_detectors/_all/结果/overall_buckets"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

默认情况下，整个存储桶的跨度等于指定异常情况检测作业的最大存储桶跨度。若要覆盖该行为，请使用可选的"bucket_span"参数。要了解有关存储桶概念的更多信息，请参阅存储桶。

"overall_score"是通过组合整个存储桶跨度内所有存储桶的分数来计算的。首先，计算整个存储桶中每个异常检测作业的最大"anomaly_score"。然后将这些分数的"top_n"平均以得出"overall_score"。这意味着您可以微调"overall_score"，使其对同时检测异常的作业数量或多或少敏感。例如，如果将"top_n"设置为"1"，则"overall_score"是整个存储桶中的最大存储桶分数。或者，如果将"top_n"设置为作业数，则仅当所有作业都检测到该总体存储桶中的异常时，"overall_score"才会很高。如果您设置了"bucket_span"参数(设置为大于 itsdefault 的值)，则"overall_score"是跨度等于作业最大存储桶跨度的总体存储桶的最大"overall_score"。

### 路径参数

`<job_id>`

    

(必需，字符串)异常情况检测作业的标识符。它可以是作业标识符、组名称、以逗号分隔的作业或组列表或通配符表达式。

您可以使用"_all"或指定"*"作为作业标识符来汇总所有异常情况检测作业的存储桶结果。

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的作业。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时，它将返回一个空的"jobs"数组，当存在部分匹配时，它将返回结果的子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`bucket_span`

     (Optional, string) The span of the overall buckets. Must be greater or equal to the largest bucket span of the specified anomaly detection jobs, which is the default value. 
`end`

     (Optional, string) Returns overall buckets with timestamps earlier than this time. Defaults to `-1`, which means it is unset and results are not limited to specific timestamps. 
`exclude_interim`

     (Optional, Boolean) If `true`, the output excludes interim overall buckets. Overall buckets are interim if any of the job buckets within the overall bucket interval are interim. Defaults to `false`, which means interim results are included. 
`overall_score`

     (Optional, double) Returns overall buckets with overall scores greater or equal than this value. Defaults to `0.0`. 
`start`

     (Optional, string) Returns overall buckets with timestamps after this time. Defaults to `-1`, which means it is unset and results are not limited to specific timestamps. 
`top_n`

     (Optional, integer) The number of top anomaly detection job bucket scores to be used in the `overall_score` calculation. Defaults to `1`. 

### 请求正文

您还可以在请求正文中指定查询参数(例如"allow_no_match"和"bucket_span")。

### 响应正文

API 返回一个整体存储桶对象的数组，这些对象具有以下属性：

`bucket_span`

     (number) The length of the bucket in seconds. Matches the `bucket_span` of the job with the longest one. 
`is_interim`

     (Boolean) If `true`, this is an interim result. In other words, the results are calculated based on partial input data. 
`jobs`

     (array) An array of objects that contain the `max_anomaly_score` per `job_id`. 
`overall_score`

     (number) The `top_n` average of the max bucket `anomaly_score` per job. 
`result_type`

     (string) Internal. This is always set to `overall_bucket`. 
`timestamp`

     (date) The start time of the bucket for which these results were calculated. 

###Examples

    
    
    response = client.ml.get_overall_buckets(
      job_id: 'job-*',
      body: {
        overall_score: 80,
        start: '1403532000000'
      }
    )
    puts response
    
    
    GET _ml/anomaly_detectors/job-*/results/overall_buckets
    {
      "overall_score": 80,
      "start": "1403532000000"
    }

在此示例中，API 返回与指定分数和时间限制匹配的单个结果。"overall_score"是最大作业分数，因为"top_n"在未指定时默认为 1：

    
    
    {
      "count": 1,
      "overall_buckets": [
        {
          "timestamp" : 1403532000000,
          "bucket_span" : 3600,
          "overall_score" : 80.0,
          "jobs" : [
            {
              "job_id" : "job-1",
              "max_anomaly_score" : 30.0
            },
            {
              "job_id" : "job-2",
              "max_anomaly_score" : 10.0
            },
            {
              "job_id" : "job-3",
              "max_anomaly_score" : 80.0
            }
          ],
          "is_interim" : false,
          "result_type" : "overall_bucket"
        }
      ]
    }

下一个示例类似，但这次"top_n"设置为"2"：

    
    
    response = client.ml.get_overall_buckets(
      job_id: 'job-*',
      body: {
        top_n: 2,
        overall_score: 50,
        start: '1403532000000'
      }
    )
    puts response
    
    
    GET _ml/anomaly_detectors/job-*/results/overall_buckets
    {
      "top_n": 2,
      "overall_score": 50.0,
      "start": "1403532000000"
    }

请注意，"overall_score"现在是前 2 个工作分数的平均值：

    
    
    {
      "count": 1,
      "overall_buckets": [
        {
          "timestamp" : 1403532000000,
          "bucket_span" : 3600,
          "overall_score" : 55.0,
          "jobs" : [
            {
              "job_id" : "job-1",
              "max_anomaly_score" : 30.0
            },
            {
              "job_id" : "job-2",
              "max_anomaly_score" : 10.0
            },
            {
              "job_id" : "job-3",
              "max_anomaly_score" : 80.0
            }
          ],
          "is_interim" : false,
          "result_type" : "overall_bucket"
        }
      ]
    }

[« Get anomaly detection job model snapshot upgrade statistics API](ml-get-
job-model-snapshot-upgrade-stats.md) [Get scheduled events API »](ml-get-
calendar-event.md)
