

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Metadata fields](mapping-fields.md)

[« `_doc_count` field](mapping-doc-count-field.md) [`_ignored` field
»](mapping-ignored-field.md)

## '_field_names'字段

"_field_names"字段，用于索引文档中每个字段的名称，其中包含"null"以外的任何值。"存在"查询使用此字段来查找具有或不包含特定字段的任何非"null"值的文档。

现在，"_field_names"字段仅索引禁用了"doc_values"和"规范"的字段的名称。对于启用了"doc_values"或"norm"的字段，"exists"查询仍然可用，但不会使用"_field_names"字段。

### 禁用"_field_names"

无法再禁用"_field_names"。它现在默认启用，因为它不再承载以前那样的索引开销。

已删除对禁用"_field_names"的支持。在新索引上使用它将引发错误。仍然允许在 8.0 之前的索引中使用它，但会发出充分警告。

[« `_doc_count` field](mapping-doc-count-field.md) [`_ignored` field
»](mapping-ignored-field.md)
