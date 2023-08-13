

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Enabling anonymous access](anonymous-access.md) [Controlling the user
cache »](controlling-user-cache.md)

## 查找未进行身份验证的用户

Elasticsearch 领域主要是为了支持用户身份验证而存在的。某些领域使用密码对用户进行身份验证(例如"本机"和"ldap"域)，而其他领域使用更复杂的身份验证协议(例如"saml"和"oidc"域)。在每种情况下，领域的主要目的是建立向 Elasticsearch API 发出请求的用户的身份。

但是，某些 Elasticsearch 功能需要在不使用其凭据的情况下_look up_用户。

* "run_as"功能代表其他用户执行请求。具有"run_as"权限的经过身份验证的用户可以代表另一个未经身份验证的用户执行请求。  * 委派授权功能将两个领域链接在一起，以便针对一个领域进行身份验证的用户可以将角色和元数据与来自不同领域的用户相关联。

在每种情况下，用户必须首先对一个领域进行身份验证，然后 Elasticsearch 将查询第二个领域以查找其他用户。经过身份验证的用户凭据仅用于在第一个领域中进行身份验证，第二个领域中的用户按用户名检索，而无需凭据。

当 Elasticsearch 使用用户的凭据解析用户时(如在第一个领域中执行的那样)，它被称为_user authentication_。

当 Elasticsearch 仅使用用户名解析用户时(如在第二个领域中执行的那样)，它被称为_user lookup_。

请参阅run_as和委派授权文档以了解有关这些功能的更多信息，包括哪些领域和身份验证方法支持"run_as"或委托授权。在这两种情况下，只有以下领域可以用于用户查找：

* 保留的"本机"和"文件"域始终支持用户查找。  * "ldap"领域支持在_user search_模式下配置领域时的用户查找。当领域配置为"user_dn_templates"时，不支持用户查找。  * "active_directory"领域中的用户查找支持要求为域配置"bind_dn"和绑定密码。

'pki'、'saml'、'oidc'、'kerberos' 和 'jwt' 领域不支持用户查找。

如果只想将某个领域用于用户查找并阻止用户对该领域进行身份验证，则可以配置该领域并将"authentication.enabled"设置为"false"

用户查找功能是一项内部功能，用于实现"运行身份"和委派授权功能 - 没有用于用户查找的 API。如果要测试用户查找配置，可以使用"run_as"执行此操作。使用 Authenticate API，以"超级用户"(例如内置的"弹性"用户)身份进行身份验证，并指定"es-security-runas-user"请求标头。

获取用户 API 和用户配置文件功能是检索有关 Elastic Stack 用户信息的替代方法。这些 API 与用户查找功能无关。

[« Enabling anonymous access](anonymous-access.md) [Controlling the user
cache »](controlling-user-cache.md)
