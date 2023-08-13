

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Create or update users API](security-api-put-user.md) [Delegate PKI
authentication API »](security-api-delegate-pki-authentication.md)

## 创建服务账号令牌接口

创建服务帐户令牌以进行访问，而无需基本身份验证。

###Request

'POST /_security/service///<namespace><service>credential/token/<token_name>'

'PUT /_security/service///<namespace><service>credential/token/<token_name>'

'POST /_security/service///<namespace><service>credential/token'

###Prerequisites

* 要使用此 API，您必须至少具有"manage_service_account"群集权限。

###Description

成功的创建服务帐户令牌 API 调用会返回一个 JSON 结构，其中包含服务帐户令牌、其名称和机密值。

服务帐户令牌永不过期。如果不再需要它们，则必须主动删除它们。

### 路径参数

`namespace`

     (Required, string) Name of the namespace. 
`service`

     (Required, string) Name of the service name. 
`token_name`

    

(可选，字符串)服务帐户令牌的名称。如果省略，将生成一个随机名称。

令牌名称必须至少为 1 个字符且不超过 256 个字符。它们可以包含字母数字字符("a-z"、"A-Z"、"0-9")、短划线 ("-") 和下划线，但不能以下划线('_')开头。

令牌名称在关联的服务帐户的上下文中必须是唯一的。它们还必须具有全局唯一的完全限定名称，这些名称由服务帐户主体和令牌名称组成，例如"/<namespace><service>/<token-name>"。

###Examples

以下请求创建服务帐户令牌：

    
    
    POST /_security/service/elastic/fleet-server/credential/token/token1

响应包括服务帐户令牌、其名称和机密值：

    
    
    {
      "created": true,
      "token": {
        "name": "token1",
        "value": "AAEAAWVsYXN0aWM...vZmxlZXQtc2VydmVyL3Rva2VuMTo3TFdaSDZ" __}
    }

__

|

用作持有者令牌的机密值 ---|--- 要使用服务帐户令牌，请在请求中包含生成的令牌值，标头为"授权：持有者"：

    
    
    curl -H "Authorization: Bearer AAEAAWVsYXN0aWM...vZmxlZXQtc2VydmVyL3Rva2VuMTo3TFdaSDZ" http://localhost:9200/_cluster/health

如果您的节点将"xpack.security.http.ssl.enabled"设置为"true"，则必须在请求URL中指定"https"。

以下请求使用自动生成的令牌名称创建服务令牌：

    
    
    POST /_security/service/elastic/fleet-server/credential/token

响应包括服务帐户令牌、其自动生成的名称及其密钥值：

    
    
    {
      "created": true,
      "token": {
        "name": "Jk5J1HgBuyBK5TpDrdo4",
        "value": "AAEAAWVsYXN0aWM...vZmxlZXQtc2VydmVyL3Rva2VuMTo3TFdaSDZ"
      }
    }

[« Create or update users API](security-api-put-user.md) [Delegate PKI
authentication API »](security-api-delegate-pki-authentication.md)
