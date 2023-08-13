

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md)

[« How monitoring works](how-monitoring-works.md) [Collecting Elasticsearch
monitoring data with Elastic Agent »](configuring-elastic-agent.md)

## 生产环境中的监控

在生产中，您应该将监视数据发送到单独的 _monitoringcluster_，以便即使正在监视的节点不可用，也可以使用历史数据。

Elastic 代理和 Metricbeat 是收集监控数据并将其传送到监控集群的推荐方法。

如果您之前配置了旧版收集方法，则应迁移到使用 Elastic Agent 或 Metricbeat 收集。不要将旧收集与其他收集方法一起使用。

如果您至少拥有黄金订阅，则使用专用监控集群还可以从一个中心位置监控多个集群。

要将监控数据存储在单独的集群中，请执行以下操作：

1. 设置要用作监控集群的 Elasticsearch 集群。例如，您可以使用节点"es-mon-1"和"es-mon-2"设置两个主机群集。

    * Ideally the monitoring cluster and the production cluster run on the same Elastic Stack version. However, a monitoring cluster on the latest release of 8.x also works with production clusters that use the same major version. Monitoring clusters that use 8.x also work with production clusters that use the latest release of 7.x. 
    * There must be at least one [ingest node](ingest.html "Ingest pipelines") in the monitoring cluster; it does not need to be a dedicated ingest node. 

    1. (Optional) Verify that the collection of monitoring data is disabled on the monitoring cluster. By default, the `xpack.monitoring.collection.enabled` setting is `false`.

例如，可以使用以下 API 查看和更改此设置：

        
                response = client.cluster.get_settings
        puts response
        
        response = client.cluster.put_settings(
          body: {
            persistent: {
              "xpack.monitoring.collection.enabled": false
            }
          }
        )
        puts response
        
                GET _cluster/settings
        
        PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": false
          }
        }

    2. If the Elasticsearch security features are enabled on the monitoring cluster, create users that can send and retrieve monitoring data:

如果您计划使用 Kibana 查看监控数据，用户名和密码凭据必须在 Kibana 服务器和监控集群上都有效。

      * If you plan to use Elastic Agent, create a user that has the `remote_monitoring_collector` [built-in role](built-in-roles.html#built-in-roles-remote-monitoring-agent). 
      * If you plan to use Metricbeat, create a user that has the `remote_monitoring_collector` built-in role and a user that has the `remote_monitoring_agent` [built-in role](built-in-roles.html#built-in-roles-remote-monitoring-agent). Alternatively, use the `remote_monitoring_user` [built-in user](built-in-users.html "Built-in users"). 
      * If you plan to use HTTP exporters to route data through your production cluster, create a user that has the `remote_monitoring_agent` [built-in role](built-in-roles.html#built-in-roles-remote-monitoring-agent).

例如，以下请求创建具有"remote_monitoring_agent"角色的"remote_monitor"用户：

            
                        POST /_security/user/remote_monitor
            {
              "password" : "changeme",
              "roles" : [ "remote_monitoring_agent"],
              "full_name" : "Internal Agent For Remote Monitoring"
            }

或者，使用"remote_monitoring_user"内置用户。

2. 配置生产集群以收集数据并将其发送到监控集群：

    * [Elastic Agent collection methods](configuring-elastic-agent.html "Collecting Elasticsearch monitoring data with Elastic Agent")
    * [Metricbeat collection methods](configuring-metricbeat.html "Collecting Elasticsearch monitoring data with Metricbeat")
    * [Legacy collection methods](collecting-monitoring-data.html "Collecting monitoring data using legacy collectors")

3. (可选)配置 Logstash 以收集数据并将其发送到监控集群。  4. (可选)配置企业级搜索监视。  5. (可选)配置 Beats 以收集数据并将其发送到监控集群。对于由弹性代理管理的 Beat，请跳过此步骤。

    * [Auditbeat](/guide/en/beats/auditbeat/8.9/monitoring.html)
    * [Filebeat](/guide/en/beats/filebeat/8.9/monitoring.html)
    * [Heartbeat](/guide/en/beats/heartbeat/8.9/monitoring.html)
    * [Metricbeat](/guide/en/beats/metricbeat/8.9/monitoring.html)
    * [Packetbeat](/guide/en/beats/packetbeat/8.9/monitoring.html)
    * [Winlogbeat](/guide/en/beats/winlogbeat/8.9/monitoring.html)

6. (可选)配置 APM 服务器监控 7.(可选)配置 Kibana 以收集数据并将其发送到监控集群：

    * [Elastic Agent collection methods](/guide/en/kibana/8.9/monitoring-elastic-agent.html)
    * [Metricbeat collection methods](/guide/en/kibana/8.9/monitoring-metricbeat.html)
    * [Legacy collection methods](/guide/en/kibana/8.9/monitoring-kibana.html)

8. (可选)创建用于监控的专用 Kibana 实例，而不是使用单个 Kibana 实例来访问生产集群和监控集群。

如果您使用 SAML、Kerberos、PKI、OpenID Connect 或令牌身份验证提供程序登录 Kibana，则需要专用的 Kibana 实例。在这些上下文中使用的安全令牌是特定于集群的;因此您不能使用单个 Kibana 实例同时连接到生产集群和监控集群。

    1. (Optional) Disable the collection of monitoring data in this Kibana instance. Set the `xpack.monitoring.kibana.collection.enabled` setting to `false` in the `kibana.yml` file. For more information about this setting, see [Monitoring settings in Kibana](/guide/en/kibana/8.9/monitoring-settings-kb.html). 

9. 配置 Kibana 以检索和显示监控数据。

[« How monitoring works](how-monitoring-works.md) [Collecting Elasticsearch
monitoring data with Elastic Agent »](configuring-elastic-agent.md)
