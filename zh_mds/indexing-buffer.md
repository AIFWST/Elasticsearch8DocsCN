

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Index recovery settings](recovery.md) [License settings »](license-
settings.md)

## 索引缓冲区设置

索引缓冲区用于存储新编制索引的文档。当它填满时，缓冲区中的文档将写入磁盘上的段。它在节点上的所有分片之间划分。

以下设置是 _static_，必须在群集中的每个数据节点上配置：

`indices.memory.index_buffer_size`

     ([Static](settings.html#static-cluster-setting)) Accepts either a percentage or a byte size value. It defaults to `10%`, meaning that `10%` of the total heap allocated to a node will be used as the indexing buffer size shared across all shards. 
`indices.memory.min_index_buffer_size`

     ([Static](settings.html#static-cluster-setting)) If the `index_buffer_size` is specified as a percentage, then this setting can be used to specify an absolute minimum. Defaults to `48mb`. 
`indices.memory.max_index_buffer_size`

     ([Static](settings.html#static-cluster-setting)) If the `index_buffer_size` is specified as a percentage, then this setting can be used to specify an absolute maximum. Defaults to unbounded. 

[« Index recovery settings](recovery.md) [License settings »](license-
settings.md)
