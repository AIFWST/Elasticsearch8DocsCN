

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Gsub processor](gsub-processor.md) [Inference processor »](inference-
processor.md)

## HTML 条带处理器

从字段中删除 HTML 标记。如果字段是字符串数组，则 HTML标记将从数组的所有成员中删除。

每个 HTML 标记都替换为"\n"字符。

**表 26.网页条选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

用于从"target_field"中删除 HTML 标记的字符串值字段

|

no

|

`field`

|

默认情况下，要为其分配值的字段"字段"将就地更新"ignore_missing"

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

处理器的标识符。对于调试和指标很有用。               { "html_strip"： { "field"： "foo" } }

[« Gsub processor](gsub-processor.md) [Inference processor »](inference-
processor.md)
