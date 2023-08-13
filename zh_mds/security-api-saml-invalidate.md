

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« SAML logout API](security-api-saml-logout.md) [SAML complete logout API
»](security-api-saml-complete-logout.md)

## SAML 无效API

向 Elasticsearch 提交 SAML LogoutRequest 消息以供使用。

此 API 旨在供 Kibana 以外的自定义 Web 应用程序使用。如果您使用的是 Kibana，请参阅在 ElasticStack 上配置 SAML 单点登录。

###Request

'POST /_security/saml/invalidate'

###Description

注销请求来自 IdP 启动的单点注销期间的 SAML IdP。自定义 Web 应用程序可以使用此 API 让 Elasticsearch 处理"LogoutRequest"。成功验证请求后，Elasticsearch 将使对应于该特定 SAML 主体的访问令牌和刷新令牌失效，并提供包含 SAMLLogoutResponse 消息的 URL，以便可以将用户重定向回其 IdP。

Elasticsearch通过SAML API公开所有必要的SAML相关功能。这些 API 由 Kibana 在内部使用，以提供基于 SAML 的身份验证，但也可供其他自定义 Web 应用程序或其他客户端使用。另请参阅 SAML 身份验证 API、SAML 准备身份验证 API、SAML 注销 API 和 SAML 完整注销 API。

### 请求正文

`acs`

     (Optional, string) The Assertion Consumer Service URL that matches the one of the SAML realm in Elasticsearch that should be used. You must specify either this parameter or the `realm` parameter. 
`query_string`

     (Required, string) The query part of the URL that the user was redirected to by the SAML IdP to initiate the Single Logout. This query should include a single parameter named `SAMLRequest` that contains a SAML logout request that is deflated and Base64 encoded. If the SAML IdP has signed the logout request, the URL should include two extra parameters named `SigAlg` and `Signature` that contain the algorithm used for the signature and the signature value itself. In order for Elasticsearch to be able to verify the IdP's signature, the value of the query_string field must be an exact match to the string provided by the browser. The client application must not attempt to parse or process the string in any way. 
`queryString`

     [7.14.0]  Deprecated in 7.14.0. Use query_string instead  See `query_string`. 
`realm`

     (Optional, string) The name of the SAML realm in Elasticsearch the configuration. You must specify either this parameter or the `acs` parameter. 

### 响应正文

`invalidated`

     (integer) The number of tokens that were invalidated as part of this logout. 
`realm`

     (string) The realm name of the SAML realm in Elasticsearch that authenticated the user. 
`redirect`

     (string) A SAML logout response as a parameter so that the user can be redirected back to the SAML IdP. 

###Examples

以下示例使领域"saml1"的所有令牌失效，这些令牌与 SAML 注销请求中标识的用户相关：

    
    
    POST /_security/saml/invalidate
    {
      "query_string" : "SAMLRequest=nZFda4MwFIb%2FiuS%2BmviRpqFaClKQdbvo2g12M2KMraCJ9cRR9utnW4Wyi13sMie873MeznJ1aWrnS3VQGR0j4mLkKC1NUeljjA77zYyhVbIE0dR%2By7fmaHq7U%2BdegXWGpAZ%2B%2F4pR32luBFTAtWgUcCv56%2Fp5y30X87Yz1khTIycdgpUW9kY7WdsC9zxoXTvMvWuVV98YyMnSGH2SYE5pwALBIr9QKiwDGpW0oGVUznGeMyJZKFkQ4jBf5HnhUymjIhzCAL3KNFihbYx8TBYzzGaY7EnIyZwHzCWMfiDnbRIftkSjJr%2BFu0e9v%2B0EgOquRiiZjKpiVFp6j50T4WXoyNJ%2FEWC9fdqc1t%2F1%2B2F3aUpjzhPiXpqMz1%2FHSn4A&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=MsAYz2NFdovMG2mXf6TSpu5vlQQyEJAg%2B4KCwBqJTmrb3yGXKUtIgvjqf88eCAK32v3eN8vupjPC8LglYmke1ZnjK0%2FKxzkvSjTVA7mMQe2AQdKbkyC038zzRq%2FYHcjFDE%2Bz0qISwSHZY2NyLePmwU7SexEXnIz37jKC6NMEhus%3D",
      "realm" : "saml1"
    }
    
    
    {
      "redirect" : "https://my-idp.org/logout/SAMLResponse=....",
      "invalidated" : 2,
      "realm" : "saml1"
    }

[« SAML logout API](security-api-saml-logout.md) [SAML complete logout API
»](security-api-saml-complete-logout.md)
