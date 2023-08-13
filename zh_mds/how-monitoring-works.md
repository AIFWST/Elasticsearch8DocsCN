

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md)

[« Monitoring overview](monitoring-overview.md) [Monitoring in a production
environment »](monitoring-production.md)

## 监控的工作原理

每个受监控的弹性堆栈组件在集群中都被视为唯一基于其持久 UUID，该 UUID 在节点或实例启动时写入 'path.data' 目录。

监控文档只是通过以指定的收集间隔监控每个 Elastic Stack 组件而构建的普通 JSON 文档。如果要更改这些文档的结构或存储方式，请参阅_Configuringdata流/索引以获取monitoring_。

您可以使用弹性代理或 Metricbeat 收集监控数据并将其直接传送到监控集群。

若要了解如何收集监视数据，请参阅：

* 以下主题之一，具体取决于您希望如何从 Elasticsearch 收集监控数据：

    * [_Collecting monitoring data with Elastic Agent_](configuring-elastic-agent.html "Collecting Elasticsearch monitoring data with Elastic Agent"): Uses a single agent to gather logs and metrics. Can be managed from a central location in Fleet. 
    * [_Collecting monitoring data with Metricbeat_](configuring-metricbeat.html "Collecting Elasticsearch monitoring data with Metricbeat"): Uses a lightweight Beats shipper to gather metrics. May be preferred if you have an existing investment in Beats or are not yet ready to use Elastic Agent. 
    * [_Legacy collection methods_](collecting-monitoring-data.html "Collecting monitoring data using legacy collectors"): Uses internal exporters to gather metrics. Not recommended. If you have previously configured legacy collection methods, you should migrate to using Elastic Agent or Metricbeat. 

* 监控木花 * 监控日志 * 监控企业搜索 * 监控节拍：

    * [Auditbeat](/guide/en/beats/auditbeat/8.9/monitoring.html)
    * [Filebeat](/guide/en/beats/filebeat/8.9/monitoring.html)
    * [Functionbeat](/guide/en/beats/functionbeat/8.9/monitoring.html)
    * [Heartbeat](/guide/en/beats/heartbeat/8.9/monitoring.html)
    * [Metricbeat](/guide/en/beats/metricbeat/8.9/monitoring.html)
    * [Packetbeat](/guide/en/beats/packetbeat/8.9/monitoring.html)
    * [Winlogbeat](/guide/en/beats/winlogbeat/8.9/monitoring.html)

* 监控 APM 服务器 * 监控弹性代理队列管理的代理)或为独立弹性代理配置监控

[« Monitoring overview](monitoring-overview.md) [Monitoring in a production
environment »](monitoring-production.md)
