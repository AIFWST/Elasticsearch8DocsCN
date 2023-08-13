

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md) ›[Collecting monitoring data
using legacy collectors](collecting-monitoring-data.md)

[« Collecting monitoring data using legacy collectors](collecting-monitoring-
data.md) [Exporters »](es-monitoring-exporters.md)

##Collectors

Elastic 代理和 Metricbeat 是收集监控数据并将其传送到监控集群的推荐方法。

如果您之前配置了旧版收集方法，则应迁移到使用 Elastic Agent 或 Metricbeat 收集。不要将旧收集与其他收集方法一起使用。

收藏家，顾名思义，收集东西。每个收集器在每个收集间隔运行一次，以从它选择监控的Elasticsearch和X-Pack中的公共API获取数据。数据收集完成后，数据将批量移交给导出器，以发送到监控集群。无论导出器的数量如何，每个收集器在每个收集间隔中仅运行一次。

每种收集的数据类型只有一个收集器。换句话说，对于创建的任何监视文档，它来自单个收集器，而不是从多个收集器合并。Elasticsearch 监控功能目前有一些收集器，因为目标是最大限度地减少它们之间的重叠以获得最佳性能。

每个收集器可以创建零个或多个监视文档。例如，"index_stats"收集器同时收集所有索引统计信息，以避免许多不必要的调用。

收藏家 |数据类型 |描述 ---|---|--- 集群统计信息

|

`cluster_stats`

|

收集有关群集状态的详细信息，包括实际群集状态的部分内容(例如"GET /_cluster/state")和有关它的统计信息(例如，"GET /_cluster/stats")。这将生成单个文档类型。在 X-Pack 5.5 之前的反转中，这实际上是三个独立的收集器，产生了三种不同的类型："cluster_stats"、"cluster_state"和"cluster_info"。在 5.5 及更高版本中，这三者都合并为"cluster_stats"。这仅在 _elected_ 主节点上运行，收集的数据('cluster_stats')在很大程度上控制着 UI。当此数据不存在时，它表示所选主节点上的配置错误、与数据收集相关的超时或存储数据的问题。每个集合仅生成一个文档。   指数统计

|

"indices_stats"、"index_stats"

|

以摘要和单独方式收集有关群集中索引的详细信息。这将创建许多表示索引统计输出部分的文档(例如，"GET /_stats")。此信息只需要收集一次，因此在 _elected_ 主节点上收集。此收集器最常见的故障与索引数量过多有关，因此需要时间收集索引，从而导致超时。每个馆藏生成一个摘要indices_stats"文档，每个馆藏每个索引生成一个"index_stats"文档。   索引恢复

|

`index_recovery`

|

收集有关群集中索引恢复的详细信息。索引恢复表示在集群级别分配 _shards_。如果索引未恢复，则无法使用。这也对应于通过快照进行分片恢复。此信息只需要收集一次，因此the_elected_主节点上收集。此收集器最常见的故障与极多的分片有关 - 因此收集它们的时间 - 导致超时。这将创建一个包含默认情况下所有恢复的文档，该文档可能非常大，但它提供了生产群集中恢复的最准确情况。   碎片

|

`shards`

|

收集有关所有索引的所有 _已分配_ 分片的详细信息，特别是包括分片分配给哪个节点。此信息只需要收集一次，因此在 _elected_ 主节点上收集。与大多数其他收集器不同，收集器使用本地群集状态来获取路由表，而不会出现任何网络超时问题。每个分片由一个单独的监控文档表示。   工作

|

`job_stats`

|

收集有关所有机器学习作业统计信息的详细信息(例如，"GET/_ml/anomaly_detectors/_stats")。此信息只需要收集一次，因此在 _elected_ 主节点上收集。但是，为了使主节点能够执行收集，主节点必须将"xpack.ml.enabled"设置为 true(默认)并支持机器学习的许可证级别。   节点统计

|

`node_stats`

|

收集有关正在运行的节点的详细信息，例如内存利用率和 CPU 使用率(例如，"GET /_nodes/_local/stats")。这在启用了监视功能的_every_节点上运行。一个常见的故障会导致节点统计信息请求由于段文件过多而超时。因此，收集器花费太多时间等待文件系统统计信息的计算，直到它最终超时。每个集合创建一个"node_stats"文档。这是按节点收集的，以帮助发现节点相互通信的问题，而不是与监控集群通信的问题(例如，间歇性网络问题或内存压力)。   Elasticsearch 监控功能使用单线程调度程序来运行每个节点上所有适当的收集器收集的 Elasticsearch 监控数据。此调度程序由每个节点在本地管理，其间隔通过在节点或集群级别指定"xpack.monitoring.collection.interval"来控制，默认为 10 秒("10s")。

从根本上说，每个收集器都遵循相同的原理。每个收集间隔，检查每个收集器以查看它是否应运行，然后运行相应的收集器。单个收集器的故障不会影响任何其他收集器。

收集完成后，所有监控数据都将传递给导出器，以将监控数据路由到监控集群。

如果 Kibana 中的监控图表中存在间隙，通常是因为收集器出现故障或监控集群未收到数据(例如，正在重新启动)。如果收集器发生故障，则尝试执行收集的节点上应存在记录错误。

收集当前是串行完成的，而不是并行完成的，以避免在选定的主节点上产生额外的开销。此方法的缺点是收集器可能会在同一收集周期内观察到不同版本的群集状态。实际上，这不会产生重大差异，并行运行收集器不会阻止这种可能性。

有关收集器的配置选项的详细信息，请参阅监视收集器设置。

##### 从 ElasticStack 中收集数据

Elasticsearch 监控功能还可以从 Elastic Stack 的其他部分接收监控数据。通过这种方式，它充当堆栈的计划外监视数据收集器。

默认情况下，数据收集处于禁用状态。不会收集 Elasticsearch 监控数据，并且忽略来自其他来源(如 Kibana、Beats 和 Logstash)的所有监控数据。您必须将"xpack.monitoring.collection.enabled"设置为"true"才能启用监控数据的收集。请参阅监视设置。

收到数据后，将转发给导出器，以便像所有监控数据一样路由到监控集群。

由于此堆栈级"收集器"位于 Elasticsearch 监控功能的收集间隔之外，因此它不受"xpack.monitoring.collection.interval"设置的影响。因此，只要收到数据，就会将其传递给出口商。此行为可能会导致意外创建 Kibana、Logstash 或 Beats 的索引。

在收集和处理监视数据时，会将一些生产群集元数据添加到传入文档中。此元数据使 Kibana 能够将监控数据链接到相应的集群。如果此链接对于您正在监视的基础结构不重要，则配置 Logstash 和 Beats 以将监视数据直接报告给监视群集可能更简单。此方案还可以防止生产群集增加与监视数据相关的额外开销，这在存在大量 Logstash 节点或 Beats 时非常有用。

有关典型监视体系结构的详细信息，请参阅_How itworks_。

[« Collecting monitoring data using legacy collectors](collecting-monitoring-
data.md) [Exporters »](es-monitoring-exporters.md)
