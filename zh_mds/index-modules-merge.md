

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md)

[« Mapper](index-modules-mapper.md) [Similarity module »](index-modules-
similarity.md)

##Merge

Elasticsearch 中的分片是 Lucene 索引，Lucene 索引被分解为多个段。段是存储索引数据的索引中的内部存储元素，并且是不可变的。较小的段会定期合并到较大的段中，以保持索引大小不变并删除。

合并过程使用自动限制来平衡合并和其他活动(如搜索)之间硬件资源的使用。

### 合并调度

合并调度程序 (ConcurrentMergeScheduler) 在需要时控制合并操作的执行。合并在单独的线程中运行，当达到最大线程数时，进一步的合并将等待，直到合并线程可用。

合并计划程序支持以下 _dynamic_ 设置：

`index.merge.scheduler.max_thread_count`

     The maximum number of threads on a single shard that may be merging at once. Defaults to `Math.max(1, Math.min(4, <<node.processors, node.processors>> / 2))` which works well for a good solid-state-disk (SSD). If your index is on spinning platter drives instead, decrease this to 1. 

[« Mapper](index-modules-mapper.md) [Similarity module »](index-modules-
similarity.md)
