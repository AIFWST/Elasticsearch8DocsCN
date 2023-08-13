

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.4.3](release-notes-8.4.3.md) [Elasticsearch
version 8.4.1 »](release-notes-8.4.1.md)

## 弹性搜索版本8.4.2

另请参阅 8.4 中的重大更改。

### 已知问题

* **此版本包含使用"cross_fields"评分类型的回归multi_match"查询。 弹性搜索

当运行"cross_fields"类型的"multi_match"查询时，Elasticsearch有时会抛出IllegalArgument异常，并显示消息"totalTermFreq Must be at 至少docFreq"。如果使用"cross_fields"评分类型，建议跳过版本 8.4.2。此回归已在版本 8.4.3 中修复。

* 当使用没有所有日期字段(缺少月份或日期)的格式的日期范围搜索时，可能会使用错误解析的日期。解决方法是对所有日期字段(年、月、日)使用日期模式(问题：#90187)* 如果自版本 6.x 以来未修改任何机器学习数据源，则无法列出机器学习数据源

如果您的数据馈送是在版本 5.x 或 6.x 中创建的，并且自 7.0 版以来未更新，则无法在 8.4 和 8.5 中列出数据馈送。这意味着无法使用 Kibana 管理异常检测作业。此问题已在 8.6.0 中修复。

如果使用此类数据馈送升级到 8.4 或 8.5，则需要通过使用以下步骤更新每个数据馈送的授权信息来解决此问题。

* 使用 'settings.json' 文件配置 Elasticsearch 的编排器可能会在主选举期间遇到死锁(问题：#92812)

要解决死锁，请删除"settings.json"文件并重新启动受影响的节点。

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456) * 当使用摄取附件处理器时，Tika 与 log4j 2.18.0 及更高版本(在 Elasticsearch 8.4.0 中引入)的交互会导致过多的日志记录。此日志记录过多，可能导致群集不稳定，直至群集不可用且必须重新启动节点。(问题：#91964)。此问题已在 Elasticsearch 8.7.0 (#93878) 中修复

要解决此问题，请升级到 8.7.0 或更高版本。

### 错误修正

Allocation

    

* 修复了"最大重试分配决策程序"#89973 中的调试模式

Authentication

    

* 修复了"传输打开ID连接准备身份验证操作"#89930 中的响应重复发送

Autoscaling

    

* 修复了克隆或拆分后自动缩放的问题 #89768(问题：#89758)

Health

    

* 修复获取远程主历史记录的条件 #89472(问题：#89431)

ILM+SLM

    

* 在 ILM 别名交换期间复制"isHidden"#89650(问题：#89604)

Infra/Core

    

* 将日期舍入逻辑扩展为有条件的 #89693(问题：#89096、#58986) * 修复错误更新 #89630 时"文件设置服务"挂起 * 实施修复以终止文件观察程序线程以避免死锁 #89934

采集节点

    

* 修复"on_failure"块 #89632 内的摄取元数据中不存在的管道"id"

机器学习

    

* 修复"传输删除过期数据操作"#89935 中的内存泄漏 * 当现有类别匹配时，不要保留分类令牌 #2398

Network

    

* 修复了双重调用"RestChannel.sendResponse"时内存泄漏的问题 #89873

Ranking

    

* 避免使用"cross_fields"类型#89016(问题：#44700)的负分数

Rollup

    

* 将"传输汇总CapsAction"分叉到管理池 #89803

Search

    

* 空间隔需要从位置 -1 #89962 开始(问题：#89789)

Transform

    

* 计划程序并发修复 #89716(问题：#88991)

###Enhancements

Allocation

    

* 记录从 Web 身份令牌获取凭据的失败尝试 #88241

Health

    

* 将延迟分配诊断案例添加到分片可用性指示器 #89056

###Upgrades

Packaging

    

* 将 OpenJDK 更新到 18.0.2.1 #89535(问题：#89531)

[« Elasticsearch version 8.4.3](release-notes-8.4.3.md) [Elasticsearch
version 8.4.1 »](release-notes-8.4.1.md)
