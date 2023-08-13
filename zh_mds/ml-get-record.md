

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get filters API](ml-get-filter.md) [Open anomaly detection jobs API
»](ml-open-job.md)

## 获取记录接口

检索异常情况检测作业的异常记录。

###Request

"获取_ml/anomaly_detectors/<job_id>/结果/记录"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

记录包含详细的分析结果。它们描述了基于检测器配置的输入数据中已识别的异常活动。

根据输入数据的特征和大小，可能会有许多异常记录。在实践中，通常太多而无法手动处理它们。因此，机器学习功能将异常记录复杂地聚合到存储桶中。

记录结果的数量取决于在每个存储桶中发现的异常数量，这与正在建模的时间序列数量和检测器数量有关。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 查询参数

`desc`

     (Optional, Boolean) If true, the results are sorted in descending order. 
`end`

     (Optional, string) Returns records with timestamps earlier than this time. Defaults to `-1`, which means it is unset and results are not limited to specific timestamps. 
`exclude_interim`

     (Optional, Boolean) If `true`, the output excludes interim results. Defaults to `false`, which means interim results are included. 
`from`

     (Optional, integer) Skips the specified number of records. Defaults to `0`. 
`record_score`

     (Optional, double) Returns records with anomaly scores greater or equal than this value. Defaults to `0.0`. 
`size`

     (Optional, integer) Specifies the maximum number of records to obtain. Defaults to `100`. 
`sort`

     (Optional, string) Specifies the sort field for the requested records. By default, the records are sorted by the `record_score` value. 
`start`

     (Optional, string) Returns records with timestamps after this time. Defaults to `-1`, which means it is unset and results are not limited to specific timestamps. 

### 请求正文

您还可以在请求正文中指定查询参数;例外是"发件人"和"大小"，请改用"页面"：

`page`

     Properties of `page`

`from`

     (Optional, integer) Skips the specified number of records. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of records to obtain. Defaults to `100`. 

### 响应正文

API 返回一个记录对象数组，这些对象具有以下属性：

`actual`

     (array) The actual value for the bucket. 

`anomaly_score_explanation`

    

(对象)如果存在，它提供有关影响初始异常分数的因素的信息。

"anomaly_score_explanation"的属性

`anomaly_characteristics_impact`

     (Optional, integer) Impact from the duration and magnitude of the detected anomaly relative to the historical average. 
`anomaly_length`

     (Optional, integer) Length of the detected anomaly in the number of buckets. 
`anomaly_type`

     (Optional, string) Type of the detected anomaly: spike or dip. 
`high_variance_penalty`

     (Optional, boolean) Indicates reduction of anomaly score for the bucket with large confidence intervals. If a bucket has large confidence intervals, the score is reduced. 
`incomplete_bucket_penalty`

     (Optional, boolean) If the bucket contains fewer samples than expected, the score is reduced. If the bucket contains fewer samples than expected, the score is reduced. 
`lower_confidence_bound`

     (Optional, double) Lower bound of the 95% confidence interval. 
`multimodal_distribution`

     (Optional, boolean) Indicates whether the bucket values' probability distribution has several modes. When there are multiple modes, the typical value may not be the most likely. 
`multi_bucket_impact`

     (Optional, integer) Impact of the deviation between actual and typical values in the past 12 buckets. 
`single_bucket_impact`

     (Optional, integer) Impact of the deviation between actual and typical values in the current bucket. 
`typical_value`

     (Optional, double) Typical (expected) value for this bucket. 
`upper_confidence_bound`

     (Optional, double) Upper bound of the 95% confidence interval. 

`bucket_span`

     (number) The length of the bucket in seconds. This value matches the `bucket_span` that is specified in the job. 
`by_field_name`

     (string) The field used to split the data. In particular, this property is used for analyzing the splits with respect to their own history. It is used for finding unusual values in the context of the split. 
`by_field_value`

     (string) The value of `by_field_name`. 
`causes`

     (array) For population analysis, an over field must be specified in the detector. This property contains an array of anomaly records that are the causes for the anomaly that has been identified for the over field. If no over fields exist, this field is not present. This sub-resource contains the most anomalous records for the `over_field_name`. For scalability reasons, a maximum of the 10 most significant causes of the anomaly are returned. As part of the core analytical modeling, these low-level anomaly records are aggregated for their parent over field record. The causes resource contains similar elements to the record resource, namely `actual`, `typical`, `geo_results.actual_point`, `geo_results.typical_point`, `*_field_name` and `*_field_value`. Probability and scores are not applicable to causes. 
