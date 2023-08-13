

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Use Elasticsearch for time series data](use-elasticsearch-for-time-series-
data.md) [Fix common cluster issues »](fix-common-cluster-issues.md)

#Troubleshooting

本节提供了一系列故障排除解决方案，旨在帮助用户解决 Elasticsearch 部署可能遇到的问题。

###General

* 修复常见群集问题 * 可以使用运行状况 API 诊断多个故障排除问题。

###Data

* 修复磁盘空间不足导致的水印错误 * 为系统添加缺失层 * 允许 Elasticsearch 分配系统中的数据 * 允许 Elasticsearch 分配索引 * 索引混合索引分配过滤器与数据层节点角色以在数据层之间移动 * 没有足够的节点来分配所有分片副本 * 超出单个节点上索引的分片总数 * 已达到每个节点的分片总数 * 故障排除数据损坏

###Management

* 启动索引生命周期管理 * 启动快照生命周期管理

###Capacity

* 修复磁盘外的数据节点 * 修复磁盘外的主节点 * 修复磁盘外的其他角色节点

### 快照和还原

* 从快照恢复数据 * 多个部署写入同一快照存储库 * 排查重复的快照故障

###Others

* 排查不稳定集群问题 * 发现疑难解答 * 监控疑难解答 * 转换疑难解答 * 观察程序疑难解答 * 搜索疑难解答 * 分片容量排查

如果这些解决方案都与您的问题无关，您仍然可以获得帮助：

* 对于具有有效订阅的用户，您可以通过多种方式获得帮助：

    * Go directly to the [Support Portal](http://support.elastic.co)
    * From the Elasticsearch Service Console, go to the [Support page](https://cloud.elastic.co/support?baymax=docs-body&elektra=docs), or select the support icon that looks like a life preserver on any page. 
    * Contact us by email: [support@elastic.co](mailto:support@elastic.co)

如果您通过电子邮件与我们联系，请使用您注册时使用的电子邮件地址，以便我们更快地为您提供帮助。如果您使用通讯组列表作为您的注册电子邮件，您也可以向我们注册第二个电子邮件地址。只需打开一个案例，让我们知道您要添加的姓名和电子邮件地址。

* 对于没有有效订阅的用户，请访问 Elastic 社区论坛，从社区专家(包括 Elastic 人员)那里获得答案。

[« Use Elasticsearch for time series data](use-elasticsearch-for-time-series-
data.md) [Fix common cluster issues »](fix-common-cluster-issues.md)
