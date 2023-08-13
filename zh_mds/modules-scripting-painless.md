

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md)

[« Scripting](modules-scripting.md) [How to write scripts »](modules-
scripting-using.md)

## 无痛脚本语言

_Painless_ 是一种高性能、安全的脚本语言，专为 Elasticsearch 设计。您可以使用 Painless 安全地编写内联和存储脚本，只要 Elasticsearch 支持脚本。

Painless 提供了围绕以下核心原则的众多功能：

* **安全**：确保集群的安全性至关重要。为此，Painless 使用细粒度的允许列表，其粒度可细化到类的成员。不属于允许列表的任何内容都会导致编译错误。有关每个脚本上下文的可用类、方法和字段的完整列表，请参阅无痛 API 参考。  * **性能**：Painless直接编译成JVM字节码，以利用JVM提供的所有可能的优化。此外，Painless 通常避免在运行时需要额外较慢检查的功能。  * **简单**：Painless实现了对任何具有基本编码经验的人来说自然熟悉的语法。Painless 使用 Java 语法的一个子集，并进行一些额外的改进，以增强可读性并删除样板文件。

### 启动脚本

准备好开始使用无痛编写脚本了吗？了解如何编写您的第一个脚本。

如果您已经熟悉 Painless，请参阅 Painless 语言规范，了解 Painless 语法和语言功能的详细说明。

[« Scripting](modules-scripting.md) [How to write scripts »](modules-
scripting-using.md)
