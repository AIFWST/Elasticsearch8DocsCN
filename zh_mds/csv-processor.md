

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Convert processor](convert-processor.md) [Date processor »](date-
processor.md)

## CSV 处理器

从文档中的单个文本字段中提取 CSV 行中的字段。CSV 中的任何空字段都将被跳过。

**表 10.CSV 选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

用于从"target_fields"中提取数据的字段

|

yes

|

-

|

要将提取的值分配给"分隔符"的字段数组

|

no

|

,

|

CSV 中使用的分隔符，必须是单个字符串"quote"

|

no

|

"

|

CSV 中使用的引号必须是单字符串 'ignore_missing'

|

no

|

`false`

|

如果"true"和"field"不存在，处理器将静默退出，而不修改文档"trim"

|

no

|

`false`

|

修剪不带引号的字段"empty_value"中的空格

|

no

|

-

|

用于填充空字段的值，如果未提供，将跳过空字段。空字段是没有值(2 个连续分隔符)或空引号 ('""') "description" 的字段

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

处理器的标识符。对于调试和指标很有用。               { "csv"： { "field"： "my_field"， "target_fields"： ["field1"， "field2"] } }

如果启用了"trim"选项，则每个不带引号的字段开头和结尾的任何空格都将被修剪。例如，对于上述配置，值"A， B"将导致字段"field2"具有值"{nbsp}B"(开头有空格)。如果启用了"trim"，则"A，B"将导致字段"field2"的值为"B"(无空格)。带引号的字段将保持不变。

[« Convert processor](convert-processor.md) [Date processor »](date-
processor.md)
