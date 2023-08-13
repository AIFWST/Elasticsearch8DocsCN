

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md)

[« Migrating to 8.9](migrating-8.9.md) [Migrating to 8.7
»](migrating-8.7.md)

## 迁移到 8.8

本节讨论将应用程序迁移到 Elasticsearch 8.8 时需要注意的更改。

另请参阅_What发行说明中的新增8.9_and。

### 重大变更

Elasticsearch 8.8 中没有重大更改。

###Deprecations

以下功能已在 Elasticsearch 8.8 中弃用，并将在未来的版本中删除。虽然这不会对应用程序产生直接影响，但我们强烈建议您在升级到 8.8 后采取所述步骤来更新代码。

若要了解是否正在使用任何已弃用的功能，请启用弃用日志记录。

#### 群集和节点设置弃用

弃用"cluster.routing.allocation.type"

**详细信息** "cluster.routing.allocation.type"设置已弃用，并将在将来的版本中删除。

**影响** 停止使用"cluster.routing.allocation.type"设置。

[« Migrating to 8.9](migrating-8.9.md) [Migrating to 8.7
»](migrating-8.7.md)
