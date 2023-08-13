

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« SAML invalidate API](security-api-saml-invalidate.md) [SAML service
provider metadata API »](security-api-saml-sp-metadata.md)

## SAML 完整注销接口

验证从 SAML IdP 发送的注销响应。

此 API 旨在供 Kibana 以外的自定义 Web 应用程序使用。如果您使用的是 Kibana，请参阅在 ElasticStack 上配置 SAML 单点登录。

###Request

'POST /_security/saml/complete_logout'

###Description

SAML IdP 可能会在处理 SP 启动的 SAML 单次注销后将注销响应发送回 SP。此 API 通过确保内容相关并验证其签名来验证响应。如果验证过程成功，则返回空响应。响应可以由 IdP 使用 HTTP-重定向或 HTTP-Post 绑定发送。此 API 的调用方必须相应地准备请求，以便此 API 可以处理其中任何一个。

Elasticsearch通过SAML API公开所有必要的SAML相关功能。这些 API 由 Kibana 在内部使用，以提供基于 SAML 的身份验证，但也可供其他自定义 Web 应用程序或其他客户端使用。另请参阅 SAML 身份验证 API、SAML 准备身份验证 API、SAML 无效 API 和 SAML 注销 API。

### 请求正文

`realm`

     (Required, string) The name of the SAML realm in Elasticsearch for which the configuration is used to verify the logout response. 
`ids`

     (Required, array) A json array with all the valid SAML Request Ids that the caller of the API has for the current user. 
`query_string`

     (Optional, string) If the SAML IdP sends the logout response with the HTTP-Redirect binding, this field must be set to the query string of the redirect URI. 
`queryString`

     [7.14.0]  Deprecated in 7.14.0. Use query_string instead  See `query_string`
`content`

     (Optional, string) If the SAML IdP sends the logout response with the HTTP-Post binding, this field must be set to the value of the `SAMLResponse` form parameter from the logout response. 

###Examples

以下示例使用 HTTP 重定向绑定验证 SAML IdP 发送的注销响应：

    
    
    POST /_security/saml/complete_logout
    {
      "realm": "saml1",
      "ids": [ "_1c368075e0b3..." ],
      "query_string": "SAMLResponse=fZHLasMwEEVbfb1bf...&SigAlg=http%3A%2F%2Fwww.w3.org%2F2000%2F09%2Fxmldsig%23rsa-sha1&Signature=CuCmFn%2BLqnaZGZJqK..."
    }

如果注销响应是使用 HTTP-Post 绑定发送的，则可以按如下方式进行验证：

    
    
    POST /_security/saml/complete_logout
    {
      "realm": "saml1",
      "ids": [ "_1c368075e0b3..." ],
      "content": "PHNhbWxwOkxvZ291dFJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46..."
    }

API 在成功时返回空响应。

[« SAML invalidate API](security-api-saml-invalidate.md) [SAML service
provider metadata API »](security-api-saml-sp-metadata.md)
