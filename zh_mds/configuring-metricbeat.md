

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md)

[« Collecting Elasticsearch monitoring data with Elastic Agent](configuring-
elastic-agent.md) [Collecting Elasticsearch log data with Filebeat
»](configuring-filebeat.md)

## 使用 Metricbeat 收集 Elasticsearch 监控数据

在 6.5 及更高版本中，您可以使用 Metricbeat 收集有关 Elasticsearch 的数据并将其发送到监控集群，而不是像_Legacy收集methods_中所述通过导出器路由数据。

想要改用弹性代理？请参阅使用弹性Agent__Collecting监控数据。

!示例监视体系结构

1. 安装指标节拍。理想情况下，安装配置了"scope：cluster"的单个 Metricbeat 实例，并将"主机"配置为指向端点(例如负载平衡代理)，该端点将请求定向到集群中不符合主节点条件的节点。如果无法做到这一点，则为生产集群中的每个 Elasticsearch 节点安装一个 Metricbeat 实例，并使用默认的"scope： node"。当 Metricbeat 使用 'scope： node' 监控 Elasticsearch 时，您必须为每个 Elasticsearch 节点安装一个 Metricbeat 实例。否则，将不会收集某些指标。具有"scope： node"的 Metricbeat 从集群的选定主节点收集大部分指标，因此您必须纵向扩展所有符合主节点条件的节点以应对此额外负载，如果您有专用主节点，则不应使用此模式。  2. 在每个 Elasticsearch 节点上启用 Metricbeat 中的 Elasticsearch 模块。

例如，要在"modules.d"目录中启用弹性堆栈监控功能的默认配置，请运行以下命令：

    
        metricbeat modules enable elasticsearch-xpack

有关更多信息，请参阅 Elasticsearchmodule。

3. 在每个 Elasticsearch 节点上的 Metricbeat 中配置 Elasticsearch 模块。

'modules.d/elasticsearch-xpack.yml' 文件包含以下设置：

    
          - module: elasticsearch
        xpack.enabled: true
        period: 10s
        hosts: ["http://localhost:9200"] __#scope: node __#username: "user"
        #password: "secret"
        #ssl.enabled: true
        #ssl.certificate_authorities: ["/etc/pki/root/ca.pem"]
        #ssl.certificate: "/etc/pki/client/cert.pem"
        #ssl.key: "/etc/pki/client/cert.key"
        #ssl.verification_mode: "full"

__

|

默认情况下，该模块从'http：//localhost：9200'收集Elasticsearch监控指标。如果该主机和端口号不正确，则必须更新"主机"设置。如果您将 Elasticsearch 配置为使用加密通信，则必须通过 HTTPS 访问它。例如，使用"主机"设置，如"https://localhost:9200"。   ---|---    __

|

默认情况下，"scope"设置为"node"，"hosts"列表中的每个条目都表示 Elasticsearch 集群中的一个不同节点。如果将"scope"设置为"cluster"，则"hosts"列表中的每个条目都表示不同 Elasticsearch 集群的单个端点(例如，集群前面的负载均衡代理)。如果集群具有专用主节点，则应使用"scope：cluster"，并在"hosts"列表中将端点配置为不将请求定向到专用主节点。   如果启用了 Elastic 安全功能，您还必须提供用户 ID 和密码，以便 Metricbeat 可以成功收集指标：

    1. Create a user on the production cluster that has the [`remote_monitoring_collector` built-in role](built-in-roles.html "Built-in roles"). Alternatively, use the [`remote_monitoring_user` built-in user](built-in-users.html "Built-in users"). 
    2. Add the `username` and `password` settings to the Elasticsearch module configuration file. 
    3. If TLS is enabled on the HTTP layer of your Elasticsearch cluster, you must either use https as the URL scheme in the `hosts` setting or add the `ssl.enabled: true` setting. Depending on the TLS configuration of your Elasticsearch cluster, you might also need to specify [additional ssl.*](/guide/en/beats/metricbeat/8.9/configuration-ssl.html) settings. 

4. 可选：禁用 Metricbeat 中的系统模块。

默认情况下，系统模块处于启用状态。但是，它收集的信息不会显示在 Kibana 的"**监视**"页面上。除非您要将该信息用于其他目的，否则请运行以下命令：

    
        metricbeat modules disable system

5. 确定将监视数据发送到何处。

在生产环境中，我们强烈建议使用单独的集群(称为_monitoring cluster_)来存储数据。使用单独的监控集群可防止生产集群中断影响您访问监控数据的能力。它还可以防止监视活动影响生产群集的性能。

例如，在 Metricbeatconfiguration 文件 ('metricbeat.yml') 中指定 Elasticsearch 输出信息：

    
        output.elasticsearch:
      # Array of hosts to connect to.
      hosts: ["http://es-mon-1:9200", "http://es-mon-2:9200"] __# Optional protocol and basic auth credentials.
      #protocol: "https"
      #username: "elastic"
      #password: "changeme"

__

|

在此示例中，数据存储在节点为"es-mon-1"和"es-mon-2"的监控集群上。   ---|--- 如果将监控集群配置为使用加密通信，则必须通过 HTTPS 访问它。例如，使用"主机"设置，如"https://es-mon-1:9200"。

Elasticsearch 监控功能使用采集管道，因此存储监控数据的集群必须至少有一个采集节点。

如果在监控集群上启用了 Elasticsearch 安全功能，您必须提供有效的用户 ID 和密码，以便 Metricbeat 可以成功发送指标：

    1. Create a user on the monitoring cluster that has the [`remote_monitoring_agent` built-in role](built-in-roles.html "Built-in roles"). Alternatively, use the [`remote_monitoring_user` built-in user](built-in-users.html "Built-in users"). 
    2. Add the `username` and `password` settings to the Elasticsearch output information in the Metricbeat configuration file. 

有关这些配置选项的更多信息，请参阅配置 Elasticsearch 输出。

6. 在每个节点上启动指标节拍。  7. 查看木花中的监控数据。

[« Collecting Elasticsearch monitoring data with Elastic Agent](configuring-
elastic-agent.md) [Collecting Elasticsearch log data with Filebeat
»](configuring-filebeat.md)
