

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get service account credentials API](security-api-get-service-
credentials.md) [Get user privileges API »](security-api-get-user-
privileges.md)

## 获取令牌API

创建用于访问的持有者令牌，而无需基本身份验证。

###Request

'POST /_security/oauth2/token'

###Prerequisites

* 要使用此 API，您必须具有"manage_token"群集权限。

###Description

令牌由 Elasticsearch 令牌服务创建，当您在 HTTP 接口上配置 TLS 时，该服务会自动启用。请参阅为 Elasticsearch 加密 HTTP 客户端通信。或者，您可以显式启用"xpack.security.authc.token.enabled"设置。当您运行生产模式时，引导程序检查会阻止您启用令牌服务，除非您还在 HTTP 接口上启用 TLS。

获取令牌 API 采用与典型 OAuth 2.0 令牌 API 相同的参数，但使用 JSON 请求正文除外。

成功的获取令牌 API 调用将返回一个 JSON 结构，其中包含访问令牌、令牌过期的时间量(秒)、类型和范围(如果可用)。

获取令牌 API 返回的令牌具有有限的有效时间段，在该时间段之后，它们将无法再使用。该时间段由"xpack.security.authc.token.timeout"设置定义。有关详细信息，请参阅令牌服务设置。

如果要立即使令牌失效，可以使用使令牌无效 API 来实现。

### 请求正文

可以在 POST 请求的正文中指定以下参数，并与创建令牌相关：

`grant_type`

    

(必需，字符串)赠款的类型。支持的授权类型包括："密码"、"_kerberos"、"client_credentials"和"refresh_token"。

`client_credentials`

     This grant type implements the Client Credentials Grant of OAuth2. It is geared for machine to machine communication and is not suitable or designed for the self-service user creation of tokens. It generates only access tokens that cannot be refreshed. The premise is that the entity that uses `client_credentials` has constant access to a set of (client, not end-user) credentials and can authenticate itself at will. 
`_kerberos`

     This grant type is supported internally and implements SPNEGO based Kerberos support. The `_kerberos` grant type may change from version to version. 
`password`

     This grant type implements the Resource Owner Password Credentials Grant of OAuth2. In this grant, a trusted client exchanges the end user's credentials for an access token and (possibly) a refresh token. The request needs to be made by an authenticated user but happens _on behalf_ of another authenticated user (the one whose credentials are passed as request parameters). This grant type is not suitable or designed for the self-service user creation of tokens. 
`refresh_token`

     This grant type implements the Refresh Token Grant of OAuth2. In this grant a user exchanges a previously issued refresh token for a new access token and a new refresh token. 

`password`

     (Optional*, string) The user's password. If you specify the `password` grant type, this parameter is required. This parameter is not valid with any other supported grant type. 
`kerberos_ticket`

     (Optional*, string) The base64 encoded kerberos ticket. If you specify the `_kerberos` grant type, this parameter is required. This parameter is not valid with any other supported grant type. 
`refresh_token`

     (Optional*, string) The string that was returned when you created the token, which enables you to extend its life. If you specify the `refresh_token` grant type, this parameter is required. This parameter is not valid with any other supported grant type. 
`scope`

     (Optional, string) The scope of the token. Currently tokens are only issued for a scope of `FULL` regardless of the value sent with the request. 
`username`

     (Optional*, string) The username that identifies the user. If you specify the `password` grant type, this parameter is required. This parameter is not valid with any other supported grant type. 

###Examples

以下示例使用"client_credentials"授权类型获取令牌，该授权类型仅以经过身份验证的用户身份创建令牌：

    
    
    POST /_security/oauth2/token
    {
      "grant_type" : "client_credentials"
    }

以下示例输出包含访问令牌、令牌过期的时间量(以秒为单位)以及类型：

    
    
    {
      "access_token" : "dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ==",
      "type" : "Bearer",
      "expires_in" : 1200,
      "authentication" : {
        "username" : "test_admin",
        "roles" : [
          "superuser"
        ],
        "full_name" : null,
        "email" : null,
        "metadata" : { },
        "enabled" : true,
        "authentication_realm" : {
          "name" : "file",
          "type" : "file"
        },
        "lookup_realm" : {
          "name" : "file",
          "type" : "file"
        },
        "authentication_type" : "realm"
      }
    }

