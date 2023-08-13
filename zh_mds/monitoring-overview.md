

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md)

[« Monitor a cluster](monitor-elasticsearch-cluster.md) [How monitoring
works »](how-monitoring-works.md)

## 监控概述

监控集群时，您需要从集群中的 Elasticsearch 节点、Logstash 节点、Kibana 实例、企业级搜索、APM 服务器和 Beats 收集数据。您还可以收集日志。

所有监控指标都存储在 Elasticsearch 中，使您能够轻松地在 Kibana 中可视化数据。默认情况下，监控指标在本地索引中恢复。

在生产中，我们强烈建议使用单独的监视群集。使用单独的监控集群可防止生产集群中断影响您访问监控数据的能力。它还可以防止监视活动影响生产群集的性能。出于同样的原因，我们还建议使用单独的 Kibanainstance 来查看监控数据。

您可以使用 Elastic 代理或 Metricbeat 收集数据并将其直接传送到监控集群，而不是通过生产集群进行路由。

下图说明了具有独立生产和监视群集的典型监视体系结构。此示例显示了 Metricbeat，但您可以改用弹性代理。

!典型的监控环境

如果您拥有适当的许可证，则可以将数据从多个生产集群路由到单个监控集群。有关不同订阅级别之间的差异的详细信息，请参阅：https：//www.elastic.co/subscriptions

通常，监控集群和被监控集群应运行相同版本的堆栈。监控集群无法监控运行较新版本堆栈的生产集群。如有必要，监控集群可以监控运行以前主要版本的最新版本的生产集群。

[« Monitor a cluster](monitor-elasticsearch-cluster.md) [How monitoring
works »](how-monitoring-works.md)
