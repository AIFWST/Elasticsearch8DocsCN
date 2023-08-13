

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.5.2](release-notes-8.5.2.md) [Elasticsearch
version 8.5.0 »](release-notes-8.5.0.md)

## 弹性搜索版本8.5.1

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

Audit

    

* 修复了审核不存在的运行身份用户的"身份验证成功"中的 NPE #91171

Authentication

    

* 确保 PKI 的"delegated_by_realm"元数据遵循运行方式 #91173

Authorization

    

* 确保"条款枚举"操作与 API 密钥正确配合使用 #91170

集群协调

    

*修复具有相同名称的索引和别名中损坏的元数据 #91456

EQL

    

* 修复 EQLSearchRequest 序列化 (bwc) #91402

Geo

    

* 修复了在 mvt API #91105 中处理跨越日期变更线的索引信封(问题：#91060)

Infra/CLI

    

* 修复了从航站楼 #91131 读取长线时删除回车的问题(问题：#89227)

Infra/Core

    

* 修复 APM 配置文件删除 #91058(问题：#89439)

机器学习

    

* 允许在设置跨度时更新 NLP 截断选项 #91224 * 临时存储桶不应计入存储桶总数 #91288

Network

    

* 修复本地执行的"传输操作代理"#91289

Transform

    

* 使转换"_preview"请求可取消 #91313(问题：#91286)

###Enhancements

Authorization

    

* 添加连接器索引创建的权限 #91026 * 在企业级搜索服务帐户中添加爬网程序日志索引的权限 #91094

Infra/Core

    

* 允许旧索引上的旧索引设置 #90264(问题：#84992) * 在节点关闭时检查未分配的分片 #91297(问题：#88635)

###Upgrades

Packaging

    

* 将捆绑的 JDK 更新到 Java 19.0.1 #91025(问题：#91010)

[« Elasticsearch version 8.5.2](release-notes-8.5.2.md) [Elasticsearch
version 8.5.0 »](release-notes-8.5.0.md)
