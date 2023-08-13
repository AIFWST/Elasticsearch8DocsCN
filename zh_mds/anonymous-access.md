

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Integrating with other authentication systems](custom-realms.md) [Looking
up users without authentication »](user-lookup.md)

## 启用匿名访问

要嵌入 Kibana 仪表板或授予对 Kibana 的访问权限而无需凭据，请改用 Kibana 的匿名身份验证功能。

如果没有身份验证令牌可以从传入请求中提取，则传入请求被视为 _anonymous_。默认情况下，匿名请求被拒绝并返回身份验证错误(状态代码"401")。

要启用匿名访问，请在"elasticsearch.yml"配置文件中为匿名用户分配一个或多个角色。例如，以下配置为匿名用户分配"role1"和"role2"：

    
    
    xpack.security.authc:
      anonymous:
        username: anonymous_user __roles: role1, role2 __authz_exception: true __

__

|

匿名用户的用户名/主体。如果未指定，则默认为"_es_anonymous_user"。   ---|---    __

|

要与匿名用户关联的角色。如果未指定角色，则禁用匿名访问 - 匿名请求将被拒绝并返回身份验证错误。   __

|

如果为"true"，则如果匿名用户没有执行请求的操作所需的权限，则返回 403 HTTP 状态代码，并且不会提示用户提供凭据来访问请求的资源。当"false"时，如果匿名用户没有必要的权限，并且系统会提示用户输入凭据以访问请求的资源，则会返回 401 HTTP 状态代码。如果将匿名访问与 HTTP 结合使用，则可能需要将"authz_exception"设置为"false"(如果客户端不支持抢占式基本身份验证)。默认为"true"。   « 与其他身份验证系统集成 无需身份验证即可查找用户 »