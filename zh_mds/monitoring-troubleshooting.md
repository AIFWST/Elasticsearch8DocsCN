

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Troubleshooting discovery](discovery-troubleshooting.md) [Troubleshooting
transforms »](transform-troubleshooting.md)

## 故障排除监控

使用本节中的信息可以解决常见问题并查找常见问题的答案。另请参阅在 Logstash 中排除监控故障。

对于您无法自己解决的问题...我们随时为您提供帮助。如果您是持有支持合同的现有 Elastic 客户，请在 Elastic 支持门户中创建工单。或者在 Elastic 论坛上发帖。

### 在 Kibana 中看不到监控数据

**症状**：Kibana 中的堆栈监控**页面上没有有关集群的信息。

解决方案**：检查监控集群上是否存在相应的索引。例如，使用 cat indices 命令来验证您的 Kibana 监控数据是否有 '.monitoring-kibana*' 索引，以及 Elasticsearchmonitoring 数据是否存在 '.monitoring-es*' 索引。如果使用 Metricbeat 收集监控数据，则索引的名称中包含"-mb"。如果索引不存在，请查看您的配置。例如，请参阅productionenvironment_中的_Monitoring。

### Kibana 缺少某些弹性堆栈节点或实例的监控数据

**症状**：Kibana 中的堆栈监控**页面不显示集群中某些节点或实例的信息。

**解决方法**：验证缺少的项目是否具有唯一的 UUID。每个Elasticsearch节点，Logstash节点，Kibana实例，Beat实例和APMServer被认为是唯一的，基于其持久UUID，该UUID位于其"path.data"目录中。或者，您可以在启动时在产品日志中找到 UUID。

在某些情况下，您还可以通过 API 检索此信息：

* 对于 Beat 实例，请使用 HTTP 终端节点检索"uuid"属性。例如，请参阅为 Filebeat 指标配置 HTTP 终结点。  * 对于 Kibana 实例，请使用状态端点检索"uuid"属性。  * 对于 Logstash 节点，请使用监控 API 根资源检索"id"属性。

当你安装 Elasticsearch、Logstash、Kibana、APM Server 或 Beats 时，它们的 'path.data' 目录应该不存在或为空;不要从其他安装复制此目录。

[« Troubleshooting discovery](discovery-troubleshooting.md) [Troubleshooting
transforms »](transform-troubleshooting.md)
