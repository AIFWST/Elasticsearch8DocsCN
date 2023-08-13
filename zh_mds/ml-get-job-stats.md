

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get anomaly detection jobs API](ml-get-job.md) [Get model snapshots API
»](ml-get-snapshot.md)

## 获取异常检测作业统计信息API

检索异常情况检测作业的使用情况信息。

###Request

"得到_ml/anomaly_detectors/<job_id>/_stats"

"获取_ml/anomaly_detectors<job_id>/，<job_id>/_stats"

"得到_ml/anomaly_detectors/_stats"

"获取_ml/anomaly_detectors/_all/_stats"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

此 API 最多返回 10，000 个作业。

### 路径参数

`<job_id>`

     (Optional, string) Identifier for the anomaly detection job. It can be a job identifier, a group name, or a wildcard expression. You can get statistics for multiple anomaly detection jobs in a single API request by using a group name, a comma-separated list of jobs, or a wildcard expression. You can get statistics for all anomaly detection jobs by using `_all`, by specifying `*` as the job identifier, or by omitting the identifier. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的作业。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时，它将返回一个空的"jobs"数组，当存在部分匹配时，它将返回结果的子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

### 响应正文

API 返回有关作业操作进度的以下信息：

`assignment_explanation`

     (string) For open anomaly detection jobs only, contains messages relating to the selection of a node to run the job. 

`data_counts`

    

(对象)描述作业输入数量和任何相关错误计数的对象。"data_count"值是作业生存期内的累积值。如果还原模型快照或删除旧结果，则不会重置作业计数。

"data_counts"的属性

`bucket_count`

     (long) The number of bucket results produced by the job. 
`earliest_record_timestamp`

     (date) The timestamp of the earliest chronologically input document. 
`empty_bucket_count`

     (long) The number of buckets which did not contain any data. If your data contains many empty buckets, consider increasing your `bucket_span` or using functions that are tolerant to gaps in data such as `mean`, `non_null_sum` or `non_zero_count`. 
`input_bytes`

     (long) The number of bytes of input data posted to the anomaly detection job. 
`input_field_count`

     (long) The total number of fields in input documents posted to the anomaly detection job. This count includes fields that are not used in the analysis. However, be aware that if you are using a datafeed, it extracts only the required fields from the documents it retrieves before posting them to the job. 
`input_record_count`

     (long) The number of input documents posted to the anomaly detection job. 
`invalid_date_count`

     (long) The number of input documents with either a missing date field or a date that could not be parsed. 
`job_id`

     (string) Identifier for the anomaly detection job. 
`last_data_time`

     (date) The timestamp at which data was last analyzed, according to server time. 
`latest_empty_bucket_timestamp`

     (date) The timestamp of the last bucket that did not contain any data. 
`latest_record_timestamp`

     (date) The timestamp of the latest chronologically input document. 
`latest_sparse_bucket_timestamp`

     (date) The timestamp of the last bucket that was considered sparse. 
`log_time`

     (date) The timestamp of the `data_counts` according to server time. 
`missing_field_count`

    

(长)缺少异常情况检测作业配置为分析的字段的输入文档数。仍会处理缺少字段的输入文档，因为可能并非所有字段都丢失。

如果使用数据馈送或以 JSON 格式将数据发布到作业，则高"missing_field_count"通常不表示存在数据问题。这不一定引起关注。

"processed_record_count"的值包括此计数。

`out_of_order_timestamp_count`

     (long) The number of input documents that have a timestamp chronologically preceding the start of the current anomaly detection bucket offset by the latency window. This information is applicable only when you provide data to the anomaly detection job by using the [post data API](ml-post-data.html "Post data to jobs API"). These out of order documents are discarded, since jobs require time series data to be in ascending chronological order. 
`processed_field_count`

     The total number of fields in all the documents that have been processed by the anomaly detection job. Only fields that are specified in the detector configuration object contribute to this count. The timestamp is not included in this count. 
`processed_record_count`

     (long) The number of input documents that have been processed by the anomaly detection job. This value includes documents with missing fields, since they are nonetheless analyzed. If you use datafeeds and have aggregations in your search query, the `processed_record_count` is the number of aggregation results processed, not the number of Elasticsearch documents. 
`sparse_bucket_count`

     (long) The number of buckets that contained few data points compared to the expected number of data points. If your data contains many sparse buckets, consider using a longer `bucket_span`. 

`deleting`

     (Boolean) Indicates that the process of deleting the job is in progress but not yet completed. It is only reported when `true`. 

`forecasts_stats`

    

(对象)一个对象，提供有关属于此作业的预测的统计信息。如果没有做出预测，则省略一些统计数据。

除非至少有一个预测，否则将省略"memory_bytes"、"记录"、"processing_time_ms"和"状态"属性。

"forecasts_stats"的属性

`forecasted_jobs`

     (long) A value of `0` indicates that forecasts do not exist for this job. A value of `1` indicates that at least one forecast exists. 
`memory_bytes`

     (object) The `avg`, `min`, `max` and `total` memory usage in bytes for forecasts related to this job. If there are no forecasts, this property is omitted. 
