

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md)

[« Snapshot and restore](snapshot-restore.md) [Azure repository
»](repository-azure.md)

## 注册快照存储库

本指南介绍如何注册快照存储库。快照存储库是快照的群集外存储位置。必须先注册存储库，然后才能拍摄或还原快照。

在本指南中，你将了解如何：

* 注册快照存储库 * 验证存储库是否正常运行 * 清理存储库以删除不需要的文件

###Prerequisites

* 要使用 Kibana 的"快照和还原"功能，您必须具有以下权限：

    * [Cluster privileges](security-privileges.html#privileges-list-cluster "Cluster privileges"): `monitor`, `manage_slm`, `cluster:admin/snapshot`, and `cluster:admin/repository`
    * [Index privilege](security-privileges.html#privileges-list-indices "Indices privileges"): `all` on the `monitor` index 

* 要注册快照存储库，集群的全局元数据必须是可写的。确保没有任何阻止写入访问的群集块。

###Considerations

注册快照存储库时，请记住以下几点：

* 每个快照存储库都是独立且独立的。Elasticsearch 不会在存储库之间共享数据。  * 集群应仅注册一次特定的快照存储库存储桶。如果将同一快照存储库注册到多个集群，则只有一个集群应具有对该存储库的写入权限。在其他集群上，将存储库注册为只读。

这可以防止多个集群同时写入存储库并损坏存储库的内容。它还阻止 Elasticsearch 缓存存储库的内容，这意味着其他集群所做的更改将立即可见。

* 将 Elasticsearch 升级到较新版本时，您可以继续使用升级前使用的同一存储库。如果存储库由多个集群访问，则它们都应具有相同的版本。一旦存储库被特定版本的 Elasticsearch 修改，当被旧版本访问时，它可能无法正常工作。但是，您可以通过将升级前拍摄的快照还原到运行升级前版本的集群中来从失败的升级中恢复，即使您在升级期间或之后拍摄了更多快照也是如此。

### 管理快照存储库

您可以通过两种方式注册和管理快照存储库：

* Kibana 的 Snapshot and Restore** 功能 * Elasticsearch 的快照存储库管理 API

要在 Kibana 中管理存储库，请转到主菜单并单击"堆栈管理">"快照和还原">"存储库"。要注册快照存储库，请单击 **注册存储库**。

您还可以使用创建快照存储库 API 注册存储库。

### 快照存储库类型

支持的快照存储库类型因部署类型而异：

* Elasticsearch Service 存储库类型 * 自我管理的存储库类型

#### 弹性搜索服务存储库类型

Elasticsearch Service 部署会自动注册"找到的快照"存储库。Elasticsearch Service 使用此存储库和"云快照策略"来定期拍摄集群快照。您还可以将"找到的快照"存储库用于您自己的 SLM 策略或存储可搜索的快照。

"找到的快照"存储库特定于每个部署。但是，如果部署位于同一帐户和同一区域中，则可以从其他部署的"找到的快照"存储库还原快照。请参阅云快照和还原文档以了解更多信息。

Elasticsearch Service 部署还支持以下存储库类型：

* Azure * Google Cloud Storage * AWS S3 * 仅源代码

#### 自管理存储库类型

如果您管理自己的 Elasticsearch 集群，则可以使用以下内置快照存储库类型：

* Azure * Google Cloud Storage * AWS S3 * 共享文件系统 * 只读网址 * 仅源代码

其他存储库类型可通过官方插件获得：

Hadoop分布式文件系统(HDFS)

您还可以将这些存储库类型使用备用存储实现，只要替代实现完全兼容即可。例如，MinIO 提供了 AWS S3 API 的替代实施，您可以将 MinIO 与"s3"存储库类型一起使用。

请注意，某些存储系统声称与这些存储库类型兼容，但没有完全模拟其行为。Elasticsearch 需要完全兼容。特别是，替代实现必须支持同一组 API 端点，在发生故障时返回相同的错误，并提供等效的一致性保证和性能，即使由多个节点并发访问也是如此。不兼容的错误代码、一致性或性能可能特别难以跟踪，因为错误、一致性故障和性能问题通常很少见且难以重现。

您可以使用存储库分析 API 对存储系统的适用性执行一些基本检查。如果此 API 未成功完成或指示性能不佳，则存储系统不完全兼容，因此不适合用作快照存储库。您需要与存储系统的供应商合作，以解决您遇到的任何不兼容问题。

### 验证存储库

当您注册快照存储库时，Elasticsearch 会自动验证该存储库在所有主节点和数据节点上是否可用且正常运行。

要禁用此验证，请将创建快照存储库 API 的"验证"查询参数设置为"false"。您无法在 Kibana 中禁用存储库验证。

    
    
    response = client.snapshot.create_repository(
      repository: 'my_unverified_backup',
      verify: false,
      body: {
        type: 'fs',
        settings: {
          location: 'my_unverified_backup_location'
        }
      }
    )
    puts response
    
    
    PUT _snapshot/my_unverified_backup?verify=false
    {
      "type": "fs",
      "settings": {
        "location": "my_unverified_backup_location"
      }
    }

如果需要，您可以手动运行存储库验证检查。要在 Kibana 中验证存储库，请转到"**存储库**"列表页面，然后单击存储库的名称。然后单击"**验证存储库**"。您还可以使用验证快照存储库 API。

    
    
    response = client.snapshot.verify_repository(
      repository: 'my_unverified_backup'
    )
    puts response
    
    
    POST _snapshot/my_unverified_backup/_verify

如果成功，请求将返回用于验证存储库的节点列表。如果验证失败，请求将返回错误。

您可以使用存储库分析API 更彻底地测试存储库。

### 清理存储库

随着时间的推移，存储库可能会累积任何现有快照未引用的数据。这是快照功能在快照创建期间的故障情况下提供的数据安全保证以及快照创建过程的分散性的结果。这些未引用的数据绝不会对快照存储库的性能或安全性产生负面影响，但会导致超出必要的存储使用量。要删除此未引用的数据，可以在存储库上运行清理操作。这将触发对存储库内容的完整核算并删除任何未引用的数据。

要在 Kibana 中运行存储库清理操作，请转到"**存储库**列表"页面，然后单击存储库的名称。然后单击"**清理存储库**"。

您还可以使用清理快照存储库 API。

    
    
    response = client.snapshot.cleanup_repository(
      repository: 'my_repository'
    )
    puts response
    
    
    POST _snapshot/my_repository/_cleanup

该 API 返回：

    
    
    {
      "results": {
        "deleted_bytes": 20,
        "deleted_blobs": 5
      }
    }

根据具体的存储库实现，显示的可用字节数以及删除的 blob 数将是近似值或确切结果。已删除的 Blob 数的任何非零值都意味着找到并随后清理了未引用的 Blob。

请注意，从存储库中删除任何快照时，此端点执行的大多数清理操作都会自动执行。如果您定期删除快照，则在大多数情况下，使用此功能不会节省任何或仅节省少量空间，并且应相应地降低调用它的频率。

### 备份存储库

您可能希望对存储库进行独立备份，例如，以便拥有其内容的存档副本，以便以后可以使用该副本重新创建当前状态的存储库。

您必须确保 Elasticsearch 在备份其内容时不会写入存储库。您可以通过在所有集群上取消注册它或使用"readonly： true"注册它来执行此操作。如果 Elasticsearch 在备份期间将任何数据写入存储库，则备份的内容可能不一致，并且将来可能无法从中恢复任何数据。

或者，如果您的存储库支持它，您可以拍摄底层文件系统的原子快照，然后备份此文件系统快照。以原子方式拍摄文件系统快照非常重要。

不能将单个节点的文件系统快照用作备份机制。您必须使用 Elasticsearch 快照和恢复功能将集群内容复制到单独的存储库。然后，如果需要，您可以拍摄此存储库的文件系统快照。

从备份恢复存储库时，在存储库内容完全还原之前，不得向 Elasticsearch 注册存储库。如果您在向 Elasticsearch 注册存储库时更改了存储库的内容，则该存储库可能会变得不可读或可能会静默丢失其某些内容。

[« Snapshot and restore](snapshot-restore.md) [Azure repository
»](repository-azure.md)
