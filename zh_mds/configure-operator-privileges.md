

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Operator privileges](operator-
privileges.md)

[« Operator privileges](operator-privileges.md) [Operator-only functionality
»](operator-only-functionality.md)

## 配置操作员权限

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

在使用操作员权限之前，必须在群集中的所有节点上启用该功能并指定操作员用户。

### 启用操作员权限

要使用操作员权限功能，必须在群集中的每个节点上显式启用该功能。在每个"弹性搜索.yml"文件中添加以下设置：

    
    
    xpack.security.operator_privileges.enabled: true

如果在进行此更改之前节点已在运行，则必须重新启动节点才能使该功能生效。

需要跨群集中的所有节点一致地启用或禁用该功能。否则，您可能会得到不一致的行为，具体取决于哪个节点首先收到请求以及哪个节点执行请求。

在集群上启用操作员权限时，特定功能将受到限制，并且只能由已明确指定为操作员用户的用户执行。如果普通用户尝试执行这些功能(即使他们具有"超级用户"角色)，则会发生安全异常。

### 指定运算符用户

操作员用户只是普通的 Elasticsearch 用户，具有执行仅操作员功能的特殊权限。它们在 'operator_users.yml' 文件中指定，该文件位于 config 目录(由 'ES_PATH_CONF' 环境变量定义)。与其他安全配置文件类似，"operator_users.yml"文件是节点的本地文件，不会全局应用于群集。这意味着，在大多数情况下，应将同一文件分发或复制到群集中的所有节点。

"operator_users.yml"文件定义了一组条件，身份验证用户必须匹配这些条件才能被视为操作员用户。以下代码片段显示了此类文件的示例：

    
    
    operator: __- usernames: ["system_agent_1","system_agent_2"] __realm_type: "file" __auth_type: "realm" __

__

|

固定值"operator"表示定义的开始。   ---|---    __

|

操作员用户允许的用户名列表。此字段为必填字段。   __

|

操作员用户允许的身份验证领域类型。默认值和唯一可接受的值是"file"。   __

|

操作员用户允许的身份验证类型。默认值和唯一可接受的值是"领域"。   您必须至少指定"用户名"字段。如果未指定其他字段，则使用其默认值。必须匹配所有字段，用户才能被限定为操作员用户。您还可以指定多组条件。这目前不是很有用，因为此功能尚不支持其他领域或身份验证类型。

还有两个隐式规则会影响哪些用户是操作员用户：

1. 如果身份验证用户以其他用户身份运行，则他们都不被视为操作员用户。  2. 所有内部用户都是隐式操作员用户。

将用户指定为操作员用户后，他们仍需接受常规 RBAC 用户授权检查。也就是说，除了指定用户是操作员用户之外，您还必须授予他们执行任务所需的 Elasticsearch 角色。因此，操作员用户完全有可能遇到"拒绝访问"错误，并且由于 RBAC 检查失败而无法执行某些操作。简而言之，操作员用户不是自动的"超级用户"。

[« Operator privileges](operator-privileges.md) [Operator-only functionality
»](operator-only-functionality.md)
