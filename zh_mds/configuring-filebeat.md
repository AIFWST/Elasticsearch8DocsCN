

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md)

[« Collecting Elasticsearch monitoring data with Metricbeat](configuring-
metricbeat.md) [Configuring data streams/indices for monitoring »](config-
monitoring-indices.md)

## 使用 Filebeat 收集 Elasticsearch 日志数据

您可以使用 Filebeat 监控 Elasticsearch 日志文件，收集日志事件，并将其传送到监控集群。您最近的日志显示在 Kibana 的"**监控**"页面上。

如果您使用的是弹性代理，请不要部署 Filebeat 进行日志收集。相反，请配置 Elasticsearch 集成以收集日志。

1. 验证 Elasticsearch 是否正在运行，以及监控集群是否已准备好从 Filebeat 接收数据。

在生产环境中，我们强烈建议使用单独的集群(称为_monitoring cluster_)来存储数据。使用单独的监控集群可防止生产集群中断影响您访问监控数据的能力。它还可以防止监视活动影响生产群集的性能。请参阅_Monitoring生产environment_。

2. 确定要监视的日志。

Filebeat Elasticsearch 模块可以处理审计日志、弃用日志、gclogs、服务器日志和慢日志。有关 Elasticsearchlogs 位置的更多信息，请参阅 path.logs 设置。

如果日志同时存在结构化("*.json")和非结构化(纯文本)版本，则必须使用结构化日志。否则，它们可能不会出现在 Kibana 的相应上下文中。

3. 在包含要监控的日志的 Elasticsearch 节点上安装 Filebeat。  4. 确定将日志数据发送到何处。

例如，在 Filebeat 配置文件 ('filebeat.yml') 中指定监控集群的 Elasticsearch 输出信息：

    
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

如果在监控集群上启用了 Elasticsearch 安全功能，您必须提供有效的用户 ID 和密码，Filebeat 才能成功发送指标。

有关这些配置选项的更多信息，请参阅配置 Elasticsearch 输出。

5. 可选：确定可视化数据的位置。

Filebeat 提供了示例 Kibana 仪表板、可视化和搜索。要将仪表板加载到相应的 Kibana 实例中，请在每个节点上的 Filebeat 配置文件 ('filebeat.yml') 中指定"setup.kibana"信息：

    
        setup.kibana:
      host: "localhost:5601"
      #username: "my_kibana_user"
      #password: "YOUR_PASSWORD"

在生产环境中，我们强烈建议为您的监控集群使用专用的 Kibanainstance。

如果启用了安全功能，那么必须提供有效的用户 ID 和密码，以便 Filebeat 可以连接到 Kibana：

    1. Create a user on the monitoring cluster that has the [`kibana_admin` built-in role](built-in-roles.html "Built-in roles") or equivalent privileges. 
    2. Add the `username` and `password` settings to the Elasticsearch output information in the Filebeat configuration file. The example shows a hard-coded password, but you should store sensitive values in the [secrets keystore](/guide/en/beats/filebeat/8.9/keystore.html). 

请参阅配置 Kibana 端点。

6. 启用 Elasticsearch 模块，并在每个节点上设置初始 Filebeat 环境。

例如：

    
        filebeat modules enable elasticsearch
    filebeat setup -e

有关更多信息，请参阅 Elasticsearchmodule。

7. 在每个节点上的 Filebeat 中配置 Elasticsearch 模块。

如果要监视的日志不在默认位置，请在"modules.d/elasticsearch.yml"文件中设置适当的路径变量。请参阅配置 Elasticsearch 模块。

如果有 JSON 日志，请将"var.paths"设置配置为指向它们而不是纯文本日志。

8. 在每个节点上启动文件节拍。

根据安装 Filebeat 的方式，在尝试运行 Filebeat 模块时，可能会看到与文件所有权或权限相关的错误。请参阅配置文件所有权和权限。

9. 检查监控集群上是否存在相应的索引。

例如，使用 cat 索引命令验证是否存在新的"filebeat-*"索引。

如果要在 Kibana 中使用 **Monitoring** UI，还必须有 '.monitoring-*' 索引。这些索引是在收集有关 Elastic Stack 产品的指标时生成的。例如，请参阅使用 Metricbeat_ _Collecting监控数据。

10. 查看木花中的监控数据。

[« Collecting Elasticsearch monitoring data with Metricbeat](configuring-
metricbeat.md) [Configuring data streams/indices for monitoring »](config-
monitoring-indices.md)
