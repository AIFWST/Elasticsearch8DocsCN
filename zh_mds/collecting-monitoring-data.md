

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md)

[« Configuring indices created by Metricbeat 7 or internal collection](config-
monitoring-indices-metricbeat-7-internal-collection.md) [Collectors »](es-
monitoring-collectors.md)

## 使用旧版收集器收集监视数据

### 在 7.16 中已弃用。

不推荐使用 Elasticsearch 监控插件来收集和发送监控数据。Elastic 代理和 Metricbeat 是收集监控数据并将其传送到监控集群的推荐方法。如果您之前配置了旧版收集方法，则应迁移到使用 Elastic 代理或 Metricbeatcollection 方法。

这种收集有关 Elasticsearch 指标的方法涉及使用导出器将指标发送到监控集群。

通过高级监控设置，您可以控制收集数据的频率、配置超时以及设置本地存储的监控索引的保留期。您还可以调整监控数据的显示方式。

若要了解一般监视，请参阅监视群集。

1. 配置集群以收集监控数据：

    1. Verify that the `xpack.monitoring.elasticsearch.collection.enabled` setting is `true`, which is its default value, on each node in the cluster.

您可以在每个节点上的"elasticsearch.yml"中指定此设置，也可以在整个集群中将此设置指定为动态集群设置。如果启用了 Elasticsearch 安全功能，您必须具有"监控"集群权限才能查看集群设置，并具有"管理"集群权限才能更改它们。

有关详细信息，请参阅监视设置和群集更新设置。

    2. Set the `xpack.monitoring.collection.enabled` setting to `true` on each node in the cluster. By default, it is disabled (`false`).

您可以在每个节点上的"elasticsearch.yml"中指定此设置，也可以在整个集群中将此设置指定为动态集群设置。如果启用了 Elasticsearch 安全功能，您必须具有"监控"集群权限才能查看集群设置，并具有"管理"集群权限才能更改它们。

例如，使用以下 API 查看和更改此设置：

        
                response = client.cluster.get_settings
        puts response
        
                GET _cluster/settings
        
                response = client.cluster.put_settings(
          body: {
            persistent: {
              "xpack.monitoring.collection.enabled": true
            }
          }
        )
        puts response
        
                PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": true
          }
        }

或者，您也可以在 Kibana 中启用此设置。在侧边导航中，单击"**监视**"。如果禁用了数据收集，系统会提示您打开它。

有关详细信息，请参阅监视设置和群集更新设置。

    3. Optional: Specify which indices you want to monitor.

默认情况下，监控代理从所有 Elasticsearch 索引中收集数据。要从特定索引收集数据，请配置"xpack.monitoring.collection.index"设置。您可以将多个索引指定为逗号分隔的列表，也可以使用索引模式来匹配多个索引。例如：

        
                xpack.monitoring.collection.indices: logstash-*, index1, test2

可以在前面加上"-"以显式排除索引名称或模式。例如，要包含除"test3"之外的所有以"test"开头的索引，您可以指定"test*，-test3"。要包含 .security 和 .kibana 等系统索引，请将".*"添加到包含的名称列表中。例如".*，测试*，-test3"

    4. Optional: Specify how often to collect monitoring data. The default value for the `xpack.monitoring.collection.interval` setting 10 seconds. See [Monitoring settings](monitoring-settings.html "Monitoring settings in Elasticsearch"). 

2. 确定存储监视数据的位置。

默认情况下，使用"本地"导出器将数据存储在同一群集上。或者，您可以使用"http"导出器将数据发送到单独的_monitoring cluster_。

Elasticsearch 监控功能使用采集管道，因此存储监控数据的集群必须至少有一个采集节点。

有关典型监视体系结构的详细信息，请参阅_How itworks_。

3. 如果您选择使用"http"导出器：

    1. On the cluster that you want to monitor (often called the _production cluster_ ), configure each node to send metrics to your monitoring cluster. Configure an HTTP exporter in the `xpack.monitoring.exporters` settings in the `elasticsearch.yml` file. For example:
        
                xpack.monitoring.exporters:
          id1:
            type: http
            host: ["http://es-mon-1:9200", "http://es-mon-2:9200"]

    2. If the Elastic security features are enabled on the monitoring cluster, you must provide appropriate credentials when data is shipped to the monitoring cluster:

      1. Create a user on the monitoring cluster that has the [`remote_monitoring_agent` built-in role](built-in-roles.html "Built-in roles"). Alternatively, use the [`remote_monitoring_user` built-in user](built-in-users.html "Built-in users"). 
      2. Add the user ID and password settings to the HTTP exporter settings in the `elasticsearch.yml` file and keystore on each node.  

例如：

            
                        xpack.monitoring.exporters:
              id1:
                type: http
                host: ["http://es-mon-1:9200", "http://es-mon-2:9200"]
                auth.username: remote_monitoring_user
                # "xpack.monitoring.exporters.id1.auth.secure_password" must be set in the keystore

    3. If you configured the monitoring cluster to use [encrypted communications](security-basic-setup.html#encrypt-internode-communication "Encrypt internode communications with TLS"), you must use the HTTPS protocol in the `host` setting. You must also specify the trusted CA certificates that will be used to verify the identity of the nodes in the monitoring cluster.

      * To add a CA certificate to an Elasticsearch node's trusted certificates, you can specify the location of the PEM encoded certificate with the `certificate_authorities` setting. For example:
            
                        xpack.monitoring.exporters:
              id1:
                type: http
                host: ["https://es-mon1:9200", "https://es-mon-2:9200"]
                auth:
                  username: remote_monitoring_user
                  # "xpack.monitoring.exporters.id1.auth.secure_password" must be set in the keystore
                ssl:
                  certificate_authorities: [ "/path/to/ca.crt" ]

      * Alternatively, you can configure trusted certificates using a truststore (a Java Keystore file that contains the certificates). For example:
            
                        xpack.monitoring.exporters:
              id1:
                type: http
                host: ["https://es-mon1:9200", "https://es-mon-2:9200"]
                auth:
                  username: remote_monitoring_user
                  # "xpack.monitoring.exporters.id1.auth.secure_password" must be set in the keystore
                ssl:
                  truststore.path: /path/to/file
                  truststore.password: password

4. 配置集群以将监控数据从 Kibana、Beats 和 Logstash 等源路由到监控集群。有关配置每个产品以收集和发送监控数据的信息，请参阅监控集群。  5. 如果您更新了生产集群上"elasticsearch.yml"文件中的设置，请重新启动 Elasticsearch。请参阅_Stopping Elasticsearch_和_Starting Elasticsearch_。

您可能希望在重新启动节点之前暂时禁用分片分配，以避免在安装过程中不必要的分片重新分配。

6. 可选：配置存储监控数据的索引。  7. 查看木花中的监控数据。

[« Configuring indices created by Metricbeat 7 or internal collection](config-
monitoring-indices-metricbeat-7-internal-collection.md) [Collectors »](es-
monitoring-collectors.md)
