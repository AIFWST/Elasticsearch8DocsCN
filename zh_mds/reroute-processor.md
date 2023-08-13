

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Rename processor](rename-processor.md) [Script processor »](script-
processor.md)

## 重新路由处理器

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"重新路由"处理器允许将文档路由到另一个目标索引或数据流。它有两种主要模式：

设置"目标"选项时，将显式指定目标，并且无法设置"数据集"和"命名空间"选项。

如果未设置"目标"选项，则此处理器处于数据流模式。请注意，在此模式下，"重新路由"处理器只能用于遵循数据流命名方案的数据流。尝试在名称不合规的数据流上使用此处理器将引发异常。

数据流的名称由三部分组成："-<type><dataset>-<namespace>"。有关更多详细信息，请参阅数据流命名方案文档。

此处理器可以使用文档中的静态值或引用字段来确定 newtarget 的"数据集"和"命名空间"组件。有关更多详细信息，请参见表 38 "重新路由选项"。

无法使用"重新路由"处理器更改数据流的"类型"。

执行"重新路由"处理器后，将跳过当前管道的所有其他处理器，包括最终管道。如果在流水线的上下文中执行当前管道，则调用流水线也将跳过。这意味着在管道中最多执行一个"重新路由"处理器，允许定义互斥路由条件，类似于 if，else-if，else-if，...条件。

重新路由处理器确保"data_stream.<类型|数据集|命名空间>'字段是根据新目标设置的。如果文档包含"event.dataset"值，它将更新以反映与"data_stream.dataset"相同的值。

请注意，客户端需要具有对最终目标的权限。否则，文档将被拒绝，并出现如下所示的安全异常：

    
    
    {"type":"security_exception","reason":"action [indices:admin/auto_create] is unauthorized for API key id [8-dt9H8BqGblnY2uSI--] of user [elastic/fleet-server] on indices [logs-foo-default], this action is granted by the index privileges [auto_configure,create_index,manage,all]"}

**表 38.重新路由选项**

姓名 |必填 |默认 |描述 ---|---|---|--- '目的地'

|

no

|

-

|

目标的静态值。设置"数据集"或"命名空间"选项时无法设置。   "数据集"

|

no

|

`{{data_stream.dataset}}`

|

字段引用或数据流名称的数据集部分的静态值。除了索引名称的条件外，不能包含"-"，并且不得超过 100 个字符。示例值为"nginx.access"和"nginx.error"。

支持具有类似胡须的语法的字段引用(表示为"{{双}}"或"{{{三重}}}"大括号)。解析字段引用时，处理器将无效字符替换为"_"。<dataset>如果所有字段引用都解析为"null"、缺失或非字符串值，则使用索引名称的""部分作为回退。   "命名空间"

|

no

|

`{{data_stream.namespace}}`

|

字段引用或数据流名称的命名空间部分的静态值。请参阅允许字符的索引名称条件。不得超过 100 个字符。

支持具有类似胡须的语法的字段引用(表示为"{{双}}"或"{{{三重}}}"大括号)。解析字段引用时，处理器将无效字符替换为"_"。<namespace>如果所有字段引用都解析为"null"、缺失或非字符串值，则使用索引名称的""部分作为回退。   "说明"

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

处理器的标识符。对于调试和指标很有用。   "if"选项可用于定义文档应重新路由到新目标的条件。

    
    
    {
      "reroute": {
        "tag": "nginx",
        "if" : "ctx?.log?.file?.path?.contains('nginx')",
        "dataset": "nginx"
      }
    }

数据集和命名空间选项可以包含单个值或用作回退的值列表。如果字段引用的计算结果为"null"，文档中不存在，则使用下一个值或字段引用。如果字段引用的计算结果为非"字符串"值，则处理器将失败。

在以下示例中，处理器将首先尝试解析"service.name"字段的值，以确定"数据集"的值。如果该字段解析为"null"、缺失或为非字符串值，它将尝试列表中的下一个元素。在本例中，这是静态值"通用"。"命名空间"选项仅配置了一个静态值。

    
    
    {
      "reroute": {
        "dataset": [
            "{{service.name}}",
            "generic"
        ],
        "namespace": "default"
      }
    }

[« Rename processor](rename-processor.md) [Script processor »](script-
processor.md)