此 API 返回的令牌可以通过发送带有"Authorization"标头的请求来使用，该标头的值具有前缀"Bearer"，后跟"access_token"的值。

    
    
    curl -H "Authorization: Bearer dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ==" http://localhost:9200/_cluster/health

以下示例使用"密码"授权类型获取"test_admin"用户的令牌。此请求需要由经过身份验证的用户发出，该用户具有足够的权限，该权限可能与在"用户名"参数中传递的用户名相同，也可能不同：

    
    
    POST /_security/oauth2/token
    {
      "grant_type" : "password",
      "username" : "test_admin",
      "password" : "x-pack-test-password"
    }

以下示例输出包含访问令牌、令牌过期的时间量(以秒为单位)、类型和刷新令牌：

    
    
    {
      "access_token" : "dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ==",
      "type" : "Bearer",
      "expires_in" : 1200,
      "refresh_token": "vLBPvmAB6KvwvJZr27cS",
      "authentication" : {
        "username" : "test_admin",
        "roles" : [
          "superuser"
        ],
        "full_name" : null,
        "email" : null,
        "metadata" : { },
        "enabled" : true,
        "authentication_realm" : {
          "name" : "file",
          "type" : "file"
        },
        "lookup_realm" : {
          "name" : "file",
          "type" : "file"
        },
        "authentication_type" : "realm"
      }
    }

要延长使用"密码"授权类型获取的现有令牌的寿命，您可以在令牌创建后的 24 小时内使用刷新令牌再次调用 API。例如：

    
    
    POST /_security/oauth2/token
    {
      "grant_type": "refresh_token",
      "refresh_token": "vLBPvmAB6KvwvJZr27cS"
    }

API 将返回新令牌和刷新令牌。每个刷新令牌只能使用一次。

    
    
    {
      "access_token" : "dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ==",
      "type" : "Bearer",
      "expires_in" : 1200,
      "refresh_token": "vLBPvmAB6KvwvJZr27cS",
      "authentication" : {
        "username" : "test_admin",
        "roles" : [
          "superuser"
        ],
        "full_name" : null,
        "email" : null,
        "metadata" : { },
        "enabled" : true,
        "authentication_realm" : {
          "name" : "file",
          "type" : "file"
        },
        "lookup_realm" : {
          "name" : "file",
          "type" : "file"
        },
        "authentication_type" : "token"
      }
    }

以下示例使用"kerberos"授权类型获取访问令牌和刷新令牌，该授权类型仅创建一个令牌以换取 base64 编码的 kerberos 票证：

    
    
    POST /_security/oauth2/token
    {
      "grant_type" : "_kerberos",
      "kerberos_ticket" : "YIIB6wYJKoZIhvcSAQICAQBuggHaMIIB1qADAgEFoQMCAQ6iBtaDcp4cdMODwOsIvmvdX//sye8NDJZ8Gstabor3MOGryBWyaJ1VxI4WBVZaSn1WnzE06Xy2"
    }

如果 kerberos 身份验证成功，API 将返回新令牌并刷新令牌。每个刷新令牌只能使用一次。当在 Spnego GSS 上下文中请求相互身份验证时，服务器将在"kerberos_authentication_response_token"中返回一个 base64 编码的令牌，供客户端使用和完成身份验证。

    
    
    {
      "access_token" : "dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ==",
      "type" : "Bearer",
      "expires_in" : 1200,
      "refresh_token": "vLBPvmAB6KvwvJZr27cS"
      "kerberos_authentication_response_token": "YIIB6wYJKoZIhvcSAQICAQBuggHaMIIB1qADAg",
      "authentication" : {
        "username" : "test_admin",
        "roles" : [
          "superuser"
        ],
        "full_name" : null,
        "email" : null,
        "metadata" : { },
        "enabled" : true,
        "authentication_realm" : {
          "name" : "file",
          "type" : "file"
        },
        "lookup_realm" : {
          "name" : "file",
          "type" : "file"
        },
        "authentication_type" : "realm"
      }
    }

[« Get service account credentials API](security-api-get-service-
credentials.md) [Get user privileges API »](security-api-get-user-
privileges.md)
