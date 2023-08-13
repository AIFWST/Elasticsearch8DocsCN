

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md)

[« Restore a snapshot](snapshots-restore-snapshot.md) [Secure the Elastic
Stack »](secure-cluster.md)

## 可搜索快照

可搜索快照允许您使用快照以非常经济高效的方式搜索不常访问的数据和只读数据。冷和冻结数据层使用可搜索快照来降低存储和运营成本。

从热层滚动更新后，可搜索快照消除了对副本分片的需求，可能会将搜索数据所需的本地存储减半。可搜索快照依赖于已用于备份的相同快照机制，对快照存储库存储成本的影响最小。

### 使用可搜索快照

搜索可搜索快照索引与搜索任何其他索引相同。

默认情况下，可搜索快照索引没有副本。底层快照提供了弹性，查询量预计足够低，单个分片副本就足够了。但是，如果需要支持更高的查询量，可以通过调整"index.number_of_replicas"索引设置来添加副本。

如果一个节点发生故障，并且需要在其他地方恢复可搜索的快照分片，那么 Elasticsearch 会有一个短暂的时间窗口，将分片分配给集群运行状况不会为"绿色"的其他节点。命中这些分片的搜索可能会失败或返回部分结果，直到分片重新分配给运行状况良好的节点。

您通常通过 ILM 管理可搜索的快照。可搜索快照操作会在常规索引达到"冷"或"冻结"阶段时自动将其转换为可搜索快照索引。您还可以通过使用 mountsnapshotAPI 手动挂载现有快照中的索引来使索引可搜索。

要从包含多个索引的快照挂载索引，我们建议创建仅包含要搜索的索引的快照克隆，然后挂载克隆。如果快照具有任何挂载的索引，则不应删除该快照，因此创建克隆使您能够独立于任何可搜索快照来管理备份快照的生命周期。如果使用 ILM 来管理可搜索的快照，则它将根据需要自动查看克隆快照。

您可以使用与常规索引相同的机制来控制可搜索快照索引的分片的分配。例如，您可以使用索引级分片分配筛选将可搜索快照分片限制为节点的子集。

可搜索快照索引的恢复速度受存储库设置"max_restore_bytes_per_sec"和节点设置"index.recovery.max_bytes_per_sec"的限制，就像正常的恢复操作一样。默认情况下，"max_restore_bytes_per_sec"是无限的，但默认值"index.recovery.max_bytes_per_sec"取决于节点的配置。请参阅恢复设置。

我们建议您先强制合并索引到每个分片的单个段，然后再拍摄将作为可搜索快照索引挂载的快照。从快照存储库中读取的每次操作都需要花费时间和金钱，而且段越少，恢复快照或响应搜索所需的读取次数就越少。

可搜索快照非常适合管理大型历史数据存档。搜索历史信息的频率通常低于最近数据，因此可能不需要副本来实现其性能优势。

对于更复杂或耗时的搜索，您可以将异步搜索与可搜索快照一起使用。

将以下任何存储库类型与可搜索快照结合使用：

* AWS S3 * Google Cloud Storage * Azure Blob Storage * Hadoop Distributed File Store (HDFS) * 共享文件系统，如 NFS * 只读 HTTP 和 HTTPS 存储库

您还可以使用这些存储库类型的替代实现，例如 MinIO，只要它们完全兼容即可。使用存储库分析 API 分析存储库是否适合用于可搜索快照。

### 可搜索快照的工作原理

从快照挂载索引时，Elasticsearch 会将其分片分配给集群内的数据节点。然后，数据节点根据指定的挂载选项自动将相关分片数据从存储库检索到本地存储上。如果可能，搜索将使用本地存储中的数据。如果数据在本地不可用，Elasticsearch 会从快照存储库下载所需的数据。

如果持有其中一个分片的节点发生故障，Elasticsearch 会自动将受影响的分片分配到另一个节点上，并且该节点会从存储库中恢复相关的分片数据。不需要副本，并且不需要复杂的监控或编排来恢复丢失的分片。尽管默认情况下可搜索快照索引没有副本，但您可以通过调整"index.number_of_replicas"向这些索引添加副本。可搜索快照分片的副本是通过从快照存储库复制数据来恢复的，就像可搜索快照分片的主副本一样。相反，常规索引的副本是通过从主索引复制数据来恢复的。

#### 挂载选项

