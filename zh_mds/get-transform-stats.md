

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Get transforms API](get-transform.md) [Preview transform API »](preview-
transform.md)

## 获取转换统计信息API

检索转换的使用情况信息。

###Request

"得到_transform/<transform_id>/_stats"

"得到_transform/<transform_id>，<transform_id>/_stats"

"获取_transform/_stats"

"获取_transform/_all/_stats"

"获取_transform/*/_stats"

###Prerequisites

需要以下权限：

* 集群："monitor_transform"("transform_user"内置角色授予此权限) * 目标索引："读取"、"view_index_metadata"。

###Description

您可以使用逗号分隔的标识符列表或通配符表达式在单个 API 请求中获取多个转换的统计信息。您可以通过使用"_all"、将"*"指定为"<transform_id>"或省略""来获取所有转换的统计信息<transform_id>。

### 路径参数

`<transform_id>`

     (Optional, string) Identifier for the transform. It can be a transform identifier or a wildcard expression. If you do not specify one of these options, the API returns information for all transforms. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的转换。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回一个空的"转换"数组，当存在部分匹配时返回结果的子集。

如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`from`

     (Optional, integer) Skips the specified number of transforms. The default value is `0`. 
`size`

     (Optional, integer) Specifies the maximum number of transforms to obtain. The default value is `100`. 

### 响应正文

API 返回转换的统计信息对象数组，这些对象按"id"值升序排序。所有这些属性都是信息性的;您无法更新其值。

`checkpointing`

    

(对象)包含有关检查点的统计信息。

"检查点"的属性

`changes_last_detected_at`

     (date) The timestamp when changes were last detected in the source indices. 

`last`

    

(对象)包含有关上次完成的检查点的统计信息。

"最后"的属性

`checkpoint`

     (integer) The sequence number for the checkpoint. 
`time_upper_bound_millis`

     (date) When using time-based synchronization, this timestamp indicates the upper bound of data that is included in the checkpoint. 
`timestamp_millis`

     (date) The timestamp of the checkpoint, which indicates when the checkpoint was created. 

`last_search_time`

     (date) The timestamp of the last search in the source indices. This field is only shown if the transform is running. 

`next`

    

(对象)包含有关当前正在进行的下一个检查点的统计信息。仅当转换"状态"为"索引"时，才会显示此对象。

"下一个"的属性

`checkpoint`

     (integer) The sequence number for the checkpoint. 
`checkpoint_progress`

     (object) Contains statistics about the progress of the checkpoint. For example, it lists the `total_docs`, `docs_remaining`, `percent_complete`, `docs_processed`, and `docs_indexed`. This information is available only for batch transforms and the first checkpoint of continuous transforms. 
`time_upper_bound_millis`

     (date) When using time-based synchronization, this timestamp indicates the upper bound of data that is included in the checkpoint. 
`timestamp_millis`

     (date) The timestamp of the checkpoint, which indicates when the checkpoint was created. 

`operations_behind`

     (integer) The number of operations that have occurred on the source index but have not been applied to the destination index yet. A high number can indicate that the transform is failing to keep up. 

`health`

    

(对象)此转换的运行状况指示器。

"健康"的属性

`status`

    

(字符串)此转换的运行状况。状态为：

* "绿色"：转换正常。  * "未知"：无法确定转换的运行状况。  * "黄色"：转换的功能处于降级状态，可能需要修正以避免运行状况变为"红色"。  * "红色"：转换遇到中断或无法使用。

`issues`

    

(可选，数组)如果返回非正常状态，则包含转换的问题列表。

"问题"的属性

`issue`

     (string) A description of the issue. 
`details`

     (Optional, string) Details about the issue. 
`count`

     (integer) Number of times the issue has occured since it started. 
`first_occurrence`

     (Optional, date) The timestamp this issue occured for the first time. 

`id`

     (string) Identifier for the transform. 

`node`

    

(对象)仅对于已启动的转换，为启动转换的节点。

"节点"的属性

`attributes`

     (object) A list of attributes for the node. 
`ephemeral_id`

     (string) The node ephemeral ID. 
`id`

     (string) The unique identifier of the node. For example, "0-o0tOoRTwKFZifatTWKNw". 
`name`

     (string) The node name. For example, `0-o0tOo`. 
