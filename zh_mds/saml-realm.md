

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« PKI user authentication](pki-realm.md) [Kerberos authentication
»](kerberos-realm.md)

## SAML身份验证

弹性堆栈安全功能支持使用 SAML 单点登录 (SSO) 进行用户身份验证。安全功能使用 SAML 2.0 协议的 Web 浏览器 SSO 配置文件提供此支持。

此协议专门设计用于支持通过交互式 Web 浏览器进行身份验证，因此它不作为标准身份验证领域运行。相反，Kibana 和 Elasticsearch 安全功能协同工作以支持交互式 SAML 会话。

这意味着 SAML 领域不适合由标准 REST 客户端使用。如果您配置要在 Kibana 中使用 SAML 领域，则还应配置另一个领域，例如身份验证链中的本机领域。

为了简化在弹性堆栈中配置 SAML 身份验证的过程，提供了在弹性堆栈上配置 SAML 单点登录的分步指南。

[« PKI user authentication](pki-realm.md) [Kerberos authentication
»](kerberos-realm.md)