`records`

     (object) The `avg`, `min`, `max` and `total` number of `model_forecast` documents written for forecasts related to this job. If there are no forecasts, this property is omitted. 
`processing_time_ms`

     (object) The `avg`, `min`, `max` and `total` runtime in milliseconds for forecasts related to this job. If there are no forecasts, this property is omitted. 
`status`

     (object) The count of forecasts by their status. For example: {"finished" : 2, "started" : 1}. If there are no forecasts, this property is omitted. 
`total`

     (long) The number of individual forecasts currently available for the job. A value of `1` or more indicates that forecasts exist. 

`job_id`

     (string) Identifier for the anomaly detection job. 

`model_size_stats`

    

(对象)一个对象，提供有关模型的大小和内容的信息。

"model_size_stats"的属性

`assignment_memory_basis`

    

(字符串)指示在何处查找用于确定作业运行位置的内存要求。可能的值为：

* "model_memory_limit"：作业的内存需求是根据其模型内存将增长到其配置的"analysis_limits"中指定的"model_memory_limit"来计算的。  * "current_model_bytes"：作业的内存需求是根据其当前模型内存大小很好地反映将来的情况来计算的。  * "peak_model_bytes"：作业的内存需求是根据其峰值模型内存大小很好地反映将来模型大小来计算的。

`bucket_allocation_failures_count`

     (long) The number of buckets for which new entities in incoming data were not processed due to insufficient model memory. This situation is also signified by a `hard_limit: memory_status` property value. 
`categorized_doc_count`

     (long) The number of documents that have had a field categorized. 
`categorization_status`

    

(字符串)作业的分类状态。包含以下值之一：

* "ok"：分类表现良好(或根本不使用)。  * "warn"：分类是检测类别的分布，表明输入数据不适合分类。问题可能是只有一个类别，超过90%的类别是罕见的，类别的数量大于分类文档数量的50%，没有经常匹配的类别，或者超过50%的类别是死的。

`dead_category_count`

     (long) The number of categories created by categorization that will never be assigned again because another category's definition makes it a superset of the dead category. (Dead categories are a side effect of the way categorization has no prior training.) 
`failed_category_count`

     (long) The number of times that categorization wanted to create a new category but couldn't because the job had hit its `model_memory_limit`. This count does not track which specific categories failed to be created. Therefore you cannot use this value to determine the number of unique categories that were missed. 
`frequent_category_count`

     (long) The number of categories that match more than 1% of categorized documents. 
`job_id`

     (string) Identifier for the anomaly detection job. 
`log_time`

     (date) The timestamp of the `model_size_stats` according to server time. 
`memory_status`

    

(字符串)数学模型的状态，可以具有以下值之一：

* "ok"：模型保持在配置值以下。  * "soft_limit"：模型使用的内存限制超过 60%，将修剪较旧的未使用模型以释放空间。此外，在分类作业中，不会存储其他类别示例。  * "hard_limit"：模型使用的空间超过配置的内存限制。因此，并非所有传入数据都已处理。

`model_bytes`

     (long) The number of bytes of memory used by the models. This is the maximum value since the last time the model was persisted. If the job is closed, this value indicates the latest size. 
`model_bytes_exceeded`

     (long) The number of bytes over the high limit for memory usage at the last allocation failure. 
`model_bytes_memory_limit`

     (long) The upper limit for model memory usage, checked on increasing values. 
`peak_model_bytes`

     (long) The peak number of bytes of memory ever used by the models. 
`rare_category_count`

     (long) The number of categories that match just one categorized document. 
`result_type`

     (string) For internal use. The type of result. 
`total_by_field_count`

     (long) The number of `by` field values that were analyzed by the models. This value is cumulative for all detectors in the job. 
`total_category_count`

     (long) The number of categories created by categorization. 
`total_over_field_count`

     (long) The number of `over` field values that were analyzed by the models. This value is cumulative for all detectors in the job. 
`total_partition_field_count`

     (long) The number of `partition` field values that were analyzed by the models. This value is cumulative for all detectors in the job. 
`timestamp`

     (date) The timestamp of the last record when the model stats were gathered. 

`node`

    

(对象)包含运行作业的节点的属性。此信息仅适用于打开的职位。

"节点"的属性

`attributes`

     (object) Lists node attributes such as `ml.machine_memory` or `ml.max_open_jobs` settings. 
`ephemeral_id`

     (string) The ephemeral ID of the node. 
`id`

     (string) The unique identifier of the node. 
`name`

     (string) The node name. 
`transport_address`

     (string) The host and port where transport HTTP connections are accepted. 

`open_time`

     (string) For open jobs only, the elapsed time for which the job has been open. 
`state`

    

(字符串)异常情况检测作业的状态，可以是以下值之一：

