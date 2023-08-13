

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md)

[« Monitoring in a production environment](monitoring-production.md)
[Collecting Elasticsearch monitoring data with Metricbeat »](configuring-
metricbeat.md)

## 使用 ElasticAgent 收集 Elasticsearch 监控数据

在 8.5 及更高版本中，您可以使用 Elastic 代理收集有关 Elasticsearch 的数据并将其传送到监控集群，而不是按照收集methods_in_Legacy中所述使用 Metricbeat 或通过导出器路由数据。

###Prerequisites

*(可选)按照在生产environment_中_Monitoring中所述创建监控集群。  * 在具有"remote_monitoring_collector"内置角色的生产群集上创建一个用户。

### 添加弹性搜索监控数据

要收集 Elasticsearch 监控数据，请将 Elasticsearch 集成添加到 Elastic 代理，并将其部署到运行 Elasticsearch 的主机上。

1. 转到 Kibana 主页，然后单击"添加集成**"。  2. 在查询栏中，搜索并选择弹性代理的 **弹性搜索** 集成。  3. 阅读概述，确保您了解集成要求和其他注意事项。  4. 单击"添加弹性搜索"。

如果您是首次安装集成，系统可能会提示您安装 Elastic 代理。单击**仅添加集成(跳过代理安装)**。

5. 配置集成名称并选择性地添加描述。确保配置所有必需的设置：

    1. Under **Collect Elasticsearch logs** , modify the log paths to match your Elasticsearch environment. 
    2. Under **Collect Elasticsearch metrics** , make sure the hosts setting points to your Elasticsearch host URLs. By default, the integration collects Elasticsearch monitoring metrics from `localhost:9200`. If that host and port number are not correct, update the `hosts` setting. If you configured Elasticsearch to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://localhost:9200`. 
    3. Expand **Advanced options**. If the Elastic security features are enabled, enter the username and password of a user that has the `remote_monitoring_collector` role. 
    4. Specify the scope:

      * Specify `cluster` if each entry in the hosts list indicates a single endpoint for a distinct Elasticsearch cluster (for example, a load-balancing proxy fronting the cluster that directs requests to the master-ineligible nodes in the cluster). 
      * Otherwise, accept the default scope, `node`. If this scope is set, you will need to install Elastic Agent on each Elasticsearch node to collect all metrics. Elastic Agent will collect most of the metrics from the elected master of the cluster, so you must scale up all your master-eligible nodes to account for this extra load. Do not use this `node` if you have dedicated master nodes. 

6. 选择添加集成策略的位置。单击"**新主机**"将其添加到新的代理策略，或单击"现有主机**"将其添加到现有代理策略。  7. 单击**保存并继续**。此步骤需要一两分钟才能完成。完成后，您将拥有一个代理策略，其中包含用于从 Elasticsearch 收集监控数据的集成。  8. 如果弹性代理已分配给策略并部署到运行 Elasticsearch 的主机，则您已完成操作。否则，您需要部署弹性代理。要部署弹性代理，请执行以下操作：

    1. Go to **Fleet -> Agents**, then click **Add agent**. 
    2. Follow the steps in the **Add agent** flyout to download, install, and enroll the Elastic Agent. Make sure you choose the agent policy you created earlier. 

9. 等待一两分钟，直到确认传入数据。  10. 查看木花中的监控数据。

[« Monitoring in a production environment](monitoring-production.md)
[Collecting Elasticsearch monitoring data with Metricbeat »](configuring-
metricbeat.md)
