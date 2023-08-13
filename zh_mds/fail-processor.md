

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Enrich processor](enrich-processor.md) [Fingerprint processor
»](fingerprint-processor.md)

## 故障处理器

引发异常。当您预计管道失败并希望将特定消息中继给请求者时，这很有用。

**表 18.失败选项**

姓名 |必填 |默认 |描述 ---|---|---|--- '消息'

|

yes

|

-

|

处理器引发的错误消息。支持模板片段。   "说明"

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

处理器的标识符。对于调试和指标很有用。               { "fail"： { "if" ： "ctx.tags.contains('production') ！= true"， "message"： "生产标签不存在，找到标签： {{{tags}}}" } }

[« Enrich processor](enrich-processor.md) [Fingerprint processor
»](fingerprint-processor.md)
