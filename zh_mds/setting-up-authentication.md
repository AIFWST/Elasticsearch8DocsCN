

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« Update security certificates with a different CA](update-node-certs-
different.md) [Built-in users »](built-in-users.md)

## 用户身份验证

身份验证标识个人。若要访问受限资源，用户必须通过密码、凭据或某些其他方式(通常称为身份验证令牌)证明其身份。

Elastic Stack 通过识别命中集群的请求背后的用户并验证他们是否是他们声称的身份来对用户进行身份验证。身份验证过程由一个或多个称为 _realms_ 的身份验证服务处理。

您可以使用本机支持来管理和验证用户，或与外部用户管理系统(如 LDAP 和 ActiveDirectory)集成。

Elastic Stack 安全功能提供了内置领域，例如"本机"、"ldap"、"active_directory"、"pki"、"file"、"saml"、"kerberos"、"oidc"和"jwt"。如果没有任何内置领域满足您的需求，您也可以构建自己的自定义领域并将其插入 Elastic Stack。

启用安全功能后，根据您配置的领域，您必须将用户凭证附加到发送到 Elasticsearch 的请求。例如，当使用支持用户名和密码的领域时，您可以简单地将 basicauth 标头附加到请求中。

安全功能提供两种服务：令牌服务和 API 密钥服务。您可以使用这些服务将当前身份验证交换为令牌或密钥。然后，可以将此令牌或密钥用作对新请求进行身份验证的凭据。默认情况下，API 密钥服务处于启用状态。当为 HTTP 启用 TLS/SSL 时，默认情况下会启用令牌服务。

[« Update security certificates with a different CA](update-node-certs-
different.md) [Built-in users »](built-in-users.md)
