

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Node query cache settings](query-cache.md) [Security settings in
Elasticsearch »](security-settings.md)

## 搜索设置

可以设置以下专家设置来管理全局搜索和聚合限制。

`indices.query.bool.max_clause_count`

    

8.0.0] 在 8.0.0 中已弃用。 ([静态，整数)此已弃用的设置不起作用。

Elasticsearch 现在将根据搜索线程池的大小和分配给 JVM 的堆大小使用启发式方法，动态设置查询中允许的最大子句数。此限制的最小值为 1024，并且在大多数情况下会更大(例如，具有 30Gb RAM 和 48 个 CPU 的节点的最大子句计数约为 27，000)。堆越大会导致更高的值，而线程池越大会导致值越低。

应尽可能避免使用具有许多子句的查询。如果您之前为了适应繁重的查询而修改了此设置，则可能需要增加 Elasticsearch 可用的内存量，或者减小搜索线程池的大小，以便每个并发搜索有更多的内存可用。

在以前版本的 Lucene 中，您可以通过将布尔查询相互嵌套来绕过此限制，但现在该限制基于整个查询中的叶查询总数，此解决方法将不再有用。

`search.max_buckets`

    

(动态，整数)单个响应中允许的最大聚合存储桶数。默认值为 65，536。

尝试返回超过此限制的请求将返回错误。

`indices.query.bool.max_nested_depth`

    

(静态，整数)查询的最大嵌套深度。默认为"30"。

此设置限制查询的嵌套深度。查询的深度嵌套可能会导致堆栈溢出错误。

[« Node query cache settings](query-cache.md) [Security settings in
Elasticsearch »](security-settings.md)
