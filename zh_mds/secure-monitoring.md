

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Securing clients and
integrations](security-clients-integrations.md)

[« ES-Hadoop and Security](hadoop.md) [Operator privileges »](operator-
privileges.md)

## 监控和安全

Elastic Stack 监控功能由两个组件组成：一个安装在每个 Elasticsearch 和 Logstash 节点上的代理，以及 Kibana 中的监控 UI。监控代理从节点收集指标并为其编制索引，您可以通过 Kibana 中的监控仪表板可视化数据。代理可以索引同一 Elasticsearch 集群上的数据，或将其发送到外部监控集群。

要在启用安全功能的情况下使用监控功能，您需要设置 Kibana 以使用安全功能，并为监控 UI 创建至少一个用户。如果您使用的是外部监控集群，则还需要为监控代理配置用户，并将代理配置为在与监控集群通信时使用适当的凭据。

有关详细信息，请参阅：

* 在生产environment_中_Monitoring * 在 Kibana 中配置监控 * 配置日志节点监控

[« ES-Hadoop and Security](hadoop.md) [Operator privileges »](operator-
privileges.md)