要搜索快照，必须先将其作为索引在本地挂载。通常 ILM 会自动执行此操作，但您也可以自己调用 mountsnapshotAPI。从快照挂载索引有两个选项，每个选项都有不同的性能特征和本地存储占用空间：

完全安装的索引

    

将快照索引的分片完全缓存在 Elasticsearch 集群中。ILM 在"热"和"冷"阶段使用此选项。

完全挂载索引的搜索性能通常与常规索引相当，因为访问快照存储库的需求最小。在恢复过程中，搜索性能可能比使用非常规索引慢，因为搜索可能需要一些尚未检索到本地缓存中的数据。如果发生这种情况，Elasticsearch 将急切地检索完成搜索所需的数据，同时进行正在进行的恢复。磁盘上的数据在重新启动后保留，因此节点在重新启动后不需要重新下载已存储在节点上的数据。

由 ILM 管理的索引在完全装载时以"还原-"为前缀。

部分装载的索引

    

使用本地缓存，该缓存仅包含最近搜索的快照索引数据部分。此缓存具有固定大小，并在同一数据节点上分配的部分挂载索引的分片之间共享。ILM 在"冻结"阶段使用此选项。

如果搜索需要的数据不在缓存中，Elasticsearch 会从快照存储库中获取缺失的数据。需要这些读取的搜索速度较慢，但提取的数据存储在缓存中，以便将来可以更快地提供类似的搜索。Elasticsearch将从缓存中逐出常用数据以释放空间。节点重新启动时将清除缓存。

尽管比完全挂载的索引或常规索引慢，但部分挂载的索引仍然快速返回搜索结果，即使对于大型数据集也是如此，因为存储库中的数据布局针对搜索进行了大量优化。许多搜索在返回结果之前只需要检索总分片数据的一小部分。

由 ILM 管理的索引在部分装载时以"部分-"为前缀。

要部分挂载索引，必须有一个或多个具有可用共享缓存的节点。默认情况下，专用冻结数据层节点(具有"data_frozen"角色且没有其他数据角色的节点)配置了共享缓存，使用总磁盘空间的 90% 和总磁盘空间减去 100GB 的较大值。

强烈建议在生产中使用专用的冻结层。如果没有专用的冻结层，则必须配置"xpack.searchable.snapshot.shared_cache.size"设置，以便为一个或多个节点上的缓存保留空间。部分挂载的索引仅分配给具有共享高速缓存的节点。

