

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md)

[« `term_vector`](term-vector.md) [Removal of mapping types »](removal-of-
types.md)

## 映射限制设置

使用以下设置来限制字段映射(手动或动态创建)的数量，并防止文档导致映射爆炸：

`index.mapping.total_fields.limit`

    

索引中的最大字段数。字段和对象映射以及字段别名计入此限制。映射的运行时字段也计入此限制。默认值为"1000"。

设置此限制是为了防止映射和搜索变得太大。较高的值可能会导致性能下降和内存问题，尤其是在负载较高或资源较少的集群中。

如果增加此设置，我们建议您同时增加"index.query.bool.max_clause_count"设置，该设置限制查询中的最大子句数。

如果字段映射包含大量任意键，请考虑使用平展数据类型。

`index.mapping.depth.limit`

     The maximum depth for a field, which is measured as the number of inner objects. For instance, if all fields are defined at the root object level, then the depth is `1`. If there is one object mapping, then the depth is `2`, etc. Default is `20`. 

`index.mapping.nested_fields.limit`

     The maximum number of distinct `nested` mappings in an index. The `nested` type should only be used in special cases, when arrays of objects need to be queried independently of each other. To safeguard against poorly designed mappings, this setting limits the number of unique `nested` types per index. Default is `50`. 

`index.mapping.nested_objects.limit`

     The maximum number of nested JSON objects that a single document can contain across all `nested` types. This limit helps to prevent out of memory errors when a document contains too many nested objects. Default is `10000`. 
`index.mapping.field_name_length.limit`

     Setting for the maximum length of a field name. This setting isn't really something that addresses mappings explosion but might still be useful if you want to limit the field length. It usually shouldn't be necessary to set this setting. The default is okay unless a user starts to add a huge number of fields with really long names. Default is `Long.MAX_VALUE` (no limit). 
`index.mapping.dimension_fields.limit`

     ([Dynamic](index-modules.html#dynamic-index-settings "Dynamic index settings"), integer) Maximum number of [time series dimensions](tsds.html#time-series-dimension "Dimensions") for the index. Defaults to `21`. 

[« `term_vector`](term-vector.md) [Removal of mapping types »](removal-of-
types.md)
