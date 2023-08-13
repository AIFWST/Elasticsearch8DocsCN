

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Remove processor](remove-processor.md) [Reroute processor »](reroute-
processor.md)

## 重命名处理器

重命名现有字段。如果该字段不存在或新名称已使用，则会引发异常。

**表 37.重命名选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要重命名的字段。支持模板代码段。   "target_field"

|

yes

|

-

|

字段的新名称。支持模板代码段。   "ignore_missing"

|

no

|

`false`

|

如果"true"和"field"不存在，处理器将静默退出，而不修改文档"描述"

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

处理器的标识符。对于调试和指标很有用。               { "重命名"： { "字段"： "提供程序"， "target_field"： "cloud.provider" } } }

[« Remove processor](remove-processor.md) [Reroute processor »](reroute-
processor.md)
