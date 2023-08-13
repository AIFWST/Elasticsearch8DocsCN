

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Drop processor](drop-processor.md) [Fail processor »](fail-
processor.md)

## 扩充处理器

"扩充"处理器可以使用来自另一个索引的数据来丰富文档。有关如何进行此设置的详细信息，请参阅丰富数据部分。

**表 17.丰富选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'policy_name'

|

yes

|

-

|

要使用的扩充策略的名称。   "字段"

|

yes

|

-

|

输入文档中与策略匹配的字段match_field用于检索扩充数据。支持模板片段。   "target_field"

|

yes

|

-

|

添加到传入文档以包含扩充数据的字段。此字段包含扩充策略中指定的"match_field"和"enrich_fields"。支持模板代码段。   "ignore_missing"

|

no

|

false

|

如果"true"和"field"不存在，处理器将静默退出，而不修改文档"override"

|

no

|

true

|

如果处理器将使用预先存在的非空值字段更新字段。当设置为"false"时，不会触及此类字段。   "max_matches"

|

no

|

1

|

要包含在配置的目标字段下的最大匹配文档数。如果"max_matches"大于 1，则"target_field"将转换为 json 数组，否则"target_field"将成为 json 对象。为了避免文档变得太大，允许的最大值为 128。   "shape_relation"

|

no

|

`INTERSECTS`

|

一种空间关系运算符，用于将传入文档的地理形状与丰富索引中的文档进行匹配。此选项仅用于"geo_match"扩充策略类型。有关运算符，请参阅空间关系和详细信息。   "说明"

|

no

|

-

|

处理器的说明。用于描述处理器的目的或其配置。   "如果"

|

no

|

-

|

有条件地执行处理器。请参阅有条件运行处理器。   "ignore_failure"

|

no

|

`false`

|

忽略处理器的故障。请参阅处理管道故障。   "on_failure"

|

no

|

-

|

处理处理器的故障。请参阅处理管道故障。   "标签"

|

no

|

-

|

处理器的标识符。对于调试和指标很有用。   « 掉落处理器故障处理器 »