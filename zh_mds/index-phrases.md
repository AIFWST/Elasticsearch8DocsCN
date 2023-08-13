

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `index_options`](index-options.md) [`index_prefixes` »](index-
prefixes.md)

##'index_phrases'

如果启用，两个术语组合 ( _s带状疱疹_ ) 将被索引到一个单独的字段中。这允许精确短语查询(无 slop)更有效地运行，但代价是更大的索引。请注意，这在不删除停用词时效果最佳，因为包含非索引字的短语将不会使用附属字段，而是将回退到标准短语查询。接受"真"或"假"(默认值)。

[« `index_options`](index-options.md) [`index_prefixes` »](index-
prefixes.md)