`xpack.searchable.snapshot.shared_cache.size`

     ([Static](settings.html#static-cluster-setting)) Disk space reserved for the shared cache of partially mounted indices. Accepts a percentage of total disk space or an absolute [byte value](api-conventions.html#byte-units "Byte size units"). Defaults to `90%` of total disk space for dedicated frozen data tier nodes. Otherwise defaults to `0b`. 
`xpack.searchable.snapshot.shared_cache.size.max_headroom`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) For dedicated frozen tier nodes, the max headroom to maintain. If `xpack.searchable.snapshot.shared_cache.size` is not explicitly set, this setting defaults to `100GB`. Otherwise it defaults to `-1` (not set). You can only configure this setting if `xpack.searchable.snapshot.shared_cache.size` is set as a percentage. 

为了说明这些设置如何协同工作，让我们看两个示例在专用冻结节点上使用设置的默认值时：

* 4000 GB 磁盘将生成大小为 3900 GB 的共享缓存。4000 GB 的 90% 是 3600 GB，剩下 400 GB 的余量。默认的"max_headroom"100 GB 生效，因此结果为 3900 GB。  * 400 GB 磁盘将生成大小为 360 GB 的共享缓存。

您可以在"elasticsearch.yml"中配置设置：

    
    
    xpack.searchable.snapshot.shared_cache.size: 4TB

您只能在具有"data_frozen"角色的节点上配置这些设置。此外，具有共享缓存的节点只能具有单个数据路径。

Elasticsearch 还使用名为".snapshot-blob-cache"的专用系统索引来加快可搜索快照分片的恢复速度。此索引用作部分或完全挂载数据之上的附加缓存层，并包含启动可搜索快照分片所需的最少数据。Elasticsearch 会自动删除此索引中不再使用的文档。可以使用以下设置调整此定期清理：

`searchable_snapshots.blob_cache.periodic_cleanup.interval`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The interval at which the periodic cleanup of the `.snapshot-blob-cache` index is scheduled. Defaults to every hour (`1h`). 
`searchable_snapshots.blob_cache.periodic_cleanup.retention_period`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The retention period to keep obsolete documents in the `.snapshot-blob-cache` index. Defaults to every hour (`1h`). 
`searchable_snapshots.blob_cache.periodic_cleanup.batch_size`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The number of documents that are searched for and bulk-deleted at once during the periodic cleanup of the `.snapshot-blob-cache` index. Defaults to `100`. 
`searchable_snapshots.blob_cache.periodic_cleanup.pit_keep_alive`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The value used for the [point-in-time keep alive](point-in-time-api.html#point-in-time-keep-alive "Keeping point in time alive") requests executed during the periodic cleanup of the `.snapshot-blob-cache` index. Defaults to `10m`. 

### 使用可搜索快照降低成本

在大多数情况下，可搜索快照消除了对副本分片和在节点之间复制分片数据的需要，从而降低了运行集群的成本。但是，如果从环境中的快照存储库检索数据的成本特别高，则可搜索快照的成本可能高于常规索引。在使用可搜索快照之前，请确保操作环境的成本结构与可搜索快照兼容。

#### 复制成本

为了实现弹性，常规索引需要跨多个节点的每个分片的多个冗余副本。如果节点发生故障，Elasticsearch 将使用冗余来重建任何丢失的分片副本。可搜索快照索引不需要副本。如果包含可搜索快照索引的节点出现故障，Elasticsearch 可以从快照存储库重建丢失的分片缓存。

如果没有副本，很少访问的可搜索快照索引需要的资源要少得多。包含无副本的完全挂载的可搜索快照索引的冷数据层需要的节点和磁盘空间是常规索引中包含相同数据的层的一半。冻结层仅包含部分挂载的可搜索快照索引，需要的资源更少。

#### 数据传输费用

在节点之间移动常规索引的分片时，其内容将从集群中的另一个节点复制。在许多环境中，在节点之间移动数据的成本很高，尤其是在节点位于不同区域的云环境中运行时。相反，挂载可搜索的快照索引或移动其分片之一时，始终会从快照存储库复制数据。这通常便宜得多。

大多数云提供商对区域之间传输的数据以及从其平台传输的数据收取高额费用。您只应将快照挂载到与快照存储库位于同一区域的集群中。如果您希望跨多个区域搜索数据，请配置多个集群并使用跨集群搜索或跨集群复制，而不是可搜索的快照。

### 备份和恢复可搜索快照

您可以使用常规快照备份包含可搜索快照索引的集群。还原包含可搜索快照索引的快照时，这些索引将再次还原为可搜索快照索引。

在还原包含可搜索快照索引的快照之前，必须先注册包含原始索引快照的存储库。还原后，可搜索的快照索引会从其原始存储库中装载原始索引快照。如果需要，您可以为常规快照和可搜索快照使用单独的存储库。

可搜索快照索引的快照仅包含少量标识其原始索引快照的元数据。它不包含原始索引中的任何数据。备份的还原将无法还原原始索引快照不可用的任何可搜索快照索引。

由于可搜索快照索引不是常规索引，因此无法使用仅源存储库拍摄可搜索快照索引的快照。

### 可搜索快照的可靠性

可搜索快照索引中数据的唯一副本是存储在存储库中的底层快照。例如：

* 当仓库包含的任何可搜索快照挂载在 Elasticsearch 中时，您无法取消注册仓库。如果快照的任何索引作为可搜索快照挂载在同一集群中，则也无法删除快照。  * 如果从不同集群具有写入访问权限的存储库中保存的快照挂载索引，则必须确保其他集群不会删除这些快照。  * 如果在将快照装载为可搜索快照时将其删除，则数据将丢失。同样，如果存储库发生故障或损坏快照的内容，则数据将丢失。  * 尽管 Elasticsearch 可能已将数据缓存到本地存储中，但这些缓存可能不完整，无法用于在存储库发生故障后恢复任何数据。您必须确保您的存储库是可靠的，并且可以防止数据在存储库中处于静止状态时损坏。

所有主要公共云提供商提供的 blob 存储通常提供非常好的保护，防止数据丢失或损坏。如果您管理自己的存储库存储，那么您要对其可靠性负责。

[« Restore a snapshot](snapshots-restore-snapshot.md) [Secure the Elastic
Stack »](secure-cluster.md)
