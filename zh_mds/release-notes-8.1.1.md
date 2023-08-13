

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.1.2](release-notes-8.1.2.md) [Elasticsearch
version 8.1.0 »](release-notes-8.1.0.md)

## 弹性搜索版本8.1.1

另请参阅 8.1 中的重大更改。

### 已知问题

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 错误修正

Analysis

    

* 修复"min_hash"配置设置名称 #84753(问题：#84578)

EQL

    

* 在出现异常时，通过序列匹配器和断路器清理任何已用内存 #84451

Engine

    

* 在快照索引提交之前增加存储引用 #84776

ILM+SLM

    

* 为新创建的索引调用初始"AsyncActionStep" #84541(问题：#77269)

索引接口

    

* 在模拟索引模板之前删除现有的"索引/数据流/别名" #84675(问题：#84256)

Infra/Core

    

* 修复了"系统索引元数据升级服务"隐藏别名处理中的"空指针异常" #84780 (问题： #81411) * 需要并保留过滤的 rest 请求的内容类型 #84914 (问题： #84784) * 在"doPrivileged"调用中包装线程创建 #85180

基础设施/休息接口

    

* 正确返回 V7 兼容模式 #84873 中文档的"_type"字段(问题：#84173)

Ingest

    

* 向后移植将"GeoIpDownloaderTask"标记为取消后完成 #84028 #85014(问题：#84028、#84652) * "复合处理器"在执行处理器时还应捕获异常 #84838(问题：#84781)

机器学习

    

* 修复文本结构端点 #84967 中的 Kibana 日期格式和类似覆盖 * 修复了文本结构端点 #85066 中的多行开始模式 * 返回获取异常情况检测作业中的所有数据馈送 API #84759

Packaging

    

* 删除使用 Cloudflare zlib #84680

Search

    

* 修复"磁盘使用情况"API #84909 中的点访问者 * "点扩展XContent解析器"以公开原始令牌位置 #84970

Snapshot/Restore

    

* 如果没有 AWS Web 身份令牌的符号链接，则不会失败 #84697 * 从 STS 终端节点 #84585 查找 STS 客户端的 AWS 区域(问题：#83826)

###Enhancements

SQL

    

* JDBC 驱动程序 #84499 的前向警告标头

Watcher

    

* 为 Watcher 电子邮件操作 #84894 添加允许的域列表(问题：#84739)

[« Elasticsearch version 8.1.2](release-notes-8.1.2.md) [Elasticsearch
version 8.1.0 »](release-notes-8.1.0.md)
