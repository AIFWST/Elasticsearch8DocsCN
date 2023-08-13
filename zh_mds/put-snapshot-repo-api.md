

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Snapshot and restore APIs](snapshot-restore-apis.md) [Verify snapshot
repository API »](verify-snapshot-repo-api.md)

## 创建或更新快照存储库API

注册或更新快照存储库。

    
    
    response = client.snapshot.create_repository(
      repository: 'my_repository',
      body: {
        type: 'fs',
        settings: {
          location: 'my_backup_location'
        }
      }
    )
    puts response
    
    
    PUT /_snapshot/my_repository
    {
      "type": "fs",
      "settings": {
        "location": "my_backup_location"
      }
    }

###Request

"放/_snapshot/<repository>"

"发布/_snapshot/<repository>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

* 要注册快照存储库，集群的全局元数据必须是可写的。确保没有任何阻止写入访问的群集块。

### 路径参数

`<repository>`

     (Required, string) Name of the snapshot repository to register or update. 

### 查询参数

可以使用查询参数或请求正文参数指定此 API 的多个选项。如果同时指定了这两个参数，则仅使用查询参数。

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`verify`

    

(可选，布尔值)如果为"true"，则请求将验证存储库在群集中的所有主节点和数据节点上是否正常运行。如果为"false"，则跳过此验证。默认为"真"。

您可以使用验证快照存储库 API 手动执行此验证。

### 请求正文

`type`

    

(必需，字符串)存储库类型。

"类型"的有效值

`azure`

     [Azure repository](repository-azure.html "Azure repository")
`gcs`

     [Google Cloud Storage repository](repository-gcs.html "Google Cloud Storage repository")
`s3`

     [S3 repository](repository-s3.html "S3 repository")
`fs`

     [Shared file system repository](snapshots-filesystem-repository.html "Shared file system repository")
`source`

     [Source-only repository](snapshots-source-only-repository.html "Source-only repository")
`url`

     [Read-only URL repository](snapshots-read-only-repository.html "Read-only URL repository")

其他存储库类型可通过官方插件获得：

`hdfs`

     [Hadoop Distributed File System (HDFS) repository](/guide/en/elasticsearch/plugins/8.9/repository-hdfs.html)

`settings`

    

(必填，对象)存储库的设置。支持的设置因存储库类型而异：

* Azure 存储库 * Google Cloud Storage 存储库 * S3 存储库 * 共享文件系统存储库 * 只读 URL 存储库 * 仅源代码存储库

其他存储库类型可通过官方插件获得：

* Hadoop 分布式文件系统 (HDFS) 存储库

`verify`

    

(可选，布尔值)如果为"true"，则请求将验证存储库在群集中的所有主节点和数据节点上是否正常运行。如果为"false"，则跳过此验证。默认为"真"。

您可以使用验证快照存储库 API 手动执行此验证。

[« Snapshot and restore APIs](snapshot-restore-apis.md) [Verify snapshot
repository API »](verify-snapshot-repo-api.md)
