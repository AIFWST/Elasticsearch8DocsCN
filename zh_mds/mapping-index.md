

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `ignore_malformed`](ignore-malformed.md) [`index_options` »](index-
options.md)

##'索引'

"索引"选项控制是否为字段值编制索引。它接受"真"或"假"，默认为"真"。

为字段编制索引会创建数据结构，以便有效地查询字段。当数字类型、日期类型、布尔类型、IP 类型、geo_point类型和关键字类型未编制索引但仅启用了文档值时，也可以查询它们。对这些字段的查询速度很慢，因为必须对索引进行全面扫描。所有其他字段都不可查询。

[« `ignore_malformed`](ignore-malformed.md) [`index_options` »](index-
options.md)
