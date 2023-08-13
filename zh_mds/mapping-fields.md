

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md)

[« Version field type](version.md) [`_doc_count` field »](mapping-doc-count-
field.md)

## 元数据字段

每个文档都有与之关联的元数据，例如"_index"和"_id"元数据字段。创建映射时，可以自定义其中一些元数据字段的行为。

### 标识元数据字段

"_index"

|

文档所属的索引。   ---|--- "_id"

|

文档的 ID。   ### 文档源元数据字段编辑

"_source"

     The original JSON representing the body of the document. 
[`_size`](/guide/en/elasticsearch/plugins/8.9/mapper-size.html)

     The size of the `_source` field in bytes, provided by the [`mapper-size` plugin](/guide/en/elasticsearch/plugins/8.9/mapper-size.html). 

### 文档计数元数据字段

"_doc_count"

     A custom field used for storing doc counts when a document represents pre-aggregated data. 

### 为元数据字段编制索引

"_field_names"

     All fields in the document which contain non-null values. 
[`_ignored`](mapping-ignored-field.html "_ignored field")

     All fields in the document that have been ignored at index time because of [`ignore_malformed`](ignore-malformed.html "ignore_malformed"). 

### 路由元数据字段

"_routing"

     A custom routing value which routes a document to a particular shard. 

### 其他元数据字段

"_meta"

     Application specific metadata. 
[`_tier`](mapping-tier-field.html "_tier field")

     The current data tier preference of the index to which the document belongs. 

[« Version field type](version.md) [`_doc_count` field »](mapping-doc-count-
field.md)
