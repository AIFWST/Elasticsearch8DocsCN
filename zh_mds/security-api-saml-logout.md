

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« SAML authenticate API](security-api-saml-authenticate.md) [SAML
invalidate API »](security-api-saml-invalidate.md)

## SAML logoutAPI

提交使访问令牌失效和刷新令牌的请求。

此 API 旨在供 Kibana 以外的自定义 Web 应用程序使用。如果您使用的是 Kibana，请参阅在 ElasticStack 上配置 SAML 单点登录。

###Request

'POST /_security/saml/logout'

###Description

此 API 使 SAMLauthenticate API 为用户生成的令牌失效。

如果 Elasticsearch 中的 SAML 领域进行了相应的配置，并且 SAML IdP 支持此功能，则 Elasticsearch 响应将包含一个 URL，用于将用户重定向到包含 SAML 注销请求的 IdP(启动 SP 启动的 SAMLSingle 注销)。

Elasticsearch通过SAML API公开所有必要的SAML相关功能。这些 API 由 Kibana 在内部使用，以提供基于 SAML 的身份验证，但也可供其他自定义 Web 应用程序或其他客户端使用。另请参阅 SAML 身份验证 API、SAML 准备身份验证 API、SAML 无效 API 和 SAML 完整注销 API。

### 请求正文

`token`

     (Required, string) The access token that was returned as a response to calling the [SAML authenticate API](security-api-saml-authenticate.html "SAML authenticate API"). Alternatively, the most recent token that was received after refreshing the original one by using a `refresh_token`. 
`refresh_token`

     (Optional, string) The refresh token that was returned as a response to calling the [SAML authenticate API](security-api-saml-authenticate.html "SAML authenticate API"). Alternatively, the most recent refresh token that was received after refreshing the original access token. 

### 响应正文

`redirect`

     (string) A URL that contains a SAML logout request as a parameter. The user can use this URL to be redirected back to the SAML IdP and to initiate Single Logout. 

###Examples

以下示例使通过调用 SAML 身份验证 API 生成的令牌对失效，并成功响应 SAML：

    
    
    POST /_security/saml/logout
    {
      "token" : "46ToAxZVaXVVZTVKOVF5YU04ZFJVUDVSZlV3",
      "refresh_token" : "mJdXLtmvTUSpoLwMvdBt_w"
    }

API 返回以下响应：

    
    
    {
      "redirect" : "https://my-idp.org/logout/SAMLRequest=...."
    }

[« SAML authenticate API](security-api-saml-authenticate.md) [SAML
invalidate API »](security-api-saml-invalidate.md)
