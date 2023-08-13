

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Native user authentication](native-realm.md) [PKI user authentication
»](pki-realm.md)

## OpenID 连接身份验证

OpenID Connect 领域使 Elasticsearch 能够充当 OpenID ConnectRelying 方 (RP)，并在 Kibana 中提供单点登录 (SSO) 支持。

它专门设计用于支持通过交互式 Web 浏览器进行身份验证，因此它不作为标准身份验证领域运行。相反，有 Kibana 和 Elasticsearch 安全功能协同工作，以实现交互式 OpenID Connect 会话。

这意味着 OpenID Connect 领域不适合由 standardREST 客户端使用。如果配置要在 Kibana 中使用的 OpenID Connect 领域，则还应配置另一个领域，例如身份验证链中的本机领域。

为了简化在弹性堆栈中配置 OpenID Connect 身份验证的过程，有一个分步指南：使用 OpenID Connect 配置对弹性堆栈的单点登录。

[« Native user authentication](native-realm.md) [PKI user authentication
»](pki-realm.md)
