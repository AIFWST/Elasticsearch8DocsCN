

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md) ›[Register a snapshot
repository](snapshots-register-repository.md)

[« S3 repository](repository-s3.md) [Read-only URL repository »](snapshots-
read-only-repository.md)

## 共享文件系统存储库

此存储库类型仅在您自己的硬件上运行 Elasticsearch 时才可用。如果您使用 Elasticsearch Service，请参阅 Elasticsearch Servicerepository 类型。

使用共享文件系统存储库将快照存储在共享文件系统上。

要注册共享文件系统存储库，请先将文件系统挂载到所有主节点和数据节点上的同一位置。然后将文件系统的路径或父目录添加到每个主节点和数据节点的"elasticsearch.yml"中的"path.repo"设置中。对于正在运行的群集，这需要对每个节点进行滚动重启。

支持的"path.repo"值因平台而异：

类Unix系统窗口

Linux 和 macOS 安装支持 Unix 样式的路径：

    
    
    path:
      repo:
        - /mount/backups
        - /mount/long_term_backups

重新启动每个节点后，使用 Kibana 或创建快照存储库 API 注册存储库。注册存储库时，请指定文件系统的路径：

    
    
    PUT _snapshot/my_fs_backup
    {
      "type": "fs",
      "settings": {
        "location": "/mount/backups/my_fs_backup_location"
      }
    }

如果指定相对路径，Elasticsearch 将使用 'path.repo' 设置中的第一个值解析路径。

    
    
    response = client.snapshot.create_repository(
      repository: 'my_fs_backup',
      body: {
        type: 'fs',
        settings: {
          location: 'my_fs_backup_location'
        }
      }
    )
    puts response
    
    
    PUT _snapshot/my_fs_backup
    {
      "type": "fs",
      "settings": {
        "location": "my_fs_backup_location"        __}
    }

__

|

"path.repo"设置中的第一个值是"/mount/backups"。此相对路径"my_fs_backup_location"解析为"/mount/backups/my_fs_backup_location"。   ---|--- 集群应仅注册一次特定的快照存储库存储桶。如果将同一快照存储库注册到多个集群，则只有一个集群应具有对该存储库的写入访问权限。在其他集群上，将存储库注册为只读。

这可以防止多个集群同时写入存储库并损坏存储库的内容。它还阻止 Elasticsearch 缓存存储库的内容，这意味着其他集群所做的更改将立即可见。

要使用创建快照存储库 API 将文件系统存储库注册为只读，请将"只读"参数设置为 true。或者，您可以为文件系统注册 URL 存储库。

    
    
    response = client.snapshot.create_repository(
      repository: 'my_fs_backup',
      body: {
        type: 'fs',
        settings: {
          location: 'my_fs_backup_location',
          readonly: true
        }
      }
    )
    puts response
    
    
    PUT _snapshot/my_fs_backup
    {
      "type": "fs",
      "settings": {
        "location": "my_fs_backup_location",
        "readonly": true
      }
    }

Windows 安装同时支持 DOS 和 Microsoft UNC 路径。转义路径中的任何反斜杠。对于 UNC 路径，请提供服务器和共享名称作为前缀。

    
    
    path:
      repo:
        - "E:\\Mount\\Backups"                      __- "\\\\MY_SERVER\\Mount\\Long_term_backups" __

__

|

DOS 路径 ---|--- __

|

UNC 路径 重新启动每个节点后，使用 Kibana 或创建快照存储库 API 注册存储库。注册存储库时，请指定文件系统的路径：

    
    
    response = client.snapshot.create_repository(
      repository: 'my_fs_backup',
      body: {
        type: 'fs',
        settings: {
          location: 'E:\\Mount\\Backups\\My_fs_backup_location'
        }
      }
    )
    puts response
    
    
    PUT _snapshot/my_fs_backup
    {
      "type": "fs",
      "settings": {
        "location": "E:\\Mount\\Backups\\My_fs_backup_location"
      }
    }