* "已关闭"：作业成功完成，其模型状态保持不变。必须先打开作业，然后才能接受更多数据。  * "关闭"：作业关闭操作正在进行中，尚未完成。关闭作业无法接受更多数据。  * "失败"：由于错误，作业未成功完成。这种情况可能是由于输入数据无效、分析期间发生的致命错误或外部交互(例如进程被 Linux 内存不足 (OOM) 终止器终止所致。如果作业不可挽回地失败，则必须强制关闭它，然后将其删除。如果可以更正数据馈送，则可以关闭作业，然后重新打开。  * "打开"：作业可用于接收和处理数据。  * "开放"：作业打开操作正在进行中，尚未完成。

`timing_stats`

    

(对象)一个对象，提供有关此作业的计时方面的统计信息。

"timing_stats"的属性

`average_bucket_processing_time_ms`

     (double) Average of all bucket processing times in milliseconds. 
`bucket_count`

     (long) The number of buckets processed. 
`exponential_average_bucket_processing_time_ms`

     (double) Exponential moving average of all bucket processing times, in milliseconds. 
`exponential_average_bucket_processing_time_per_hour_ms`

     (double) Exponentially-weighted moving average of bucket processing times calculated in a 1 hour time window, in milliseconds. 
`job_id`

     (string) Identifier for the anomaly detection job. 
`maximum_bucket_processing_time_ms`

     (double) Maximum among all bucket processing times, in milliseconds. 
`minimum_bucket_processing_time_ms`

     (double) Minimum among all bucket processing times, in milliseconds. 
`total_bucket_processing_time_ms`

     (double) Sum of all bucket processing times, in milliseconds. 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

    
    
    response = client.ml.get_job_stats(
      job_id: 'low_request_rate'
    )
    puts response
    
    
    GET _ml/anomaly_detectors/low_request_rate/_stats

API 返回以下结果：

    
    
    {
      "count" : 1,
      "jobs" : [
        {
          "job_id" : "low_request_rate",
          "data_counts" : {
            "job_id" : "low_request_rate",
            "processed_record_count" : 1216,
            "processed_field_count" : 1216,
            "input_bytes" : 51678,
            "input_field_count" : 1216,
            "invalid_date_count" : 0,
            "missing_field_count" : 0,
            "out_of_order_timestamp_count" : 0,
            "empty_bucket_count" : 242,
            "sparse_bucket_count" : 0,
            "bucket_count" : 1457,
            "earliest_record_timestamp" : 1575172659612,
            "latest_record_timestamp" : 1580417369440,
            "last_data_time" : 1576017595046,
            "latest_empty_bucket_timestamp" : 1580356800000,
            "input_record_count" : 1216
          },
          "model_size_stats" : {
            "job_id" : "low_request_rate",
            "result_type" : "model_size_stats",
            "model_bytes" : 41480,
            "model_bytes_exceeded" : 0,
            "model_bytes_memory_limit" : 10485760,
            "total_by_field_count" : 3,
            "total_over_field_count" : 0,
            "total_partition_field_count" : 2,
            "bucket_allocation_failures_count" : 0,
            "memory_status" : "ok",
            "categorized_doc_count" : 0,
            "total_category_count" : 0,
            "frequent_category_count" : 0,
            "rare_category_count" : 0,
            "dead_category_count" : 0,
            "failed_category_count" : 0,
            "categorization_status" : "ok",
            "log_time" : 1576017596000,
            "timestamp" : 1580410800000
          },
          "forecasts_stats" : {
            "total" : 1,
            "forecasted_jobs" : 1,
            "memory_bytes" : {
              "total" : 9179.0,
              "min" : 9179.0,
              "avg" : 9179.0,
              "max" : 9179.0
            },
            "records" : {
              "total" : 168.0,
              "min" : 168.0,
              "avg" : 168.0,
              "max" : 168.0
            },
            "processing_time_ms" : {
              "total" : 40.0,
              "min" : 40.0,
              "avg" : 40.0,
              "max" : 40.0
            },
            "status" : {
              "finished" : 1
            }
          },
          "state" : "opened",
          "node" : {
            "id" : "7bmMXyWCRs-TuPfGJJ_yMw",
            "name" : "node-0",
            "ephemeral_id" : "hoXMLZB0RWKfR9UPPUCxXX",
            "transport_address" : "127.0.0.1:9300",
            "attributes" : {
              "ml.machine_memory" : "17179869184",
              "xpack.installed" : "true",
              "ml.max_open_jobs" : "512"
            }
          },
          "assignment_explanation" : "",
          "open_time" : "13s",
          "timing_stats" : {
            "job_id" : "low_request_rate",
            "bucket_count" : 1457,
            "total_bucket_processing_time_ms" : 1094.000000000001,
            "minimum_bucket_processing_time_ms" : 0.0,
            "maximum_bucket_processing_time_ms" : 48.0,
            "average_bucket_processing_time_ms" : 0.75085792724777,
            "exponential_average_bucket_processing_time_ms" : 0.5571716855800993,
            "exponential_average_bucket_processing_time_per_hour_ms" : 15.0
          }
        }
      ]
    }

[« Get anomaly detection jobs API](ml-get-job.md) [Get model snapshots API
»](ml-get-snapshot.md)
