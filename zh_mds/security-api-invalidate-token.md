

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Invalidate API key API](security-api-invalidate-api-key.md) [OpenID
Connect prepare authentication API »](security-api-oidc-prepare-
authentication.md)

## 使令牌API失效

使一个或多个访问令牌或刷新令牌失效。

###Request

"删除/_security/oauth2/token"

###Description

获取令牌 API 返回的访问令牌具有有限的有效时间段，在该时间段之后，它们将无法再使用。该时间段由"xpack.security.authc.token.timeout"设置定义。有关详细信息，请参阅令牌服务设置。

获取令牌 API 返回的刷新令牌仅在 24 小时内有效。它们也可以恰好使用一次。

如果要立即使一个或多个访问令牌或刷新令牌失效，请使用此使令牌 API 失效。

### 请求正文

可以在 DELETE 请求的正文中指定以下参数，这些参数与使令牌失效有关：

`token`

     (Optional, string) An access token. This parameter cannot be used any of `refresh_token`, `realm_name` or `username` are used. 
`refresh_token`

     (Optional, string) A refresh token. This parameter cannot be used any of `refresh_token`, `realm_name` or `username` are used. 
`realm_name`

     (Optional, string) The name of an authentication realm. This parameter cannot be used with either `refresh_token` or `token`. 
`username`

     (Optional, string) The username of a user. This parameter cannot be used with either `refresh_token` or `token`

虽然所有参数都是可选的，但至少其中一个是必需的。更具体地说，需要"令牌"或"refresh_token"参数之一。如果这两个都没有指定，则需要指定"realm_name"和/或"用户名"。

### 响应正文

成功的调用会返回一个 JSON 结构，其中包含已失效的令牌数、已失效的令牌数，以及可能使特定令牌失效时遇到的错误列表。

###Examples

例如，如果使用"client_credentials"授权类型创建令牌，则如下所示：

    
    
    POST /_security/oauth2/token
    {
      "grant_type" : "client_credentials"
    }

获取令牌 API 返回有关访问令牌的以下信息：

    
    
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

现在可以立即使此访问令牌失效，如以下示例所示：

    
    
    DELETE /_security/oauth2/token
    {
      "token" : "dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ=="
    }

如果使用"密码"授权类型获取用户的令牌，则响应可能还包含刷新令牌。例如：

    
    
    POST /_security/oauth2/token
    {
      "grant_type" : "password",
      "username" : "test_admin",
      "password" : "x-pack-test-password"
    }

获取令牌 API 返回以下信息：

    
    
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

刷新令牌现在也可以立即失效，如以下示例所示：

    
    
    DELETE /_security/oauth2/token
    {
      "refresh_token" : "vLBPvmAB6KvwvJZr27cS"
    }

以下示例立即使"saml1"领域的所有访问令牌和刷新令牌失效：

    
    
    DELETE /_security/oauth2/token
    {
      "realm_name" : "saml1"
    }

以下示例立即使所有领域中用户"myuser"的所有访问令牌和刷新令牌失效：

    
    
    DELETE /_security/oauth2/token
    {
      "username" : "myuser"
    }

最后，以下示例立即使"saml1"领域中用户"myuser"的所有访问令牌和刷新令牌失效：

    
    
    DELETE /_security/oauth2/token
    {
      "username" : "myuser",
      "realm_name" : "saml1"
    }
    
    
    {
      "invalidated_tokens":9, __"previously_invalidated_tokens":15, __"error_count":2, __"error_details":[ __{
          "type":"exception",
          "reason":"Elasticsearch exception [type=exception, reason=foo]",
          "caused_by":{
            "type":"exception",
            "reason":"Elasticsearch exception [type=illegal_argument_exception, reason=bar]"
          }
        },
        {
          "type":"exception",
          "reason":"Elasticsearch exception [type=exception, reason=boo]",
          "caused_by":{
            "type":"exception",
            "reason":"Elasticsearch exception [type=illegal_argument_exception, reason=far]"
          }
        }
      ]
    }

__

|

作为此请求的一部分而失效的令牌数。   ---|---    __

|

已失效的令牌数。   __

|

使令牌失效时遇到的错误数。   __

|

有关这些错误的详细信息。当"error_count"为 0 时，响应中不存在此字段。   « 使API密钥API无效 开放IDConnect 准备身份验证API »