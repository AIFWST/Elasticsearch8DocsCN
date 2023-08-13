

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Plugins](modules-plugins.md) [Archived settings »](archived-
settings.md)

# 升级弹性搜索

Elasticsearch 集群通常可以一次升级一个节点，因此升级不会中断服务。有关升级说明，请参阅升级到 Elastic 8.9.0。

### 从 7.x 升级

要从 7.16 或更早版本升级到 8.9.0，**您必须先升级到 7.17** ，即使您选择执行全集群重新启动而不是滚动升级也是如此。这使您能够使用**升级助手**来识别和解决问题，重新索引7.0之前创建的索引，然后执行滚动升级。在继续升级之前，您必须解决所有关键问题。有关说明，请参阅准备从 7.x 升级。

### 索引兼容性

Elasticsearch 对在以前的主要版本中创建的索引具有完整的查询和写入支持。如果您在 6.x 或更早版本中创建了索引，则可以使用归档功能将它们导入到较新的 Elasticsearch 版本中，或者您必须在升级到 8.9.0 之前重新索引或删除它们。6.x 或更早版本索引的快照只能使用 归档功能恢复到 8.x 集群，即使它们是由 7.x 集群创建的。7.17 中的"升级助手"标识需要重新编制索引或删除的任何索引。

### REST API 兼容性

REST API 兼容性是一项按请求选择加入的功能，可帮助 REST 客户端缓解对 REST API 的不兼容(中断)更改。

### FIPS 合规性和 Java17

Elasticsearch 8.9.0 需要 Java 17 或更高版本。目前还没有一个 FIPS 认证的 Java 17 安全模块，您可以在 FIPS 140-2 模式下运行 Elasticsearch 8.9.0 时使用。如果您在 FIPS 140-2 模式下运行，则需要向安全组织请求例外以升级到 Elasticsearch 8.9.0，或者继续使用 Elasticsearch 7.x，直到 Java 17 通过认证。或者，考虑在FedRAMP认证的GovCloud区域中使用Elasticsearch Service。

[« Plugins](modules-plugins.md) [Archived settings »](archived-
settings.md)
