

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.3.2](release-notes-8.3.2.md) [Elasticsearch
version 8.3.0 »](release-notes-8.3.0.md)

## 弹性搜索版本8.3.1

另请参阅 8.3 中的重大更改。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Audit

    

* 支持删除审核日志记录的忽略过滤器 #87675(问题：#68588)

Ingest

    

* 不要忽略批量 API 中更新插入的管道 #87719(问题：#87131) * Geoip 处理器应遵守"ignore_missing"，以防缺少数据库 #87793(问题：#87345)

机器学习

    

* 改进训练模型统计信息 API 性能 #87978

Snapshot/Restore

    

* 使用提供的 SAS 令牌，而不使用 SDK 清理，这可能会产生无效签名 #88155(问题：#88140)

Stats

    

* 在管理池上运行"传输群集信息操作" #87679

Transform

    

* 将"_refresh"(具有系统权限)与"按查询删除"(具有用户权限)分开执行 #88005(问题：#88001)

###Enhancements

Discovery-Plugins

    

* 从发现 Azure 中删除冗余的杰克逊依赖项 #87898

Performance

    

* 警告大型预读对搜索的影响 #88007

[« Elasticsearch version 8.3.2](release-notes-8.3.2.md) [Elasticsearch
version 8.3.0 »](release-notes-8.3.0.md)
