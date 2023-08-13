

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md) ›[Register a snapshot
repository](snapshots-register-repository.md)

[« Azure repository](repository-azure.md) [S3 repository
»](repository-s3.md)

## 谷歌云存储库

您可以将 Google Cloud StorageService 用作快照/还原的存储库。

### 入门

此存储库类型使用 Google Cloud Java Client forStorage 连接到存储服务。如果您是第一次使用 Google CloudStorage，则必须连接到 Google Cloud PlatformConsole 并创建一个新项目。创建项目后，您必须为项目启用云存储服务。

#### 创建存储桶

Google Cloud Storage 服务使用 abucket 的概念作为所有数据的容器。存储桶通常使用 Google Cloud PlatformConsole 创建。此存储库类型不会自动创建存储桶。

要创建新存储桶，请执行以下操作：

1. 连接到 Google Cloud Platform Console。  2. 选择您的项目。  3. 转到存储浏览器。  4. 单击**创建存储桶**按钮。  5. 输入新存储桶的名称。  6. 选择存储类。  7. 选择一个位置。  8. 单击**创建**按钮。

有关更详细的说明，请参阅 Google 云文档。

#### 服务身份验证

存储库必须对其向 Google CloudStorage 服务发出的请求进行身份验证。Google 客户端库通常采用名为应用程序默认凭据的策略。但是，Elasticsearch仅**部分支持该策略。该存储库在Elasticsearch进程下运行，该进程在启用安全管理器的情况下运行。当环境变量"GOOGLE_APPLICATION_CREDENTIALS"指向磁盘上的本地文件时，安全管理器会阻止"自动"凭据发现。但是，它可以检索附加到运行 Elasticsearch 的资源的服务帐户，或者回退到 Compute Engine、Kubernetes Engine 或 App Engine 提供的默认服务帐户。或者，如果您使用的环境不支持自动凭据发现，则必须配置服务帐户凭据。

#### 使用服务帐户

您必须手动获取并提供服务帐户凭据。

有关生成 JSON 服务帐户文件的详细信息，请参阅 Google 云文档。请注意，此存储库类型不支持 PKCS12 格式。

以下是步骤摘要：

1. 连接到 Google Cloud Platform Console。  2. 选择您的项目。  3. 选择"服务帐户"选项卡。  4. 单击"**创建服务帐户**"。  5. 创建帐户后，选择它并转到 **密钥**。  6. 选择"**添加密钥**"，然后选择"创建新密钥**"。  7. 选择密钥类型 **JSON**，因为不支持 P12。

JSON 服务帐户文件如下所示：

    
    
    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "...",
      "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
      "client_email": "service-account-for-your-repository@your-project-id.iam.gserviceaccount.com",
      "client_id": "...",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-bucket@your-project-id.iam.gserviceaccount.com"
    }

要将此文件提供给存储库，它必须存储在 Elasticsearch 密钥库中。您必须使用"add-file"子命令添加名称为"gcs.client.NAME.credentials_file"的"文件"设置。"NAME"是存储库的客户端配置的名称。隐式客户端名称为"默认"，但可以使用"client"键在存储库设置中指定不同的客户端名称。

不支持通过GOOGLE_APPLICATION_CREDENTIALS环境变量传递文件路径。

例如，如果您在密钥库中添加了"gcs.client.my_alternate_client.credentials_file"设置，则可以将存储库配置为使用这些凭证，如下所示：

    
    
    PUT _snapshot/my_gcs_repository
    {
      "type": "gcs",
      "settings": {
        "bucket": "my_bucket",
        "client": "my_alternate_client"
      }
    }

"credentials_file"设置是可重新加载的。重新加载设置后，用于传输快照内容的内部"gcs"客户端将使用密钥库中的最新设置。

正在进行的快照或还原作业不会被客户端"credentials_file"设置的**重新加载**抢占。他们完成使用操作开始时构建的客户端。

### 客户端设置

用于连接到 Google Cloud Storage 的客户端有许多可用的设置。客户端设置名称的格式为gcs.client.CLIENT_NAME。SETTING_NAME"，并在"elasticsearch.yml"中指定。由"gcs"存储库查找的默认客户端名称称为"默认"，但可以使用存储库设置"client"进行自定义。

