

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Bulk update API keys API](security-api-bulk-update-api-keys.md) [SAML
authenticate API »](security-api-saml-authenticate.md)

## SAML 准备身份验证API

根据 <AuthnRequest>Elasticsearch 中相应 SAML 领域的配置，以 URL 字符串的形式创建 SAML 身份验证请求 ('')。

此 API 旨在供 Kibana 以外的自定义 Web 应用程序使用。如果您使用的是 Kibana，请参阅在 ElasticStack 上配置 SAML 单点登录。

###Request

'POST /_security/saml/prepare'

###Description

此 API 返回指向 SAML 身份提供程序的 URL。您可以使用URL重定向用户的浏览器，以便继续身份验证过程。该 URL 包含一个名为"SAMLRequest"的单个参数，其中包含一个经过压缩和 Base64 编码的 SAML 身份验证请求。如果配置规定应对 SAML 身份验证请求进行签名，则 URL 有两个额外的参数，分别名为"SigAlg"和"签名"。这些参数包含用于签名的算法和签名值本身。它还返回一个随机字符串，用于唯一标识此 SAML 身份验证请求。此 API 的调用方需要存储此标识符，因为它需要在身份验证过程的后续步骤中使用(请参阅 SAML 身份验证 API)。

Elasticsearch通过SAML API公开所有必要的SAML相关功能。这些 API 由 Kibana 在内部使用，以提供基于 SAML 的身份验证，但也可供其他自定义 Web 应用程序或其他客户端使用。另请参阅 SAML 身份验证 API、SAML 无效 API、SAML 注销 API 和 SAML 完整注销 API。

### 请求正文

`acs`

     (Optional, string) The Assertion Consumer Service URL that matches the one of the SAML realms in Elasticsearch. The realm is used to generate the authentication request. You must specify either this parameter or the `realm` parameter. 
`realm`

     (Optional, string) The name of the SAML realm in Elasticsearch for which the configuration is used to generate the authentication request. You must specify either this parameter or the `acs` parameter. 
`relay_state`

     (Optional, string) A string that will be included in the redirect URL that this API returns as the `RelayState` query parameter. If the Authentication Request is signed, this value is used as part of the signature computation. 

### 响应正文

`id`

     (string) A unique identifier for the SAML Request to be stored by the caller of the API. 
`realm`

     (string) The name of the Elasticsearch realm that was used to construct the authentication request. 
`redirect`

     (string) The URL to redirect the user to. 

###Examples

以下示例为名为"saml1"的 SAMLrealm 生成 SAML 身份验证请求

    
    
    POST /_security/saml/prepare
    {
      "realm" : "saml1"
    }

以下示例使用 SAMLrealm 生成一个 SAML 身份验证请求，其断言使用服务 URL 匹配'https：//kibana.org/api/security/saml/callback

    
    
    POST /_security/saml/prepare
    {
      "acs" : "https://kibana.org/api/security/saml/callback"
    }

此 API 返回以下响应：

    
    
    {
      "redirect": "https://my-idp.org/login?SAMLRequest=fVJdc6IwFP0rmbwDgUKLGbFDtc462%2B06FX3Yl50rBJsKCZsbrPbXL6J22hdfk%2FNx7zl3eL%2BvK7ITBqVWCfVdRolQuS6k2iR0mU2dmN6Phgh1FTQ8be2rehH%2FWoGWdESF%2FPST0NYorgElcgW1QG5zvkh%2FPfHAZbwx2upcV5SkiMLYzmqsFba1MAthdjIXy5enhL5a23DPOyo6W7kGBa7cwhZ2gO7G8OiW%2BR400kORt0bag7fzezAlk24eqcD2OxxlsNN5O3MdsW9c6CZnbq7rntF4d3s0D7BaHTZhIWN52P%2BcjiuGRbDU6cdj%2BEjJbJLQv4N4ADdhxBiEZbQuWclY4Q8iABbCXczCdSiKMAC%2FgyO2YqbQgrIJDZg%2FcFjsMD%2Fzb3gUcBa5sR%2F9oWR%2BzuJBqlPG14Jbn0DIf2TZ3Jn%2FXmSUrC5ddQB6bob37uZrJdeF4dIDHV3iuhb70Ptq83kOz53ubDLXlcwPJK0q%2FT42AqxIaAkVCkqm2tRgr49yfJGFU%2FZQ3hy3QyuUpd7obPv97kb%2FAQ%3D%3D"}",
      "realm": "saml1",
      "id": "_989a34500a4f5bf0f00d195aa04a7804b4ed42a1"
    }

[« Bulk update API keys API](security-api-bulk-update-api-keys.md) [SAML
authenticate API »](security-api-saml-authenticate.md)
