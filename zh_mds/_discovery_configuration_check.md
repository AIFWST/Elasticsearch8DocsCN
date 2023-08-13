

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« All permission check](_all_permission_check.md) [Bootstrap Checks for
X-Pack »](bootstrap-checks-xpack.md)

## 发现配置检查

默认情况下，当 Elasticsearch 首次启动时，它将尝试发现在同一主机上运行的其他节点。如果在几秒钟内无法发现选定的主节点，那么 Elasticsearch 将形成一个集群，其中包含发现的任何其他节点。能够在开发模式下无需任何额外配置即可形成此群集很有用，但这不适合生产，因为可能会形成多个群集并因此丢失数据。

此引导程序检查可确保发现未使用默认配置运行。可以通过设置以下至少一个属性来满足它：

* "discovery.seed_hosts" * "discovery.seed_providers" * "cluster.initial_master_nodes"

请注意，您应该在集群首次启动后从配置中删除"cluster.initial_master_nodes"。重新启动节点或向现有群集添加新节点时，请勿使用此设置。相反，请配置"discovery.seed_hosts"或"discovery.seed_providers"。如果不需要任何发现配置，例如，如果运行单节点群集，请设置"discovery.seed_hosts： []"以禁用发现并满足此引导程序检查。

[« All permission check](_all_permission_check.md) [Bootstrap Checks for
X-Pack »](bootstrap-checks-xpack.md)
