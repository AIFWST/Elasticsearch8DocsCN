

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up a
cluster for high availability](high-availability.md)

[« Resilience in larger clusters](high-availability-cluster-design-large-
clusters.md) [Tutorial: Set up cross-cluster replication »](ccr-getting-
started-tutorial.md)

## 跨集群复制

通过跨集群复制，您可以跨集群复制索引以：

* 在数据中心中断时继续处理搜索请求 * 防止搜索量影响索引吞吐量 * 通过处理与用户地理位置接近的搜索请求来减少搜索延迟

跨集群复制使用主动-被动模型。索引到a_leader_索引，数据将复制到一个或多个只读_follower_indices。在向集群添加追随者索引之前，必须配置包含领导者索引的_remote cluster_。

当领导索引收到写入时，从属索引从远程集群上的领导索引中提取更改。您可以手动创建追随者索引，或配置自动关注模式以自动为新的时间序列索引创建追随者索引。

您可以在单向或双向设置中配置跨集群复制集群：

* 在单向配置中，一个集群仅包含领导者索引，另一个集群仅包含追随者索引。  * 在双向配置中，每个集群都包含领导者和追随者索引。

在单向配置中，包含追随者索引的集群必须运行与远程集群相同或更新的 Elasticsearch 版本。如果较新，则版本还必须兼容，如以下矩阵中所述。

版本兼容性矩阵

|

本地群集 ---|--- 远程群集

|

5.0–5.5

|

5.6

|

6.0–6.6

|

6.7

|

6.8

|

7.0

|

7.1–7.16

|

7.17

|

8.0–8.9    5.0–5.5

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 5.6

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 6.0–6.6

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 6.7

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 6.8

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!否 7.0

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!否 7.1–7.16

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!否 7.17

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.0–8.9

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 ### 多群集体系结构编辑

使用跨集群复制在弹性堆栈中构建多个多集群架构：

* 主集群发生故障时的灾难恢复，辅助集群作为热备份 * 数据局部性，可在应用程序服务器(和用户)附近维护数据集的多个副本，并减少代价高昂的延迟 * 集中报告，用于最大限度地减少查询多个地理分布式 Elasticsearch 集群的网络流量和延迟，或者通过将搜索卸载到辅助集群来防止搜索负载干扰索引

观看跨集群复制网络研讨会，了解有关以下用例的更多信息。然后，在本地计算机上设置跨集群复制，并完成网络研讨会中的演示。

在所有这些用例中，您必须在每个集群上独立配置安全性。为灾难恢复配置跨群集复制时，不会复制安全配置。为了确保备份 Elasticsearch 的"安全"功能状态，请定期拍摄快照。然后，您可以从安全配置中还原本机用户、角色和令牌。

#### 灾难恢复和高可用性

灾难恢复为任务关键型应用程序提供了承受数据中心或区域中断的容错能力。此用例是最常见的跨集群复制部署。您可以配置集群不同架构，以支持灾难恢复和高可用性：

* 单个灾难恢复数据中心 * 多个灾难恢复数据中心 * 链式复制 * 双向复制

##### 单个灾难恢复数据中心

在此配置中，数据从生产数据中心复制到灾难恢复数据中心。由于追随者索引复制了领导者索引，因此如果生产数据中心不可用，应用程序可以使用灾难恢复数据中心。

!将数据复制到灾难恢复数据中心的生产数据中心

##### 多个灾难恢复数据中心

可以将数据从一个数据中心复制到多个数据中心。此配置提供灾难恢复和高可用性，确保在主数据中心关闭或不可用时在两个数据中心复制数据。

在下图中，数据中心 A 中的数据将复制到数据中心频段数据中心 C，这两个频段都具有来自数据中心 A 的领导者索引的只读副本。

!将数据复制到其他两个数据中心的生产数据中心

##### 链式复制

可以跨多个数据中心复制数据以形成复制链。在下图中，数据中心 A 包含领导者索引。数据中心 B 从数据中心 A 复制数据，数据中心 C 从数据中心 B 中的从属索引复制数据。这些数据中心之间的连接形成链式复制模式。

!连接三个数据中心以形成复制链

##### 双向复制

