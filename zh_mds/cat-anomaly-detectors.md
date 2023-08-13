

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat allocation API](cat-allocation.md) [cat component templates API
»](cat-component-templates.md)

## 猫异常检测器API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取异常情况检测作业统计信息 API。

返回有关异常情况检测作业的配置和使用情况信息。

###Request

'获取 /_cat/ml/anomaly_detectors/<job_id>'

'获取/_cat/ml/anomaly_detectors"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"monitor_ml"、"监控"、"manage_ml"或"管理"集群权限才能使用此 API。请参阅安全特权和机器学习安全特权。

###Description

此 API 最多返回 10，000 个作业。

有关异常情况检测的详细信息，请参阅查找异常。

### 路径参数

`<job_id>`

     (Optional, string) Identifier for the anomaly detection job. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的作业。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时，它将返回一个空的"jobs"数组，当存在部分匹配时，它将返回结果的子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`bytes`

     (Optional, [byte size units](api-conventions.html#byte-units "Byte size units")) Unit used to display byte values. 
`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

"assignment_explanation"、"ae"

     For open anomaly detection jobs only, contains messages relating to the selection of a node to run the job. 
`buckets.count`, `bc`, `bucketsCount`

     (Default) The number of bucket results produced by the job. 
`buckets.time.exp_avg`, `btea`, `bucketsTimeExpAvg`

     Exponential moving average of all bucket processing times, in milliseconds. 
`buckets.time.exp_avg_hour`, `bteah`, `bucketsTimeExpAvgHour`

     Exponentially-weighted moving average of bucket processing times calculated in a 1 hour time window, in milliseconds. 
`buckets.time.max`, `btmax`, `bucketsTimeMax`

     Maximum among all bucket processing times, in milliseconds. 
`buckets.time.min`, `btmin`, `bucketsTimeMin`

     Minimum among all bucket processing times, in milliseconds. 
`buckets.time.total`, `btt`, `bucketsTimeTotal`

     Sum of all bucket processing times, in milliseconds. 
`data.buckets`, `db`, `dataBuckets`

     The number of buckets processed. 
`data.earliest_record`, `der`, `dataEarliestRecord`

     The timestamp of the earliest chronologically input document. 
`data.empty_buckets`, `deb`, `dataEmptyBuckets`

     The number of buckets which did not contain any data. If your data contains many empty buckets, consider increasing your `bucket_span` or using functions that are tolerant to gaps in data such as `mean`, `non_null_sum` or `non_zero_count`. 
`data.input_bytes`, `dib`, `dataInputBytes`

     The number of bytes of input data posted to the anomaly detection job. 
`data.input_fields`, `dif`, `dataInputFields`

     The total number of fields in input documents posted to the anomaly detection job. This count includes fields that are not used in the analysis. However, be aware that if you are using a datafeed, it extracts only the required fields from the documents it retrieves before posting them to the job. 
`data.input_records`, `dir`, `dataInputRecords`

     The number of input documents posted to the anomaly detection job. 
`data.invalid_dates`, `did`, `dataInvalidDates`

     The number of input documents with either a missing date field or a date that could not be parsed. 
`data.last`, `dl`, `dataLast`

     The timestamp at which data was last analyzed, according to server time. 
`data.last_empty_bucket`, `dleb`, `dataLastEmptyBucket`

     The timestamp of the last bucket that did not contain any data. 
`data.last_sparse_bucket`, `dlsb`, `dataLastSparseBucket`

     The timestamp of the last bucket that was considered sparse. 
`data.latest_record`, `dlr`, `dataLatestRecord`

     The timestamp of the latest chronologically input document. 
`data.missing_fields`, `dmf`, `dataMissingFields`

    

缺少异常情况检测作业配置为分析的字段的输入文档数。仍会处理缺少字段的输入文档，因为可能并非所有字段都丢失。

如果使用数据馈送或以 JSON 格式将数据发布到作业，则高"missing_field_count"通常不表示存在数据问题。这不一定引起关注。

'data.out_of_order_timestamps'， 'doot'， 'dataOutOfOrderTimestamps'

     The number of input documents that have a timestamp chronologically preceding the start of the current anomaly detection bucket offset by the latency window. This information is applicable only when you provide data to the anomaly detection job by using the [post data API](ml-post-data.html "Post data to jobs API"). These out of order documents are discarded, since jobs require time series data to be in ascending chronological order. 
`data.processed_fields`, `dpf`, `dataProcessedFields`

     The total number of fields in all the documents that have been processed by the anomaly detection job. Only fields that are specified in the detector configuration object contribute to this count. The timestamp is not included in this count. 
`data.processed_records`, `dpr`, `dataProcessedRecords`

     (Default) The number of input documents that have been processed by the anomaly detection job. This value includes documents with missing fields, since they are nonetheless analyzed. If you use datafeeds and have aggregations in your search query, the `processed_record_count` is the number of aggregation results processed, not the number of Elasticsearch documents. 
`data.sparse_buckets`, `dsb`, `dataSparseBuckets`

     The number of buckets that contained few data points compared to the expected number of data points. If your data contains many sparse buckets, consider using a longer `bucket_span`. 
`forecasts.memory.avg`, `fmavg`, `forecastsMemoryAvg`

     The average memory usage in bytes for forecasts related to the anomaly detection job. 
`forecasts.memory.max`, `fmmax`, `forecastsMemoryMax`

     The maximum memory usage in bytes for forecasts related to the anomaly detection job. 
`forecasts.memory.min`, `fmmin`, `forecastsMemoryMin`

     The minimum memory usage in bytes for forecasts related to the anomaly detection job. 
`forecasts.memory.total`, `fmt`, `forecastsMemoryTotal`

     The total memory usage in bytes for forecasts related to the anomaly detection job. 
`forecasts.records.avg`, `fravg`, `forecastsRecordsAvg`

     The average number of `model_forecast` documents written for forecasts related to the anomaly detection job. 
`forecasts.records.max`, `frmax`, `forecastsRecordsMax`

     The maximum number of `model_forecast` documents written for forecasts related to the anomaly detection job. 
`forecasts.records.min`, `frmin`, `forecastsRecordsMin`

     The minimum number of `model_forecast` documents written for forecasts related to the anomaly detection job. 
`forecasts.records.total`, `frt`, `forecastsRecordsTotal`

     The total number of `model_forecast` documents written for forecasts related to the anomaly detection job. 
`forecasts.time.avg`, `ftavg`, `forecastsTimeAvg`

     The average runtime in milliseconds for forecasts related to the anomaly detection job. 
`forecasts.time.max`, `ftmax`, `forecastsTimeMax`

     The maximum runtime in milliseconds for forecasts related to the anomaly detection job. 
`forecasts.time.min`, `ftmin`, `forecastsTimeMin`

     The minimum runtime in milliseconds for forecasts related to the anomaly detection job. 
`forecasts.time.total`, `ftt`, `forecastsTimeTotal`

     The total runtime in milliseconds for forecasts related to the anomaly detection job. 
`forecasts.total`, `ft`, `forecastsTotal`

     (Default) The number of individual forecasts currently available for the job. A value of `1` or more indicates that forecasts exist. 
`id`

     (Default) Identifier for the anomaly detection job. 
`model.bucket_allocation_failures`, `mbaf`, `modelBucketAllocationFailures`

     The number of buckets for which new entities in incoming data were not processed due to insufficient model memory. This situation is also signified by a `hard_limit: memory_status` property value. 
`model.by_fields`, `mbf`, `modelByFields`

     The number of `by` field values that were analyzed by the models. This value is cumulative for all detectors in the job. 
`model.bytes`, `mb`, `modelBytes`

     (Default) The number of bytes of memory used by the models. This is the maximum value since the last time the model was persisted. If the job is closed, this value indicates the latest size. 
`model.bytes_exceeded`, `mbe`, `modelBytesExceeded`

     The number of bytes over the high limit for memory usage at the last allocation failure. 
`model.categorization_status`, `mcs`, `modelCategorizationStatus`

    

作业的分类状态。包含以下值之一：

* "ok"：分类表现良好(或根本不使用)。  * "warn"：分类是检测类别的分布，表明输入数据不适合分类。问题可能是只有一个类别，超过90%的类别是罕见的，类别的数量大于分类文档数量的50%，没有经常匹配的类别，或者超过50%的类别是死的。

'model.categorized_doc_count'， 'mcdc'， 'modelClassdDocCount'

     The number of documents that have had a field categorized. 
`model.dead_category_count`, `mdcc`, `modelDeadCategoryCount`

     The number of categories created by categorization that will never be assigned again because another category's definition makes it a superset of the dead category. (Dead categories are a side effect of the way categorization has no prior training.) 
`model.failed_category_count`, `mdcc`, `modelFailedCategoryCount`

     The number of times that categorization wanted to create a new category but couldn't because the job had hit its `model_memory_limit`. This count does not track which specific categories failed to be created. Therefore you cannot use this value to determine the number of unique categories that were missed. 
`model.frequent_category_count`, `mfcc`, `modelFrequentCategoryCount`

     The number of categories that match more than 1% of categorized documents. 
`model.log_time`, `mlt`, `modelLogTime`

     The timestamp when the model stats were gathered, according to server time. 
`model.memory_limit`, `mml`, `modelMemoryLimit`

     The upper limit for model memory usage, checked on increasing values. 
`model.memory_status`, `mms`, `modelMemoryStatus`

    

(默认)数学模型的状态，可以具有以下值之一：

* "ok"：模型保持在配置值以下。  * "soft_limit"：模型使用的内存限制超过 60%，将修剪较旧的未使用模型以释放空间。此外，在分类作业中，不会存储其他类别示例。  * "hard_limit"：模型使用的空间超过配置的内存限制。因此，并非所有传入数据都已处理。

"model.over_fields"、"mof"、"modelOverFields"

     The number of `over` field values that were analyzed by the models. This value is cumulative for all detectors in the job. 
`model.partition_fields`, `mpf`, `modelPartitionFields`

     The number of `partition` field values that were analyzed by the models. This value is cumulative for all detectors in the job. 
`model.rare_category_count`, `mrcc`, `modelRareCategoryCount`

     The number of categories that match just one categorized document. 
`model.timestamp`, `mt`, `modelTimestamp`

     The timestamp of the last record when the model stats were gathered. 
`model.total_category_count`, `mtcc`, `modelTotalCategoryCount`

     The number of categories created by categorization. 
`node.address`, `na`, `nodeAddress`

    

节点的网络地址。

包含运行作业的节点的属性。此信息仅适用于打开的职位。

'node.ephemeral_id'， 'ne'， 'nodeEphemeralId'

    

节点的临时 ID。

包含运行作业的节点的属性。此信息仅适用于打开的职位。

'node.id'， 'ni'， 'nodeId'

    

节点的唯一标识符。

包含运行作业的节点的属性。此信息仅适用于打开的职位。

"node.name"、"nn"、"节点名称"

    

节点名称。

包含运行作业的节点的属性。此信息仅适用于打开的职位。

"opened_time"、"奥特"

     For open jobs only, the elapsed time for which the job has been open. 
`state`, `s`

    

(默认)异常情况检测作业的状态，可以是以下值之一：

* "已关闭"：作业成功完成，其模型状态保持不变。必须先打开作业，然后才能接受更多数据。  * "关闭"：作业关闭操作正在进行中，尚未完成。关闭作业无法接受更多数据。  * "失败"：由于错误，作业未成功完成。这种情况可能是由于输入数据无效、分析期间发生的致命错误或外部交互(例如进程被 Linux 内存不足 (OOM) 终止器终止所致。如果作业不可挽回地失败，则必须强制关闭它，然后将其删除。如果可以更正数据馈送，则可以关闭作业，然后重新打开。  * "打开"：作业可用于接收和处理数据。  * "开放"：作业打开操作正在进行中，尚未完成。

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    response = client.cat.ml_jobs(
      h: 'id,s,dpr,mb',
      v: true
    )
    puts response
    
    
    GET _cat/ml/anomaly_detectors?h=id,s,dpr,mb&v=true
    
    
    id                        s dpr   mb
    high_sum_total_sales closed 14022 1.5mb
    low_request_rate     closed 1216  40.5kb
    response_code_rates  closed 28146 132.7kb
    url_scanning         closed 28146 501.6kb

[« cat allocation API](cat-allocation.md) [cat component templates API
»](cat-component-templates.md)
