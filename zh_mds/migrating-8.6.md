

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md)

[« Migrating to 8.7](migrating-8.7.md) [Migrating to 8.5
»](migrating-8.5.md)

## 迁移到 8.6

本节讨论将应用程序迁移到 Elasticsearch 8.6 时需要注意的更改。

另请参阅_What发行说明中的新增8.9_and。

### 重大变更

Elasticsearch 8.6 中没有重大更改。

###Deprecations

以下功能已在 Elasticsearch 8.6 中弃用，并将在未来的版本中删除。虽然这不会对应用程序产生直接影响，但我们强烈建议您在升级到 8.6 后采取所述步骤来更新代码。

若要了解是否正在使用任何已弃用的功能，请启用弃用日志记录。

#### 原油弃用

弃用_remove_binary_摄取附件处理器的默认值 false。

**详细信息** 附件处理器的默认"remove_binary"选项将在以后的 Elasticsearch 版本中从 false 更改为 true。这意味着发送到 Elasticsearch 的二进制文件将不会保留。

**影响** 用户应将"remove_binary"选项更新为显式 true 或 false，而不是依赖默认值，这样任何默认值更改都不会影响 Elasticsearch。

#### 群集和节点设置弃用

确保余额阈值至少为 1

**详细信息** 小于"1"的"cluster.routing.allocation.balance.threshold"的值现在被忽略。不推荐使用此设置小于"1"的值，并且在将来的版本中将禁止。

**影响** 将"cluster.routing.allocation.balance.threshold"设置为至少"1"。

#### 映射弃用

弃用静默忽略元数据字段定义中的类型、字段、copy_to和提升

**详细信息** 当作为索引映射中元数据字段配置的一部分提供时，不支持的参数(如类型、字段、copy_to和提升)将被静默忽略。当在从 8.6 开始创建的索引的映射中使用时，它们将导致弃用警告。

**影响** 若要解决弃用警告，请从任何元数据字段定义中删除对类型、字段copy_to或提升的提及，作为索引映射的一部分。它们不会生效，因此删除它们除了解决弃用警告外不会产生任何影响。

#### REST API弃用

状态字段在 /_cluster/重新路由响应中已弃用

**详细信息**"状态"字段在"/_cluster/reroute"响应中已弃用。群集状态不提供有关重新路由/命令执行结果的有意义的信息。不能保证会应用此确切状态。

**影响** 重新路由 API 用户不应依赖"状态"字段，而应使用"解释"来请求命令执行的结果。

[« Migrating to 8.7](migrating-8.7.md) [Migrating to 8.5
»](migrating-8.5.md)