`transport_address`

     (string) The host and port where transport HTTP connections are accepted. For example, `127.0.0.1:9300`. 

`reason`

     (string) If a transform has a `failed` state, this property provides details about the reason for the failure. 
`state`

    

(字符串)转换的状态，可以是以下值之一：

* "正在中止"：转换正在中止。  * "失败"：转换失败。有关失败的详细信息，请检查原因字段。  * "索引"：转换正在主动处理数据并创建新文档。  * "started"：转换正在运行，但未主动索引数据。  * "停止"：转换已停止。  * "停止"：转换正在停止。

`stats`

    

(对象)提供有关转换的统计信息的对象。

"统计"的属性

`delete_time_in_ms`

     (long) The amount of time spent deleting, in milliseconds. 
`documents_deleted`

     (long) The number of documents that have been deleted from the destination index due to the retention policy for this transform. 
`documents_indexed`

     (long) The number of documents that have been indexed into the destination index for the transform. 
`documents_processed`

     (long) The number of documents that have been processed from the source index of the transform. 
`exponential_avg_checkpoint_duration_ms`

     (double) Exponential moving average of the duration of the checkpoint, in milliseconds. 
`exponential_avg_documents_indexed`

     (double) Exponential moving average of the number of new documents that have been indexed. 
`exponential_avg_documents_processed`

     (double) Exponential moving average of the number of documents that have been processed. 
`index_failures`

     (long) The number of indexing failures. 
`index_time_in_ms`

     (long) The amount of time spent indexing, in milliseconds. 
`index_total`

     (long) The number of index operations. 
`pages_processed`

     (long) The number of search or bulk index operations processed. Documents are processed in batches instead of individually. 
`processing_time_in_ms`

     (long) The amount of time spent processing results, in milliseconds. 
`processing_total`

     (long) The number of processing operations. 
`search_failures`

     (long) The number of search failures. 
`search_time_in_ms`

     (long) The amount of time spent searching, in milliseconds. 
`search_total`

     (long) The number of search operations on the source index for the transform. 
`trigger_count`

     (long) The number of times the transform has been triggered by the scheduler. For example, the scheduler triggers the transform indexer to check for updates or ingest new data at an interval specified in the [`frequency` property](put-transform.html#put-transform-request-body "Request body"). 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

以下示例跳过前五个转换，并获取最多十个结果的使用情况信息：

    
    
    response = client.indices.get(
      index: '_transform',
      from: 5,
      size: 10
    )
    puts response
    
    
    GET _transform/_stats?from=5&size=10

以下示例获取转换的使用情况信息：

    
    
    response = client.transform.get_transform_stats(
      transform_id: 'ecommerce-customer-transform'
    )
    puts response
    
    
    GET _transform/ecommerce-customer-transform/_stats

API 返回以下结果：

    
    
    {
      "count" : 1,
      "transforms" : [
        {
          "id" : "ecommerce-customer-transform",
          "state" : "started",
          "node" : {
            "id" : "cpTIGMsVQ8Gqwqlxxxxxxx",
            "name" : "my.home",
            "ephemeral_id" : "5-L21nFsQxxxxxxxxxx-xx",
            "transport_address" : "127.0.0.1:9300",
            "attributes" : { }
          },
          "stats" : {
            "pages_processed" : 78,
            "documents_processed" : 6027,
            "documents_indexed" : 68,
            "documents_deleted": 22,
            "delete_time_in_ms": 214,
            "trigger_count" : 168,
            "index_time_in_ms" : 412,
            "index_total" : 20,
            "index_failures" : 0,
            "search_time_in_ms" : 353,
            "search_total" : 78,
            "search_failures" : 0,
            "processing_time_in_ms" : 8,
            "processing_total" : 78,
            "exponential_avg_checkpoint_duration_ms" : 97.30637923893185,
            "exponential_avg_documents_indexed" : 2.2064915040974062,
            "exponential_avg_documents_processed" : 179.89419945785045
          },
          "checkpointing" : {
            "last" : {
              "checkpoint" : 20,
              "timestamp_millis" : 1585344558220,
              "time_upper_bound_millis" : 1585344498220
            },
            "changes_last_detected_at" : 1585344558219
          },
          "health": {
            "status": "green"
          }
        }
      ]
    }

[« Get transforms API](get-transform.md) [Preview transform API »](preview-
transform.md)
