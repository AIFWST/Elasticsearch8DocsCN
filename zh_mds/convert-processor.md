

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Community ID processor](community-id-processor.md) [CSV processor »](csv-
processor.md)

## 转换处理器

将当前引入的文档中的字段转换为其他类型，例如将字符串转换为整数。如果字段值是数组，则将转换所有成员。

支持的类型包括："整数"、"长整型"、"浮点数"、"双精度"、"字符串"、"布尔值"、"ip"和"自动"。

如果字段的字符串值等于"true"(忽略大小写)，则指定"布尔值"会将字段设置为 true，如果其字符串值等于"false"(忽略大小写)，则设置为 false，否则将引发异常。

如果目标字段包含可索引为 IP 字段类型的有效 IPv4 或 IPv6 地址，则指定"ip"会将目标字段设置为"字段"的值。

指定"auto"将尝试将字符串值的"字段"转换为最接近的非字符串、非 IP 类型。例如，值为"true"的字段将转换为其各自的布尔类型："true"。请注意，浮点数在"自动"中优先于双精度。值"242.15"将"自动"转换为类型为"float"的"242.15"。如果提供的字段无法正确转换，处理器仍将成功处理并将字段值保留原样。在这种情况下，"target_field"将使用未转换的字段值进行更新。

**表 9.转换选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

其值要转换为"target_field"的字段

|

no

|

`field`

|

要将转换后的值分配到的字段，默认情况下，"字段"将就地更新为"类型"

|

yes

|

-

|

将现有值转换为"ignore_missing"的类型

|

no

|

`false`

|

如果"true"和"field"不存在或为"null"，处理器将悄悄退出而不修改文档"描述"

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

处理器的标识符。对于调试和指标很有用。               PUT _ingest/pipeline/my-pipeline-id { "description"： "将 id 字段的内容转换为整数"， "处理器" ： [ { "转换" ： { "field" ： "id"， "type"： "integer" } } }

[« Community ID processor](community-id-processor.md) [CSV processor »](csv-
processor.md)