例如：

    
    
    PUT _snapshot/my_gcs_repository
    {
      "type": "gcs",
      "settings": {
        "bucket": "my_bucket",
        "client": "my_alternate_client"
      }
    }

某些设置是敏感的，必须存储在 Elasticsearchkey store 中。服务帐户文件就是这种情况：

    
    
    bin/elasticsearch-keystore add-file gcs.client.default.credentials_file /path/service-account.json

以下是可用的客户端设置。必须存储在密钥库中的那些被标记为"安全"。

"credentials_file"(安全，可重新加载)

     The service account file that is used to authenticate to the Google Cloud Storage service. 
`endpoint`

     The Google Cloud Storage service endpoint to connect to. This will be automatically determined by the Google Cloud Storage client but can be specified explicitly. 
`connect_timeout`

     The timeout to establish a connection to the Google Cloud Storage service. The value should specify the unit. For example, a value of `5s` specifies a 5 second timeout. The value of `-1` corresponds to an infinite timeout. The default value is 20 seconds. 
`read_timeout`

     The timeout to read data from an established connection. The value should specify the unit. For example, a value of `5s` specifies a 5 second timeout. The value of `-1` corresponds to an infinite timeout. The default value is 20 seconds. 
`application_name`

     Name used by the client when it uses the Google Cloud Storage service. Setting a custom name can be useful to authenticate your cluster when requests statistics are logged in the Google Cloud Platform. Default to `repository-gcs`
`project_id`

     The Google Cloud project id. This will be automatically inferred from the credentials file but can be specified explicitly. For example, it can be used to switch between projects when the same credentials are usable for both the production and the development projects. 
`proxy.host`

     Host name of a proxy to connect to the Google Cloud Storage through. 
`proxy.port`

     Port of a proxy to connect to the Google Cloud Storage through. 
`proxy.type`

     Proxy type for the client. Supported values are `direct` (no proxy), `http`, and `socks`. Defaults to `direct`. 

### 存储库设置

"gcs"存储库类型支持多种设置，用于自定义数据在 Google Cloud Storage 中的存储方式。

这些可以在创建存储库时指定。例如：

    
    
    PUT _snapshot/my_gcs_repository
    {
      "type": "gcs",
      "settings": {
        "bucket": "my_other_bucket",
        "base_path": "dev"
      }
    }

支持以下设置：

`bucket`

     The name of the bucket to be used for snapshots. (Mandatory) 
`client`

     The name of the client to use to connect to Google Cloud Storage. Defaults to `default`. 
`base_path`

    

指定存储桶中到存储库数据的路径。默认为存储桶的根。

在为 Elastic CloudEnterprise 配置快照存储库时，请勿设置"base_path"。弹性云企业自动生成每个部署的"base_path"，以便多个部署可以共享同一个存储桶。

`chunk_size`

     Big files can be broken down into multiple smaller blobs in the blob store during snapshotting. It is not recommended to change this value from its default unless there is an explicit reason for limiting the size of blobs in the repository. Setting a value lower than the default can result in an increased number of API calls to the Google Cloud Storage Service during snapshot create as well as restore operations compared to using the default value and thus make both operations slower as well as more costly. Specify the chunk size as a value and unit, for example: `10MB`, `5KB`, `500B`. Defaults to the maximum size of a blob in the Google Cloud Storage Service which is `5TB`. 
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

`application_name`

     [6.3.0]  Deprecated in 6.3.0. This setting is now defined in the [client settings](repository-gcs.html#repository-gcs-client "Client settings").  Name used by the client when it uses the Google Cloud Storage service. 

#### 推荐的存储桶权限

用于访问存储桶的服务账户必须具有对存储桶的"写入器"访问权限：

1. 连接到 Google Cloud Platform Console。  2. 选择您的项目。  3. 转到存储浏览器。  4. 选择存储桶并"编辑存储桶权限"。  5. 服务帐户必须配置为具有"编写器"访问权限的"用户"。

[« Azure repository](repository-azure.md) [S3 repository
»](repository-s3.md)
