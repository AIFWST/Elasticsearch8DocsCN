

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.0.0-rc2](release-notes-8.0.0-rc2.md)
[Elasticsearch version 8.0.0-beta1 »](release-notes-8.0.0-beta1.md)

## 弹性搜索版本8.0.0-rc1

另请参阅 8.0 中的重大更改。

### 已知问题

* **不要将生产集群升级到 Elasticsearch 8.0.0-rc1.** Elasticsearch 8.0.0-rc1 是 Elasticsearch 8.0 的预发行版，仅用于测试目的。

不支持从预发布版本升级，这可能会导致错误或数据丢失。如果从已发布版本(如 7.16)升级到预发布版本进行测试，请在完成后放弃群集的内容。请勿尝试升级到最终的 8.0 版本。

对于 Elasticsearch 8.0.0-rc1，Elasticsearch SQL JDBC 驱动程序需要 Java 17 或更高版本。在 Elasticsearch 8.0.0-rc2 中，JDBC 驱动程序只需要 Java 8 或更高版本。<https://github.com/elastic/elasticsearch/pull/82325>

### 重大变更

Infra/Core

    

* 所有系统索引均为隐藏索引 #79512

Snapshot/Restore

    

* 调整快照索引解析行为以使其更直观 #79670(问题：#78320)

###Deprecations

Engine

    

* 弃用设置"max_merge_at_once_explicit"#80574

机器学习

    

* 弃用"estimated_heap_memory_usage_bytes"并替换为"model_size_bytes" #80554

Search

    

* 根据节点特征配置 'IndexSearcher.maxClauseCount()' #81525 (问题： #46433)

Transform

    

* 改进转换弃用消息 #81847(问题：#81521、#81523)

###Enhancements

Authorization

    

* 授予"kibana_system"保留角色对".internal.preview.alerts*"索引 #80889 的"所有"权限的访问权限(问题：#76624、#80746、#116374) * 授予"kibana_system"保留角色对 .preview.alerts* 索引的"所有"权限的访问权限 #80746 * 授予编辑者和查看者角色对警报即数据索引的访问权限 #81285

ILM+SLM

    

* 将未更改的 ILM 策略更新转换为 noop #82240(问题：#82065)

索引接口

    

* 批量滚动更新群集状态更新 #79945(问题：#77466、#79782)* 在元数据类 #80348 中重用"映射元数据"实例(问题：#69772、#77466)

Infra/Settings

    

* 通过字符串实习实现设置重复数据删除 #80493(问题：#77466、#78892)

Ingest

    

* 从二进制文件中提取更多标准元数据 #78754(问题：#22339)

机器学习

    

* 将"deployment_stats"添加到训练模型统计信息 #80531 * 设置"use_auto_machine_memory_percent"现在默认为"max_model_memory_limit" #80532(问题：#80415)

Monitoring

    

* 为公测弹性云服务器数据添加默认模板 #81744

Network

    

* 改进慢速入站处理以包括响应类型 #80425

Recovery

    

* 修复了"挂起复制操作"将大量"NOOP"任务提交到"通用"#82092(问题：#77466、#79837)

Reindex

    

* 如果最大文档数小于滚动大小，则不要滚动(通过查询更新/删除)#81654(问题：#54270)

Security

    

* "BaseRunAsSuperuserCommand" #81025 的 URL 选项(问题：#80481)

### 错误修正

Autoscaling

    

* 自动缩放使用调整后的总内存 #80528(问题：#78750)

数据流

    

* 禁止还原具有冲突写入数据流的数据流别名 #81217(问题：#80976)

ILM+SLM

    

* SLM 元数据中快照故障的详细序列化较少 #80942(问题：#77466)

索引接口

    

* 修复"可组合索引模板"等于"composed_of"为空时 #80864

基础设施/休息接口

    

* 处理从"RestCompatibleVersionHelper"#80253 (问题： #78214， #79060)

Ingest

    

* 将默认 geoip 日志记录调整为不那么详细 #81404(问题：#81356)

机器学习

    

* 将模型状态兼容版本设置为 8.0.0 #2139

[« Elasticsearch version 8.0.0-rc2](release-notes-8.0.0-rc2.md)
[Elasticsearch version 8.0.0-beta1 »](release-notes-8.0.0-beta1.md)
