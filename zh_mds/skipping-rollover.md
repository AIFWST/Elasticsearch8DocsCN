

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Manage existing indices](ilm-with-existing-indices.md) [Restore a managed
data stream or index »](index-lifecycle-and-snapshots.md)

## 跳过翻转

当"index.lifecycle.indexing_complete"设置为"true"时，ILM 将不会对索引执行滚动更新操作，即使它在其他方面满足滚动更新条件也是如此。它由 ILM 在滚动更新操作成功完成时自动设置。

如果需要对正常生命周期策略进行例外并更新别名以强制滚动更新，但希望 ILM 继续管理索引，则可以手动将其设置为跳过滚动更新。如果使用滚动更新 API，则无需手动配置此设置。

如果删除索引的生命周期策略，此设置也会被删除。

当"index.lifecycle.indexing_complete"为"true"时，ILM 将验证索引是否不再是由"index.lifecycle.rollover_alias"指定的别名的写入索引。如果索引仍然是写入索引或未设置滚动更新别名，则索引将移至"ERROR"步骤。

例如，如果需要更改系列中新索引的名称，同时根据配置的策略保留以前编制索引的数据，则可以：

1. 为使用相同策略的新索引模式创建模板。  2. 引导初始索引。  3. 使用别名 API 将别名的写入索引更改为引导索引。  4. 在旧索引上将"index.lifecycle.indexing_complete"设置为"true"，以指示它不需要滚动更新。

ILM 将继续按照您的现有策略管理旧索引。新索引根据新模板命名，并根据同一策略进行管理，而不会中断。

[« Manage existing indices](ilm-with-existing-indices.md) [Restore a managed
data stream or index »](index-lifecycle-and-snapshots.md)
