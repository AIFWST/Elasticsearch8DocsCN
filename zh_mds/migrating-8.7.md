

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md)

[« Migrating to 8.8](migrating-8.8.md) [Migrating to 8.6
»](migrating-8.6.md)

## 迁移到 8.7

本节讨论在将应用程序迁移到 Elasticsearch 8.7 时需要注意的更改。

另请参阅_What发行说明中的新增8.9_and。

### 重大变更

Elasticsearch 8.7 中的以下更改可能会影响您的应用程序并阻止它们正常运行。在升级到 8.7 之前，请查看这些更改并采取所述的步骤来减轻影响。

Elasticsearch 8.7 中没有明显的重大变化。但是有一些不太关键的中断性更改。

#### 引入更改

使"JsonProcessor"更严格，以便它不会静默地丢弃数据

**详细信息** 摄取节点的"json"处理器以前是宽松的。如果它以有效的 JSON 数据开头，它将接受无效的 JSON 数据。验证部分之后的任何内容都将被静默丢弃。从 8.7 开始，默认行为是拒绝无效的 JSON 数据并出现异常，以便数据不会以静默方式丢失。可以通过传递"false"作为新的"strict_json_parsing"处理器参数的值来重现旧行为。我们认为此更改是错误修复，但在此处将其列为重大更改，因为它可能会影响向"json"处理器发送无效 JSON 数据的应用程序的行为。

**影响** 确保应用程序仅将有效的 JSON 数据发送到"json"处理器，或修改管道中的"json"处理器以将"strict_json_parsing"参数设置为"false"。

[« Migrating to 8.8](migrating-8.8.md) [Migrating to 8.6
»](migrating-8.6.md)
