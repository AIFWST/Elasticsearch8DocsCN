

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up a
cluster for high availability](high-availability.md) ›[Designing for
resilience](high-availability-cluster-design.md)

[« Designing for resilience](high-availability-cluster-design.md)
[Resilience in larger clusters »](high-availability-cluster-design-large-
clusters.md)

## 小型集群中的弹性

在较小的群集中，对单节点故障具有复原能力最为重要。本部分提供了一些指导，说明如何使群集尽可能能够复原单个节点的故障。

### 单节点集群

如果群集由一个节点组成，则该单个节点必须执行所有操作。为了适应这种情况，Elasticsearch 默认为每个角色分配节点。

单节点群集不具有复原能力。如果节点发生故障，群集将停止工作。由于单节点群集中没有副本，因此无法冗余存储数据。但是，默认情况下，"绿色"群集运行状况至少需要一个副本。要确保您的集群可以报告"绿色"状态，请通过在每个索引上将"index.number_of_replicas"设置为"0"来覆盖默认值。

如果节点发生故障，您可能需要从快照还原任何丢失索引的旧副本。

由于它们无法从任何故障中复原，因此我们不建议在生产中使用单节点群集。

### 双节点群集

如果有两个节点，建议它们都是数据节点。您还应该通过在不是可搜索快照索引的每个索引上将"index.number_of_replicas"设置为"1"来确保每个分片都冗余存储在两个节点上。这是默认行为，但可能会被索引模板覆盖。自动扩展副本也可以实现相同的功能，但没有必要在如此小的集群中使用此功能。

我们建议您仅将两个节点中的一个设置为符合主节点条件。这意味着您可以确定哪个节点是集群的选定主节点。集群可以容忍丢失另一个不符合主节点的节点。如果将两个节点都设置为符合主节点条件，则主节点选举需要两个节点。由于如果任一节点不可用，选举将失败，因此您的集群无法可靠地容忍任一节点的丢失。

默认情况下，为每个节点分配每个角色。我们建议您为这两个节点分配除主资格之外的所有其他角色。如果一个节点发生故障，另一个节点可以处理其任务。

应避免仅将客户端请求发送到其中一个节点。如果这样做并且此节点失败，则即使剩余节点本身是正常运行的群集，此类请求也不会收到响应。理想情况下，您应该在两个节点之间平衡客户端请求。执行此操作的一个好方法是在配置客户端以连接到群集时指定两个节点的地址。或者，您可以使用弹性负载均衡器在群集中的节点之间平衡客户端请求。

由于它不能从故障中复原，因此我们不建议在生产环境中部署双节点群集。

### 具有 atiebreaker 的双节点群集

由于主选举是基于多数的，因此上面描述的双节点群集可以容忍丢失其中一个节点，但不能容忍另一个节点的丢失。您不能配置双节点群集，以便它可以容忍of_either_节点丢失，因为这在理论上是不可能的。您可能会期望，如果其中一个节点发生故障，那么 Elasticsearch 可以选择剩余的节点作为主节点，但无法区分远程节点的故障和节点之间的连接丢失。如果两个节点都能够运行独立选举，则失去连接将导致裂脑问题)，从而导致数据丢失。Elasticsearch 避免了这种情况，并通过选择两个节点作为主节点来保护您的数据，直到该节点可以确保它具有最新的集群状态并且集群中没有其他主节点。这可能会导致集群在连接恢复之前没有主节点。

您可以通过添加第三个节点并使所有三个节点都符合主节点资格来解决此问题。主节点选举只需要三个符合主节点条件的节点中的两个。这意味着群集可以容忍任何单个节点的丢失。在两个原始节点彼此断开连接的情况下，此第三个节点充当仲裁。您可以通过使此额外节点成为专用的仅投票主节点(也称为专用仲裁节点)来减少此额外节点的资源需求。由于专用仲裁器没有其他角色，因此不需要像其他两个节点那样强大。它不会执行任何搜索，也不会协调任何客户端请求，并且不能被选为集群的主节点。

