

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat shards API](cat-shards.md) [cat task management API »](cat-
tasks.md)

## 猫快照接口

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取快照 API。

返回有关存储在一个或多个存储库中的快照的信息。快照是 anindex 或正在运行的 Elasticsearch 集群的备份。

###Request

'获取/_cat/快照/<repository>'

"获取/_cat/快照"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"monitor_snapshot"、"create_snapshot"或"管理"集群权限才能使用此 API。

### 路径参数

`<repository>`

    

(可选，字符串)用于限制请求的快照存储库的逗号分隔列表。接受通配符表达式。"_all"返回所有存储库。

如果任何存储库在请求期间失败，Elasticsearch 将返回错误。

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将按下面列出的顺序返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

"id"、"快照"

     (Default) ID of the snapshot, such as `snap1`. 
`repository`, `re`, `repo`

     (Default) Name of the repository, such as `repo1`. 
`status`, `s`

    

(默认)快照进程的状态。返回的值为：

* "失败"：快照过程失败。  * "不兼容"：快照过程与当前集群版本不兼容。  * "IN_PROGRESS"：快照过程已开始但尚未完成。  * "部分"：快照过程部分成功完成。  * "成功"：快照过程完全成功完成。

"start_epoch"、"ste"、"startEpoch"

     (Default) [Unix `epoch` time](https://en.wikipedia.org/wiki/Unix_time) at which the snapshot process started. 
`start_time`, `sti`, `startTime`

     (Default) `HH:MM:SS` time at which the snapshot process started. 
`end_epoch`, `ete`, `endEpoch`

     (Default) [Unix `epoch` time](https://en.wikipedia.org/wiki/Unix_time) at which the snapshot process ended. 
`end_time`, `eti`, `endTime`

     (Default) `HH:MM:SS` time at which the snapshot process ended. 
`duration`, `dur`

     (Default) Time it took the snapshot process to complete in [time units](api-conventions.html#time-units "Time units"). 
`indices`, `i`

     (Default) Number of indices in the snapshot. 
`successful_shards`, `ss`

     (Default) Number of successful shards in the snapshot. 
`failed_shards`, `fs`

     (Default) Number of failed shards in the snapshot. 
`total_shards`, `ts`

     (Default) Total number of shards in the snapshot. 
`reason`, `r`

     Reason for any snapshot failures. 

`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`ignore_unavailable`

     (Optional, Boolean) If `true`, the response does not include information from unavailable snapshots. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    GET /_cat/snapshots/repo1?v=true&s=id

API 返回以下响应：

    
    
    id     repository status start_epoch start_time end_epoch  end_time duration indices successful_shards failed_shards total_shards
    snap1  repo1      FAILED 1445616705  18:11:45   1445616978 18:16:18     4.6m       1                 4             1            5
    snap2  repo1      SUCCESS 1445634298  23:04:58   1445634672 23:11:12     6.2m       2                10             0           10

[« cat shards API](cat-shards.md) [cat task management API »](cat-
tasks.md)
