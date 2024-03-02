

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Reading indices from older Elasticsearch versions](archive-indices.md)
[Analysis »](index-modules-analysis.md)

# 索引模块

索引模块是每个索引创建的模块,用于控制与索引相关的所有方面。

## 索引设置

可以按索引设置索引级别设置。设置可能是:

- static 静态设置:
只能在索引创建时或在已关闭的索引上设置。
- dynamic 动态设置
可以使用[update-index-settings](./indices-update-settings.md "Update index settings API") API 在实时索引上进行更改的设置。

注意:更改已关闭索引的静态static或动态dynamic索引设置可能会导致不正确的设置,如果不删除和重新创建索引,就无法修改这些设置。

### 静态索引设置

以下是 static索引设置的列表:

`index.number_of_shards`:<br>
 
    (1)索引应具有的主分片数。默认为"1"。只能在创建索引时设置此设置,不能在关闭的索引上更改。
    (2)每个索引的分片数量限制为"1024"。此限制是一个安全限制,以防止意外创建可能因资源分配而破坏集群稳定性的索引。
    (3)可以通过在属于群集的每个节点上指定"export ES_JAVA_OPTS="-Des.index.max_number_of_shards=128""系统属性来修改限制。

`index.number_of_routing_shards`:<br>

    与"index.number_of_shards"一起使用的整数值,用于将文档路由到主分片。请参阅"_routing"字段。

    Elasticsearch 在拆分索引时使用此值。例如,将"number_of_routing_shards"设置为"30"("5 x 2 x 3")的 5 分片索引可以按因子"2"或"3"进行拆分。换句话说,它可以拆分如下:

    * "5" -> "10" -> "30"(除以 2,然后除以 3) 
    * "5" -> "15" -> "30"(除以 3,然后除以 2)
    * "5" -> "30"(除以 6)

    此设置的默认值取决于索引中主分片的数量。默认值旨在允许您按 2 到最多 1024 个分片的因子进行拆分。

    在 Elasticsearch 7.0.0 及更高版本中,此设置会影响文档在分片之间的分布方式。使用自定义路由重新索引旧索引时,必须显式设置"index.number_of_routing_shards"以维护相同的文档分发。请参阅相关的中断性变更。

