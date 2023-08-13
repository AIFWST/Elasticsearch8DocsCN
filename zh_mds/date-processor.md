

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« CSV processor](csv-processor.md) [Date index name processor »](date-
index-name-processor.md)

## 日期处理器

分析字段中的日期，然后使用日期或时间戳作为文档的时间戳。默认情况下，日期处理器将解析的日期添加为名为"@timestamp"的换行符。您可以通过设置"target_field"配置参数来指定其他字段。支持同一日期处理器定义的一部分使用多种日期格式。它们将按顺序用于尝试解析日期字段，其顺序与它们被定义为处理器定义的一部分的顺序相同。

**表 11.日期选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要从中获取日期的字段。   "target_field"

|

no

|

@timestamp

|

将保存已分析日期的字段。   "格式"

|

yes

|

-

|

预期日期格式的数组。可以是 Java 时间模式或以下格式之一：ISO8601、UNIX、UNIX_MS 或 TAI64N。   "时区"

|

no

|

UTC

|

分析日期时要使用的时区。支持模板片段。   "区域设置"

|

no

|

ENGLISH

|

分析日期时要使用的区域设置，与分析月份名称或周日相关。支持模板代码段。   "output_format"

|

no

|

`yyyy-MM-dd'T'HH:mm:ss.SSSXXX`

|

将日期写入"target_field"时使用的格式。必须是有效的 java 时间模式。   "说明"

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

处理器的标识符。对于调试和指标很有用。   下面是一个基于"initial_date"字段将解析日期添加到"时间戳"字段的示例：

    
    
    {
      "description" : "...",
      "processors" : [
        {
          "date" : {
            "field" : "initial_date",
            "target_field" : "timestamp",
            "formats" : ["dd/MM/yyyy HH:mm:ss"],
            "timezone" : "Europe/Amsterdam"
          }
        }
      ]
    }

"时区"和"区域设置"处理器参数是模板化的。这意味着可以从文档中的字段中提取它们的值。下面的示例演示如何从包含时区和区域设置值的摄取文档中的现有字段"my_timezone"和"my_locale"中提取区域设置/时区详细信息。

    
    
    {
      "description" : "...",
      "processors" : [
        {
          "date" : {
            "field" : "initial_date",
            "target_field" : "timestamp",
            "formats" : ["ISO8601"],
            "timezone" : "{{{my_timezone}}}",
            "locale" : "{{{my_locale}}}"
          }
        }
      ]
    }

[« CSV processor](csv-processor.md) [Date index name processor »](date-
index-name-processor.md)
