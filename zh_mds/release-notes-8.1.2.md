

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.1.3](release-notes-8.1.3.md) [Elasticsearch
version 8.1.1 »](release-notes-8.1.1.md)

## 弹性搜索版本8.1.2

另请参阅 8.1 中的重大更改。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Authorization

    

* 为 APM #85085 的"kibana_system"添加删除权限

Engine

    

* 在快照索引提交之前增加存储引用 #84776

Infra/Core

    

* 返回空版本，如果找不到它，则不会炸毁 #85244 * 验证系统索引描述符的索引格式协议 #85173 * 在"doPrivileged"调用中包装线程创建 #85180

机器学习

    

* 查找最新状态文档的索引时不要获取源代码 #85334 * 修复了文本结构端点中的多行开始模式 #85066 * 在节点关闭事件时重新分配模型部署 #85310

Mapping

    

* 不要在重复的内容字段过滤器上失败 #85382

Search

    

* 在分析磁盘使用情况之前增加存储引用 #84774 * 限制磁盘使用情况 API 中的并发分片请求 #84900(问题：#84779) * "传输广播操作"应始终为每个分片设置响应 #84926

Snapshot/Restore

    

* 修复冻结层 #85239 上的泄漏侦听器错误

Watcher

    

* 不再需要主节点来安装观察程序模板 #85287(问题：#85043)

[« Elasticsearch version 8.1.3](release-notes-8.1.3.md) [Elasticsearch
version 8.1.1 »](release-notes-8.1.1.md)
