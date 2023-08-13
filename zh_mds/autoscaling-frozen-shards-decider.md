

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Autoscaling](xpack-autoscaling.md) ›[Autoscaling deciders](autoscaling-
deciders.md)

[« Proactive storage decider](autoscaling-proactive-storage-decider.md)
[Frozen storage decider »](autoscaling-frozen-storage-decider.md)

## 冻结分片决策程序

冻结分片决策程序 ('frozen_shards') 计算在冻结层中搜索当前部分挂载的索引集所需的内存。根据每个分片所需的内存量，它会计算冻结层中的必要内存。

### 配置设置

`memory_per_shard`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) The memory needed per shard, in bytes. Defaults to 2000 shards per 64 GB node (roughly 32 MB per shard). Notice that this is total memory, not heap, assuming that the Elasticsearch default heap sizing mechanism is used and that nodes are not bigger than 64 GB. 

[« Proactive storage decider](autoscaling-proactive-storage-decider.md)
[Frozen storage decider »](autoscaling-frozen-storage-decider.md)
