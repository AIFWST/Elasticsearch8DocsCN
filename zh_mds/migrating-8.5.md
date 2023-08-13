

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md)

[« Migrating to 8.6](migrating-8.6.md) [Migrating to 8.4
»](migrating-8.4.md)

## 迁移到 8.5

本节讨论将应用程序迁移到 Elasticsearch 8.5 时需要注意的更改。

另请参阅_What发行说明中的新增8.9_and。

### 重大变更

Elasticsearch 8.5 中的以下更改可能会影响您的应用程序并阻止它们正常运行。在升级到 8.5 之前，请查看这些更改并采取所述的步骤来减轻影响。

#### REST API 更改

批量 API 现在拒绝包含无法识别的操作的请求

**详细信息** 对批量 API 的请求由一系列项目组成，每个项目都以描述该项目的 JSON 对象开头。此对象包括要对项目执行的操作类型，该操作类型应该是"创建"、"更新"、"索引"或"删除"之一。早期版本的 Elasticsearch 有一个错误，导致它们忽略无法识别类型的项目，跳过请求中的下一行，但这种宽松的行为意味着客户端无法将响应中的项目与请求中的项目相关联，在某些情况下，它会导致请求的其余部分被正确解析。

从版本 8.5 开始，对批量 API 的请求必须仅包含具有可识别类型的项目。Elasticsearch 将拒绝包含任何类型无法识别的项目的请求，并显示"400 错误请求"错误响应。

我们认为此更改是一个错误修复，但在此处将其列为重大更改，因为它可能会影响依赖于能够向 Elasticsearch 发送无法识别的操作的应用程序的行为。

**影响** 确保应用程序仅将类型为"创建"、"更新"、"索引"或"删除"的项目发送到批量 API。

###Deprecations

以下功能已在 Elasticsearch 8.5 中弃用，并将在未来的版本中删除。虽然这不会对应用程序产生直接影响，但我们强烈建议您在升级到 8.5 后采取所述步骤来更新代码。

若要了解是否正在使用任何已弃用的功能，请启用弃用日志记录。

#### 插件 API 弃用

扩展网络插件接口的插件已被弃用。

Details

**详细信息**插件可以覆盖控制节点如何通过TCP / IP与其他节点连接的功能。这些插件扩展了网络插件接口。在下一个主要版本中，这些插件将无法安装。

**影响** 停止使用任何扩展网络插件的插件。您可以通过检查 Elasticsearch 弃用日志来查看是否有任何插件使用已弃用的功能。

扩展发现插件以覆盖加入验证器或选举策略已被弃用

**详细信息**扩展DiscoveryPlugin的插件可能会覆盖getJoinValidator和getElectionStrategies。这些方法是 Elasticsearch 中集群机制的实现细节。不应覆盖它们。在下一个主要版本中，覆盖getJoinValidator orgetElectionStrategies的插件将无法安装。

**影响** 停止使用任何覆盖 DiscoveryPlugin 中的 getJoinValidator orgetElectionStrategies 的插件。您可以通过查看 Elasticsearch 弃用日志来查看是否有任何插件使用了已弃用的功能。

[« Migrating to 8.6](migrating-8.6.md) [Migrating to 8.4
»](migrating-8.4.md)
