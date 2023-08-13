

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.2.0](release-notes-8.2.0.md) [Elasticsearch
version 8.1.2 »](release-notes-8.1.2.md)

## 弹性搜索版本8.1.3

另请参阅 8.1 中的重大更改。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Authorization

    

* 解决超级用户 #85519 时忽略应用程序权限失败

机器学习

    

* 避免重整化器中的多个排队分位数文档 #85555(问题：#85539)

Mapping

    

* 不要在重复的内容字段过滤器上失败 #85382

Search

    

* 修复了"indices.queries.cache.all_segments"的跳过缓存因子 #85510

Snapshot/Restore

    

* 公开 GCS 存储库的代理设置 #85785 (问题： #84569)

Watcher

    

* 避免在数据流指向多个索引时出现观察程序验证错误 #85507(问题：#85508) * 在 WARN 级别记录观察程序群集状态验证错误 #85632

[« Elasticsearch version 8.2.0](release-notes-8.2.0.md) [Elasticsearch
version 8.1.2 »](release-notes-8.1.2.md)
