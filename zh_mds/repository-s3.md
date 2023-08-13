

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md) ›[Register a snapshot
repository](snapshots-register-repository.md)

[« Google Cloud Storage repository](repository-gcs.md) [Shared file system
repository »](snapshots-filesystem-repository.md)

## S3存储库

您可以将 AWS S3 用作快照/还原的存储库。

**如果您正在寻找 AWS 上的 Elasticsearch 托管解决方案，pleasevisithttps://www.elastic.co/cloud/。

### 入门

要注册 S3 存储库，请在创建存储库时将类型指定为"s3"。存储库默认使用 ECS IAMRole 凭据进行身份验证。您还可以使用对 Kubernetes 服务账户使用 IAM 角色对 Kubernetes 服务账户进行身份验证。

唯一的强制设置是存储桶名称：

    
    
    PUT _snapshot/my_s3_repository
    {
      "type": "s3",
      "settings": {
        "bucket": "my-bucket"
      }
    }

### 客户端设置

您用于连接到 S3 的客户端具有许多可用设置。这些设置的形式为"s3.client.CLIENT_NAME"。SETTING_NAME'。默认情况下，"s3"存储库使用名为"default"的客户端，但可以使用存储库设置"client"进行修改。例如：

    
    
    PUT _snapshot/my_s3_repository
    {
      "type": "s3",
      "settings": {
        "bucket": "my-bucket",
        "client": "my-alternate-client"
      }
    }

大多数客户端设置都可以添加到"elasticsearch.yml"配置文件中，但安全设置除外，您可以将其添加到Elasticsearch密钥库中。有关创建和更新 Elasticsearch 密钥库的更多信息，请参阅安全设置。

例如，如果要使用特定凭证访问 S3，请运行以下命令将这些凭证添加到密钥库：

    
    
    bin/elasticsearch-keystore add s3.client.default.access_key
    bin/elasticsearch-keystore add s3.client.default.secret_key
    # a session token is optional so the following command may not be needed
    bin/elasticsearch-keystore add s3.client.default.session_token

如果您想使用实例角色或容器角色访问 S3，则应取消设置这些设置。您可以通过从密钥库中除去这些设置，从使用特定凭证切换回使用实例角色或容器角色的缺省设置，如下所示：

    
    
    bin/elasticsearch-keystore remove s3.client.default.access_key
    bin/elasticsearch-keystore remove s3.client.default.secret_key
    # a session token is optional so the following command may not be needed
    bin/elasticsearch-keystore remove s3.client.default.session_token

**此存储库类型的所有**客户端安全设置均可重新加载。重新装入设置后，用于传输快照内容的内部"s3"客户机将利用密钥库中的最新设置。任何现有的"s3"存储库以及任何新创建的存储库都将选取存储在密钥库中的新值。

正在进行的快照/还原任务不会被客户端安全设置的**重新加载**抢占。任务将使用操作开始时生成的客户端完成。

以下列表包含可用的客户端设置。那些必须存储在密钥库中的那些被标记为"安全"并且是**可重新加载的**;其他设置属于"elasticsearch.yml"文件。

"access_key"(安全，可重新加载)

     An S3 access key. If set, the `secret_key` setting must also be specified. If unset, the client will use the instance or container role instead. 
