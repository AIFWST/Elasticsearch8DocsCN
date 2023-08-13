

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Security APIs](security-api.md) [Change passwords API »](security-api-
change-password.md)

## 认证接口

使您能够提交具有基本身份验证标头的请求，以对用户进行身份验证并检索有关经过身份验证的用户的信息。

###Request

"获取/_security/_authenticate"

###Description

成功的调用会返回一个 JSON 结构，该结构显示用户信息，例如其用户名、分配给用户的角色、任何已分配的元数据以及有关对用户进行身份验证和授权的领域的信息。

### 响应码

如果无法对用户进行身份验证，此 API 将返回 401 状态代码。

###Examples

要对用户进行身份验证，请向"/_security/_authenticate"端点提交 GET 请求：

    
    
    GET /_security/_authenticate

以下示例输出提供有关"rdeniro"用户的信息：

    
    
    {
      "username": "rdeniro",
      "roles": [
        "admin"
      ],
      "full_name": null,
      "email":  null,
      "metadata": { },
      "enabled": true,
      "authentication_realm": {
        "name" : "file",
        "type" : "file"
      },
      "lookup_realm": {
        "name" : "file",
        "type" : "file"
      },
      "authentication_type": "realm"
    }

[« Security APIs](security-api.md) [Change passwords API »](security-api-
change-password.md)
