

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Inference processor](inference-processor.md) [JSON processor »](json-
processor.md)

## 连接处理器

在每个元素之间使用分隔符将数组的每个元素联接到单个字符串中。当字段不是数组时引发错误。

**表 28.加入选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

包含要连接"分隔符"的数组值的字段

|

yes

|

-

|

分隔符"target_field"

|

no

|

`field`

|

要向其分配联接值的字段，默认情况下，"字段"将就地更新"说明"

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

处理器的标识符。对于调试和指标很有用。               { "join"： { "field"： "joined_array_field"， "separator"： "-" } }

[« Inference processor](inference-processor.md) [JSON processor »](json-
processor.md)
