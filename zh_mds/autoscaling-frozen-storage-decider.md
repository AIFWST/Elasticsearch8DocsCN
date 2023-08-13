

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Autoscaling](xpack-autoscaling.md) ›[Autoscaling deciders](autoscaling-
deciders.md)

[« Frozen shards decider](autoscaling-frozen-shards-decider.md) [Frozen
existence decider »](autoscaling-frozen-existence-decider.md)

## 冻结存储决策程序

冻结存储决策程序 ('frozen_storage') 根据此类索引的总数据集大小的百分比计算搜索当前部分挂载索引集所需的本地存储。当现有容量小于百分比乘以总数据集大小时，它表示需要额外的存储容量。

冻结存储决策程序为管理冻结数据节点的所有策略启用，并且没有配置选项。

### 配置设置

`percentage`

     (Optional, number value) Percentage of local storage relative to the data set size. Defaults to 5. 

[« Frozen shards decider](autoscaling-frozen-shards-decider.md) [Frozen
existence decider »](autoscaling-frozen-existence-decider.md)
