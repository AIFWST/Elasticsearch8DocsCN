

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.1.0](release-notes-8.1.0.md) [Elasticsearch
version 8.0.0 »](release-notes-8.0.0.md)

## 弹性搜索版本8.0.1

另请参阅 8.0 中的重大更改。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Aggregations

    

* 修复与 7.17.0 #83715 的向后兼容性

Distributed

    

* 正确处理具有 500 个或更多实例的大型区域 #83785(问题：#83783)

ILM+SLM

    

* 不允许在解释生命周期 API 响应中出现负年龄 #84043

Infra/Core

    

* 在线程上下文存储中复制"trace.id" #83218 * 在"结果重复数据删除器"中保留上下文 #84038(问题：#84036) * 如果"_meta"为空，则更新系统索引映射 #83896(问题：#83890)

Ingest

    

* 修复滚动升级期间启动的"GeoIpDownloader"问题 #84000 * 第一次匹配后短路日期模式 #83764

机器学习

    

* 在重新定位期间重试异常检测作业恢复 #83456

Packaging

    

* 将"log4j-slf4j-impl"添加到"repository-azure"#83661(问题：#83652)

Recovery

    

* 将缺少的"indices.recovery.internal_action_retry_timeout"添加到设置列表中 #83354

SQL

    

* 修复空结果集的 txt 格式 #83376

Search

    

* 避免在获取阶段急切加载"存储字段读取器"#83693(问题：#82777) * 当没有索引匹配时返回有效的 PIT #83424

Security

    

* 将 jANSI 依赖项升级到 2.4.0 #83566

Snapshot/Restore

    

* 将获取快照序列化移动到管理池 #83215 * 在"快照删除侦听器"中保留上下文 #84089(问题：#84036)

Transform

    

* 修复转换停止处理存储桶的情况 #82852

Watcher

    

* 允许监视定义中的空类型数组 #83524(问题：#83235)

###Enhancements

基础设施/休息接口

    

* 更新 YAML REST 测试以检查所有响应上的产品标题 #83290

Recovery

    

* 根据外部设置调整"索引恢复.max_字节数_每秒" #82819

###Upgrades

Geo

    

*更新矢量瓷砖谷歌protobuf到3.16.1 #83402

Packaging

    

* 将 JDK 捆绑到 17.0.2+8 #83243(问题：#83242)

[« Elasticsearch version 8.1.0](release-notes-8.1.0.md) [Elasticsearch
version 8.0.0 »](release-notes-8.0.0.md)
