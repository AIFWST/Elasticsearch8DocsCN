

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher actions](actions.md)

[« Watcher webhook action](actions-webhook.md) [Watcher logging Action
»](actions-logging.md)

## 观察程序索引操作

使用 'index' 操作将数据索引到 Elasticsearch 中。有关支持的属性，请参阅索引操作属性。

### 配置索引操作

以下代码片段显示了一个简单的"索引"操作定义：

    
    
    "actions" : {
      "index_payload" : { __"condition": { ... }, __"transform": { ... }, __"index" : {
          "index" : "my-index-000001", __"doc_id": "my-id" __}
      }
    }

__

|

操作的 id ---|--- __

|

限制操作执行的可选条件 __

|

一个可选的转换，用于转换有效负载并准备应编制索引的数据 __

|

数据将写入的索引、别名或数据流 __

|

文档的可选"_id" ### 索引操作属性编辑

姓名 |必填 |默认 |描述 ---|---|---|--- 'index'

|

yes*

|

-

|

要索引到的索引、别名或数据流。

*如果您动态设置"_index"值，则不需要此参数。请参阅多文档支持。   "doc_id"

|

no

|

-

|

文档的可选"_id"。   "op_type"

|

no

|

`index`

|

索引操作的op_type。必须是"索引"或"创建"之一。如果"索引"是数据流，则必须为"创建"。   "execution_time_field"

|

no

|

-

|

将存储/索引监视执行时间的字段。   "超时"

|

no

|

60s

|

等待索引 api 调用返回的超时。如果在此时间内未返回任何响应，则索引操作将超时并失败。此设置将覆盖默认超时。   "刷新"

|

no

|

-

|

写入请求的刷新策略的可选设置 ### 多文档支持它

与所有其他操作一样，您可以使用转换将当前执行上下文有效负载替换为另一个有效负载，并通过该负载更改最终将编制索引的文档。

索引操作通过支持特殊的"_doc"有效负载字段与转换配合得很好。

解析要编制索引的文档时，索引操作首先在有效负载中查找"_doc"字段。如果未找到，则有效负载将作为单个文档编制索引。

当存在"_doc"字段时，如果该字段包含对象，则会将其提取并作为单个文档编制索引。如果字段包含对象数组，则每个对象都被视为一个文档，索引操作会批量索引所有这些对象。

可以为每个文档添加"_index"或"_id"值，以动态设置索引文档的索引和 ID。

以下代码片段显示了多文档"索引"操作定义：

    
    
    "actions": {
      "index_payload": {
        "transform": {
          "script": """
          def documents = ctx.payload.hits.hits.stream()
            .map(hit -> [
              "_index": "my-index-000001", __"_id": hit._id, __"severity": "Sev: " + hit._source.severity __])
            .collect(Collectors.toList());
          return [ "_doc" : documents]; __"""
        },
        "index": {} __}
    }

__

|

文档的索引 ---|--- __

|

文档的可选"_id" __

|

从原始文档 __ 派生的新"严重性"字段

|

有效负载"_doc"字段，它是文档 __ 的数组

|

由于每个文档都通知了"_index"，因此这应该是空的 « 观察者网络钩子操作 观察者日志记录操作»