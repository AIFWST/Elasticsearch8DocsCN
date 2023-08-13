

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Join processor](join-processor.md) [KV processor »](kv-processor.md)

## JSON 处理器

将 JSON 字符串转换为结构化 JSON 对象。

**表 29.Json 选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要分析的字段。   "target_field"

|

no

|

`field`

|

转换后的结构化对象将写入的字段。此字段中的任何现有内容都将被覆盖。   "add_to_root"

|

no

|

false

|

强制在文档顶层添加已解析的 JSON 的标志。选择此选项时，不得设置"target_field"。   "add_to_root_conflict_strategy"

|

no

|

`replace`

|

当设置为"替换"时，与解析的 JSON 中的字段冲突的根字段将被覆盖。当设置为"合并"时，将出现冲突字段。仅当"add_to_root"设置为"true"时才适用。   "allow_duplicate_keys"

|

no

|

false

|

设置为 "true" 时，如果 JSON 包含重复键，则 JSON 解析器不会失败。而是任何重复键的最后一个遇到的值。   "strict_json_parsing"

|

no

|

true

|

当设置为"true"时，JSON 解析器将严格解析字段值。当设置为"false"时，JSON 解析器将更加宽松，但也更有可能删除部分字段值。例如，如果"strict_json_parsing"设置为"true"，字段值为"123 "foo"，则处理器将抛出 anIllegalArgumentException。但是，如果"strict_json_parsing"设置为"false"，则字段值将被解析为"123"。   "说明"

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

处理器的标识符。对于调试和指标很有用。   将解析所有 JSON 支持的类型(空值、布尔值、数字、数组、对象、字符串)。

假设您提供"json"处理器的以下配置：

    
    
    {
      "json" : {
        "field" : "string_source",
        "target_field" : "json_target"
      }
    }

如果处理以下文档：

    
    
    {
      "string_source": "{\"foo\": 2000}"
    }

"JSON"处理器在其上运行后，它将如下所示：

    
    
    {
      "string_source": "{\"foo\": 2000}",
      "json_target": {
        "foo": 2000
      }
    }

如果提供了以下配置，请省略可选的"target_field"设置：

    
    
    {
      "json" : {
        "field" : "source_and_target"
      }
    }

然后在"JSON"处理器对此文档进行操作之后：

    
    
    {
      "source_and_target": "{\"foo\": 2000}"
    }

它将看起来像：

    
    
    {
      "source_and_target": {
        "foo": 2000
      }
    }

这说明，除非在处理器配置中明确命名，否则"target_field"与必需的"字段"配置中提供的字段相同。

[« Join processor](join-processor.md) [KV processor »](kv-processor.md)
