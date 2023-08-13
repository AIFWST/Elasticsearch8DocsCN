

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Open anomaly detection jobs API](ml-open-job.md) [Preview datafeeds API
»](ml-preview-datafeed.md)

## 将数据发布到作业API

### 在 7.11.0 中已弃用。

不推荐将数据直接发布到异常情况检测作业，在未来的主要版本中将需要数据馈送。

将数据发送到异常情况检测作业进行分析。

###Request

"发布 _ml/anomaly_detectors/<job_id>/_data"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

作业必须具有"打开"状态才能接收和处理数据。

发送到作业的数据必须使用 JSON 格式。可以发送多个 JSON 文档，要么相邻，中间没有分隔符，要么用空格分隔。换行符分隔的JSON(NDJSON)是一种可能的空格分隔格式，为此，"内容类型"标头应设置为"application/x-ndjson"。

上传大小限制为 Elasticsearch HTTP 接收缓冲区大小(默认为 100 Mb)。如果数据较大，请将其拆分为多个区块，并按时间顺序分别上传每个区块。实时运行时，通常建议您执行许多小上传，而不是排队数据上传较大的文件。

上传数据时，请检查作业数据计数的进度。以下文件将不予处理：

* 文档不按时间顺序排列，且超出延迟窗口 * 时间戳无效的记录

对于每个作业，一次只能接受来自单个连接的数据。目前无法使用通配符或逗号分隔列表将数据发布到多个作业。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 查询参数

`reset_start`

     (Optional, string) Specifies the start of the bucket resetting range. 
`reset_end`

     (Optional, string) Specifies the end of the bucket resetting range. 

### 请求正文

包含要分析的数据的一个或多个 JSON 文档的序列。文档之间只允许使用空格字符。

###Examples

以下示例将"it_ops_new_kpi.json"文件中的数据发布到"it_ops_new_kpi"作业：

    
    
    $ curl -s -H "Content-type: application/json"
    -X POST http:\/\/localhost:9200/_ml/anomaly_detectors/it_ops_new_kpi/_data
    --data-binary @it_ops_new_kpi.json

发送数据时，您将收到有关作业操作进度的信息。例如：

    
    
    {
    	"job_id":"it_ops_new_kpi",
    	"processed_record_count":21435,
    	"processed_field_count":64305,
    	"input_bytes":2589063,
    	"input_field_count":85740,
    	"invalid_date_count":0,
    	"missing_field_count":0,
    	"out_of_order_timestamp_count":0,
    	"empty_bucket_count":16,
    	"sparse_bucket_count":0,
    	"bucket_count":2165,
    	"earliest_record_timestamp":1454020569000,
    	"latest_record_timestamp":1455318669000,
    	"last_data_time":1491952300658,
    	"latest_empty_bucket_timestamp":1454541600000,
    	"input_record_count":21435
    }

有关这些属性的详细信息，请参阅响应正文。

[« Open anomaly detection jobs API](ml-open-job.md) [Preview datafeeds API
»](ml-preview-datafeed.md)
