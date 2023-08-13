

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Operator privileges](operator-
privileges.md)

[« Operator-only functionality](operator-only-functionality.md)
[Troubleshooting security »](security-troubleshooting.md)

## 快照和还原的操作员权限

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

调用仅限操作员的 API 或更新仅限操作员的动态群集设置通常会导致群集状态发生更改。群集状态可以包含在群集快照中。快照是保留集群数据的好方法，例如，稍后可以将其还原以引导新集群、执行迁移或灾难恢复。在传统的自我管理环境中，目的是让还原过程在请求时复制整个群集状态。但是，在更多托管环境(如 ElasticsearchService)中，与仅操作员功能关联的数据由基础结构代码显式管理。

还原与仅操作员功能关联的快照数据可能会出现问题，因为：

1. 快照可能包含仅限操作员的功能的不正确值。例如，快照可能是在要求不同或未启用操作员权限功能的不同集群中拍摄的。还原与仅操作员功能关联的数据会破坏操作员权限的保证。  2. 即使基础结构代码可以在还原后立即更正值，也总会在短时间内群集处于不一致状态。  3. 基础结构代码倾向于从单个位置(即通过 API 调用)配置仅限操作员的功能。

因此，启用操作员权限功能后，不会还原与任何仅操作员功能关联的快照数据。

拍摄快照时仍包含该信息，以便始终保留所有数据。

[« Operator-only functionality](operator-only-functionality.md)
[Troubleshooting security »](security-troubleshooting.md)
