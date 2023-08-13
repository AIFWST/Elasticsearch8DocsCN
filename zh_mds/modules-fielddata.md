

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Discovery and cluster formation settings](modules-discovery-settings.md)
[Health diagnostic settings in Elasticsearch »](health-diagnostic-
settings.md)

## 字段数据缓存设置

字段数据缓存包含字段数据和全局序号，它们都用于支持某些字段类型的聚合。由于这些是堆上数据结构，因此监视缓存的使用非常重要。

#### 缓存大小

缓存中的条目的生成成本很高，因此默认行为是将缓存加载到内存中。默认缓存大小不受限制，导致缓存增长，直到达到字段数据断路器设置的限制。可以配置此行为。

如果设置了缓存大小限制，缓存将开始清除缓存中最近更新最少的条目。此设置可以自动避免断路器限制，但代价是根据需要重建缓存。

如果达到断路器限制，将阻止进一步增加缓存大小的请求。在这种情况下，您应该手动清除缓存。

`indices.fielddata.cache.size`

     ([Static](settings.html#static-cluster-setting)) The max size of the field data cache, eg `38%` of node heap space, or an absolute value, eg `12GB`. Defaults to unbounded. If you choose to set it, it should be smaller than [Field data circuit breaker](circuit-breaker.html#fielddata-circuit-breaker "Field data circuit breaker") limit. 

#### 监控现场数据

您可以使用节点统计信息 API 或 cat 字段数据 API 监视字段数据的内存使用情况以及字段数据断路器。

[« Discovery and cluster formation settings](modules-discovery-settings.md)
[Health diagnostic settings in Elasticsearch »](health-diagnostic-
settings.md)
