

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md) ›[Configuring data
streams/indices for monitoring](config-monitoring-indices.md)

[« Configuring data streams/indices for monitoring](config-monitoring-
indices.md) [Configuring data streams created by Metricbeat 8 »](config-
monitoring-data-streams-metricbeat-8.md)

## 配置弹性代理创建的数据流

使用 Elastic 代理进行监控时，数据存储在一组名为"指标-{产品}.stack_monitoring的数据流中。{数据集}-{命名空间}'。例如："metrics-elasticsearch.stack_monitoring.shard-default"。

这些数据流的设置和映射由名为"metrics-{product}.stack_monitoring的索引模板确定。{数据集}'。例如："metrics-elasticsearch.stack_monitoring.shard"。

要更改每个数据流的设置，请编辑"指标-{产品}.stack_monitoring。{数据集}@custom已存在的组件模板。您可以在 Kibana 中执行此操作：

* 导航到 **堆栈管理** > **索引管理** > **组件模板**。  * 搜索组件模板。  * 选择"编辑"操作。

你也可以使用 Elasticsearch API：

* 使用获取组件模板 API 检索组件模板。  * 编辑组件模板。  * 使用更新组件模板 API 存储更新的组件模板。

更改组件模板后，更新的设置仅应用于数据流的新支持索引。将鼠标悬停在数据流上以立即将更新的设置应用于数据流的写入索引。

[« Configuring data streams/indices for monitoring](config-monitoring-
indices.md) [Configuring data streams created by Metricbeat 8 »](config-
monitoring-data-streams-metricbeat-8.md)