两个原始节点不应是仅投票的主节点，因为弹性集群至少需要三个符合主节点条件的节点，其中至少两个不是仅投票的主节点。如果三个节点中的两个是仅投票的主节点，则当选的主节点必须是第三个节点。然后，此节点将成为单点故障。

我们建议为两个非仲裁节点分配所有其他角色。这通过确保群集中的任何任务都可以由任一节点处理来创建冗余。

不应将任何客户机请求发送到专用仲裁节点。还应避免仅将客户端请求发送到其他两个节点之一。如果这样做，并且此节点失败，则任何请求都不会收到响应，即使其余节点形成健康的群集也是如此。理想情况下，您应该在两个非仲裁节点之间平衡客户端请求。您可以通过在配置客户端以连接到群集时指定两个节点的地址来执行此操作。或者，您可以使用弹性负载均衡器在群集中的相应节点之间平衡客户端请求。弹性云服务提供了这样的负载均衡器。

具有附加仲裁节点的双节点集群是适用于生产部署的最小可能集群。

### 三节点集群

如果您有三个节点，我们建议它们都是数据节点，并且每个不是可搜索快照索引的索引都应至少有一个副本。默认情况下，节点是数据节点。您可能希望某些索引具有两个副本，以便每个节点在这些索引中具有每个分片的副本。您还应该将每个节点配置为符合主节点条件，以便其中任意两个节点都可以举行主节点选举，而无需与第三个节点通信。默认情况下，节点符合主节点条件。此群集将能够抵御任何单个节点的丢失。

应避免仅将客户端请求发送到其中一个节点。如果这样做，并且此节点失败，则即使其余两个节点形成健康的群集，任何请求也不会收到响应。理想情况下，您应该在所有三个节点之间平衡客户端请求。为此，您可以在配置客户端以连接到群集时指定多个节点的地址。或者，您可以使用弹性负载均衡器来平衡集群中的客户端请求。弹性云服务提供了这样的负载均衡器。

### 具有三个以上节点的集群

一旦您的集群增长到三个以上的节点，您就可以开始根据这些节点的职责专门化这些节点，从而允许您根据需要独立扩展其资源。您可以拥有任意数量的数据节点、采集节点、机器学习节点等。根据需要支持您的工作负载。随着群集越来越大，我们建议为每个角色使用专用节点。这允许您为每个任务独立缩放资源。

但是，最好将群集中符合主节点条件的节点数限制为三个。主节点不像其他节点类型那样扩展，因为集群始终只选择其中一个作为集群的主节点。如果符合主节点条件的节点过多，则主节点选举可能需要更长的时间才能完成。在较大的集群中，我们建议您将某些节点配置为符合主条件的专用节点，并避免向这些专用节点发送任何客户端请求。如果符合主节点条件的节点被其他节点之一处理的不必要的额外工作所淹没，则您的集群可能会变得不稳定。

您可以将其中一个符合主节点条件的节点配置为仅投票节点，这样它就永远不能被选为主节点。例如，您可能有两个专用主节点和第三个节点，该节点既是数据节点，又是仅投票的主节点。这第三个仅投票节点将在主选举中充当破坏者，但永远不会成为主节点本身。

###Summary

只要以下条件，群集就可以灵活应对任何节点的丢失：

* 群集运行状况为"绿色"。  * 至少有两个数据节点。  * 除了主索引之外，每个不是可搜索快照索引的索引每个分片至少有一个副本。  * 群集至少具有三个符合主节点条件的节点，只要其中至少两个节点不是仅投票的主节点。  * 客户端配置为将其请求发送到多个节点，或者配置为使用负载均衡器在一组适当的节点之间平衡请求。弹性云服务提供了这样的负载均衡器。

[« Designing for resilience](high-availability-cluster-design.md)
[Resilience in larger clusters »](high-availability-cluster-design-large-
clusters.md)
