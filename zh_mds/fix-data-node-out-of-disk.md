

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Troubleshooting corruption](corruption-troubleshooting.md) [Increase the
disk capacity of data nodes »](increase-capacity-data-node.md)

## 修复磁盘外数据节点

Elasticsearch 使用数据节点在集群内分发数据。如果其中一个或多个节点的空间不足，Elasticsearch 会采取措施在节点内重新分发数据，以便所有节点都有足够的可用磁盘空间。如果 Elasticsearch 无法在节点中提供足够的可用空间，则需要通过以下两种方式之一进行干预：

1. 增加集群的磁盘容量 2.通过减少数据量来减少磁盘使用量

[« Troubleshooting corruption](corruption-troubleshooting.md) [Increase the
disk capacity of data nodes »](increase-capacity-data-node.md)
