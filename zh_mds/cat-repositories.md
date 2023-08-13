

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat recovery API](cat-recovery.md) [cat segments API »](cat-
segments.md)

## 猫存储库API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取快照存储库 API。

返回群集的快照存储库。

###Request

'获取/_cat/存储库'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"monitor_snapshot"、"create_snapshot"或"管理"集群权限才能使用此 API。

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
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    response = client.cat.repositories(
      v: true
    )
    puts response
    
    
    GET /_cat/repositories?v=true

API 返回以下响应：

    
    
    id    type
    repo1   fs
    repo2   s3

[« cat recovery API](cat-recovery.md) [cat segments API »](cat-
segments.md)
