

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[ILM concepts](ilm-concepts.md)

[« Rollover](index-rollover.md) [Index lifecycle actions »](ilm-
actions.md)

## 生命周期策略更新

您可以通过修改当前策略或切换到其他策略来更改索引或滚动索引集合的生命周期的管理方式。

为了确保策略更新不会将索引置于无法对当前阶段进行着色的状态，阶段定义在进入阶段时缓存在索引元数据中。如果可以安全地应用更改，ILM 将更新缓存的阶段定义。如果不能，阶段执行将继续使用缓存的定义。

当索引前进到下一阶段时，它将使用更新的策略中的阶段定义。

### 如何应用更改

当策略最初应用于索引时，索引将获取策略的最新版本。如果更新策略，策略版本将出现碰撞，ILM 可以检测到索引使用的是需要更新的早期版本。

对"min_age"的更改不会传播到缓存的定义。更改阶段的"min_age"不会影响当前正在执行该阶段的索引。

例如，如果创建的策略具有未指定"min_age"的热阶段，则在应用策略时，索引将立即进入热阶段。如果随后更新策略以将热阶段的"min_age"指定为 1 天，则对已处于热阶段的索引没有影响。在策略更新之后创建的索引在一天前不会进入热阶段。

### 如何应用新策略

将不同的策略应用于托管索引时，索引将使用上一个策略中的缓存定义完成当前阶段。索引在进入下一阶段时开始使用新策略。

[« Rollover](index-rollover.md) [Index lifecycle actions »](ilm-
actions.md)
