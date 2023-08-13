

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Transform limitations](transform-limitations.md) [Designing for
resilience »](high-availability-cluster-design.md)

# 设置集群实现高可用

您的数据对您很重要。保持它的安全性和可用性对Elasticsearch来说很重要。有时，群集可能会遇到硬件故障或断电。为了帮助您进行规划，Elasticsearch 提供了许多功能，以便在出现故障的情况下实现高可用性。

* 通过适当的规划，可以将群集设计为能够恢复许多经常出错的情况，从单个节点或网络连接的丢失到区域范围的中断(如断电)。  * 您可以使用跨集群复制将数据复制到远程 _follower_ 集群，该集群可能位于不同的数据中心，甚至与领导集群位于不同的大陆。从属集群充当热备用集群，随时准备在发生严重到领导集群发生故障的灾难时进行故障转移。关注者群集还可以充当异地副本，以提供来自附近客户端的搜索。  * 防止数据丢失的最后一道防线是定期拍摄集群快照，以便在需要时可以在其他位置恢复其全新的副本。

[« Transform limitations](transform-limitations.md) [Designing for
resilience »](high-availability-cluster-design.md)
