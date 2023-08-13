

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md)

[« Migrating to 8.2](migrating-8.2.md) [Migrating to 8.0
»](migrating-8.0.md)

## 迁移到 8.1

本节讨论将应用程序迁移到 Elasticsearch 8.1 时需要注意的更改。

另请参阅_What发行说明中的新增8.9_and。

### 重大变更

Elasticsearch 8.1 中的以下更改可能会影响您的应用程序并阻止它们正常运行。在升级到 8.1 之前，请查看这些更改并采取所述的步骤来减轻影响。

#### REST API 更改

搜索 API 的"字段"参数现在规范化跨越国际日期变更线的几何对象

**详细信息** 搜索 API 的"字段"参数现在规范化穿过国际日期变更线(+/-180° 经度)的"geo_shape"对象。例如，如果多边形与日期变更线交叉，则"fields"参数将其作为两个多边形返回。您仍然可以从"_source"中检索原始的非规范化几何对象。

**影响** 如果应用程序需要非规范化的几何对象，请从"_source"中检索它们，而不是使用"fields"参数。

###Deprecations

以下功能已在 Elasticsearch 8.1 中弃用，并将在未来的版本中删除。虽然这不会对应用程序产生直接影响，但我们强烈建议您在升级到 8.1 后执行所述步骤来更新代码。

若要了解是否正在使用任何已弃用的功能，请启用弃用日志记录。

#### 群集和节点设置弃用

"discovery.type"设置的旧值已弃用

**详细信息** "discovery.type"设置的旧值已弃用，并且在将来的版本中将被禁止。

**影响** 不要将"discovery.type"设置为除"单节点"或"多节点"以外的任何值。所有其他值等效于默认发现类型"多节点"。在可能的情况下，省略此设置，以便 Elasticsearch 使用默认的发现类型。

#### REST API弃用

不推荐对批量操作进行宽松解析

**详细信息** 旧版本的 Elasticsearch 非常宽松地解析批量请求的操作行，并且会静默地忽略无效或格式错误的操作。此宽大已弃用，将来的版本将拒绝包含无效操作的批量请求。

**影响** 确保批量操作是格式正确的 JSON 对象，其中包含具有正确键的单个条目。

弃用"_sql"API 中的"index_include_frozen"请求参数

**详细信息** 在弃用冻结索引之后，"index_include_frozen"参数和"冻结"语法现在也被弃用。

**影响** 您应该使用 unfreeze indexAPI 解冻冻结的索引，并停止在 SQLquery 中使用 'index_include_frozen' 参数或 'FROZEN' 关键字。对于某些用例，冻结层可能是冻结索引的合适替代品。有关详细信息，请参阅数据层。

[« Migrating to 8.2](migrating-8.2.md) [Migrating to 8.0
»](migrating-8.0.md)
