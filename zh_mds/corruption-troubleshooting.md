

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Total number of shards per node has been reached](increase-cluster-shard-
limit.md) [Fix data nodes out of disk »](fix-data-node-out-of-disk.md)

## 疑难解答损坏

Elasticsearch 希望它从磁盘读取的数据与之前写入的数据完全一致。如果它检测到磁盘上的数据与它写入的数据不同，那么它将报告某种异常，例如：

* 'org.apache.lucene.index.CorruptIndexException' * 'org.elasticsearch.gateway.CorruptStateException' * 'org.elasticsearch.index.translog.TranslogCorruptedException'

通常，这些异常是由于校验和不匹配而发生的。Elasticsearch写入磁盘的大部分数据后跟使用称为CRC32的简单算法的校验和，该算法计算速度快，并且擅长检测使用故障存储时可能发生的随机损坏类型。CRC32校验和不匹配肯定表明某些东西有问题，尽管当然匹配校验和并不能证明没有损坏。

验证校验和是昂贵的，因为它涉及读取文件的每个字节，这需要付出很大的努力，并且可能会从文件系统缓存中逐出更多有用的数据，因此系统通常不会经常验证文件的校验和。这就是为什么您往往只在发生异常情况时才遇到损坏异常的原因。例如，在合并、分片移动和快照期间经常检测到损坏。这并不意味着这些进程会导致损坏：它们是需要读取整个文件的罕见情况的示例。Elasticsearch借此机会同时验证校验和，这是检测到并报告损坏的时候。它不指示损坏的原因或发生的时间。损坏可能会在数月内未被发现。

构成 Lucene 索引的文件从头到尾按顺序写入，然后永远不会修改或覆盖。这种访问模式意味着校验和计算非常简单，可以在文件最初写入时即时发生，并且还使得由于写入文件时的用户空间错误而导致不正确的校验和的可能性很小。Elasticsearch 中计算校验和的部分很简单，被广泛使用，并且经过了很好的测试，因此您可以非常确信校验和不匹配确实表明从磁盘读取的数据与 Elasticsearch 之前写入的数据不同。

组成 Lucene 索引的文件在使用之前会完整写入。如果在重新启动后需要某个文件来恢复索引，则您的存储系统之前已向 Elasticsearch 确认此文件已持久同步到磁盘。在 Linux 上，这意味着"fsync()"系统调用成功返回。Elasticsearch 有时会报告索引已损坏，因为恢复所需的文件已被截断或缺少其页脚。这表示存储系统未正确确认持久写入。

对于 Elasticsearch 检测集群中的损坏，有很多可能的解释。像Elasticsearch这样的数据库会产生具有挑战性的I / O工作负载，这可能会发现其他测试可能会遗漏的微妙的基础设施问题。众所周知，Elasticsearch 会将以下问题暴露为文件损坏：

* 文件系统错误，特别是在较新的非标准文件系统中，这些文件系统可能没有看到足够的实际生产使用情况来确信它们能够正常工作。  * 内核错误。  * 驱动器或 RAID 控制器上运行的固件中的错误。  * 配置不正确，例如配置"fsync()"以在所有持久写入完成之前报告成功。  * 硬件故障，可能包括驱动器本身、RAID 控制器、RAM 或 CPU。  * 修改 Elasticsearch 写入的文件的第三方软件。

除了校验和不匹配之外，数据损坏通常不会导致其他问题证据。不要将此解释为表明您的存储子系统工作正常，因此 Elasticsearch 本身导致了损坏。除了数据损坏之外，故障存储很少显示任何问题的证据，但数据损坏本身是一个非常强烈的指标，表明您的存储子系统无法正常工作。

要排除 Elasticsearch 作为数据损坏的来源，请使用 Elasticsearch 以外的其他方式生成 I/O 工作负载，并查找数据完整性错误。在Linux上，"fio"和"stress-ng"工具既可以生成具有挑战性的I / O工作负载，也可以验证它们写入的数据的完整性。使用版本 0.12.01 或更高版本的"stress-ng"，因为早期版本没有足够强大的完整性检查。使用"diskchecker.pl"等脚本验证持久写入是否在断电后持续存在。或者，使用诸如"strace"之类的工具来观察Elasticsearch在写入数据时所做的系统调用序列，并确认该序列不能解释报告的损坏。

要缩小损坏的来源范围，请系统地更改群集环境中的组件，直到损坏停止。详细信息将取决于环境的确切配置，但可能包括以下内容：

* 尝试使用不同的文件系统或内核。  * 尝试依次更改每个硬件组件，最好更改为不同的型号或制造商。  * 为每个硬件组件尝试不同的固件版本。  * 删除任何可能修改 Elasticsearch 数据路径内容的第三方软件。

[« Total number of shards per node has been reached](increase-cluster-shard-
limit.md) [Fix data nodes out of disk »](fix-data-node-out-of-disk.md)
