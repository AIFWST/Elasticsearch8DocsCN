

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.5.0](release-notes-8.5.0.md) [Elasticsearch
version 8.4.2 »](release-notes-8.4.2.md)

## 弹性搜索版本8.4.3

另请参阅 8.4 中的重大更改。

### 已知问题

* 当使用没有所有日期字段(缺少月份或日期)的格式的日期范围搜索时，可能会使用错误解析的日期。解决方法是对所有日期字段(年、月、日)使用日期模式(问题：#90187)* 如果自版本 6.x 以来未修改任何机器学习数据源，则无法列出机器学习数据源

如果您的数据馈送是在版本 5.x 或 6.x 中创建的，并且自 7.0 版以来未更新，则无法在 8.4 和 8.5 中列出数据馈送。这意味着无法使用 Kibana 管理异常检测作业。此问题已在 8.6.0 中修复。

如果使用此类数据馈送升级到 8.4 或 8.5，则需要通过使用以下步骤更新每个数据馈送的授权信息来解决此问题。

* 使用 'settings.json' 文件配置 Elasticsearch 的编排器可能会在主选举期间遇到死锁(问题：#92812)

要解决死锁，请删除"settings.json"文件并重新启动受影响的节点。

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456) * 当使用摄取附件处理器时，Tika 与 log4j 2.18.0 及更高版本(在 Elasticsearch 8.4.0 中引入)的交互会导致过多的日志记录。此日志记录过多，可能导致群集不稳定，直至群集不可用且必须重新启动节点。(问题：#91964)。此问题已在 Elasticsearch 8.7.0 (#93878) 中修复

要解决此问题，请升级到 8.7.0 或更高版本。

### 错误修正

Infra/Core

    

* 修复文件权限错误以避免在 Windows #90271 上重复错误保存循环(问题：#90222)

采集节点

    

* 防止节点统计信息 API #90319 中的序列化错误(问题：#77973)

###Regressions

Ranking

    

* 确保"cross_fields"始终使用有效的术语统计信息 #90314

[« Elasticsearch version 8.5.0](release-notes-8.5.0.md) [Elasticsearch
version 8.4.2 »](release-notes-8.4.2.md)
