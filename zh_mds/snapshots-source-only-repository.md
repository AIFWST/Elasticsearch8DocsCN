

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md) ›[Register a snapshot
repository](snapshots-register-repository.md)

[« Read-only URL repository](snapshots-read-only-repository.md) [Create a
snapshot »](snapshots-take-snapshot.md)

## 仅源代码存储库

您可以使用仅源存储库拍摄最少的仅源快照，这些快照使用的磁盘空间比常规快照少 50%。

与其他存储库类型不同，仅源存储库不直接存储快照。它将存储委托给另一个已注册的快照存储库。

当您使用仅源存储库拍摄快照时，Elasticsearch 会在委派存储库中创建仅源快照。此快照仅包含存储的字段和元数据。它不包括索引或文档值结构，并且在还原时无法立即搜索。要搜索其中存储的数据，首先必须将其重新索引到新的数据流或索引中。

仅当启用了"_source"字段且未应用源筛选时，才支持仅源快照。还原仅源快照时：

* 恢复的索引是只读的，只能提供"match_all"搜索或滚动请求以启用重新索引。  * 不支持"match_all"和"_get"请求以外的查询。  * 恢复索引的映射为空，但原始映射可从类型顶级"meta"元素获得。

在注册纯源存储库之前，请使用 Kibana 或创建快照存储库 API 注册其他类型的快照存储库以用于存储。然后注册仅源存储库并在请求中指定委派存储库。

    
    
    response = client.snapshot.create_repository(
      repository: 'my_src_only_repository',
      body: {
        type: 'source',
        settings: {
          delegate_type: 'fs',
          location: 'my_backup_repository'
        }
      }
    )
    puts response
    
    
    PUT _snapshot/my_src_only_repository
    {
      "type": "source",
      "settings": {
        "delegate_type": "fs",
        "location": "my_backup_repository"
      }
    }

### 存储库设置

`chunk_size`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Maximum size of files in snapshots. In snapshots, files larger than this are broken down into chunks of this size or smaller. Defaults to `null` (unlimited file size). 
`compress`

     (Optional, Boolean) If `true`, metadata files, such as index mappings and settings, are compressed in snapshots. Data files are not compressed. Defaults to `true`. 
`delegate_type`

    

(可选，字符串)委派存储库类型。有关有效值，请参阅"类型"参数。

"源"存储库可以使用其委派存储库类型的"设置"属性。请参阅仅源存储库。

`max_number_of_snapshots`

     (Optional, integer) Maximum number of snapshots the repository can contain. Defaults to `Integer.MAX_VALUE`, which is `2^31-1` or `2147483647`. 
`max_restore_bytes_per_sec`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Maximum snapshot restore rate per node. Defaults to unlimited. Note that restores are also throttled through [recovery settings](recovery.html "Index recovery settings"). 
`max_snapshot_bytes_per_sec`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Maximum snapshot creation rate per node. Defaults to `40mb` per second. Note that if the [recovery settings for managed services](recovery.html#recovery-settings-for-managed-services "Recovery settings for managed services") are set, then it defaults to unlimited, and the rate is additionally throttled through [recovery settings](recovery.html "Index recovery settings"). 

`readonly`

    

(可选，布尔值)如果为"true"，则存储库为只读。集群可以从存储库检索和还原快照，但不能写入存储库或在其中创建快照。

只有具有写入权限的集群才能在存储库中创建快照。连接到存储库的所有其他集群应将"只读"参数设置为"true"。

如果为"false"，则集群可以写入存储库并在 init 中创建快照。默认为"假"。

如果将同一快照存储库注册到多个集群，则只有一个集群应具有对该存储库的写入权限。让多个集群同时写入存储库可能会损坏存储库的内容。

[« Read-only URL repository](snapshots-read-only-repository.md) [Create a
snapshot »](snapshots-take-snapshot.md)
