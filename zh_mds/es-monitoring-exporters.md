

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md) ›[Collecting monitoring data
using legacy collectors](collecting-monitoring-data.md)

[« Collectors](es-monitoring-collectors.md) [Local exporters »](local-
exporter.md)

##Exporters

Elastic 代理和 Metricbeat 是收集监控数据并将其传送到监控集群的推荐方法。

如果您之前配置了旧版收集方法，则应迁移到使用 Elastic Agent 或 Metricbeat 收集。不要将旧收集与其他收集方法一起使用。

导出器的目的是获取从任何弹性堆栈源收集的数据，并将其路由到监控集群。可以配置多个导出器，但常规和默认设置是使用单个导出器。

Elasticsearch 中有两种类型的导出器：

`local`

     The default exporter used by Elasticsearch monitoring features. This exporter routes data back into the _same_ cluster. See [Local exporters](local-exporter.html "Local exporters"). 
`http`

     The preferred exporter, which you can use to route data into any supported Elasticsearch cluster accessible via HTTP. Production environments should always use a separate monitoring cluster. See [HTTP exporters](http-exporter.html "HTTP exporters"). 

这两个导出器具有相同的目的：设置监控集群和路由监控数据。但是，它们以非常不同的方式执行这些任务。即使事情发生不同，两个导出器也能够发送所有相同的数据。

导出器可在节点和集群级别进行配置。使用"_cluster/settings"API 更新的集群范围设置优先于每个节点上"elasticsearch.yml"文件中的设置。更新导出器时，它将完全替换为导出器的更新版本。

所有节点共享相同的设置至关重要。否则，监视数据可能会以不同的方式路由或路由到不同的位置。

当导出器将监控数据路由到监控集群时，它们使用"_bulk"索引以获得最佳性能。所有监视数据都将批量转发到同一节点上所有已启用的导出器。从那里，导出器序列化监控数据并向监控集群发送批量请求。没有队列(在内存中或持久保存到磁盘)，因此导出期间的任何故障都会导致该批监视数据丢失。这种设计限制了对 Elasticsearch 的影响，并且假设下一次传递会成功。

路由监视数据涉及将其索引到相应的监视索引中。为数据编制索引后，它就存在于监视索引中，默认情况下，该索引以每日索引模式命名。对于 Elasticsearch monitoringdata，这是一个与 '.monitoring-es-6-*' 匹配的索引。从那里，数据位于监控集群内，必须根据需要进行策划或清理。如果不整理监视数据，它最终会填满节点，并且群集可能会因磁盘空间不足而失败。

强烈建议您管理索引的管理，尤其是监控指数。为此，您可以利用 Cleaner 服务或 ElasticCurator。

还有一个磁盘水印(称为泛洪阶段水印)，可防止群集磁盘空间不足。触发此功能时，它将使所有索引(包括监视索引)为只读，直到问题得到解决并且用户手动使索引再次可写。虽然活动监视索引是只读的，但它自然无法写入(索引)新数据，并且会持续记录指示写入失败的错误。更多信息，请参见基于磁盘的分片分配设置。

#### 默认导出器

如果节点或集群未显式定义导出器，则使用以下默认导出器：

    
    
    xpack.monitoring.exporters.default_local: __type: local

__

|

导出器名称唯一定义导出器，但在其他方面未使用。指定自己的导出器时，不需要显式覆盖或引用"default_local"。   ---|--- 如果已定义另一个导出器，则创建默认导出器_not_。定义新导出器时，如果默认导出器存在，则会自动将其删除。

#### 导出器模板和引入管道

在导出者可以路由监控数据之前，他们必须设置某些 Elasticsearch 资源。这些资源包括模板和引入管道。下表列出了导出器可以路由监视数据之前所需的模板：

模板 |目的 ---|--- '.监视警报'

|

用于监视数据的所有群集警报。   ".监听节拍"

|

所有 Beats 监控数据。   '.monitoring-es'

|

所有 Elasticsearch 监控数据。   '.监控-木花'

|

所有 Kibana 监控数据。   '.监控日志'

|

所有日志存储监控数据。   这些模板是普通的 Elasticsearch 模板，用于控制监控索引的默认设置和映射。

默认情况下，监控索引是每天创建的(例如，".monitoring-es-6-2017.08.26")。您可以使用"index.name.time_format"设置更改监控索引的默认日期后缀。您可以使用此设置来控制特定"http"导出器创建监视索引的频率。您不能将此设置用于"本地"导出器。有关详细信息，请参阅 HTTP 导出器设置。

某些用户创建自己的模板，这些模板与 _all_ 索引模式匹配，因此会影响创建的监视索引。不要禁用监控索引的"_source"存储，这一点至关重要。如果这样做，Kibana 监控功能将不起作用，并且您无法可视化集群的监控数据。

下表列出了导出器可以路由监视数据之前所需的引入管道：

管道 |目的 ---|--- "xpack_monitoring_2"

|

升级来自 X-Pack 5.0 - 5.4 的 X-Pack 监控数据，使其与 5.5 监控功能中使用的格式兼容。   "xpack_monitoring_6"

|

为空的占位符管道。   导出器在发送数据之前处理这些资源的设置。如果资源设置失败(例如，由于安全权限)，则不会发送任何数据并记录警告。

在索引期间，将在协调节点上评估空管道，并且无需任何额外工作即可忽略它们。这本质上使它们成为安全的无操作操作。

对于在所有节点上禁用"node.ingest"的监控集群，可以禁用摄取管道功能的使用。但是，这样做会阻止其目的，即随着映射的改进而升级较旧的监视数据。从 6.0 开始，采集管道功能是监控集群上的一项要求;您必须在至少一个节点上启用"node.ingest"。

任何运行 5.5 或更高版本的节点在监控集群上设置模板和摄取管道后，您必须使用 Kibana 5.5 或更高版本查看监控集群上的所有后续数据。确定此更新是否已发生的最简单方法是检查是否存在与".monitoring-es-6-*"匹配的索引(或者更具体地说，是否存在新管道)。5.5 之前的版本使用".monitoring-es-2-*"。

导出器创建的每个资源都有一个"版本"字段，用于确定是否应替换资源。"版本"字段值表示更改了该源的监视功能的最新版本。如果资源由监视功能外部的某人或某些内容编辑，则下次发生自动更新时，这些更改将丢失。

[« Collectors](es-monitoring-collectors.md) [Local exporters »](local-
exporter.md)
