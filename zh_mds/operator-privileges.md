

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« Monitoring and security](secure-monitoring.md) [Configure operator
privileges »](configure-operator-privileges.md)

## 运算符权限

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

在典型的 Elasticsearch 部署中，管理集群的人员也在基础架构级别操作集群。基于基于角色的访问控制 (RBAC) 的用户授权对于此环境是有效且可靠的。但是，在更受管理的环境中，例如Elasticsearch Service，集群基础架构的操作员和集群的管理员之间存在区别。

操作员权限将某些功能限制为操作员用户_仅_。操作员用户只是常规的 Elasticsearch 用户，可以访问仅限特定操作员的功能。群集管理员无法使用这些权限，即使他们以高特权用户(如"弹性"用户或具有"超级用户"角色的其他用户)身份登录也是如此。通过限制系统访问，操作员权限增强了 Elasticsearch 安全模型，同时保护了用户功能。

操作员权限在 Elastic Cloud 上启用，这意味着某些基础设施管理功能受到限制，您的管理用户无法访问这些功能。此功能可保护您的集群免受意外的基础架构更改。

[« Monitoring and security](secure-monitoring.md) [Configure operator
privileges »](configure-operator-privileges.md)
