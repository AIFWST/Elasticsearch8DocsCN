

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md)

[« Preloading data into the file system cache](preload-data-to-file-system-
cache.md) [History retention »](index-modules-history-retention.md)

##Translog

对 Lucene 的更改仅在 Lucene 提交期间保存到磁盘，这是一项相对昂贵的操作，因此无法在每次索引器删除操作后执行。在一次提交之后和另一次提交之前发生的更改将在进程退出或硬件故障的情况下由 Lucene 从索引中删除。

Lucene 提交的成本太高，无法对每个单独的更改执行，因此每个分片副本也将操作写入其称为the_translog_的_transaction log_。所有索引和删除操作在由内部 Lucene 索引处理后但在确认之前写入 translog。如果发生崩溃，最近已确认但尚未包含在上次 Lucene 提交中的操作将在分片恢复时从 translog 中恢复。

Elasticsearch 刷新是执行 Lucene 提交并开始新的事务日志生成的过程。刷新在后台自动执行，以确保 translog 不会变得太大，这将使重播其操作在恢复过程中花费大量时间。手动执行刷新的功能也通过 API 公开，尽管很少需要这样做。

### 转日志设置

仅当事务日志"fsync"和提交时，事务日志中的数据才会保存到磁盘。如果发生硬件故障或操作系统崩溃或 JVM 崩溃或分片故障，自上次 translog 提交以来写入的任何数据都将丢失。

默认情况下，"index.translog.durability"设置为"request"，这意味着Elasticsearch只会在translog在主副本和每个分配的副本上成功"fsync"并提交后，才会向客户端报告索引，删除，更新或批量请求的成功。如果 'index.translog.durability' 设置为 'async'，那么 Elasticsearch 'fsync' 并且每 'index.translog.sync_interval' 才提交 translog，这意味着在崩溃之前执行的任何操作都可能在节点恢复时丢失。

以下可动态更新的每索引设置控制转写日志的行为：

`index.translog.sync_interval`

     How often the translog is `fsync`ed to disk and committed, regardless of write operations. Defaults to `5s`. Values less than `100ms` are not allowed. 
`index.translog.durability`

    

是否在每个索引、删除、更新或批量请求后"fsync"并提交事务日志。此设置接受以下参数：

`request`

     (default) `fsync` and commit after every request. In the event of hardware failure, all acknowledged writes will already have been committed to disk. 
`async`

     `fsync` and commit in the background every `sync_interval`. In the event of a failure, all acknowledged writes since the last automatic commit will be discarded. 

`index.translog.flush_threshold_size`

     The translog stores all operations that are not yet safely persisted in Lucene (i.e., are not part of a Lucene commit point). Although these operations are available for reads, they will need to be replayed if the shard was stopped and had to be recovered. This setting controls the maximum total size of these operations, to prevent recoveries from taking too long. Once the maximum size has been reached a flush will happen, generating a new Lucene commit point. Defaults to `512mb`. 

[« Preloading data into the file system cache](preload-data-to-file-system-
cache.md) [History retention »](index-modules-history-retention.md)