在双向复制设置中，所有群集都有权查看所有数据，并且所有群集都有一个要写入的索引，而无需手动实现故障转移。应用程序可以写入每个数据中心内的本地索引，并跨多个索引进行读取，以获得所有信息的全局视图。

当群集或数据中心不可用时，此配置不需要手动干预。在下图中，如果数据中心 A 不可用，则可以继续使用数据中心 B，而无需手动故障转移。当数据中心 A 联机时，群集之间的复制将恢复。

!双向配置，其中每个集群都包含一个领导者索引和追随者索引

此配置对于仅索引工作负载特别有用，在这些工作负载中，文档值不会更新。在此配置中，由 Elasticsearch 索引的文档是不可变的。客户端位于每个数据中心和 Elasticsearch 集群旁边，不与不同数据中心中的集群通信。

#### 数据局部性

使数据更接近用户或应用程序服务器可以减少延迟和响应时间。此方法也适用于在 Elasticsearch 中复制数据。例如，您可以将产品目录或引用数据集复制到全球 20 个或更多数据中心，以最大程度地缩短数据与应用程序服务器之间的距离。

在下图中，数据从一个数据中心复制到另外三个数据中心，每个数据中心都位于各自的区域中。中央数据中心包含领导者索引，其他数据中心包含在该特定区域中复制数据的追随者索引。此配置使数据更接近访问它的应用程序。

!跨其他三个数据中心复制的集中式数据中心

#### 集中式报告

当跨大型网络的查询效率低下时，使用集中式报表群集非常有用。在此配置中，将数据从许多较小的群集复制到集中式报表群集。

例如，一家大型全球银行可能在全球拥有 100 个 Elasticsearch 集群，这些集群分布在每个银行分行的不同区域。使用跨集群复制，银行可以将所有 100 家银行的事件复制到中央集群，以在本地分析和聚合事件以进行报告。银行可以使用跨集群复制来复制特定索引，而不是维护镜像集群。

在下图中，来自不同区域中的三个数据中心的数据将复制到集中式报表群集。使用此配置，可以将数据从区域中心复制到中央群集，您可以在其中在本地运行所有报表。

!不同区域中的三个群集将数据发送到集中式报告群集进行分析

### 复制机制

尽管您在索引级别设置了跨集群复制，但 Elasticsearch 在分片级别实现了复制。创建追随者索引时，该索引中的每个分片都会从领导者索引中的相应分片中提取更改，这意味着追随者索引的分片数与其领导者索引相同。领导者上的所有操作都由追随者复制，例如创建、更新或删除文档的操作。这些请求可以从 leaderhard 的任何副本(主副本或副本副本)提供服务。

当从属分片发送读取请求时，领导分片会使用任何新操作进行响应，这些操作受您在配置从属索引时建立的读取参数的限制。如果没有新操作可用，领导者将等待新操作的配置超时。如果超时过后，领导者分片将响应追随者分片，指出没有新操作。追随者分片更新分片统计信息，并立即向领导者分片发送另一个读取请求。此通信模型可确保远程群集和本地群集之间的网络连接持续使用，避免外部源(如防火墙)强制终止。

如果读取请求失败，则会检查失败的原因。如果故障原因被认为是可恢复的(例如网络故障)，则跟随者分片将进入重试循环。否则，追随者分片将暂停，直到您恢复它。

#### 处理更新

您无法手动修改关注者索引的映射或别名。要进行更改，必须更新领导者索引。因为它们是只读的，所以追随者索引拒绝所有配置中的写入。

尽管对领导者索引上的别名所做的更改会复制到追随者索引，但写入索引将被忽略。追随者索引不能接受直接写入，因此如果任何领导者别名将"is_write_index"设置为"true"，则该值将强制为"false"。

例如，在数据中心 A 中为名为"doc_1"的文档编制索引，该文档复制到数据中心 B。如果客户端连接到数据中心 B 并尝试更新"doc_1"，则请求将失败。若要更新"doc_1"，客户端必须连接到数据中心 A 并更新领导索引中的文档。

当追随者分片从领导分片接收操作时，它会将这些操作放在写入缓冲区中。追随者分片使用写入缓冲区中的操作提交批量写入请求。如果写入缓冲区超过配置的限制，则不会发送其他读取请求。此配置提供针对读取请求的背压，允许从属分片在写入缓冲区不再满时恢复发送读取请求。

