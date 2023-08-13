

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.6.0](release-notes-8.6.0.md) [Elasticsearch
version 8.5.2 »](release-notes-8.5.2.md)

## 弹性搜索版本8.5.3

另请参阅 8.5 中的重大更改。

### 已知问题

* 如果自版本 6.x 以来未修改任何机器学习数据馈送，则无法列出

如果您的数据馈送是在版本 5.x 或 6.x 中创建的，并且自 7.0 版以来未更新，则无法在 8.4 和 8.5 中列出数据馈送。这意味着无法使用 Kibana 管理异常检测作业。此问题已在 8.6.0 中修复。

如果使用此类数据馈送升级到 8.4 或 8.5，则需要通过使用以下步骤更新每个数据馈送的授权信息来解决此问题。

* 使用 'settings.json' 文件配置 Elasticsearch 的编排器可能会在主选举期间遇到死锁(问题：#92812)

要解决死锁，请删除"settings.json"文件并重新启动受影响的节点。

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456) * 当使用摄取附件处理器时，Tika 与 log4j 2.18.0 及更高版本(在 Elasticsearch 8.4.0 中引入)的交互会导致过多的日志记录。此日志记录过多，可能导致群集不稳定，直至群集不可用且必须重新启动节点。(问题：#91964)。此问题已在 Elasticsearch 8.7.0 (#93878) 中修复

要解决此问题，请升级到 8.7.0 或更高版本。

### 错误修正

Infra/Core

    

* 添加"trace.id"以请求跟踪日志 #91772(问题：#88174) * "ElasticsearchEncaughtExceptionHandler"中的"DoPrivileged"并检查修改线程 #91704(问题：#91650)

采集节点

    

* 处理为"摄取文档"生成源代码时引发的任何异常 #91981

机器学习

    

* ML 统计信息失败不应停止使用 API 工作 #91917(问题：#91893)

Stats

    

* 修复 IndexService getNodeMappingStats #91334 中的 NPE(问题：#91259)

Transform

    

* 修复了从 CCS #91622 解析索引时失败的问题(问题：#91550)

###Enhancements

采集节点

    

* 重构丰富维护协调逻辑 #90931

TLS

    

* 支持受限信任的 SAN/DNS 名称 #91946

###Upgrades

Engine

    

* 将 Lucene 升级到版本 9.4.2 #91823

[« Elasticsearch version 8.6.0](release-notes-8.6.0.md) [Elasticsearch
version 8.5.2 »](release-notes-8.5.2.md)
