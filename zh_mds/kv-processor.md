

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« JSON processor](json-processor.md) [Lowercase processor »](lowercase-
processor.md)

## KV处理器

该处理器有助于自动解析"foo=bar"类型的消息(或特定事件字段)。

例如，如果您有一条包含"ip=1.2.3.4error=REFUSED"的日志消息，则可以通过配置以下内容自动解析这些字段：

    
    
    {
      "kv": {
        "field": "message",
        "field_split": " ",
        "value_split": "="
      }
    }

使用 KV 处理器可能会导致字段名称无法控制。请考虑改用平展数据类型，它将整个对象映射为单个字段，并允许对其内容进行简单搜索。

**表 30.KV 选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要分析的字段。支持模板代码段。   "field_split"

|

yes

|

-

|

用于拆分键值对"value_split"的正则表达式模式

|

yes

|

-

|

正则表达式模式用于将键与键值对"target_field"中的值拆分

|

no

|

`null`

|

要将提取的键插入到的字段。默认为文档的根目录。支持模板代码段。   "include_keys"

|

no

|

`null`

|

要筛选并插入到文档中的键列表。默认包含所有键"exclude_keys"

|

no

|

`null`

|

要从文档"ignore_missing"中排除的键列表

|

no

|

`false`

|

如果"true"和"field"不存在或为"null"，则处理器静默退出而不修改文档"前缀"

|

no

|

`null`

|

要添加到提取的键"trim_key"的前缀

|

no

|

`null`

|

要从提取的键"trim_value"中修剪的字符串

|

no

|

`null`

|

要从提取的值"strip_brackets"中修剪的字符串

|

no

|

`false`

|

如果"true"从提取的值"描述"中带去括号"()"，"<>"，"[]"以及引号""和"

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

处理器的标识符。对于调试和指标很有用。   « JSON 处理器 小写处理器 »