`index.codec`

    “default”值使用LZ4压缩来压缩存储的数据,但可以设置为“best_compression”,该值使用[DEFLATE](https://en.wikipedia.org/wiki/DEFLATE)以较慢的存储场性能为代价来获得更高的压缩比。如果要更新压缩类型,则将在合并线段后应用新的压缩类型。可以使用[force merge](./indices-formerge.mod“强制合并API”)强制合并段。

`index.routing_partition_size`

    自定义[routing](./mapping-routing-field.md“_routing-field”)值可以访问的分片数。默认值为1,只能在创建索引时设置。此值必须小于“index.number_of_shards”,除非“index.nnumber_of_shalds”值也是1。有关如何使用此设置的更多详细信息,请参阅[Routing to an index partition](./mapping-routing-field.md) 。

`index.soft_deletes.enabled`

    在7.6.0中弃用。不赞成在禁用软删除的情况下创建索引,并将在未来的Elasticsearch版本中删除。指示是否对索引启用软删除。软删除只能在创建索引时配置,也只能在Elasticsearch 6.5.0或之后创建的索引上配置。默认为“true”。

`index.soft_deletes.retention_lease.period`

    在分片历史保留租约被视为过期之前,保留该租约的最长期限。Shard历史保留租约确保在Lucene索引合并期间保留软删除。如果软删除在复制到跟随者之前被合并,则由于引线上的历史记录不完整,以下过程将失败。默认为“12h”。
     
`index.load_fixed_bitset_filters_eagerly`

    指示是否为嵌套查询预加载[cached filters](query-filter-context.html "Query and filter context")。可能的值为“true”(默认值)和“false”。
     
`index.shard.check_on_startup`

    仅限专家用户。此设置启用一些非常昂贵的处理 atshard 启动,并且仅在诊断群集中的问题时才有用。
    如果您确实使用它,则应仅暂时使用它,并在不再需要它时将其删除。 Elasticsearch 会在分片生命周期的各个时间点自动对分片的内容执行完整性检查。例如,它会验证在恢复副本或拍摄快照时传输的每个文件的校验和。
    它还会在打开分片时验证许多重要文件的完整性,这在启动节点和完成分片恢复或重定位时发生。
    因此,您可以在整个分片运行时手动验证其完整性,方法是将其快照拍摄到新存储库中或将其恢复到新节点上。
    此设置确定 Elasticsearch 在打开分片时是否执行其他完整性检查。如果这些检查检测到损坏,则它们将阻止打开分片。它接受以下值:

`false`
 
    打开碎片时不要执行其他损坏检查。这是默认和推荐的行为。
`checksum`

    验证碎片中每个文件的校验和是否与其内容匹配。这将检测从磁盘读取的数据与Elasticsearch最初写入的数据不同的情况,例如由于未检测到的磁盘损坏或其他硬件故障。这些检查需要从磁盘读取整个碎片,这需要大量的时间和IO带宽,并且可能会通过从文件系统缓存中逐出重要数据来影响集群性能。
     
`true`

    执行与“校验和”相同的检查,还检查碎片中的逻辑不一致,例如,这可能是由于RAM故障或其他硬件故障导致数据在写入时损坏所致。这些检查需要从磁盘读取整个碎片,这需要大量的时间和IO带宽,然后对碎片的内容执行各种检查,这需要花费大量的时间、CPU和内存。

### 动态索引设置

以下是与任何特定索引模块无关的所有 dynamic动态索引设置的列表:

`index.number_of_replicas`

    每个主分片具有的副本数。默认值为 1。
    警告:将其配置为0可能会在节点重新启动期间导致临时可用性丢失,或者在数据损坏的情况下导致永久数据丢失。
   

`index.auto_expand_replicas`

根据集群中的数据节点数自动扩展副本数。设置为以破折号分隔的下限和上限(例如"0-5")或使用"all"作为上限(例如"0-all")。默认为"假"(即禁用)。请注意,自动扩展的副本数仅考虑分配筛选规则,而忽略其他分配规则,例如每个节点的总分片数,如果适用的规则阻止分配所有副本,则可能导致集群运行状况变为"黄色"。

如果上限为"all",则忽略此索引的分片分配感知和"cluster.routing.allocation.same_shard.host"。

`index.search.idle.after`

     How long a shard can not receive a search or get request until it's considered search idle. (default is `30s`) 

`index.refresh_interval`

     How often to perform a refresh operation, which makes recent changes to the index visible to search. Defaults to `1s`. Can be set to `-1` to disable refresh. If this setting is not explicitly set, shards that haven't seen search traffic for at least `index.search.idle.after` seconds will not receive background refreshes until they receive a search request. Searches that hit an idle shard where a refresh is pending will trigger a refresh as part of the search operation for that shard only. This behavior aims to automatically optimize bulk indexing in the default case when no searches are performed. In order to opt out of this behavior an explicit value of `1s` should set as the refresh interval. 

`index.max_result_window`

     The maximum value of `from + size` for searches to this index. Defaults to `10000`. Search requests take heap memory and time proportional to `from + size` and this limits that memory. See [Scroll](paginate-search-results.html#scroll-search-results "Scroll search results") or [Search After](paginate-search-results.html#search-after "Search after") for a more efficient alternative to raising this. 
`index.max_inner_result_window`

     The maximum value of `from + size` for inner hits definition and top hits aggregations to this index. Defaults to `100`. Inner hits and top hits aggregation take heap memory and time proportional to `from + size` and this limits that memory. 
`index.max_rescore_window`

     The maximum value of `window_size` for `rescore` requests in searches of this index. Defaults to `index.max_result_window` which defaults to `10000`. Search requests take heap memory and time proportional to `max(window_size, from + size)` and this limits that memory. 
`index.max_docvalue_fields_search`

     The maximum number of `docvalue_fields` that are allowed in a query. Defaults to `100`. Doc-value fields are costly since they might incur a per-field per-document seek. 
`index.max_script_fields`

     The maximum number of `script_fields` that are allowed in a query. Defaults to `32`. 

`index.max_ngram_diff`

     The maximum allowed difference between min_gram and max_gram for NGramTokenizer and NGramTokenFilter. Defaults to `1`. 

`index.max_shingle_diff`

     The maximum allowed difference between max_shingle_size and min_shingle_size for the [`shingle` token filter](analysis-shingle-tokenfilter.html "Shingle token filter"). Defaults to `3`. 
`index.max_refresh_listeners`

     Maximum number of refresh listeners available on each shard of the index. These listeners are used to implement [`refresh=wait_for`](docs-refresh.html "?refresh"). 
`index.analyze.max_token_count`

     The maximum number of tokens that can be produced using _analyze API. Defaults to `10000`. 

`index.highlight.max_analyzed_offset`

     The maximum number of characters that will be analyzed for a highlight request. This setting is only applicable when highlighting is requested on a text that was indexed without offsets or term vectors. Defaults to `1000000`. 

`index.max_terms_count`

     The maximum number of terms that can be used in Terms Query. Defaults to `65536`. 

`index.max_regex_length`

     The maximum length of regex that can be used in Regexp Query. Defaults to `1000`. 

`index.query.default_field`

    

(字符串或字符串数组)与一个或多个字段匹配的通配符 ('*') 模式。默认情况下,以下查询类型搜索这些匹配字段:

* 更多类似 * 多重匹配 * 查询字符串 * 简单查询字符串

默认为"*",表示匹配符合术语级查询条件的所有字段,不包括元数据字段。

`index.routing.allocation.enable`

    

控制此索引的分片分配。它可以设置为:

* "all"(默认) - 允许为所有分片分配分片。  * "主分片" \- 仅允许为主分片分配分片。  * "new_primaries" \- 仅允许为新创建的主分片分配分片。  * "无" \- 不允许分片分配。

`index.routing.rebalance.enable`

    

为此索引启用分片重新平衡。它可以设置为:

* "all"(默认) - 允许对所有分片进行分片重新平衡。  * "主分片" \- 仅允许主分片的分片重新平衡。  * "副本" \- 仅允许副本分片的分片重新平衡。  * "无" \- 不允许分片重新平衡。

`index.gc_deletes`

     The length of time that a [deleted document's version number](docs-delete.html#delete-versioning "Versioning") remains available for [further versioned operations](docs-index_.html#index-versioning "Versioning"). Defaults to `60s`. 

`index.default_pipeline`

     Default [ingest pipeline](ingest.html "Ingest pipelines") for the index. Index requests will fail if the default pipeline is set and the pipeline does not exist. The default may be overridden using the `pipeline` parameter. The special pipeline name `_none` indicates no default ingest pipeline will run. 

`index.final_pipeline`

    

索引的最终引入管道。如果设置了最终管道且管道不存在,则索引请求将失败。最终管道始终在请求管道(如果指定)和默认管道(如果存在)之后运行。特殊管道名称"_none"表示不会运行最终的摄取管道。

不能使用最终管道更改"_index"字段。如果管道尝试更改"_index"字段,索引请求将失败。

`index.hidden`

     Indicates whether the index should be hidden by default. Hidden indices are not returned by default when using a wildcard expression. This behavior is controlled per request through the use of the `expand_wildcards` parameter. Possible values are `true` and `false` (default). 

### 其他索引模块中的设置

索引模块中提供了其他索引设置:

分析

     Settings to define analyzers, tokenizers, token filters and character filters. 
[Index shard allocation](index-modules-allocation.html "Index Shard
Allocation")

     Control over where, when, and how shards are allocated to nodes. 
[Mapping](index-modules-mapper.html "Mapper")

     Enable or disable dynamic mapping for an index. 
[Merging](index-modules-merge.html "Merge")

     Control over how shards are merged by the background merge process. 
[Similarities](index-modules-similarity.html "Similarity module")

     Configure custom similarity settings to customize how search results are scored. 
[Slowlog](index-modules-slowlog.html "Slow Log")

     Control over how slow queries and fetch requests are logged. 
[Store](index-modules-store.html "Store")

     Configure the type of filesystem used to access shard data. 
[Translog](index-modules-translog.html "Translog")

     Control over the transaction log and background flush operations. 
[History retention](index-modules-history-retention.html "History retention")

     Control over the retention of a history of operations in the index. 
[Indexing pressure](index-modules-indexing-pressure.html "Indexing pressure")

     Configure indexing back pressure limits. 

### X-Pack 索引设置

索引生命周期管理

     Specify the lifecycle policy and rollover alias for an index. 

[« Reading indices from older Elasticsearch versions](archive-indices.md)
[Analysis »](index-modules-analysis.md)
