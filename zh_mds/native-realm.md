

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« LDAP user authentication](ldap-realm.md) [OpenID Connect authentication
»](oidc-realm.md)

## 本机用户身份验证

管理和验证用户的最简单方法是使用内部"本机"领域。您可以使用 REST API 或 Kibana 添加和删除用户、分配用户角色以及管理用户密码。

### 配置本机域

默认情况下，本机领域可用并处于启用状态。您可以使用以下代码片段显式禁用它。

    
    
    xpack.security.authc.realms.native.native1:
      enabled: false

您可以在"elasticsearch.yml"的"xpack.security.authc.realms.native"命名空间中配置"本机"域。显式配置本机域使您能够设置它在域链中的显示顺序，暂时禁用域，并控制其缓存选项。

1. 将 realm 配置添加到 'xpack.security.authc.realms.native' 命名空间下的 'elasticsearch.yml' 中。建议您为领域显式设置"order"属性。

您只能在 Elasticsearch 节点上配置一个原生领域。

请参阅本机领域设置，了解可以为"本机"领域设置的所有选项。例如，以下代码片段显示了一个"本机"领域配置，该配置将"顺序"设置为零，以便首先检查领域：

    
        xpack.security.authc.realms.native.native1:
      order: 0

为了限制凭据被盗的风险并减少凭据泄露，本机域会根据安全最佳实践存储密码并缓存用户凭据。默认情况下，用户凭据的哈希版本存储在内存中，使用加盐的"sha-256"哈希算法，密码的哈希版本存储在磁盘上，并使用"bcrypt"哈希算法进行加盐和哈希。若要使用不同的哈希算法，请参阅用户缓存和密码哈希算法。

2. 重新启动弹性搜索。

### 管理本机用户

借助 Elastic Stack 安全功能，您可以在 Kibana 的 **管理 / 安全 / 用户** 页面上轻松管理用户。

或者，您可以通过"用户"API 管理用户。有关详细信息和示例，请参阅用户。

[« LDAP user authentication](ldap-realm.md) [OpenID Connect authentication
»](oidc-realm.md)
