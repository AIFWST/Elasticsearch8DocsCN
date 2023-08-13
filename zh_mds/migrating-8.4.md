

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md)

[« Migrating to 8.5](migrating-8.5.md) [Migrating to 8.3
»](migrating-8.3.md)

## 迁移到 8.4

本节讨论将应用程序迁移到 Elasticsearch 8.4 时需要注意的更改。

另请参阅_What发行说明中的新增8.9_and。

### 重大变更

Elasticsearch 8.4 中没有重大更改。

###Deprecations

以下功能已在 Elasticsearch 8.4 中弃用，并将在未来的版本中删除。虽然这不会对应用程序产生直接影响，但我们强烈建议您在升级到 8.4 后采取所述步骤来更新代码。

若要了解是否正在使用任何已弃用的功能，请启用弃用日志记录。

#### REST API弃用

弃用"_knn_search"终结点

**详情** -|不推荐使用 kNN 搜索 API，取而代之的是搜索 API 中的新 _knn_ 选项。_knn_ 选项现在是运行 ANN 搜索的推荐方式。

**影响** 用户应从"_knn_search"切换到搜索"knn"选项。

[« Migrating to 8.5](migrating-8.5.md) [Migrating to 8.3
»](migrating-8.3.md)
