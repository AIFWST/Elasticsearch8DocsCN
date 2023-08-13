

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Autoscaling](xpack-autoscaling.md) ›[Autoscaling deciders](autoscaling-
deciders.md)

[« Autoscaling deciders](autoscaling-deciders.md) [Proactive storage decider
»](autoscaling-proactive-storage-decider.md)

## 反应式存储决策程序

反应式存储决策程序 ('reactive_storage') 计算包含当前数据集所需的存储。它表示当超过现有容量时(被动地)需要额外的存储容量。

为管理数据节点的所有策略启用反应式存储决策程序，并且没有配置选项。

决策程序部分依赖于使用数据层首选项分配而不是节点属性。特别是，如果不使用基于数据层首选项的分配，将数据层缩放为存在(启动层中的第一个节点)将导致在任何数据层中启动空节点。使用 ILM 迁移操作在层之间进行迁移是分配到层的首选方法，并且完全支持将 atier 扩展到现有。

[« Autoscaling deciders](autoscaling-deciders.md) [Proactive storage decider
»](autoscaling-proactive-storage-decider.md)
