

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md) ›[Register a snapshot
repository](snapshots-register-repository.md)

[« Register a snapshot repository](snapshots-register-repository.md) [Google
Cloud Storage repository »](repository-gcs.md)

## Azurerepository

可以使用 Azure Blob 存储作为快照/还原的存储库。

###Setup

若要启用 Azure 存储库，必须先将 Azure 存储设置定义为安全设置，然后再启动节点：

    
    
    bin/elasticsearch-keystore add azure.client.default.account
    bin/elasticsearch-keystore add azure.client.default.key

请注意，您还可以定义多个帐户：

    
    
    bin/elasticsearch-keystore add azure.client.default.account
    bin/elasticsearch-keystore add azure.client.default.key
    bin/elasticsearch-keystore add azure.client.secondary.account
    bin/elasticsearch-keystore add azure.client.secondary.sas_token

有关这些设置的详细信息，请参阅客户端设置。

### 支持的 Azure 存储帐户类型

Azure 存储库类型适用于所有标准存储帐户

* 标准本地冗余存储 - "Standard_LRS" * 标准区域冗余存储 - "Standard_ZRS" * 标准异地冗余存储 - "Standard_GRS" * 标准读取访问异地冗余存储 - "Standard_RAGRS"

高级本地冗余存储 ("Premium_LRS") 不受支持，因为它只能用作 VM 磁盘存储，不能用作常规存储。

### 客户端设置

用于连接到 Azure 的客户端有许多可用的设置。这些设置的格式为"azure.client.CLIENT_NAME。SETTING_NAME'。默认情况下，"azure"存储库使用名为"default"的客户端，但可以使用存储库设置"client"进行修改。例如：

    
    
    PUT _snapshot/my_backup
    {
      "type": "azure",
      "settings": {
        "client": "secondary"
      }
    }

大多数客户端设置都可以添加到"elasticsearch.yml"配置文件中。例如：

    
    
    azure.client.default.timeout: 10s
    azure.client.default.max_retries: 7
    azure.client.default.endpoint_suffix: core.chinacloudapi.cn
    azure.client.secondary.timeout: 30s

在此示例中，对于"默认"帐户，每次尝试的客户端超时为"10s"，重试次数为"7"，然后失败。端点后缀为"core.chinacloudapi.cn"，对于重试次数为"3"的"辅助"帐户，每次尝试为"30s"。

"帐户"、"密钥"和"sas_token"存储设置是可重新加载的安全设置，您可以将其添加到 Elasticsearch 密钥库中。有关创建和更新 Elasticsearch 密钥库的更多信息，请参阅安全设置。重新加载设置后，用于传输快照的内部 Azure 客户端将使用密钥库中的最新设置。

正在进行的快照或还原作业不会被存储安全设置的"重新加载"抢占。他们将使用操作开始时构建的客户端完成。

以下列表包含可用的客户端设置。那些必须存储在密钥库中的密钥被标记为"安全";其他设置属于"elasticsearch.yml"文件。

"帐户"(安全，可重新加载)

     The Azure account name, which is used by the repository's internal Azure client. 
`endpoint_suffix`

     The Azure endpoint suffix to connect to. The default value is `core.windows.net`. 
