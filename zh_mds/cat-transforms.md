

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat trained model API](cat-trained-model.md) [Cluster APIs
»](cluster.md)

## 猫转换接口

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取转换 API。

返回有关转换的配置和使用情况信息。

###Request

'获取/_cat/转换/<transform_id>"

'获取/_cat/转换/_all"

'获取/_cat/转换/*"

"获取/_cat/转换"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"monitor_transform"集群权限才能使用此 API。内置的"transform_user"角色具有这些权限。有关详细信息，请参阅安全特权和内置角色。

### 路径参数

`<transform_id>`

     (Optional, string) Identifier for the transform. It can be a transform identifier or a wildcard expression. If you do not specify one of these options, the API returns information for all transforms. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的转换。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回一个空的"转换"数组，当存在部分匹配时返回结果的子集。

如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`from`

     (Optional, integer) Skips the specified number of transforms. The default value is `0`. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

"changes_last_detection_time"、"CLDT"

     (Default) The timestamp when changes were last detected in the source indices. 
`checkpoint`, `cp`

     (Default) The sequence number for the checkpoint. 
`checkpoint_duration_time_exp_avg`, `cdtea`, `checkpointTimeExpAvg`

     Exponential moving average of the duration of the checkpoint, in milliseconds. 
`checkpoint_progress`, `c`, `checkpointProgress`

     (Default) The progress of the next checkpoint that is currently in progress. 
`create_time`, `ct`, `createTime`

     The time the transform was created. 
`delete_time`, `dtime`

     The amount of time spent deleting, in milliseconds. 
`description`, `d`

     The description of the transform. 
`dest_index`, `di`, `destIndex`

     The _destination index_ for the transform. 

在"透视"转换的情况下，尽可能根据源字段推导目标索引的映射。如果需要备用映射，请在开始转换之前使用创建索引 API。

在"最新"转换的情况下，永远不会推断映射。如果不需要目标索引的动态映射，请在启动转换之前使用 Createindex API。

"documents_deleted"、"文档"

     The number of documents that have been deleted from the destination index due to the retention policy for this transform. 
`documents_indexed`, `doci`

     The number of documents that have been indexed into the destination index for the transform. 
`docs_per_second`, `dps`

     Specifies a limit on the number of input documents per second. This setting throttles the transform by adding a wait time between search requests. The default value is `null`, which disables throttling. 
`documents_processed`, `docp`

     (Default) The number of documents that have been processed from the source index of the transform. 
`frequency`, `f`

     The interval between checks for changes in the source indices when the transform is running continuously. The minimum value is `1s` and the maximum is `1h`. The default value is `1m`. 
`id`

     (Default) Identifier for the transform. 
`index_failure`, `if`

     The number of indexing failures. 
`index_time`, `itime`

     The amount of time spent indexing, in milliseconds. 
`index_total`, `it`

     The number of index operations. 
`indexed_documents_exp_avg`, `idea`

     Exponential moving average of the number of new documents that have been indexed. 
`last_search_time`, `lst`, `lastSearchTime`

     (Default) The timestamp of the last search in the source indices. This field is only shown if the transform is running. 
`max_page_search_size`, `mpsz`

     Defines the initial page size to use for the composite aggregation for each checkpoint. If circuit breaker exceptions occur, the page size is dynamically adjusted to a lower value. The minimum value is `10` and the maximum is `65,536`. The default value is `500`. 
`pages_processed`, `pp`

     The number of search or bulk index operations processed. Documents are processed in batches instead of individually. 
`pipeline`, `p`

     The unique identifier for an [ingest pipeline](ingest.html "Ingest pipelines"). 
`processed_documents_exp_avg`, `pdea`

     Exponential moving average of the number of documents that have been processed. 
`processing_time`, `pt`

     The amount of time spent processing results, in milliseconds. 
`reason`, `r`

     If a transform has a `failed` state, this property provides details about the reason for the failure. 
`search_failure`, `sf`

     The number of search failures. 
`search_time`, `stime`

     The amount of time spent searching, in milliseconds. 
`search_total`, `st`

     The number of search operations on the source index for the transform. 
`source_index`, `si`, `sourceIndex`

    

(默认)转换的_source indices_。它可以是单个索引、索引模式(例如，"my-index-*")、索引数组(例如，'["my-index-000001"、"my-index-000002"]')或索引模式数组(例如，"["my-index-*"、"my-other-index-*"]')。对于远程索引，请使用语法"remote_name：index_name""。

如果任何索引位于远程集群中，则主节点和至少一个转换节点必须具有"remote_cluster_client"节点角色。

"状态"、"状态"

    

(默认)转换的状态，可以是以下值之一：

* "正在中止"：转换正在中止。  * "失败"：转换失败。有关失败的详细信息，请检查原因字段。  * "索引"：转换正在主动处理数据并创建新文档。  * "started"：转换正在运行，但未主动索引数据。  * "停止"：转换已停止。  * "停止"：转换正在停止。

"transform_type"、"tt"

     Indicates the type of transform: `batch` or `continuous`. 
`trigger_count`, `tc`

     The number of times the transform has been triggered by the scheduler. For example, the scheduler triggers the transform indexer to check for updates or ingest new data at an interval specified in the [`frequency` property](put-transform.html#put-transform-request-body "Request body"). 
`version`, `v`

    

创建转换时节点上存在的 Elasticsearch 版本。

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`size`

     (Optional, integer) Specifies the maximum number of transforms to obtain. The default value is `100`. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    response = client.cat.transforms(
      v: true,
      format: 'json'
    )
    puts response
    
    
    GET /_cat/transforms?v=true&format=json
    
    
    [
      {
        "id" : "ecommerce_transform",
        "state" : "started",
        "checkpoint" : "1",
        "documents_processed" : "705",
        "checkpoint_progress" : "100.00",
        "changes_last_detection_time" : null
      }
    ]

[« cat trained model API](cat-trained-model.md) [Cluster APIs
»](cluster.md)
