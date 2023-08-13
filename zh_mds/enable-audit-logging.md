

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« Customizing roles and authorization](custom-roles-authorization.md)
[Audit events »](audit-event-types.md)

## 启用审计日志记录

您可以记录与安全相关的事件，例如身份验证失败和拒绝连接，以监控集群是否存在可疑活动(包括数据访问授权和用户安全配置更改)。

审核日志记录还可以在发生攻击时提供取证证据。

默认情况下，审核日志处于禁用状态。您必须显式启用审核日志记录。

审核日志仅在某些订阅级别可用。有关详细信息，请参阅 https://www.elastic.co/subscriptions。

要启用审核日志记录，请执行以下操作：

1. 在"elasticsearch.yml"中将"xpack.security.audit.enabled"设置为"true"。  2. 重新启动弹性搜索。

启用审核日志记录后，安全事件将保存到<clustername>主机文件系统上每个群集节点上的专用"_audit.json"文件中。有关详细信息，请参阅日志文件审核输出。

您可以配置其他选项来控制记录哪些事件以及审核日志中包含哪些信息。有关详细信息，请参阅审核设置。

[« Customizing roles and authorization](custom-roles-authorization.md)
[Audit events »](audit-event-types.md)
