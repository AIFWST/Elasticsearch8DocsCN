

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up a
cluster for high availability](high-availability.md)

[« Set up a cluster for high availability](high-availability.md) [Resilience
in small clusters »](high-availability-cluster-small-clusters.md)

## 设计弹性

像Elasticsearch这样的分布式系统被设计为即使它们的某些组件出现故障也能继续工作。只要有足够的连接良好的节点来接管它们的职责，Elasticsearch 集群就可以在其某些节点不可用或断开连接时继续正常运行。

可复原群集的尺寸存在限制。所有 Elasticsearchclusters 都需要：

* 一个选定的主节点节点 * 每个角色至少有一个节点。  * 每个分片至少有一个副本。

弹性群集需要为每个必需的群集组件提供冗余。这意味着弹性群集必须具有：

* 至少三个符合主节点条件的节点 * 每个角色至少两个节点 * 每个分片至少有两个副本(一个主副本和一个或多个副本，除非索引是可搜索的快照索引)

弹性群集需要三个符合主节点条件的节点，以便如果其中一个节点发生故障，则其余两个节点仍会形成多数并可以成功进行选举。

同样，每个角色的节点冗余意味着，如果特定角色的节点发生故障，另一个节点可以承担其职责。

最后，弹性集群应至少具有每个分片的两个副本。如果一个副本失败，那么应该有另一个好的副本来接管。Elasticsearch 会自动在剩余节点上重建任何失败的分片副本，以便在发生故障后将集群恢复到完全健康状态。

故障会暂时减少集群的总容量。此外，发生故障后，群集必须执行其他后台活动以将自身恢复正常。应确保群集具有处理工作负载的能力，即使某些节点发生故障也是如此。

根据您的需求和预算，Elasticsearch 集群可以由单个节点、数百个节点或介于两者之间的任意数量组成。设计较小的群集时，通常应侧重于使其能够复原单节点故障。大型群集的设计者还必须考虑多个节点同时发生故障的情况。以下页面提供了有关构建各种大小的可复原群集的一些建议：

* 小型集群中的弹性 * 大型集群中的弹性

[« Set up a cluster for high availability](high-availability.md) [Resilience
in small clusters »](high-availability-cluster-small-clusters.md)
