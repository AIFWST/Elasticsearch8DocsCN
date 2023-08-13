

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« OpenID Connect authenticate API](security-api-oidc-authenticate.md)
[Query API key information API »](security-api-query-api-key.md)

## OpenID Connect logoutAPI

提交请求以使刷新令牌和访问令牌失效，该令牌是为响应对"/_security/oidc/authenticate"的调用而生成的。

###Request

'POST /_security/oidc/logout'

###Description

如果相应地配置了 Elasticsearch 中的 OpenID Connect 身份验证领域，则对此调用的响应将包含一个指向 OpenID Connect 提供程序的 EndSession 端点的 URI，以便执行 SingleLogout。

Elasticsearch 通过 OpenID Connect API 公开所有必要的 OpenID Connect 相关功能。这些 API 由 Kibana 在内部使用，以提供基于 OpenID Connect 的身份验证，但也可以由其他自定义 Web 应用程序或其他客户端使用。另请参阅 OpenID Connectauthenticate API 和 OpenID Connect 准备身份验证 API。

### 请求正文

`access_token`

     (Required, string) The value of the access token to be invalidated as part of the logout. 
`refresh_token`

     (Optional, string) The value of the refresh token to be invalidated as part of the logout. 

###Examples

以下示例执行注销

    
    
    POST /_security/oidc/logout
    {
      "token" : "dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ==",
      "refresh_token": "vLBPvmAB6KvwvJZr27cS"
    }

响应的以下示例输出包含指向 OpenID Connect 提供程序的结束会话终结点的 URI，其中包含注销请求的所有参数，作为 HTTP GET 参数：

    
    
    {
      "redirect" : "https://op-provider.org/logout?id_token_hint=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c&post_logout_redirect_uri=http%3A%2F%2Foidc-kibana.elastic.co%2Floggedout&state=lGYK0EcSLjqH6pkT5EVZjC6eIW5YCGgywj2sxROO"
    }

[« OpenID Connect authenticate API](security-api-oidc-authenticate.md)
[Query API key information API »](security-api-query-api-key.md)
