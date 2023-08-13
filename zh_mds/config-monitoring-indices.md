

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md)

[« Collecting Elasticsearch log data with Filebeat](configuring-filebeat.md)
[Configuring data streams created by Elastic Agent »](config-monitoring-data-
streams-elastic-agent.md)

## 配置数据流/索引以进行监控

监控数据存储在 Elasticsearch 的数据流或索引中。默认数据流或索引设置可能不适用于您的情况。例如，您可能希望更改索引生命周期管理 (ILM) 设置、添加自定义映射或更改分片和副本的数量。更改这些设置的步骤取决于监视方法：

* 配置弹性代理创建的数据流 * 配置 Metricbeat 8 创建的数据流(弹性云上版本 8 Elasticsearch Service 部署的默认数据流) * 配置 Metricbeat 7 或内部集合创建的索引

更改映射或设置可能会导致监视仪表板停止正常工作。

[« Collecting Elasticsearch log data with Filebeat](configuring-filebeat.md)
[Configuring data streams created by Elastic Agent »](config-monitoring-data-
streams-elastic-agent.md)
