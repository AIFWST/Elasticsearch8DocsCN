

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get anomaly detection job statistics API](ml-get-job-stats.md) [Get
anomaly detection job model snapshot upgrade statistics API »](ml-get-job-
model-snapshot-upgrade-stats.md)

## 获取模型快照API

检索有关模型快照的信息。

###Request

"获取_ml/anomaly_detectors/<job_id>/model_snapshots"

"获取_ml/anomaly_detectors/<job_id>/model_snapshots/<snapshot_id>"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 
`<snapshot_id>`

    

(可选，字符串)模型快照的标识符。

您可以使用逗号分隔的列表或通配符表达式来获取多个快照的信息。您可以通过使用"_all"、指定"*"作为快照 ID 或省略快照 ID 来获取所有快照。

### 查询参数

`desc`

     (Optional, Boolean) If true, the results are sorted in descending order. Defaults to `false`. 
`end`

     (Optional, date) Returns snapshots with timestamps earlier than this time. Defaults to unset, which means results are not limited to specific timestamps. 
`from`

     (Optional, integer) Skips the specified number of snapshots. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of snapshots to obtain. Defaults to `100`. 
`sort`

     (Optional, string) Specifies the sort field for the requested snapshots. By default, the snapshots are sorted by their timestamp. 
`start`

     (Optional, string) Returns snapshots with timestamps after this time. Defaults to unset, which means results are not limited to specific timestamps. 

### 请求正文

您还可以在请求正文中指定查询参数;例外是"发件人"和"大小"，请改用"页面"：

`page`

     Properties of `page`

`from`

     (Optional, integer) Skips the specified number of snapshots. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of snapshots to obtain. Defaults to `100`. 

### 响应正文

API 返回模型快照对象的数组，这些对象具有以下属性：

`description`

     (string) An optional description of the job. 
`job_id`

     (string) A numerical character string that uniquely identifies the job that the snapshot was created for. 
`latest_record_time_stamp`

     (date) The timestamp of the latest processed record. 
`latest_result_time_stamp`

     (date) The timestamp of the latest bucket result. 
`min_version`

     (string) The minimum version required to be able to restore the model snapshot. 

`model_size_stats`

    

(对象)描述模型的摘要信息。

"model_size_stats"的属性

`assignment_memory_basis`

    

(字符串)指示在何处查找用于确定作业运行位置的内存要求。可能的值为：

* "model_memory_limit"：作业的内存需求是根据其模型内存将增长到其配置的"analysis_limits"中指定的"model_memory_limit"来计算的。  * "current_model_bytes"：作业的内存需求是根据其当前模型内存大小很好地反映将来的情况来计算的。  * "peak_model_bytes"：作业的内存需求是根据其峰值模型内存大小很好地反映将来模型大小来计算的。

`bucket_allocation_failures_count`

     (long) The number of buckets for which entities were not processed due to memory limit constraints. 
`categorized_doc_count`

     (long) The number of documents that have had a field categorized. 
`categorization_status`

    

(字符串)此作业的分类状态。包含以下值之一。

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

     (date) The timestamp that the `model_size_stats` were recorded, according to server-time. 
`memory_status`

    

(字符串)内存与其"model_memory_limit"相关的状态。包含以下值之一。

* "hard_limit"：内部模型需要的空间超过配置的内存限制。无法处理某些传入数据。  * "ok"：内部模型保持在配置值以下。  * "soft_limit"：内部模型需要超过配置的内存限制的 60%，并且将执行更积极的修剪以尝试回收空间。

`model_bytes`

     (long) An approximation of the memory resources required for this analysis. 
`model_bytes_exceeded`

     (long) The number of bytes over the high limit for memory usage at the last allocation failure. 
`model_bytes_memory_limit`

     (long) The upper limit for memory usage, checked on increasing values. 
`peak_model_bytes`

     (long) The highest recorded value for the model memory usage. 
`rare_category_count`

     (long) The number of categories that match just one categorized document. 
`result_type`

     (string) Internal. This value is always `model_size_stats`. 
`timestamp`

     (date) The timestamp that the `model_size_stats` were recorded, according to the bucket timestamp of the data. 
`total_by_field_count`

     (long) The number of _by_ field values analyzed. Note that these are counted separately for each detector and partition. 
`total_category_count`

     (long) The number of categories created by categorization. 
`total_over_field_count`

     (long) The number of _over_ field values analyzed. Note that these are counted separately for each detector and partition. 
`total_partition_field_count`

     (long) The number of _partition_ field values analyzed. 

`retain`

     (Boolean) If `true`, this snapshot will not be deleted during automatic cleanup of snapshots older than `model_snapshot_retention_days`. However, this snapshot will be deleted when the job is deleted. The default value is `false`. 
`snapshot_id`

     (string) A numerical character string that uniquely identifies the model snapshot. For example: "1491852978". 
`snapshot_doc_count`

     (long) For internal use only. 
`timestamp`

     (date) The creation timestamp for the snapshot. 

###Examples

    
    
    response = client.ml.get_model_snapshots(
      job_id: 'high_sum_total_sales',
      body: {
        start: '1575402236000'
      }
    )
    puts response
    
    
    GET _ml/anomaly_detectors/high_sum_total_sales/model_snapshots
    {
      "start": "1575402236000"
    }

在此示例中，API 提供单个结果：

    
    
    {
      "count" : 1,
      "model_snapshots" : [
        {
          "job_id" : "high_sum_total_sales",
          "min_version" : "6.4.0",
          "timestamp" : 1575402237000,
          "description" : "State persisted due to job close at 2019-12-03T19:43:57+0000",
          "snapshot_id" : "1575402237",
          "snapshot_doc_count" : 1,
          "model_size_stats" : {
            "job_id" : "high_sum_total_sales",
            "result_type" : "model_size_stats",
            "model_bytes" : 1638816,
            "model_bytes_exceeded" : 0,
            "model_bytes_memory_limit" : 10485760,
            "total_by_field_count" : 3,
            "total_over_field_count" : 3320,
            "total_partition_field_count" : 2,
            "bucket_allocation_failures_count" : 0,
            "memory_status" : "ok",
            "categorized_doc_count" : 0,
            "total_category_count" : 0,
            "frequent_category_count" : 0,
            "rare_category_count" : 0,
            "dead_category_count" : 0,
            "categorization_status" : "ok",
            "log_time" : 1575402237000,
            "timestamp" : 1576965600000
          },
          "latest_record_time_stamp" : 1576971072000,
          "latest_result_time_stamp" : 1576965600000,
          "retain" : false
        }
      ]
    }

[« Get anomaly detection job statistics API](ml-get-job-stats.md) [Get
anomaly detection job model snapshot upgrade statistics API »](ml-get-job-
model-snapshot-upgrade-stats.md)
