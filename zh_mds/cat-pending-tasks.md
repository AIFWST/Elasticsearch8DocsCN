

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat nodes API](cat-nodes.md) [cat plugins API »](cat-plugins.md)

## 猫待处理任务API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用挂起的群集任务 API。

返回尚未执行的群集级别更改，类似于挂起的群集任务 API。

###Request

"获取/_cat/pending_tasks"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    response = client.cat.pending_tasks(
      v: true
    )
    puts response
    
    
    GET /_cat/pending_tasks?v=true

API 返回以下响应：

    
    
    insertOrder timeInQueue priority source
           1685       855ms HIGH     update-mapping [foo][t]
           1686       843ms HIGH     update-mapping [foo][t]
           1693       753ms HIGH     refresh-mapping [foo][[t]]
           1688       816ms HIGH     update-mapping [foo][t]
           1689       802ms HIGH     update-mapping [foo][t]
           1690       787ms HIGH     update-mapping [foo][t]
           1691       773ms HIGH     update-mapping [foo][t]

[« cat nodes API](cat-nodes.md) [cat plugins API »](cat-plugins.md)