要管理如何从领导者索引复制操作，可以在创建从属索引时配置设置。

领导者索引上的索引映射更改将尽快复制到追随者索引。此行为也适用于索引设置，但领导者索引本地的某些设置除外。例如，从属索引不会复制更改领导者索引上的副本数，因此可能无法检索该设置。

如果对追随者索引所需的领导索引应用非动态设置更改，则从属者索引将自行关闭，应用设置更新，然后重新打开自身。追随者索引不可用于读取，并且在此周期内无法复制写入。

### 使用远程恢复初始化关注者

创建追随者索引时，在完全初始化之前无法使用它。_remote recovery_ 进程通过从领导集群中的主分片复制数据，在追随者节点上构建分片的新副本。

Elasticsearch 使用此远程恢复过程使用领导者索引中的数据引导追随者索引。此过程为追随者提供了领导者索引当前状态的副本，即使由于 Lucene 段合并而无法在领导者上提供完整的更改历史记录。

远程恢复是一个网络密集型过程，它将所有 Lucene 分段文件从领导集群传输到从属集群。追随者请求在领导集群中的主分片上启动恢复会话。然后，追随者同时从领导者请求文件块。默认情况下，进程并发请求五个 1MB 的文件块。此默认行为旨在支持领导者和追随者集群之间具有高网络延迟。

您可以修改动态远程恢复设置，以限制传输数据的速率并管理远程恢复消耗的资源。

使用包含追随者索引的集群上的恢复 API 获取有关正在进行的远程恢复的信息。由于 Elasticsearch 使用快照和恢复基础架构实现远程恢复，因此在恢复 API 中，运行远程恢复被标记为"快照"类型。

### 复制领导者需要软删除

跨集群复制的工作原理是在领导者索引的分片上执行的各个写入操作的历史记录。Elasticsearch 需要在领导者分片上保留这些操作的历史记录，以便它们可以被追随者分片任务拉取。用于保留这些操作的基本机制是_soft deletes_。

每当删除或更新现有文档时，都会发生软删除。通过将这些软删除保留到可配置的限制，操作历史记录可以保留在领导者分片上，并在重播操作历史记录时提供给追随者分片任务。

"index.soft_deletes.retention_lease.period"设置定义了在分片历史记录保留租约被视为过期之前保留的最长时间。此设置确定包含关注者索引的集群可以脱机多长时间，默认情况下为 12 小时。如果分片副本在其保留租约到期后恢复，但缺少的操作在领导者索引上仍然可用，则 Elasticsearch 将建立新的租约并复制缺少的操作。但是，Elasticsearch 不保证保留未租用的操作，因此也有可能一些缺失的操作已被领导者丢弃，现在完全不可用。如果发生这种情况，则关注者无法自动恢复，因此您必须重新创建它。

必须为要用作领导者索引的索引启用软删除。默认情况下，在 Elasticsearch 7.0.0 上或之后创建的新索引上启用软删除。

跨集群复制不能用于使用 Elasticsearch 7.0.0 或更早版本创建的现有索引，其中软删除处于禁用状态。必须将数据重新索引到启用了软删除的新索引中。

### 使用跨群集复制

以下部分提供了有关如何配置和使用跨集群复制的详细信息：

* 设置跨集群复制 * 管理跨集群复制 * 管理自动关注模式 * 升级集群

### 跨集群复制限制

跨集群复制旨在仅复制用户生成的索引，目前不复制以下任何索引：

* 系统索引 * 机器学习作业 * 索引模板 * 索引生命周期管理和快照生命周期管理策略 * 用户权限和角色映射 * 快照存储库设置 * 群集设置 * 可搜索快照

如果要复制任何此类数据，则必须手动将其复制到远程群集。

可搜索快照索引的数据存储在快照存储库中。跨集群复制不会完全复制这些索引，即使它们部分或完全缓存在 Elasticsearch 节点上。要在远程群集中实现可搜索的快照，请在远程群集上配置快照存储库，并使用本地群集中的相同索引生命周期管理策略将数据移动到远程群集上的冷层或冻结层。

[« Resilience in larger clusters](high-availability-cluster-design-large-
clusters.md) [Tutorial: Set up cross-cluster replication »](ccr-getting-
started-tutorial.md)
