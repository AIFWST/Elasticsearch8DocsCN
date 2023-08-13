

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Repository analysis API](repo-analysis-api.md) [Delete snapshot
repository API »](delete-snapshot-repo-api.md)

## 获取快照存储库API

获取有关一个或多个已注册快照存储库的信息。

    
    
    response = client.snapshot.get_repository(
      repository: 'my_repository'
    )
    puts response
    
    
    GET /_snapshot/my_repository

###Request

"获取/_snapshot/<repository>"

"获取/_snapshot"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"monitor_snapshot"、"create_snapshot"或"管理"集群权限才能使用此 API。

### 路径参数

`<repository>`

    

(可选，字符串)用于限制请求的快照存储库名称的逗号分隔列表。支持通配符 ('*') 表达式，包括将通配符与以 '-' 开头的排除模式组合在一起。

要获取有关集群中注册的所有快照存储库的信息，请省略此参数或使用"*"或"_all"。

### 查询参数

`local`

     (Optional, Boolean) If `true`, the request gets information from the local node only. If `false`, the request gets information from the master node. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 响应正文

`<repository>`

    

(对象)包含有关快照存储库的信息。键是快照存储库的名称。

""的属性<repository>

`type`

    

(字符串)存储库类型。

"类型"的值

`fs`

     Shared file system repository. See [Shared file system repository](snapshots-filesystem-repository.html "Shared file system repository"). 
`source`

     Source-only repository. See [Source-only repository](snapshots-source-only-repository.html "Source-only repository"). 
`url`

     URL repository. See [Read-only URL repository](snapshots-read-only-repository.html "Read-only URL repository"). 

更多存储库类型可通过这些官方插件获得：

* 用于 S3 存储库支持的存储库-S3 * Hadoop 环境中用于 HDFS 存储库支持的存储库-HDFS * 用于 Azure 存储库的存储库-Azure * 用于 Google Cloud 存储库的存储库-gcs

`settings`

    

(对象)包含存储库的设置。"settings"对象的有效属性取决于使用"type"参数设置的存储库类型。

有关属性，请参阅创建或更新快照存储库 API 的"设置"参数。

###Examples

    
    
    response = client.snapshot.get_repository(
      repository: 'my_repository'
    )
    puts response
    
    
    GET /_snapshot/my_repository

API 返回以下响应：

    
    
    {
      "my_repository" : {
        "type" : "fs",
        "uuid" : "0JLknrXbSUiVPuLakHjBrQ",
        "settings" : {
          "location" : "my_backup_location"
        }
      }
    }

[« Repository analysis API](repo-analysis-api.md) [Delete snapshot
repository API »](delete-snapshot-repo-api.md)
