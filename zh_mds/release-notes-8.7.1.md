

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.8.0](release-notes-8.8.0.md) [Elasticsearch
version 8.7.0 »](release-notes-8.7.0.md)

## 弹性搜索版本8.7.1

另请参阅 8.7 中的重大更改。

### 已知问题

* 创建传输消息时可能会抛出"ArrayIndexOutOfBoundsException"

对用于创建传输消息的缓冲区的某些写入和查找序列可能会遇到对齐错误，从而导致"ArrayIndexOutOfBoundsException"，从而阻止发送传输消息。

此问题已在 8.8.0 中修复。

* 分片重新平衡可能会暂时使集群失去平衡

从 8.6.0 开始，默认的分片重新平衡算法将计算最终的期望余额，然后进行分片移动以协调集群的当前状态与期望状态。但是，分片移动发生的顺序可能会偏向某些节点，从而导致集群在协调过程中暂时变得不平衡。与往常一样，一旦节点达到磁盘水印，它将不接受任何其他分片，但这种倾斜可能会导致节点在正常操作中比预期更频繁地到达其磁盘水印。对帐过程完成后，群集将再次平衡。

要避免此问题，请升级到 8.8.0 或更高版本。

### 错误修正

Allocation

    

* 基于最大分片大小的计算平衡器阈值 #95090 * 在"磁盘阈值监视器"重新路由后使用应用状态 #94916 * 在协调期间削弱节点替换决策程序 #95070

ILM+SLM

    

* 缩减采样 ILM 操作应跳过非时间序列索引 #94835(问题：#93123)

采集节点

    

* 修复异步扩充执行过早发布扩充策略锁 #94702(问题：#94690)

Network

    

* 修复了"回收字节流输出"#95036 中的逐个错误

Recovery

    

* 异步创建"索引分片"实例 #94545

Search

    

* 关闭空 PIT 或滚动时返回 200 #94708

Stats

    

* 修复_cluster/统计信息".nodes.fs"重复数据删除 #94798(问题：#24472) * 修复"FsInfo"设备重复数据删除 #94744

###Enhancements

Authorization

    

* 在角色解析中重用"字段权限缓存" #94931

###Upgrades

Packaging

    

* 将捆绑的 JDK 升级到 Java 20 #94600

[« Elasticsearch version 8.8.0](release-notes-8.8.0.md) [Elasticsearch
version 8.7.0 »](release-notes-8.7.0.md)
