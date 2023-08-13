

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up a
cluster for high availability](high-availability.md) ›[Cross-cluster
replication](xpack-ccr.md)

[« Manage auto-follow patterns](ccr-auto-follow.md) [Tutorial: Disaster
recovery based on uni-directional cross-cluster replication »](ccr-disaster-
recovery-uni-directional-tutorial.md)

## 使用跨集群复制升级集群

主动使用跨集群复制的集群需要谨慎进行升级。以下情况可能会导致索引跟踪在滚动升级期间失败：

* 尚未升级的集群将拒绝从升级的集群复制的新索引设置或映射类型。  * 当索引跟随尝试回退到基于文件的恢复时，群集中尚未升级的节点将拒绝来自已升级群集中节点的索引文件。此限制是由于 Lucene 不向前兼容。

在启用了跨集群复制的集群上运行滚动升级的方法因单向和双向索引跟随而异。

### 单向索引跟随

在单向配置中，一个集群仅包含领导者索引，另一个集群仅包含复制领导者索引的追随者索引。

在此策略中，应首先升级具有追随者索引的集群，最后升级具有领导者索引的集群。按此顺序升级群集可确保索引跟踪可以在升级期间继续，而不会停机。

您还可以使用此策略升级复制链。首先升级链末端的集群，然后返回到包含领导者索引的集群。

例如，考虑集群 A 包含所有领导者索引的配置。集群 B 遵循集群 A 中的索引，集群 C 遵循集群 B 中的索引。

    
    
    Cluster A
            ^--Cluster B
                       ^--Cluster C

在此配置中，按以下顺序升级群集：

1. 提案集 C 2.提案集 B 3.集群 A

### 双向索引跟随

在双向配置中，每个集群都包含领导者和追随者索引。

在此配置中升级集群时，请在升级两个集群之前暂停所有索引跟踪并暂停自动关注模式。

升级两个集群后，恢复索引关注并恢复自动关注模式的复制。

[« Manage auto-follow patterns](ccr-auto-follow.md) [Tutorial: Disaster
recovery based on uni-directional cross-cluster replication »](ccr-disaster-
recovery-uni-directional-tutorial.md)
