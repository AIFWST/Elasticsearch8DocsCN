

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Ingest processor reference](processors.md) [Attachment processor
»](attachment.md)

## 追加处理器

将一个或多个值追加到现有数组(如果该字段已存在并且它是一个数组)。将标量转换为数组，如果字段存在且是标量，则向其追加一个或多个值。创建一个包含提供的值的数组(如果该字段不存在)。接受单值或值数组。

**表 3.追加选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要追加到的字段。支持模板片段。   "价值"

|

yes

|

-

|

要追加的值。支持模板代码段。   "allow_duplicates"

|

no

|

true

|

如果为"false"，则处理器不会追加字段中已存在的值。   "media_type"

|

no

|

`application/json`

|

用于编码"值"的媒体类型。仅当"值"是模板片段时才适用。必须是"application/json"、"text/plain"或"application/x-www-form-urlencoded"之一。   "说明"

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

处理器的标识符。对于调试和指标很有用。               { "append"： { "field"： "tags"， "value"： ["production"， "{{{app}}}"， "{{{owner}}}"] } }

[« Ingest processor reference](processors.md) [Attachment processor
»](attachment.md)
