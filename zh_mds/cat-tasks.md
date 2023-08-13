

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat snapshots API](cat-snapshots.md) [cat templates API »](cat-
templates.md)

## 猫任务管理接口

cat 任务管理 API 是新的，仍应被视为测试功能。API 可能会以不向后兼容的方式更改。有关功能状态，请参阅#51628。

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用任务管理 API。

返回有关群集中当前执行的任务的信息，类似于任务管理 API。

###Request

"获取/_cat/任务"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

cat 任务管理 API 返回有关当前在群集中的一个或多个节点上执行的任务的信息。它是 JSON 任务管理 API 的更紧凑视图。

### 查询参数

`detailed`

     (Optional, Boolean) If `true`, the response includes detailed information about shard recoveries. Defaults to `false`. 
`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`nodes`

     (Optional, string) Comma-separated list of node IDs or names used to limit the response. Supports wildcard (`*`) expressions. 
`parent_task_id`

     (Optional, string) Parent task ID used to limit the response. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

### 响应码

"404"(缺少资源)

     If `<task_id>` is specified but not found, this code indicates that there are no resources that match the request. 

###Examples

    
    
    response = client.cat.tasks(
      v: true
    )
    puts response
    
    
    GET _cat/tasks?v=true

API 返回以下响应：

    
    
    action                         task_id                    parent_task_id             type      start_time    timestamp running_time ip             node
    cluster:monitor/tasks/lists[n] oTUltX4IQMOUUVeiohTt8A:124 oTUltX4IQMOUUVeiohTt8A:123 direct    1458585884904 01:48:24  44.1micros   127.0.0.1:9300 oTUltX4IQMOUUVeiohTt8A
    cluster:monitor/tasks/lists    oTUltX4IQMOUUVeiohTt8A:123 -                          transport 1458585884904 01:48:24  186.2micros  127.0.0.1:9300 oTUltX4IQMOUUVeiohTt8A

[« cat snapshots API](cat-snapshots.md) [cat templates API »](cat-
templates.md)
