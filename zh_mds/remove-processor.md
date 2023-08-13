

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Registered domain processor](registered-domain-processor.md) [Rename
processor »](rename-processor.md)

## 删除处理器

删除现有字段。如果一个字段不存在，则会引发异常。

**表 36.删除选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要删除的字段。支持模板代码段。   "ignore_missing"

|

no

|

`false`

|

如果"true"和"field"不存在或为"null"，则处理器静默退出而不修改文档"keep"

|

no

|

-

|

要保留的字段。设置后，将删除指定字段以外的所有字段。   "说明"

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

处理器的标识符。对于调试和指标很有用。   下面是删除单个字段的示例：

    
    
    {
      "remove": {
        "field": "user_agent"
      }
    }

若要删除多个字段，可以使用以下查询：

    
    
    {
      "remove": {
        "field": ["user_agent", "url"]
      }
    }

您还可以选择删除指定列表以外的所有字段：

    
    
    {
      "remove": {
        "keep": ["url"]
      }
    }

[« Registered domain processor](registered-domain-processor.md) [Rename
processor »](rename-processor.md)
