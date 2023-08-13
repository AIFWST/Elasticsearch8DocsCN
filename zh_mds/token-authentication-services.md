

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Internal users](internal-users.md) [User profiles »](user-profile.md)

## 基于令牌的身份验证服务

Elastic Stack 安全功能通过使用领域和一个或多个基于令牌的身份验证服务对用户进行身份验证。基于令牌的身份验证服务用于对令牌进行身份验证和管理。您可以将这些令牌附加到发送到 Elasticsearch 的请求中，并将它们用作凭证。当 Elasticsearch 收到必须进行身份验证的请求时，它会首先查询基于令牌的身份验证服务，然后查询领域链。

安全功能提供以下内置的基于令牌的身份验证服务，这些服务按查阅顺序列出：

_service-accounts_

    

服务帐户使用创建服务帐户令牌 API 或弹性搜索服务令牌 CLI 工具来生成服务帐户令牌。

要使用服务帐号令牌，请在请求中包含生成的令牌值，标头为"授权：持有者"：

    
    
    curl -H "Authorization: Bearer AAEAAWVsYXN0aWMvZ...mXQtc2VydmMTpyNXdkYmRib1FTZTl2R09Ld2FKR0F3" http://localhost:9200/_cluster/health

不要尝试使用服务帐户对单个用户进行身份验证。服务帐户只能使用服务令牌进行身份验证，这不适用于普通用户。

_token-service_

    

令牌服务使用获取令牌 API 根据 OAuth2 规范生成访问令牌和刷新令牌。访问令牌是短期令牌。默认情况下，它在 20 分钟后过期，但可以配置为最多持续 1 小时。可以使用刷新令牌刷新它，该令牌的生存期为 24 小时。访问令牌是持有者令牌。您可以通过发送带有"Authorization"标头的请求来使用它，该标头的值具有前缀"Bearer"，后跟访问令牌的值。例如：

    
    
    curl -H "Authorization: Bearer dGhpcyBpcyBub3Qx5...F0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ==" http://localhost:9200/_cluster/health

_api-key-service_

    

API 密钥服务使用创建 API 密钥 API 来生成 API 密钥。默认情况下，API 密钥不会过期。当您请求创建 API 密钥时，您可以指定 API 密钥的过期时间和权限。权限受经过身份验证的用户的权限限制。您可以通过发送带有"授权"标头的请求来使用 API 密钥，该标头的值具有前缀"ApiKey"，后跟凭据。凭据是 API 密钥 ID 的 base64 编码和由冒号连接的 API 密钥。例如：

    
    
    curl -H "Authorization: ApiKey VnVhQ2ZHY0JDZGJrU...W0tZTVhT3g6dWkybHAyYXhUTm1zeWFrd0dk5udw==" http://localhost:9200/_cluster/health

根据您的用例，您可能需要决定这些服务生成的令牌的生存期。然后，可以使用此信息来决定使用哪个服务来生成和管理令牌。未过期的 API 密钥似乎是一个简单的选择，但您必须考虑未过期密钥带来的安全隐患。_token service_ and_api密钥service_都允许您使令牌失效。请参阅使令牌 API 失效和使 API 密钥 API 失效。

对 JWT 持有者令牌的身份验证支持是在 Elasticsearch8.2 中通过 JWT 身份验证引入的，无法通过令牌身份验证服务启用。领域提供零、一个或多个 JWT 领域的灵活顺序和配置。

[« Internal users](internal-users.md) [User profiles »](user-profile.md)
