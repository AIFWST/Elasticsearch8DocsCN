

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Trim processor](trim-processor.md) [URL decode processor »](urldecode-
processor.md)

## 大写处理器

将字符串转换为大写等效字符串。如果字段是字符串数组，则将转换数组的所有成员。

**表 45.大写选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

用于使大写"target_field"的字段

|

no

|

`field`

|

要为其分配转换值的字段，默认情况下，"字段"将就地更新"ignore_missing"

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

处理器的标识符。对于调试和指标很有用。               { "大写"： { "字段"： "foo" } }

[« Trim processor](trim-processor.md) [URL decode processor »](urldecode-
processor.md)
