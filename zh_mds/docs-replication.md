

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Document APIs](docs.md) [Index API »](docs-index_.md)

## 阅读和写作文档

####Introduction

Elasticsearch 中的每个索引都分为多个分片，每个分片可以有多个副本。这些副本称为_replication group_，在添加或删除文档时必须保持同步。如果我们不这样做，从一个副本读取将导致与从另一个副本读取非常不同的结果。保持分片副本同步并从它们提供读取的过程就是我们所说的_data复制model_。

Elasticsearch的数据复制模型基于_primary备份model_and在Microsoft研究的PacificApaper中得到了很好的描述，该模型基于复制组中充当主分片的单个副本。其他副本称为_replica shards_。主节点充当所有索引操作的主入口点。它负责验证它们并确保它们是正确的。一旦主数据库接受索引操作，主数据库还负责将该操作复制到其他副本。

本节的目的是对Elasticsearch复制模型进行高级概述，并讨论它对写入和读取操作之间的各种交互的影响。

#### 基本写入模型

Elasticsearch 中的每个索引操作首先使用路由解析到复制组，通常基于文档 ID。确定复制组后，操作将在内部转发到组的当前_primary shard_。索引的这一阶段称为_coordinating stage_。

索引的下一阶段是_primary stage_，在主分片上执行。主分片负责验证操作并将其转发到其他副本。由于副本可以脱机，因此不需要将主副本复制到所有副本。相反，Elasticsearch维护一个应该接收操作的分片副本列表。此列表称为_in同步copies_，由主节点维护。顾名思义，这些是一组"好"的分片副本，保证已经处理了已向用户确认的所有索引和删除操作。主节点负责维护此不变性，因此必须将所有操作复制到此集合中的每个副本。

主分片遵循以下基本流程：

1. 验证传入操作，如果结构无效，则拒绝它(例如：有一个对象字段，其中需要数字) 2.在本地执行操作，即索引或删除相关文档。这也将验证字段的内容，并在需要时拒绝(例如：关键字值太长，无法在 Lucene 中编制索引)。  3. 将操作转发到当前同步副本集中的每个副本。如果有多个副本，则并行完成此操作。  4. 一旦所有同步副本都成功执行了操作并响应了主副本，主副本将确认成功完成对客户端的请求。

每个同步副本副本在本地执行索引操作，以便它有一个副本。索引的这一阶段是_replica stage_。

这些索引阶段(协调阶段、主索引和副本阶段)是顺序的。要启用内部重试，每个阶段的生存期包括每个后续阶段的生存期。例如，在每个主要阶段(可能分布在不同的主分片)完成之前，协调阶段不会完成。在同步副本在本地完成对文档编制索引并响应副本请求之前，每个主要阶段都不会完成。

##### 故障处理

在索引过程中，许多事情都可能出错 - 磁盘可能会损坏，节点可能会相互断开连接，或者某些配置错误可能导致副本上的操作失败，尽管它在主副本上是成功的。这些很少见，但主要必须对它们做出回应。

如果主节点本身发生故障，托管主节点的节点将向主节点发送有关它的消息。索引操作将等待(默认情况下最多 1 分钟)，以便主副本将其中一个副本提升为新的主副本。然后，该操作将转发到新的主处理。请注意，主节点还会监控节点的运行状况，并可能决定主动降级主节点。当持有主节点的节点因网络问题与群集隔离时，通常会发生这种情况。有关更多详细信息，请参阅此处。

在主节点上成功执行操作后，主数据库在副本分片上执行操作时必须处理潜在的故障。这可能是由于复制副本上的实际故障或网络问题阻止操作到达副本(或阻止副本响应)引起的。所有这些共享相同的最终结果：作为同步副本集一部分的副本错过了即将确认的操作。为了避免违反不变量，主服务器向主服务器发送消息，请求从同步副本集中删除有问题的分片。只有在主节点确认分片的删除后，主服务器才会确认操作。请注意，主节点还将指示另一个节点开始构建新的分片副本，以便将系统恢复到正常状态。

将操作转发到副本时，主数据库将使用副本来验证它是否仍然是活动的主副本。如果主数据库由于网络分区(或长 GC)而被隔离，则在意识到它已被降级之前，它可能会继续处理传入的索引操作。来自过时主数据库的操作将被副本拒绝。当主节点收到来自副本的响应，拒绝其请求，因为它不再是主节点时，它将联系主副本并了解到它已被替换。然后将操作路由到新的主数据库。

