

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md) ›[Index Sorting](index-modules-index-
sorting.md)

[« Index Sorting](index-modules-index-sorting.md) [Indexing pressure
»](index-modules-indexing-pressure.md)

## 使用索引排序加快上合词

索引排序对于组织Lucene文档ID(不要与"_id"混为一谈)非常有用，以使连词(a和b和...)更有效。为了提高效率，连词依赖于这样一个事实，即如果任何子句不匹配，则整个连词不匹配。通过使用索引排序，我们可以将不匹配的文档放在一起，这将有助于有效地跳过大量不匹配连词的文档 ID。

此技巧仅适用于低基数字段。经验法则是，应首先对基数较低且经常用于筛选的字段进行排序。排序顺序('asc' 或 'desc')并不重要，因为我们只关心放置与相同子句匹配的值。

例如，如果您正在索引待售汽车，则按燃料类型、车身类型、品牌、注册年份和最终里程进行排序可能会很有趣。

[« Index Sorting](index-modules-index-sorting.md) [Indexing pressure
»](index-modules-indexing-pressure.md)
