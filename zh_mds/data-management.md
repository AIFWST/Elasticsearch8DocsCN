

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Advanced scripts using script engines](modules-scripting-engine.md) [ILM:
Manage the index lifecycle »](index-lifecycle-management.md)

# 数据管理

存储在 Elasticsearch 中的数据通常分为两类：

* 内容：要搜索的项目集合，例如产品目录 * 时间序列数据：连续生成的时间戳数据流，例如日志条目

内容可能会频繁更新，但内容的价值随着时间的推移保持相对恒定。您希望能够快速检索项目，无论它们有多旧。

时序数据会随着时间的推移而不断累积，因此您需要策略来平衡数据的价值与存储数据的成本。随着时间的流逝，它往往变得不那么重要且访问频率较低，因此您可以将其转移到更便宜、性能较低的硬件上。对于您最旧的数据，重要的是您可以访问数据。如果查询需要更长的时间才能完成，也没关系。

为了帮助您管理数据，Elasticsearch 为您提供了索引生命周期管理 (ILM) 来管理索引和数据流，并且它是完全可定制的。

**ILM** 可用于管理索引和数据流，它允许您：

* 定义数据的保留期。保留期是您的数据存储在 Elasticsearch 中的最短时间。超过此时间段的数据可以通过 Elasticsearch 删除。  * 定义具有不同性能特征的多层数据节点。  * 根据您的性能需求和保留策略自动在数据层之间转换索引。  * 利用存储在远程存储库中的可搜索快照为旧索引提供弹性，同时降低运营成本并保持搜索性能。  * 对存储在性能较差的硬件上的数据执行异步搜索。

[« Advanced scripts using script engines](modules-scripting-engine.md) [ILM:
Manage the index lifecycle »](index-lifecycle-management.md)
