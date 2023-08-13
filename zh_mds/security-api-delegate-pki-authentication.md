

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Create service account token API](security-api-create-service-token.md)
[Delete application privileges API »](security-api-delete-privilege.md)

## 委托 PKI 认证接口

实现_X509Certificate_链与 Elasticsearchaccess 令牌的交换。

###Request

"发布/_security/delegate_pki"

###Prerequisites

* 要调用此 API，(代理)用户必须具有"delegate_pki"或"全部"群集权限。"kibana_system"内置角色已授予此权限。请参阅安全权限。

###Description

此 API 实现了_X509Certificate_链与 Elasticsearch 访问令牌的交换。根据 RFC 5280，通过按顺序考虑将"委派启用"设置为"true"(默认值为"false")的每个已安装的 PKI 域的信任配置来验证证书链。成功受信任的客户端证书还需要根据主题的领域"username_pattern"对使用者专有名称进行验证。

此 API 由 **smart** 和 **trusted** 代理(如 Kibana)调用，这些代理终止用户的 TLS 会话，但仍希望使用 PKI 领域对用户进行身份验证，就像用户直接连接到 Elasticsearch 一样。有关更多详细信息，请参阅连接到 Kibana 的客户端的 PKI 身份验证。

目标证书中的使用者公钥与相应的私钥之间的关联未经验证。这是 TLS 身份验证过程的一部分，它被委派给调用此 API 的代理。代理是受信任的，可以执行TLS身份验证，并且此API将该身份验证转换为Elasticsearch访问令牌。

### 请求正文

`x509_certificate_chain`

    

(必需，字符串列表)_X509Certificate_链，表示为有序字符串数组。数组中的每个字符串都是证书 DERencoding 的 base64 编码(RFC4648 的第 4 节 - 不是 base64url 编码)。

第一个元素是目标证书，其中包含请求访问的使用者可分辨名称。随后可能会有其他证书;每个后续证书都用于认证前一个证书。

### 响应正文

`access_token`

     (string) An access token associated to the subject distinguished name of the client's certificate. 
`expires_in`

     (time units) The amount of time (in seconds) that the token expires in. 
`type`

     (string) The type of token. 

###Examples

下面是一个示例请求：

    
    
    POST /_security/delegate_pki
    {
      "x509_certificate_chain": ["MIIDeDCCAmCgAwIBAgIUBzj/nGGKxP2iXawsSquHmQjCJmMwDQYJKoZIhvcNAQELBQAwUzErMCkGA1UEAxMiRWxhc3RpY3NlYXJjaCBUZXN0IEludGVybWVkaWF0ZSBDQTEWMBQGA1UECxMNRWxhc3RpY3NlYXJjaDEMMAoGA1UEChMDb3JnMB4XDTIzMDcxODE5MjkwNloXDTQzMDcxMzE5MjkwNlowSjEiMCAGA1UEAxMZRWxhc3RpY3NlYXJjaCBUZXN0IENsaWVudDEWMBQGA1UECxMNRWxhc3RpY3NlYXJjaDEMMAoGA1UEChMDb3JnMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAllHL4pQkkfwAm/oLkxYYO+r950DEy1bjH+4viCHzNADLCTWO+lOZJVlNx7QEzJE3QGMdif9CCBBxQFMapA7oUFCLq84fPSQQu5AnvvbltVD9nwVtCs+9ZGDjMKsz98RhSLMFIkxdxi6HkQ3Lfa4ZSI4lvba4oo+T/GveazBDS+NgmKyq00EOXt3tWi1G9vEVItommzXWfv0agJWzVnLMldwkPqsw0W7zrpyT7FZS4iLbQADGceOW8fiauOGMkscu9zAnDR/SbWl/chYioQOdw6ndFLn1YIFPd37xL0WsdsldTpn0vH3YfzgLMffT/3P6YlwBegWzsx6FnM/93Ecb4wIDAQABo00wSzAJBgNVHRMEAjAAMB0GA1UdDgQWBBQKNRwjW+Ad/FN1Rpoqme/5+jrFWzAfBgNVHSMEGDAWgBRcya0c0x/PaI7MbmJVIylWgLqXNjANBgkqhkiG9w0BAQsFAAOCAQEACZ3PF7Uqu47lplXHP6YlzYL2jL0D28hpj5lGtdha4Muw1m/BjDb0Pu8l0NQ1z3AP6AVcvjNDkQq6Y5jeSz0bwQlealQpYfo7EMXjOidrft1GbqOMFmTBLpLA9SvwYGobSTXWTkJzonqVaTcf80HpMgM2uEhodwTcvz6v1WEfeT/HMjmdIsq4ImrOL9RNrcZG6nWfw0HR3JNOgrbfyEztEI471jHznZ336OEcyX7gQuvHE8tOv5+oD1d7s3Xg1yuFp+Ynh+FfOi3hPCuaHA+7F6fLmzMDLVUBAllugst1C3U+L/paD7tqIa4ka+KNPCbSfwazmJrt4XNiivPR4hwH5g=="] __}

__

|

单元素证书链。   ---|--- 返回以下响应：

    
    
    {
      "access_token" : "dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ==",
      "type" : "Bearer",
      "expires_in" : 1200,
      "authentication" : {
        "username" : "Elasticsearch Test Client",
        "roles" : [ ],
        "full_name" : null,
        "email" : null,
        "metadata" : {
          "pki_dn" : "O=org, OU=Elasticsearch, CN=Elasticsearch Test Client",
          "pki_delegated_by_user" : "test_admin",
          "pki_delegated_by_realm" : "file"
        },
        "enabled" : true,
        "authentication_realm" : {
          "name" : "pki1",
          "type" : "pki"
        },
        "lookup_realm" : {
          "name" : "pki1",
          "type" : "pki"
        },
        "authentication_type" : "realm"
      }
    }

[« Create service account token API](security-api-create-service-token.md)
[Delete application privileges API »](security-api-delete-privilege.md)
