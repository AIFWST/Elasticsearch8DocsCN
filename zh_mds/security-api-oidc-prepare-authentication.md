

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Invalidate token API](security-api-invalidate-token.md) [OpenID Connect
authenticate API »](security-api-oidc-authenticate.md)

## OpenID Connect 准备身份验证API

根据 Elasticsearch 中相应 OpenID Connect 身份验证领域的配置，将 oAuth 2.0 身份验证请求创建为 URL 字符串。

###Request

'POST /_security/oidc/prepare'

###Description

此 API 的响应是指向已配置的 OpenID Connect 提供程序的授权终结点的 URL，可用于重定向用户的浏览器以继续身份验证过程。

Elasticsearch 通过 OpenID Connect API 公开所有必要的 OpenID Connect 相关功能。这些 API 由 Kibana 在内部使用，以提供基于 OpenID Connect 的身份验证，但也可以由其他自定义 Web 应用程序或其他客户端使用。另请参阅 OpenID Connectauthenticate API 和 OpenID Connect 注销 API。

### 请求正文

可以在请求正文中指定以下参数：

`realm`

     (Optional, string) The name of the OpenID Connect realm in Elasticsearch the configuration of which should be used in order to generate the authentication request. Cannot be specified when `iss` is specified. One of `realm`, `iss` is required. 
`state`

     (Optional, string) Value used to maintain state between the authentication request and the response, typically used as a Cross-Site Request Forgery mitigation. If the caller of the API doesn't provide a value, Elasticsearch will generate one with sufficient entropy itself and return it in the response. 
`nonce`

     (Optional, string) Value used to associate a Client session with an ID Token and to mitigate replay attacks. If the caller of the API doesn't provide a value, Elasticsearch will generate one with sufficient entropy itself and return it in the response. 
`iss`

     (Optional, string) In the case of a 3rd Party initiated Single Sign On, this is the Issuer Identifier for the OP that the RP is to send the Authentication Request to. Cannot be specified when `realm` is specified. One of `realm`, `iss` is required. 
`login_hint`

     (Optional, string) In the case of a 3rd Party initiated Single Sign On, a string value to be included in the authentication request, as the `login_hint` parameter. This parameter is not valid when `realm` is specified 

###Examples

以下示例为 OpenIDConnect Realm 'oidc1' 生成身份验证请求：

    
    
    POST /_security/oidc/prepare
    {
      "realm" : "oidc1"
    }

响应的以下示例输出包含指向 OpenID Connect 提供程序的授权终结点的 URI，其中包含身份验证请求的所有参数，作为 HTTP GET 参数：

    
    
    {
      "redirect" : "http://127.0.0.1:8080/c2id-login?scope=openid&response_type=id_token&redirect_uri=https%3A%2F%2Fmy.fantastic.rp%2Fcb&state=4dbrihtIAt3wBTwo6DxK-vdk-sSyDBV8Yf0AjdkdT5I&nonce=WaBPH0KqPVdG5HHdSxPRjfoZbXMCicm5v1OiAj0DUFM&client_id=elasticsearch-rp",
      "state" : "4dbrihtIAt3wBTwo6DxK-vdk-sSyDBV8Yf0AjdkdT5I",
      "nonce" : "WaBPH0KqPVdG5HHdSxPRjfoZbXMCicm5v1OiAj0DUFM",
      "realm" : "oidc1"
    }

以下示例为 OpenIDConnect Realm 'oidc1' 生成一个身份验证请求，其中状态和随机数的值已由客户端生成：

    
    
    POST /_security/oidc/prepare
    {
      "realm" : "oidc1",
      "state" : "lGYK0EcSLjqH6pkT5EVZjC6eIW5YCGgywj2sxROO",
      "nonce" : "zOBXLJGUooRrbLbQk5YCcyC8AXw3iloynvluYhZ5"
    }

响应的以下示例输出包含指向 OpenID Connect 提供程序的授权终结点的 URI，其中包含身份验证请求的所有参数，作为 HTTP GET 参数：

    
    
    {
      "redirect" : "http://127.0.0.1:8080/c2id-login?scope=openid&response_type=id_token&redirect_uri=https%3A%2F%2Fmy.fantastic.rp%2Fcb&state=lGYK0EcSLjqH6pkT5EVZjC6eIW5YCGgywj2sxROO&nonce=zOBXLJGUooRrbLbQk5YCcyC8AXw3iloynvluYhZ5&client_id=elasticsearch-rp",
      "state" : "lGYK0EcSLjqH6pkT5EVZjC6eIW5YCGgywj2sxROO",
      "nonce" : "zOBXLJGUooRrbLbQk5YCcyC8AXw3iloynvluYhZ5",
      "realm" : "oidc1"
    }

以下示例为第三方发起的单一登录生成身份验证请求，指定用于匹配相应 OpenID Connect 身份验证领域的颁发者：

    
    
    POST /_security/oidc/prepare
    {
      "iss" : "http://127.0.0.1:8080",
      "login_hint": "this_is_an_opaque_string"
    }

响应的以下示例输出包含指向 OpenID Connect 提供程序的授权终结点的 URI，其中包含身份验证请求的所有参数，作为 HTTP GET 参数：

    
    
    {
      "redirect" : "http://127.0.0.1:8080/c2id-login?login_hint=this_is_an_opaque_string&scope=openid&response_type=id_token&redirect_uri=https%3A%2F%2Fmy.fantastic.rp%2Fcb&state=4dbrihtIAt3wBTwo6DxK-vdk-sSyDBV8Yf0AjdkdT5I&nonce=WaBPH0KqPVdG5HHdSxPRjfoZbXMCicm5v1OiAj0DUFM&client_id=elasticsearch-rp",
      "state" : "4dbrihtIAt3wBTwo6DxK-vdk-sSyDBV8Yf0AjdkdT5I",
      "nonce" : "WaBPH0KqPVdG5HHdSxPRjfoZbXMCicm5v1OiAj0DUFM",
      "realm" : "oidc1"
    }

[« Invalidate token API](security-api-invalidate-token.md) [OpenID Connect
authenticate API »](security-api-oidc-authenticate.md)
