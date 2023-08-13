

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Reset anomaly detection jobs API](ml-reset-job.md) [Start datafeeds API
»](ml-start-datafeed.md)

## 还原模型快照API

还原到特定快照。

###Request

"发布 _ml/anomaly_detectors/<job_id>/model_snapshots<snapshot_id>//_revert"

###Prerequisites

* 在恢复到已保存的快照之前，必须关闭作业。  * 需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

机器学习功能对异常输入做出快速反应，学习数据中的新行为。高度异常的输入增加了模型中的方差，同时系统会学习这是行为的新阶跃变化还是一次性事件。如果已知此异常输入是一次性的，则可能适合将模型状态重置为此事件之前的时间。例如，您可以考虑在黑色星期五或严重系统故障之后恢复到保存的快照。

还原到快照不会更改异常情况检测作业的"data_counts"值，这些值不会还原到以前的状态。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 
`<snapshot_id>`

    

(必需，字符串)模型快照的标识符。

您可以将"空"指定为 <snapshot_id>.还原为"空"快照意味着异常情况检测作业在启动时开始从头开始学习新模型。

### 查询参数

`delete_intervening_results`

    

(可选，布尔值)如果为 true，则删除最新结果和还原快照时间之间的时间段内的结果。它还重置模型以接受此时间段的记录。默认值为 false。

如果在还原快照时选择不删除干预结果，则作业将不接受早于当前时间的输入数据。如果要重新发送数据，请删除干预结果。

### 请求正文

您还可以在请求正文中指定"delete_intervening_results"查询参数。

###Examples

    
    
    response = client.ml.revert_model_snapshot(
      job_id: 'low_request_rate',
      snapshot_id: 1_637_092_688,
      body: {
        delete_intervening_results: true
      }
    )
    puts response
    
    
    POST _ml/anomaly_detectors/low_request_rate/model_snapshots/1637092688/_revert
    {
      "delete_intervening_results": true
    }

操作完成后，您会收到以下结果：

    
    
    {
      "model" : {
        "job_id" : "low_request_rate",
        "min_version" : "7.11.0",
        "timestamp" : 1637092688000,
        "description" : "State persisted due to job close at 2021-11-16T19:58:08+0000",
        "snapshot_id" : "1637092688",
        "snapshot_doc_count" : 1,
        "model_size_stats" : {
          "job_id" : "low_request_rate",
          "result_type" : "model_size_stats",
          "model_bytes" : 45200,
          "peak_model_bytes" : 101552,
          "model_bytes_exceeded" : 0,
          "model_bytes_memory_limit" : 11534336,
          "total_by_field_count" : 3,
          "total_over_field_count" : 0,
          "total_partition_field_count" : 2,
          "bucket_allocation_failures_count" : 0,
          "memory_status" : "ok",
          "assignment_memory_basis" : "current_model_bytes",
          "categorized_doc_count" : 0,
          "total_category_count" : 0,
          "frequent_category_count" : 0,
          "rare_category_count" : 0,
          "dead_category_count" : 0,
          "failed_category_count" : 0,
          "categorization_status" : "ok",
          "log_time" : 1637092688530,
          "timestamp" : 1641495600000
        },
        "latest_record_time_stamp" : 1641502169000,
        "latest_result_time_stamp" : 1641495600000,
        "retain" : false
      }
    }

有关这些属性的说明，请参阅获取模型快照 API。

[« Reset anomaly detection jobs API](ml-reset-job.md) [Start datafeeds API
»](ml-start-datafeed.md)
