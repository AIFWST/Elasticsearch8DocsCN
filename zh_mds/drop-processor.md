

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Dot expander processor](dot-expand-processor.md) [Enrich processor
»](enrich-processor.md)

## 放置处理器

删除文档而不引发任何错误。这对于防止文档根据某些条件编制索引很有用。

**表 16.拖放选项**

姓名 |必填 |默认 |描述 ---|---|---|--- '描述'

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

处理器的标识符。对于调试和指标很有用。               { "drop"： { "if" ： "ctx.network_name == '客人'" } }

[« Dot expander processor](dot-expand-processor.md) [Enrich processor
»](enrich-processor.md)
