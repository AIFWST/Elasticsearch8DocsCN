

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get datafeed statistics API](ml-get-datafeed-stats.md) [Get anomaly
detection jobs API »](ml-get-job.md)

## 获取影响者API

检索一个或多个影响因素的异常情况检测作业结果。

###Request

"获取_ml/anomaly_detectors/<job_id>/结果/影响者"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

影响者是促成或应归咎于异常的实体。仅当在作业配置中指定了"influencer_field_name"时，影响因素结果才可用。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 查询参数

`desc`

     (Optional, Boolean) If true, the results are sorted in descending order. 
`end`

     (Optional, string) Returns influencers with timestamps earlier than this time. Defaults to `-1`, which means it is unset and results are not limited to specific timestamps. 
`exclude_interim`

     (Optional, Boolean) If `true`, the output excludes interim results. Defaults to `false`, which means interim results are included. 
`from`

     (Optional, integer) Skips the specified number of influencers. Defaults to `0`. 
`influencer_score`

     (Optional, double) Returns influencers with anomaly scores greater than or equal to this value. Defaults to `0.0`. 
`size`

     (Optional, integer) Specifies the maximum number of influencers to obtain. Defaults to `100`. 
`sort`

     (Optional, string) Specifies the sort field for the requested influencers. By default, the influencers are sorted by the `influencer_score` value. 
`start`

     (Optional, string) Returns influencers with timestamps after this time. Defaults to `-1`, which means it is unset and results are not limited to specific timestamps. 

### 请求正文

您还可以在请求正文中指定查询参数;例外是"发件人"和"大小"，请改用"页面"：

`page`

     Properties of `page`

`from`

     (Optional, integer) Skips the specified number of influencers. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of influencers to obtain. Defaults to `100`. 

### 响应正文

API 返回影响因素对象数组，这些对象具有以下属性：

`bucket_span`

     (number) The length of the bucket in seconds. This value matches the `bucket_span` that is specified in the job. 
`influencer_score`

     (number) A normalized score between 0-100, which is based on the probability of the influencer in this bucket aggregated across detectors. Unlike `initial_influencer_score`, this value will be updated by a re-normalization process as new data is analyzed. 
`influencer_field_name`

     (string) The field name of the influencer. 
`influencer_field_value`

     (string) The entity that influenced, contributed to, or was to blame for the anomaly. 
`initial_influencer_score`

     (number) A normalized score between 0-100, which is based on the probability of the influencer aggregated across detectors. This is the initial value that was calculated at the time the bucket was processed. 
`is_interim`

     (Boolean) If `true`, this is an interim result. In other words, the results are calculated based on partial input data. 
`job_id`

     (string) Identifier for the anomaly detection job. 
`probability`

     (number) The probability that the influencer has this behavior, in the range 0 to 1. For example, 0.0000109783. This value can be held to a high precision of over 300 decimal places, so the `influencer_score` is provided as a human-readable and friendly interpretation of this. 
`result_type`

     (string) Internal. This value is always set to `influencer`. 
`timestamp`

     (date) The start time of the bucket for which these results were calculated. 

根据要分析的字段添加其他影响因素属性。例如，如果它以影响因素分析"user_name"，则会将字段"user_name"添加到结果文档中。此信息使您能够更轻松地筛选异常结果。

###Examples

    
    
    response = client.ml.get_influencers(
      job_id: 'high_sum_total_sales',
      body: {
        sort: 'influencer_score',
        desc: true
      }
    )
    puts response
    
    
    GET _ml/anomaly_detectors/high_sum_total_sales/results/influencers
    {
      "sort": "influencer_score",
      "desc": true
    }

在此示例中，API 返回以下信息，这些信息根据影响因素分数降序排序：

    
    
    {
      "count": 189,
      "influencers": [
        {
          "job_id": "high_sum_total_sales",
          "result_type": "influencer",
          "influencer_field_name": "customer_full_name.keyword",
          "influencer_field_value": "Wagdi Shaw",
          "customer_full_name.keyword" : "Wagdi Shaw",
          "influencer_score": 99.02493,
          "initial_influencer_score" : 94.67233079580171,
          "probability" : 1.4784807245686567E-10,
          "bucket_span" : 3600,
          "is_interim" : false,
          "timestamp" : 1574661600000
        },
      ...
      ]
    }

[« Get datafeed statistics API](ml-get-datafeed-stats.md) [Get anomaly
detection jobs API »](ml-get-job.md)
