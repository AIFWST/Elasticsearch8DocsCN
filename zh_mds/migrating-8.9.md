

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md)

[« Migration guide](breaking-changes.md) [Migrating to 8.8
»](migrating-8.8.md)

## 迁移到 8.9

本节讨论将应用程序迁移到 Elasticsearch 8.9 时需要注意的更改。

另请参阅_What发行说明中的新增8.9_and。

### 重大变更

Elasticsearch 8.9 中的以下更改可能会影响您的应用程序并阻止它们正常运行。在升级到 8.9 之前，请查看这些更改并采取所述的步骤来减轻影响。

#### REST API 更改

默认情况下，将 TDigestState 切换为使用"混合摘要"

**详细信息** 百分位计算中 TDigest 的默认实现切换到新的内部实现，提供卓越的性能(2-10 倍加速)，对于非常大的样本群体，精度损失非常小。

**影响** 此更改会导致在百分位数计算中生成略有不同的结果。如果需要尽可能高的准确度，或者产生与以前版本完全相同的结果至关重要，则可以在给定百分位数计算的"tdigest"规范中将"execution_hint"设置为"high_accuracy"，或者在群集设置中将"search.aggs.tdigest_execution_hint"设置为"high_accuracy"以应用于所有百分位查询。

[« Migration guide](breaking-changes.md) [Migrating to 8.8
»](migrating-8.8.md)
