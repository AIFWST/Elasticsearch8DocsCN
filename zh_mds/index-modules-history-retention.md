

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md)

[« Translog](index-modules-translog.md) [Index Sorting »](index-modules-
index-sorting.md)

## 历史保留

Elasticsearch 有时需要重放一些在分片上执行的操作。例如，如果副本短暂脱机，则重放它在脱机时错过的几个操作可能比从头开始重建要高效得多。同样，跨集群复制的工作原理是在领导集群上执行操作，然后在从属集群上重放这些操作。

在 Lucene 级别，Elasticsearch 实际上只对索引执行两个写入操作：可以索引新文档，也可以删除现有文档。更新是通过以原子方式删除旧文档，然后为新文档编制索引来实现的。索引到 Lucene 中的文档已包含重播该索引操作所需的所有信息，但文档删除并非如此。为了解决这个问题，Elasticsearch 使用一个名为 _soft deletes_ 的功能来保留 Lucene 索引中的最近删除内容，以便可以重放它们。

Elasticsearch 只在索引中保留某些最近删除的文档，因为软删除的文档仍然会占用一些空间。最终Elasticsearch将完全丢弃这些软删除的文档以释放该空间，以便索引不会随着时间的推移而变得越来越大。幸运的是，Elasticsearch 不需要能够重放曾经在分片上执行过的所有操作，因为始终可以在远程节点上制作分片的完整副本。但是，复制整个分片可能比重放一些缺失的操作花费更长的时间，因此 Elasticsearch 会尝试保留它预计将来需要重放的所有操作。

Elasticsearch 使用一种称为_shard历史记录保留leases_的机制跟踪它预计将来需要重放的操作。可能需要重播操作的每个分片副本必须首先为自己创建分片历史记录保留租约。例如，在使用跨集群复制时，此分片副本可能是分片的副本，也可能是追随者索引的分片。每个保留租约都会跟踪相应分片副本未收到的第一个操作的序列号。当分片副本收到新操作时，它会增加其保留租约中包含的序列号，以指示将来不需要重播这些操作。一旦软删除操作未被任何保留租约保留，Elasticsearch 就会丢弃这些操作。

如果分片副本失败，它将停止更新其分片历史记录保留租约，这意味着 Elasticsearch 将保留所有新操作，以便在失败的分片副本恢复时可以重放它们。但是，保留租约只能持续有限的时间。如果分片副本恢复速度不够快，则其保留租约可能会过期。这可以保护 Elasticsearch 在分片副本永久失败时永久保留历史记录，因为一旦保留租约过期，Elasticsearch 就可以开始再次丢弃历史记录。如果分片副本在其保留租约到期后恢复，那么 Elasticsearch 将回退到复制整个索引，因为它不能再简单地重放丢失的历史记录。保留租约的到期时间默认为"12h"，对于大多数合理的恢复方案来说，这应该足够长。

### 历史记录保留设置

`index.soft_deletes.enabled`

     [7.6.0]  Deprecated in 7.6.0. Creating indices with soft-deletes disabled is deprecated and will be removed in future Elasticsearch versions.  Indicates whether soft deletes are enabled on the index. Soft deletes can only be configured at index creation and only on indices created on or after Elasticsearch 6.5.0. Defaults to `true`. 
`index.soft_deletes.retention_lease.period`

     The maximum period to retain a shard history retention lease before it is considered expired. Shard history retention leases ensure that soft deletes are retained during merges on the Lucene index. If a soft delete is merged away before it can be replicated to a follower the following process will fail due to incomplete history on the leader. Defaults to `12h`. 

[« Translog](index-modules-translog.md) [Index Sorting »](index-modules-
index-sorting.md)