**如果没有副本，会发生什么情况？

这是一个有效的方案，可能由于索引配置或仅仅是因为所有副本都失败而发生。在这种情况下，主数据库是在没有任何外部验证的情况下处理操作，这似乎有问题。另一方面，主分片不能自行使其他分片失败，而是代表主分片请求主分片失败。这意味着主节点知道主副本是唯一一个好的拷贝。因此，我们保证 themaster 不会将任何其他(过时的)分片副本提升为新的主副本，并且索引到主副本中的任何操作都不会丢失。当然，由于此时我们仅使用数据的单个副本运行，因此物理硬件问题可能会导致数据丢失。有关一些缓解选项，请参阅活动分片。

#### 基本读取模型

Elasticsearch 中的读取可以是按 ID 进行的非常轻量级的查找，也可以是具有复杂聚合的繁重搜索请求，这些聚合占用了不平凡的 CPU 能力。主备份模型的优点之一是它使所有分片副本保持相同(飞行中操作除外)。因此，单个同步副本足以为读取请求提供服务。

当节点收到读取请求时，该节点负责将其转发到保存相关分片的节点，整理响应并响应客户端。我们将该节点称为该请求的 _coordinatingnode_。基本流程如下：

1. 解析相关分片的读取请求。请注意，由于大多数搜索将发送到一个或多个索引，因此它们通常需要从多个分片中读取数据，每个分片代表不同的数据子集。  2. 从分片复制组中选择每个相关分片的活动副本。这可以是主副本或副本。默认情况下，Elasticsearch 使用自适应副本选择来选择分片副本。  3. 向所选副本发送分片级别读取请求。  4. 结合结果并做出回应。请注意，在按 ID 查找的情况下，只有一个分片是相关的，可以跳过此步骤。

##### 分片失败

当分片无法响应读取请求时，协调节点会将请求发送到同一复制组中的另一个分片副本。重复失败可能会导致没有可用的分片副本。

为确保快速响应，如果一个或多个分片失败，以下 API 将响应部分结果：

* 搜索 * 多重搜索 * 多重获取 API")

包含部分结果的响应仍提供"200 OK"HTTP 状态代码。分片失败由响应标头的"timed_out"和"_shards"字段指示。

#### 几个简单的含义

这些基本流程中的每一个都决定了 Elasticsearch 作为读取和写入系统的行为方式。此外，由于读取和写入请求可以同时执行，因此这两个基本流相互交互。这有一些固有的含义：

高效读取

     Under normal operation each read operation is performed once for each relevant replication group. Only under failure conditions do multiple copies of the same shard execute the same search. 
Read unacknowledged

     Since the primary first indexes locally and then replicates the request, it is possible for a concurrent read to already see the change before it has been acknowledged. 
Two copies by default

     This model can be fault tolerant while maintaining only two copies of the data. This is in contrast to quorum-based system where the minimum number of copies for fault tolerance is 3. 

####Failures

在失败的情况下，可能出现以下情况：

单个分片可能会减慢索引速度

     Because the primary waits for all replicas in the in-sync copies set during each operation, a single slow shard can slow down the entire replication group. This is the price we pay for the read efficiency mentioned above. Of course a single slow shard will also slow down unlucky searches that have been routed to it. 
Dirty reads

     An isolated primary can expose writes that will not be acknowledged. This is caused by the fact that an isolated primary will only realize that it is isolated once it sends requests to its replicas or when reaching out to the master. At that point the operation is already indexed into the primary and can be read by a concurrent read. Elasticsearch mitigates this risk by pinging the master every second (by default) and rejecting indexing operations if no master is known. 

#### 冰山一角

本文档提供了 Elasticsearch 如何处理数据的高级概述。当然，引擎盖下还有更多的事情要做。诸如主要术语、集群状态发布和主选举之类的东西都在保持该系统正常运行方面发挥作用。本文档也不涵盖已知和重要的错误(关闭和打开)。我们认识到GitHub很难跟上。为了帮助人们掌握这些内容，我们在网站上维护了一个专门的弹性页面。我们强烈建议您阅读它。

[« Document APIs](docs.md) [Index API »](docs-index_.md)
