

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md)

[« Accessing document fields and special variables](modules-scripting-
fields.md) [Lucene expressions language »](modules-scripting-
expression.md)

## 脚本和安全性

Painless 和 Elasticsearch 实现了安全层，以构建安全运行脚本的防御深度策略。

无痛使用细粒度的允许列表。不属于允许列表的任何内容都会导致编译错误。此功能是脚本的纵深防御策略中的第一层安全性。

第二层安全性是Java SecurityManager.As 其启动序列的一部分，Elasticsearch使Java SecurityManager能够限制部分代码可以执行的操作。Painless 使用 Java 安全管理器作为额外的防御层，以防止脚本执行诸如写入文件和侦听套接字之类的操作。

Elasticsearch 在 Linux 中使用 seccomp，在 macOS 中使用 Seatbelt 和 Windows 上的 ActiveProcessLimit 作为额外的安全层，以防止 Elasticsearch 分叉或运行其他进程。

您可以修改以下脚本设置以限制允许运行的脚本类型，并控制脚本可以在其中运行的可用上下文。要在纵深防御策略中实施额外的层，请遵循 Elasticsearch 安全原则。

### 允许的脚本排版设置

Elasticsearch支持两种脚本类型："内联"和"存储"。默认情况下，Elasticsearch 配置为运行这两种类型的脚本。要限制运行的脚本类型，请将"script.allowed_types"设置为"内联"或"存储"。要阻止任何脚本运行，请将"script.allowed_types"设置为"无"。

如果您使用 Kibana，请将"script.allowed_types"设置为两者或仅设置为"内联"。某些 Kibana 功能依赖于内联脚本，如果 Elasticsearch 不允许内联脚本，则无法按预期运行。

例如，要运行"内联"脚本但不运行"存储"脚本：

    
    
    script.allowed_types: inline

### 允许的脚本上下文设置

默认情况下，允许所有脚本上下文。使用"script.allowed_contexts"设置指定允许的上下文。要指定不允许任何上下文，请将"script.allowed_contexts"设置为"无"。

例如，要允许脚本仅在"评分"和"更新"上下文中运行：

    
    
    script.allowed_contexts: score, update

[« Accessing document fields and special variables](modules-scripting-
fields.md) [Lucene expressions language »](modules-scripting-
expression.md)
