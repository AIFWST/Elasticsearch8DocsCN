

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Set security user processor](ingest-node-set-security-user-processor.md)
[Split processor »](split-processor.md)

## 排序处理器

对数组的元素进行升序或降序排序。齐次数字数组将按数字排序，而字符串数组或字符串 + 数字的异构数组将按字典顺序排序。当字段不是数组时引发错误。

**表 42.排序选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要排序的字段"顺序"

|

no

|

`"asc"`

|

要使用的排序顺序。接受"asc"或"desc"。   "target_field"

|

no

|

`field`

|

要为其分配排序值的字段，默认情况下，"字段"将就地更新"说明"

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

处理器的标识符。对于调试和指标很有用。               { "sort"： { "field"： "array_field_to_sort"， "order"： "desc" } }

[« Set security user processor](ingest-node-set-security-user-processor.md)
[Split processor »](split-processor.md)
