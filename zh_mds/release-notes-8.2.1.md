

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.2.2](release-notes-8.2.2.md) [Elasticsearch
version 8.2.0 »](release-notes-8.2.0.md)

## 弹性搜索版本8.2.1

另请参阅 8.2 中的重大更改。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Aggregations

    

* 修复"自适应聚合器""toString"方法 #86042 * 降低未映射字段的键后解析复杂性 #86359(问题：#85928)

Authentication

    

* 设置用户 #86741 时确保身份验证与线路兼容(问题：#86716)

集群协调

    

* 避免打破添加/清除投票排除项 #86657

Geo

    

* 修复有界六边形网格，当它们包含其中一个极点上的箱时 #86460 * 修复 mvt 多边形方向 #86555(问题：#86560)

ILM+SLM

    

* 修复"max_primary_shard_size"调整大小因子数学 #86897 * 迁移到数据层后重新路由 路由 #86574(问题：#86572)

Infra/Core

    

* 修复"断言默认线程上下文"枚举允许的标头 #86262 * 转发端口 MDP 弃用信息 API #86103 * 使数据目录再次使用符号链接 #85878(问题：#85701) * 在队列操作数据流上设置自动扩展副本 #85511 * 不要为非主系统索引自动创建别名 #85977(问题：#85072)

Ingest

    

* 如果 geoip 系统索引被阻止，请不要下载 geoip 数据库 #86842 * 修复了使用对象字段作为扩充策略的匹配字段时的 NPE #86089(问题：#86058) * 处理".geoip_databases"是别名或具体索引 #85792(问题：#85756)

机器学习

    

* 调整"PyTorch"型号的内存开销 #86416 * 修复启用自动缩放时"_ml/info"报告的"max_model_memory_limit" #86660 * 提高大型集群中作业统计信息的可靠性 #86305 * 使自动缩放和任务分配使用相同的内存过时定义 #86632(问题：#86616) * 修复了在检测到季节性后可能导致模型边界膨胀的边缘情况 #2261

Packaging

    

* 修复忽略用户自定义堆设置的边缘情况 #86438(问题：#86431)

Security

    

* Authentication.token 现在使用现有身份验证的版本 #85978

Snapshot/Restore

    

* 部分/完全挂载索引的纯源快照失败更好 #86207 * 检查 Windows 中的可搜索快照缓存预分配是否成功 #86192 (问题： #85725) * 关机期间延迟可搜索快照分配 #86153 (问题： #85052) * 支持在未提供的情况下生成 AWS 角色会话名称 #86255

Stats

    

* 正确计算冻结数据层遥测的磁盘使用情况 #86580(问题：#86055)

###Upgrades

Packaging

    

* 切换到 OpenJDK 并升级到 18.0.1 #86554

[« Elasticsearch version 8.2.2](release-notes-8.2.2.md) [Elasticsearch
version 8.2.0 »](release-notes-8.2.0.md)