如果指定相对路径，Elasticsearch 将使用 'path.repo' 设置中的第一个值解析路径。

    
    
    response = client.snapshot.create_repository(
      repository: 'my_fs_backup',
      body: {
        type: 'fs',
        settings: {
          location: 'My_fs_backup_location'
        }
      }
    )
    puts response
    
    
    PUT _snapshot/my_fs_backup
    {
      "type": "fs",
      "settings": {
        "location": "My_fs_backup_location"        __}
    }

__

|

"path.repo"设置中的第一个值是"E：\Mount\Backups"。此相对路径"My_fs_backup_location"解析为"E：\Mount\Backups\My_fs_backup_location"。   ---|--- 集群应仅注册一次特定的快照存储库存储桶。如果将同一快照存储库注册到多个集群，则只有一个集群应具有对该存储库的写入访问权限。在其他集群上，将存储库注册为只读。

这可以防止多个集群同时写入存储库并损坏存储库的内容。它还阻止 Elasticsearch 缓存存储库的内容，这意味着其他集群所做的更改将立即可见。

要使用创建快照存储库 API 将文件系统存储库注册为只读，请将"只读"参数设置为 true。或者，您可以为文件系统注册 URL 存储库。

    
    
    response = client.snapshot.create_repository(
      repository: 'my_fs_backup',
      body: {
        type: 'fs',
        settings: {
          location: 'my_fs_backup_location',
          readonly: true
        }
      }
    )
    puts response
    
    
    PUT _snapshot/my_fs_backup
    {
      "type": "fs",
      "settings": {
        "location": "my_fs_backup_location",
        "readonly": true
      }
    }

### 存储库设置

`chunk_size`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Maximum size of files in snapshots. In snapshots, files larger than this are broken down into chunks of this size or smaller. Defaults to `null` (unlimited file size). 
`compress`

     (Optional, Boolean) If `true`, metadata files, such as index mappings and settings, are compressed in snapshots. Data files are not compressed. Defaults to `true`. 
`location`

     (Required, string) Location of the shared filesystem used to store and retrieve snapshots. This location must be registered in the `path.repo` setting on all master and data nodes in the cluster. 
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

### 共享文件系统存储库疑难解答

Elasticsearch 使用操作系统中的文件系统抽象与共享文件系统存储库进行交互。这意味着每个 Elasticsearch 节点都必须能够在存储库路径中执行操作，例如创建、打开和重命名文件，以及创建和列出目录，并且一个节点执行的操作必须在完成后立即对其他节点可见。

使用验证快照存储库 API 和存储库分析 API 检查常见的错误配置。正确配置存储库后，这些 API 将成功完成。如果验证存储库或存储库分析 API 报告了问题，那么您可以通过直接在文件系统上执行类似的操作来在 Elasticsearch 之外重现此问题。

如果验证存储库或存储库分析 API 失败并显示错误，指示权限不足，请在操作系统中调整存储库的配置，以便为 Elasticsearch 提供适当的访问级别。要直接重现此类问题，请在运行 Elasticsearch 的同一安全上下文中执行与 Elasticsearch 相同的操作。例如，在 Linux 上，使用诸如"su"之类的命令切换到运行 Elasticsearch 的用户。

如果验证存储库或存储库分析 API 失败并显示错误，指示一个节点上的操作在另一个节点上不立即可见，请在操作系统中调整存储库的配置以解决此问题。如果您的存储库不能配置足够强大的可见性保证，那么它不适合用作 Elasticsearch 快照存储库。

如果操作系统在访问存储库时返回任何其他类型的 I/O 错误，则验证存储库和存储库分析 API 也将失败。如果发生这种情况，请解决操作系统报告的 I/O 错误的原因。

许多 NFS 实现使用其_numeric_user ID (UID) 和组 ID (GID) 而不是其名称来跨节点匹配帐户。Elasticsearch 可以在每个节点上以相同名称的帐户(通常为"elasticsearch")运行，但这些帐户具有不同的数字用户或组 ID。如果您的共享文件系统使用 NFS，请确保每个节点都使用相同的数字 UID 和 GID 运行，或者更新您的 NFS 配置以考虑节点间数字 ID 的差异。

[« S3 repository](repository-s3.md) [Read-only URL repository »](snapshots-
read-only-repository.md)