`key` ([Secure](/guide/en/elasticsearch/reference/8.9/secure-settings.html),
[reloadable](/guide/en/elasticsearch/reference/8.9/secure-
settings.html#reloadable-secure-settings))

     The Azure secret key, which is used by the repository's internal Azure client. Alternatively, use `sas_token`. 
`max_retries`

     The number of retries to use when an Azure request fails. This setting helps control the exponential backoff policy. It specifies the number of retries that must occur before the snapshot fails. The default value is `3`. The initial backoff period is defined by Azure SDK as `30s`. Thus there is `30s` of wait time before retrying after a first timeout or failure. The maximum backoff period is defined by Azure SDK as `90s`. 
`proxy.host`

     The host name of a proxy to connect to Azure through. For example: `azure.client.default.proxy.host: proxy.host`. 
`proxy.port`

     The port of a proxy to connect to Azure through. For example, `azure.client.default.proxy.port: 8888`. 
`proxy.type`

     Register a proxy type for the client. Supported values are `direct`, `http`, and `socks`. For example: `azure.client.default.proxy.type: http`. When `proxy.type` is set to `http` or `socks`, `proxy.host` and `proxy.port` must also be provided. The default value is `direct`. 
`sas_token` ([Secure](/guide/en/elasticsearch/reference/8.9/secure-
settings.html), [reloadable](/guide/en/elasticsearch/reference/8.9/secure-
settings.html#reloadable-secure-settings))

     A shared access signatures (SAS) token, which the repository's internal Azure client uses for authentication. The SAS token must have read (r), write (w), list (l), and delete (d) permissions for the repository base path and all its contents. These permissions must be granted for the blob service (b) and apply to resource types service (s), container (c), and object (o). Alternatively, use `key`. 
`timeout`

     The client side timeout for any single request to Azure. The value should specify the time unit. For example, a value of `5s` specifies a 5 second timeout. There is no default value, which means that Elasticsearch uses the [default value](https://azure.github.io/azure-storage-java/com/microsoft/azure/storage/RequestOptions.html#setTimeoutIntervalInMs\(java.lang.Integer\)) set by the Azure client (known as 5 minutes). This setting can be defined globally, per account, or both. 
`endpoint`

     The Azure endpoint to connect to. It must include the protocol used to connect to Azure. 
`secondary_endpoint`

     The Azure secondary endpoint to connect to. It must include the protocol used to connect to Azure. 

### 存储库设置

Azure 存储库支持以下设置：

`client`

     Azure named client to use. Defaults to `default`. 
`container`

     Container name. You must create the azure container before creating the repository. Defaults to `elasticsearch-snapshots`. 
`base_path`

    

指定容器中存储库数据的路径。默认为空(根目录)。

在为 Elastic CloudEnterprise 配置快照存储库时，请勿设置"base_path"。弹性云企业自动生成每个部署的"base_path"，以便多个部署可以共享同一个存储桶。

`chunk_size`

     Big files can be broken down into multiple smaller blobs in the blob store during snapshotting. It is not recommended to change this value from its default unless there is an explicit reason for limiting the size of blobs in the repository. Setting a value lower than the default can result in an increased number of API calls to the Azure blob store during snapshot create as well as restore operations compared to using the default value and thus make both operations slower as well as more costly. Specify the chunk size as a value and unit, for example: `10MB`, `5KB`, `500B`. Defaults to the maximum size of a blob in the Azure blob store which is `5TB`. 
`compress`

     When set to `true` metadata files are stored in compressed format. This setting doesn't affect index files that are already compressed by default. Defaults to `true`. 
`max_restore_bytes_per_sec`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Maximum snapshot restore rate per node. Defaults to unlimited. Note that restores are also throttled through [recovery settings](recovery.html "Index recovery settings"). 
`max_snapshot_bytes_per_sec`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Maximum snapshot creation rate per node. Defaults to `40mb` per second. Note that if the [recovery settings for managed services](recovery.html#recovery-settings-for-managed-services "Recovery settings for managed services") are set, then it defaults to unlimited, and the rate is additionally throttled through [recovery settings](recovery.html "Index recovery settings"). 

`readonly`

    

(可选，布尔值)如果为"true"，则存储库为只读。集群可以从存储库检索和还原快照，但不能写入存储库或在其中创建快照。

只有具有写入权限的集群才能在存储库中创建快照。连接到存储库的所有其他集群应将"只读"参数设置为"true"。

如果为"false"，则集群可以写入存储库并在 init 中创建快照。默认为"假"。

如果将同一快照存储库注册到多个集群，则只有一个集群应具有对该存储库的写入权限。让多个集群同时写入存储库可能会损坏存储库的内容。

`location_mode`

     `primary_only` or `secondary_only`. Defaults to `primary_only`. Note that if you set it to `secondary_only`, it will force `readonly` to true. 

使用脚本的一些示例：

    
    
    # The simplest one
    PUT _snapshot/my_backup1
    {
      "type": "azure"
    }
    
    # With some settings
    PUT _snapshot/my_backup2
    {
      "type": "azure",
      "settings": {
        "container": "backup-container",
        "base_path": "backups",
        "chunk_size": "32MB",
        "compress": true
      }
    }
    
    
    # With two accounts defined in elasticsearch.yml (my_account1 and my_account2)
    PUT _snapshot/my_backup3
    {
      "type": "azure",
      "settings": {
        "client": "secondary"
      }
    }
    PUT _snapshot/my_backup4
    {
      "type": "azure",
      "settings": {
        "client": "secondary",
        "location_mode": "primary_only"
      }
    }

使用Java的示例：

    
    
    client.admin().cluster().preparePutRepository("my_backup_java1")
        .setType("azure").setSettings(Settings.builder()
            .put(Storage.CONTAINER, "backup-container")
            .put(Storage.CHUNK_SIZE, new ByteSizeValue(32, ByteSizeUnit.MB))
        ).get();

### 存储库验证规则

根据容器命名指南，容器名称必须是有效的 DNS 名称，符合以下命名规则：

* 容器名称必须以字母或数字开头，并且只能包含字母、数字和短划线 (-) 字符。  * 每个短划线 (-) 字符必须紧跟字母或数字的前后;容器名称中不允许使用连续的短划线。  * 容器名称中的所有字母必须为小写。  * 容器名称的长度必须为 3 到 63 个字符。

[« Register a snapshot repository](snapshots-register-repository.md) [Google
Cloud Storage repository »](repository-gcs.md)
