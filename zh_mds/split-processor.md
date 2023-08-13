

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Sort processor](sort-processor.md) [Trim processor »](trim-
processor.md)

## 拆分处理器

使用分隔符将字段拆分为数组。仅适用于字符串字段。

**表 43.拆分选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要拆分"分隔符"的字段

|

yes

|

-

|

与分隔符匹配的正则表达式，例如 '"，"" 或 '\s+' 'target_field'

|

no

|

`field`

|

默认情况下，要为其分配拆分值的字段"字段"将就地更新"ignore_missing"

|

no

|

`false`

|

如果"true"和"field"不存在，处理器将悄悄退出，而不修改文档"preserve_trailing"

|

no

|

`false`

|

保留空尾随字段(如果有)。   "说明"

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

处理器的标识符。对于调试和指标很有用。               { "split"： { "field"： "my_field"， "separator"： "\\s+" __} }

__

|

将所有连续的空格字符视为单个分隔符 ---|--- 如果启用了"preserve_trailing"选项，则将保留输入中的任何尾随空字段。例如，在下面的配置中，"my_field"属性中的值"A，，B，，"将被拆分为具有两个空尾随字段的五元素"["A"，""，"B"，""，""]"数组。如果未启用"preserve_trailing"属性，则将丢弃两个空的尾随字段，从而生成三元素数组"["A"，""，"B"]"。

    
    
    {
      "split": {
        "field": "my_field",
        "separator": ",",
        "preserve_trailing": true
      }
    }

[« Sort processor](sort-processor.md) [Trim processor »](trim-
processor.md)