`secret_key` ([Secure](/guide/en/elasticsearch/reference/8.9/secure-
settings.html), [reloadable](/guide/en/elasticsearch/reference/8.9/secure-
settings.html#reloadable-secure-settings))

     An S3 secret key. If set, the `access_key` setting must also be specified. 
`session_token` ([Secure](/guide/en/elasticsearch/reference/8.9/secure-
settings.html), [reloadable](/guide/en/elasticsearch/reference/8.9/secure-
settings.html#reloadable-secure-settings))

     An S3 session token. If set, the `access_key` and `secret_key` settings must also be specified. 
`endpoint`

     The S3 service endpoint to connect to. This defaults to `s3.amazonaws.com` but the [AWS documentation](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region) lists alternative S3 endpoints. If you are using an [S3-compatible service](repository-s3.html#repository-s3-compatible-services "S3-compatible services") then you should set this to the service's endpoint. 
`protocol`

     The protocol to use to connect to S3. Valid values are either `http` or `https`. Defaults to `https`. When using HTTPS, this repository type validates the repository's certificate chain using the JVM-wide truststore. Ensure that the root certificate authority is in this truststore using the JVM's `keytool` tool. 
`proxy.host`

     The host name of a proxy to connect to S3 through. 
`proxy.port`

     The port of a proxy to connect to S3 through. 
`proxy.username` ([Secure](/guide/en/elasticsearch/reference/8.9/secure-
settings.html), [reloadable](/guide/en/elasticsearch/reference/8.9/secure-
settings.html#reloadable-secure-settings))

     The username to connect to the `proxy.host` with. 
`proxy.password` ([Secure](/guide/en/elasticsearch/reference/8.9/secure-
settings.html), [reloadable](/guide/en/elasticsearch/reference/8.9/secure-
settings.html#reloadable-secure-settings))

     The password to connect to the `proxy.host` with. 
`read_timeout`

     ([time value](api-conventions.html#time-units "Time units")) The maximum time Elasticsearch will wait to receive the next byte of data over an established, open connection to the repository before it closes the connection. The default value is 50 seconds. 
`max_retries`

     The number of retries to use when an S3 request fails. The default value is `3`. 
`use_throttle_retries`

     Whether retries should be throttled (i.e. should back off). Must be `true` or `false`. Defaults to `true`. 
`path_style_access`

     Whether to force the use of the path style access pattern. If `true`, the path style access pattern will be used. If `false`, the access pattern will be automatically determined by the AWS Java SDK (See [AWS documentation](https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/services/s3/AmazonS3Builder.html#setPathStyleAccessEnabled-java.lang.Boolean-) for details). Defaults to `false`. 

在版本 '7.0'、'7.1'、'7.2' 和 '7.3' 中，所有存储桶操作都使用现已弃用的路径样式访问模式。如果您的部署需要路径样式访问模式，则应在升级时将此设置设置为"true"。

`disable_chunked_encoding`

     Whether chunked encoding should be disabled or not. If `false`, chunked encoding is enabled and will be used where appropriate. If `true`, chunked encoding is disabled and will not be used, which may mean that snapshot operations consume more resources and take longer to complete. It should only be set to `true` if you are using a storage service that does not support chunked encoding. See the [AWS Java SDK documentation](https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/services/s3/AmazonS3Builder.html#disableChunkedEncoding--) for details. Defaults to `false`. 
`region`

     Allows specifying the signing region to use. Specificing this setting manually should not be necessary for most use cases. Generally, the SDK will correctly guess the signing region to use. It should be considered an expert level setting to support S3-compatible APIs that require [v4 signatures](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) and use a region other than the default `us-east-1`. Defaults to empty string which means that the SDK will try to automatically determine the correct signing region. 
`signer_override`

     Allows specifying the name of the signature algorithm to use for signing requests by the S3 client. Specifying this setting should not be necessary for most use cases. It should be considered an expert level setting to support S3-compatible APIs that do not support the signing algorithm that the SDK automatically determines for them. See the [AWS Java SDK documentation](https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/ClientConfiguration.html#setSignerOverride-java.lang.String-) for details. Defaults to empty string which means that no signing algorithm override will be used. 

##### S3-compatibleservices

有许多存储系统提供与 S3 兼容的 API，"repository-s3"类型允许您使用这些系统代替 AWS，S3.To 这样做，您应该将"s3.client.CLIENT_NAME.endpoint"设置设置为系统的终端节点。此设置接受 IP 地址和主机名，并可能包括端口。例如，终结点可能是"172.17.0.2"或"172.17.0.2：9000"。

默认情况下，Elasticsearch 使用 HTTPS 与存储系统通信，并使用 JVM 范围的信任库验证存储库的证书链。确保 JVM 范围的信任库包含存储库的条目。如果您希望使用不安全的HTTP通信而不是HTTPS，请将"s3.client.CLIENT_NAME.protocol"设置为"http"。

MinIO 是提供与 S3 兼容的 API 的存储系统的一个示例。"repository-s3"类型允许Elasticsearch使用MinIO支持的存储库以及存储在AWS S3上的存储库。其他兼容 S3 的存储系统也可以与 Elasticsearch 配合使用，但这些都不在 Elasticsearch 测试套件中。

请注意，某些存储系统声称与 S3 兼容，但并未忠实地完全模拟 S3 的行为。"存储库-s3"类型要求与 S3 完全兼容。特别是，它必须支持同一组 API 端点，在发生故障时返回相同的错误，并提供至少与 S3 一样好的一致性和性能，即使由多个节点并发访问也是如此。不兼容的错误代码、一致性或性能可能特别难以跟踪，因为错误、一致性故障和性能问题通常很少见且难以重现。

您可以使用存储库分析 API 对存储系统的适用性执行一些基本检查。如果此 API 未成功完成或指示性能不佳，则您的存储系统与 AWS S3 不完全兼容，因此不适合用作快照存储库。您需要与存储系统的供应商合作，以解决您遇到的任何不兼容问题。

### 存储库设置

"s3"存储库类型支持许多设置，用于自定义数据在 S3 中的存储方式。这些可以在创建存储库时指定。例如：

    
    
    PUT _snapshot/my_s3_repository
    {
      "type": "s3",
      "settings": {
        "bucket": "my-bucket",
        "another_setting": "setting-value"
      }
    }

支持以下设置：

`bucket`

    

(必填)用于快照的 S3 存储桶的名称。

存储桶名称必须遵守亚马逊的 S3 存储桶命名规则。

`client`

     The name of the [S3 client](repository-s3.html#repository-s3-client "Client settings") to use to connect to S3. Defaults to `default`. 
`base_path`

    

指定存储库数据在其存储桶中的路径。默认为空字符串，表示存储库位于存储桶的根目录中。此设置的值不应以"/"开头或结尾。

在为 Elastic CloudEnterprise 配置快照存储库时，请勿设置"base_path"。弹性云企业自动生成每个部署的"base_path"，以便多个部署可以共享同一个存储桶。

`chunk_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Big files can be broken down into chunks during snapshotting if needed. Specify the chunk size as a value and unit, for example: `1TB`, `1GB`, `10MB`. Defaults to the maximum size of a blob in the S3 which is `5TB`. 
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

`server_side_encryption`

     When set to `true` files are encrypted on server side using AES256 algorithm. Defaults to `false`. 
`buffer_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Minimum threshold below which the chunk is uploaded using a single request. Beyond this threshold, the S3 repository will use the [AWS Multipart Upload API](https://docs.aws.amazon.com/AmazonS3/latest/dev/uploadobjusingmpu.html) to split the chunk into several parts, each of `buffer_size` length, and to upload each part in its own request. Note that setting a buffer size lower than `5mb` is not allowed since it will prevent the use of the Multipart API and may result in upload errors. It is also not possible to set a buffer size greater than `5gb` as it is the maximum upload size allowed by S3. Defaults to `100mb` or `5%` of JVM heap, whichever is smaller. 
`canned_acl`

     The S3 repository supports all [S3 canned ACLs](https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl) : `private`, `public-read`, `public-read-write`, `authenticated-read`, `log-delivery-write`, `bucket-owner-read`, `bucket-owner-full-control`. Defaults to `private`. You could specify a canned ACL using the `canned_acl` setting. When the S3 repository creates buckets and objects, it adds the canned ACL into the buckets and objects. 
`storage_class`

     Sets the S3 storage class for objects stored in the snapshot repository. Values may be `standard`, `reduced_redundancy`, `standard_ia`, `onezone_ia` and `intelligent_tiering`. Defaults to `standard`. Changing this setting on an existing repository only affects the storage class for newly created objects, resulting in a mixed usage of storage classes. You may use an S3 Lifecycle Policy to adjust the storage class of existing objects in your repository, but you must not transition objects to Glacier classes and you must not expire objects. If you use Glacier storage classes or object expiry then you may permanently lose access to your repository contents. For more information about S3 storage classes, see [AWS Storage Classes Guide](https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html)

在下面记录的存储库设置中定义客户端设置的选项被视为已弃用，并将在将来的版本中删除。

除了上述设置之外，您还可以在存储库设置中指定所有非安全客户端设置。在这种情况下，存储库设置中找到的客户端设置将与存储库使用的指定客户端的客户端设置合并。客户端和存储库设置之间的冲突由存储库设置优先于客户端设置来解决。

例如：

    
    
    PUT _snapshot/my_s3_repository
    {
      "type": "s3",
      "settings": {
        "client": "my-client",
        "bucket": "my-bucket",
        "endpoint": "my.s3.endpoint"
      }
    }

这将设置一个存储库，该存储库使用客户端"my_client_name"中的所有客户端设置，但存储库设置覆盖到"my.s3.endpoint"的"端点"除外。

#### 推荐的 S3 权限

为了将 Elasticsearch 快照过程限制为所需的最少资源，我们建议将 Amazon IAM 与预先存在的 S3 存储桶结合使用。下面是一个示例策略，它允许对名为"snaps.example.com"的 S3 存储桶进行快照访问。这可以通过 AWS IAM 控制台、创建自定义策略并使用与此类似的策略文档(将 snaps.example.com 更改为您的存储桶名称)进行配置。

    
    
    {
      "Statement": [
        {
          "Action": [
            "s3:ListBucket",
            "s3:GetBucketLocation",
            "s3:ListBucketMultipartUploads",
            "s3:ListBucketVersions"
          ],
          "Effect": "Allow",
          "Resource": [
            "arn:aws:s3:::snaps.example.com"
          ]
        },
        {
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
            "s3:AbortMultipartUpload",
            "s3:ListMultipartUploadParts"
          ],
          "Effect": "Allow",
          "Resource": [
            "arn:aws:s3:::snaps.example.com/*"
          ]
        }
      ],
      "Version": "2012-10-17"
    }

您可以通过在存储桶中指定名为"foo"的前缀来进一步限制权限。

    
    
    {
      "Statement": [
        {
          "Action": [
            "s3:ListBucket",
            "s3:GetBucketLocation",
            "s3:ListBucketMultipartUploads",
            "s3:ListBucketVersions"
          ],
          "Condition": {
            "StringLike": {
              "s3:prefix": [
                "foo/*"
              ]
            }
          },
          "Effect": "Allow",
          "Resource": [
            "arn:aws:s3:::snaps.example.com"
          ]
        },
        {
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
            "s3:AbortMultipartUpload",
            "s3:ListMultipartUploadParts"
          ],
          "Effect": "Allow",
          "Resource": [
            "arn:aws:s3:::snaps.example.com/foo/*"
          ]
        }
      ],
      "Version": "2012-10-17"
    }

存储桶需要存在才能为快照注册存储库。如果您未创建存储桶，则存储库注册将失败。

#### 清理分段上传

Elasticsearch 使用 S3 的多部分上传过程将较大的 blob 上传到存储库。多部分上传过程的工作原理是将每个 blob 划分为较小的部分，独立上传每个部分，然后在单独的步骤中完成上传。这减少了上传失败时 Elasticsearch 必须重新发送的数据量：Elasticsearch 只需要重新发送失败的部分，而不是从整个 blob 的开头开始。每个部分的存储从上传部分的时间开始独立收费。

如果无法完成分段上传，则必须中止该分段以删除已成功上传的任何分段，从而防止进一步累积存储费用。Elasticsearch 会在失败时自动中止多部分上传，但有时中止请求本身会失败。例如，如果存储库变得不可访问，或者运行 Elasticsearchis 的实例突然终止，则 Elasticsearch 无法完成或中止任何正在进行的上传。

您必须确保失败的上传最终中止，以避免不必要的存储成本。您可以使用列出分段上传 API 列出正在进行的上传并查找任何异常长时间运行的上传，也可以配置存储桶生命周期策略，以便在未完成的上传达到特定年龄时自动中止它们。

#### AWS VPC 带宽设置

AWS 实例将 S3 终端节点解析为公有 IP。如果弹性搜索实例驻留在 AWS VPC 的私有子网中，则发往 S3 的所有流量都将通过 VPC 的 NAT 实例。如果您的 VPC 的 NAT 实例较小(例如 t2.micro)或正在处理大量网络流量，则到 S3 的带宽可能会受到该 NAT 实例的网络带宽限制的限制。相反，我们建议创建一个 VPC终端节点，以便在驻留在 AWS VPC 中的私有子网中的实例中连接到 S3。这将消除 VPC 的 NAT 实例的网络带宽施加的任何限制。

驻留在 AWS VPC 公有子网中的实例将通过 VPC 的互联网网关连接到 S3，并且不受 VPC 的 NAT 实例的带宽限制。

#### 使用 IAM 角色对 Kubernetes 服务账户进行身份验证

如果要使用 Kubernetes 服务帐户进行身份验证，则需要在 S3 存储库配置目录中添加一个指向 '$AWS_WEB_IDENTITY_TOKEN_FILE' 环境变量(应由 Kubernetes pod 自动设置)的符号链接，以便存储库可以拥有服务帐户的读取访问权限(存储库无法读取其配置目录之外的任何文件)。例如：

    
    
    mkdir -p "${ES_PATH_CONF}/repository-s3"
    ln -s $AWS_WEB_IDENTITY_TOKEN_FILE "${ES_PATH_CONF}/repository-s3/aws-web-identity-token-file"

符号链接必须在所有数据和主节点上创建，并且"elasticsearch"用户可以读取。默认情况下，Elasticsearch 使用 uid：gid '1000：0' 以用户"elasticsearch"身份运行。

如果符号链接存在，则默认情况下，所有没有显式"客户端"凭证的 S3 存储库都将使用它。

[« Google Cloud Storage repository](repository-gcs.md) [Shared file system
repository »](snapshots-filesystem-repository.md)
