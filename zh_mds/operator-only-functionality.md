

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Operator privileges](operator-
privileges.md)

[« Configure operator privileges](configure-operator-privileges.md)
[Operator privileges for snapshot and restore »](operator-only-snapshot-and-
restore.md)

## 仅运算符功能

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

操作员权限为 API 和动态群集设置提供保护。受操作员权限保护的任何 API 或集群设置都称为仅限_operator functionality_。启用操作员权限功能后，仅操作员 API 只能由操作员用户执行。同样，仅操作员设置只能由操作员用户更新。仅操作员 API 和动态群集设置的列表在代码库中预先确定。该列表可能会在未来的版本中发展，但在给定的 Elasticsearch 版本中会得到修复。

### 仅限操作员的 API

* 投票配置排除项 * 删除许可证 * 更新许可证 * 创建或更新自动缩放策略 * 删除自动缩放策略 * 存储库分析 * 创建或更新所需节点 * 获取所需节点 * 删除所需节点 * 获得所需余额 * 删除/重置所需余额

### 仅操作员动态群集设置

* 所有 IP 过滤设置 * 以下动态机器学习设置：

    * `xpack.ml.node_concurrent_job_allocations`
    * `xpack.ml.max_machine_memory_percent`
    * `xpack.ml.use_auto_machine_memory_percent`
    * `xpack.ml.max_lazy_ml_nodes`
    * `xpack.ml.process_connect_timeout`
    * `xpack.ml.nightly_maintenance_requests_per_second`
    * `xpack.ml.max_ml_node_size`
    * `xpack.ml.enable_config_migration`
    * `xpack.ml.persist_results_max_retries`

* "cluster.routing.allocation.disk.threshold_enabled"设置 * 托管服务的以下恢复设置：

    * `node.bandwidth.recovery.operator.factor`
    * `node.bandwidth.recovery.operator.factor.read`
    * `node.bandwidth.recovery.operator.factor.write`
    * `node.bandwidth.recovery.operator.factor.max_overcommit`

[« Configure operator privileges](configure-operator-privileges.md)
[Operator privileges for snapshot and restore »](operator-only-snapshot-and-
restore.md)