`detector_index`

     (number) A unique identifier for the detector. 
`field_name`

     (string) Certain functions require a field to operate on, for example, `sum()`. For those functions, this value is the name of the field to be analyzed. 
`function`

     (string) The function in which the anomaly occurs, as specified in the detector configuration. For example, `max`. 
`function_description`

     (string) The description of the function in which the anomaly occurs, as specified in the detector configuration. 
`geo_results`

    

(可选，对象)如果检测器函数为"lat_long"，则此对象包含逗号分隔的字符串，用于实际值和典型值的纬度和经度。

"geo_results"的属性

`actual_point`

     (string) The actual value for the bucket formatted as a `geo_point`. 
`typical_point`

     (string) The typical value for the bucket formatted as a `geo_point`. 

`influencers`

     (array) If `influencers` was specified in the detector configuration, this array contains influencers that contributed to or were to blame for an anomaly. 
`initial_record_score`

     (number) A normalized score between 0-100, which is based on the probability of the anomalousness of this record. This is the initial value that was calculated at the time the bucket was processed. 
`is_interim`

     (Boolean) If `true`, this is an interim result. In other words, the results are calculated based on partial input data. 
`job_id`

     (string) Identifier for the anomaly detection job. 
`multi_bucket_impact`

     (number) An indication of how strongly an anomaly is multi bucket or single bucket. The value is on a scale of `-5.0` to `+5.0` where `-5.0` means the anomaly is purely single bucket and `+5.0` means the anomaly is purely multi bucket. 
`over_field_name`

     (string) The field used to split the data. In particular, this property is used for analyzing the splits with respect to the history of all splits. It is used for finding unusual values in the population of all splits. For more information, see [Performing population analysis](/guide/en/machine-learning/8.9/ml-configuring-populations.html). 
`over_field_value`

     (string) The value of `over_field_name`. 
`partition_field_name`

     (string) The field used to segment the analysis. When you use this property, you have completely independent baselines for each value of this field. 
`partition_field_value`

     (string) The value of `partition_field_name`. 
`probability`

     (number) The probability of the individual anomaly occurring, in the range 0 to 1. For example, 0.0000772031. This value can be held to a high precision of over 300 decimal places, so the `record_score` is provided as a human-readable and friendly interpretation of this. 
`record_score`

     (number) A normalized score between 0-100, which is based on the probability of the anomalousness of this record. Unlike `initial_record_score`, this value will be updated by a re-normalization process as new data is analyzed. 
`result_type`

     (string) Internal. This is always set to `record`. 
`timestamp`

     (date) The start time of the bucket for which these results were calculated. 
`typical`

     (array) The typical value for the bucket, according to analytical modeling. 

根据要分析的字段添加其他记录属性。例如，如果将"主机名"作为_by field_进行分析，则会将字段"主机名"添加到结果文档中。此信息使您能够更轻松地筛选异常结果。

###Examples

    
    
    response = client.ml.get_records(
      job_id: 'low_request_rate',
      body: {
        sort: 'record_score',
        desc: true,
        start: '1454944100000'
      }
    )
    puts response
    
    
    GET _ml/anomaly_detectors/low_request_rate/results/records
    {
      "sort": "record_score",
      "desc": true,
      "start": "1454944100000"
    }
    
    
    {
      "count" : 4,
      "records" : [
        {
          "job_id" : "low_request_rate",
          "result_type" : "record",
          "probability" : 1.3882308899968812E-4,
          "multi_bucket_impact" : -5.0,
          "record_score" : 94.98554565630553,
          "initial_record_score" : 94.98554565630553,
          "bucket_span" : 3600,
          "detector_index" : 0,
          "is_interim" : false,
          "timestamp" : 1577793600000,
          "function" : "low_count",
          "function_description" : "count",
          "typical" : [
            28.254208230188834
          ],
          "actual" : [
            0.0
          ]
        },
      ...
      ]
    }

[« Get filters API](ml-get-filter.md) [Open anomaly detection jobs API
»](ml-open-job.md)
