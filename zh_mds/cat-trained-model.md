

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat thread pool API](cat-thread-pool.md) [cat transforms API »](cat-
transforms.md)

## 猫训练模型API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取训练模型 API。

返回有关推理训练模型的配置和使用信息。

###Request

'获取/_cat/ml/trained_models"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有以下权限：

* 集群："monitor_ml"

有关详细信息，请参阅安全特权和机器学习安全特权。

### 查询参数

`bytes`

     (Optional, [byte size units](api-conventions.html#byte-units "Byte size units")) Unit used to display byte values. 
`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

"create_time"、"ct"

     The time when the trained model was created. 
`created_by`, `c`, `createdBy`

     Information on the creator of the trained model. 
`data_frame_analytics_id`, `df`, `dataFrameAnalytics`

     Identifier for the data frame analytics job that created the model. Only displayed if it is still available. 
`description`, `d`

     The description of the trained model. 
`heap_size`, `hs`, `modelHeapSize`

     (Default) The estimated heap size to keep the trained model in memory. 
`id`

     (Default) Identifier for the trained model. 
`ingest.count`, `ic`, `ingestCount`

     The total number of documents that are processed by the model. 
`ingest.current`, `icurr`, `ingestCurrent`

     The total number of document that are currently being handled by the trained model. 
`ingest.failed`, `if`, `ingestFailed`

     The total number of failed ingest attempts with the trained model. 
`ingest.pipelines`, `ip`, `ingestPipelines`

     (Default) The total number of ingest pipelines that are referencing the trained model. 
`ingest.time`, `it`, `ingestTime`

     The total time that is spent processing documents with the trained model. 
`license`, `l`

     The license level of the trained model. 
`operations`, `o`, `modelOperations`

     (Default) The estimated number of operations to use the trained model. This number helps measuring the computational complexity of the model. 
`version`, `v`

     The Elasticsearch version number in which the trained model was created. 

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    GET _cat/ml/trained_models?h=c,o,l,ct,v&v=ture
    
    
    id                           created_by operations license  create_time              version
    ddddd-1580216177138              _xpack 196        PLATINUM 2020-01-28T12:56:17.138Z 8.0.0
    flight-regress-1580215685537     _xpack 102        PLATINUM 2020-01-28T12:48:05.537Z 8.0.0
    lang_ident_model_1               _xpack 39629      BASIC    2019-12-05T12:28:34.594Z 7.6.0

[« cat thread pool API](cat-thread-pool.md) [cat transforms API »](cat-
transforms.md)
