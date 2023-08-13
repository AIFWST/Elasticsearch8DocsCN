

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md) ›[Configuring data
streams/indices for monitoring](config-monitoring-indices.md)

[« Configuring data streams created by Elastic Agent](config-monitoring-data-
streams-elastic-agent.md) [Configuring indices created by Metricbeat 7 or
internal collection »](config-monitoring-indices-metricbeat-7-internal-
collection.md)

## 配置由 Metricbeat8 创建的数据流

使用 Metricbeat 8 进行监控时，数据存储在一组名为".monitoring-{product}-8-mb"的数据流中。例如：".monitoring-es-8-mb"。

这些数据流的设置和映射由名为".monitoring-{product}-mb"的索引模板确定。例如：".monitoring-es-mb"。您可以通过克隆此索引模板并对其进行编辑来更改每个数据流的设置。

您需要在升级弹性堆栈时重复此过程，以获取默认监控索引模板的最新更新。

您可以在 Kibana 中克隆索引模板：

* 导航到 **堆栈管理** > **索引管理** > **索引模板**。  * 从"**视图**"下拉列表中，选择"**系统模板**"。  * 搜索索引模板。  * 选择"**克隆**"操作。  * 更改名称，例如更改为"custom_monitoring"。  * 将优先级设置为"500"，以确保它覆盖默认索引模板。  * 在"设置"部分指定要更改的设置。  * 保存克隆的模板。

你也可以使用 Elasticsearch API：

* 使用获取索引模板 API 检索索引模板。  * 编辑索引模板：将模板"优先级"设置为"500"，并在"设置"部分指定要更改的设置。  * 使用创建索引模板 API 将更新的索引模板存储在不同的名称下，例如"custom_monitoring"。

Metricbeat 8 使用可组合模板，而不是旧模板。

更改索引模板后，更新的设置仅应用于数据流的新支持索引。将鼠标悬停在数据流上以立即将更新的设置应用于数据流的写入索引。

[« Configuring data streams created by Elastic Agent](config-monitoring-data-
streams-elastic-agent.md) [Configuring indices created by Metricbeat 7 or
internal collection »](config-monitoring-indices-metricbeat-7-internal-
collection.md)
