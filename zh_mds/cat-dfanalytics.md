

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat count API](cat-count.md) [cat datafeeds API »](cat-datafeeds.md)

## 猫数据帧分析API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取数据帧分析作业统计信息 API。

返回有关数据帧分析作业的配置和使用情况信息。

###Request

'GET /_cat/ml/data_frame/analytics/<data_frame_analytics_id>'

'GET /_cat/ml/data_frame/analytics'

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有以下权限：

* 集群："monitor_ml"

有关详细信息，请参阅安全特权和机器学习安全特权。

### 路径参数

`<data_frame_analytics_id>`

     (Optional, string) Identifier for the data frame analytics job. If you do not specify this option, the API returns information for the first hundred data frame analytics jobs. 

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

"assignment_explanation"、"ae"

     Contains messages relating to the selection of a node. 
`create_time`, `ct`, `createTime`

     (Default) The time when the data frame analytics job was created. 
`description`, `d`

     A description of the job. 
`dest_index`, `di`, `destIndex`

     Name of the destination index. 
`failure_reason`, `fr`, `failureReason`

     Contains messages about the reason why a data frame analytics job failed. 
`id`

     (Default) Identifier for the data frame analytics job. 
`model_memory_limit`, `mml`, `modelMemoryLimit`

     The approximate maximum amount of memory resources that are permitted for the data frame analytics job. 
`node.address`, `na`, `nodeAddress`

     The network address of the node that the data frame analytics job is assigned to. 
`node.ephemeral_id`, `ne`, `nodeEphemeralId`

     The ephemeral ID of the node that the data frame analytics job is assigned to. 
`node.id`, `ni`, `nodeId`

     The unique identifier of the node that the data frame analytics job is assigned to. 
`node.name`, `nn`, `nodeName`

     The name of the node that the data frame analytics job is assigned to. 
`progress`, `p`

     The progress report of the data frame analytics job by phase. 
`source_index`, `si`, `sourceIndex`

     Name of the source index. 
`state`, `s`

     (Default) Current state of the data frame analytics job. 
`type`, `t`

     (Default) The type of analysis that the data frame analytics job performs. 
`version`, `v`

     The Elasticsearch version number in which the data frame analytics job was created. 

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    response = client.cat.ml_data_frame_analytics(
      v: true
    )
    puts response
    
    
    GET _cat/ml/data_frame/analytics?v=true
    
    
    id               create_time              type             state
    classifier_job_1 2020-02-12T11:49:09.594Z classification stopped
    classifier_job_2 2020-02-12T11:49:14.479Z classification stopped
    classifier_job_3 2020-02-12T11:49:16.928Z classification stopped
    classifier_job_4 2020-02-12T11:49:19.127Z classification stopped
    classifier_job_5 2020-02-12T11:49:21.349Z classification stopped

[« cat count API](cat-count.md) [cat datafeeds API »](cat-datafeeds.md)
