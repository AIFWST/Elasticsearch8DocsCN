

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md) ›[Register a snapshot
repository](snapshots-register-repository.md)

[« Shared file system repository](snapshots-filesystem-repository.md)
[Source-only repository »](snapshots-source-only-repository.md)

## 只读网址存储库

此存储库类型仅在您自己的硬件上运行 Elasticsearch 时才可用。如果您使用 Elasticsearch Service，请参阅 Elasticsearch Servicerepository 类型。

您可以使用 URL 存储库向集群授予对共享文件系统的只读访问权限。由于 URL 存储库始终是只读的，因此与注册只读共享文件系统存储库相比，它们是更安全、更方便的替代方法。

使用 Kibana 或创建快照存储库 API 注册 URL 存储库。

    
    
    PUT _snapshot/my_read_only_url_repository
    {
      "type": "url",
      "settings": {
        "url": "file:/mount/backups/my_fs_backup_location"
      }
    }

### 存储库设置

`chunk_size`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Maximum size of files in snapshots. In snapshots, files larger than this are broken down into chunks of this size or smaller. Defaults to `null` (unlimited file size). 
`http_max_retries`

     (Optional, integer) Maximum number of retries for `http` and `https` URLs. Defaults to `5`. 
`http_socket_timeout`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Maximum wait time for data transfers over a connection. Defaults to `50s`. 
`compress`

     (Optional, Boolean) If `true`, metadata files, such as index mappings and settings, are compressed in snapshots. Data files are not compressed. Defaults to `true`. 
`max_number_of_snapshots`

     (Optional, integer) Maximum number of snapshots the repository can contain. Defaults to `Integer.MAX_VALUE`, which is `2^31-1` or `2147483647`. 
`max_restore_bytes_per_sec`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Maximum snapshot restore rate per node. Defaults to unlimited. Note that restores are also throttled through [recovery settings](recovery.html "Index recovery settings"). 
`max_snapshot_bytes_per_sec`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Maximum snapshot creation rate per node. Defaults to `40mb` per second. Note that if the [recovery settings for managed services](recovery.html#recovery-settings-for-managed-services "Recovery settings for managed services") are set, then it defaults to unlimited, and the rate is additionally throttled through [recovery settings](recovery.html "Index recovery settings"). 
`url`

    

(必需，字符串)共享文件系统存储库根目录的 URL 位置。支持以下协议：

* 'file' * 'ftp' * 'http' * 'https' * 'jar'

使用"http"、"https"或"ftp"协议的网址必须明确允许使用"repositories.url.allowed_urls"群集设置。此设置支持在 URL 中代替主机、路径、查询或片段的通配符。

使用"file"协议的 URL 必须指向集群中所有主节点和数据节点均可访问的共享文件系统的位置。必须在"path.repo"设置中注册此位置。您无需在"path.repo"设置中使用"ftp"、"http"、"https"或"jar"协议注册 URL。

[« Shared file system repository](snapshots-filesystem-repository.md)
[Source-only repository »](snapshots-source-only-repository.md)
