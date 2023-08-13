

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get user privileges API](security-api-get-user-privileges.md) [Grant API
key API »](security-api-grant-api-key.md)

## 获取用户接口

检索有关本机领域中的用户和内置用户的信息。

###Request

"获取/_security/用户"

'获取/_security/用户/<username>'

###Prerequisites

* 要使用此 API，您必须至少具有"read_security"群集权限。

###Description

有关本机域的更多信息，请参阅域和本机用户身份验证。

### 路径参数

`username`

     (Optional, string) An identifier for the user. You can specify multiple usernames as a comma-separated list. If you omit this parameter, the API retrieves information about all users. 

### 响应正文

成功的调用会返回一个用户数组，其中包含用户的 JSON 表示形式。请注意，不包括用户密码。

### 响应码

如果用户未在"本机"领域中定义，则请求404s。

###Examples

要检索本机用户，请向"/_security/用户/"端点提交 GET 请求<username>：

    
    
    GET /_security/user/jacknich
    
    
    {
      "jacknich": {
        "username": "jacknich",
        "roles": [
          "admin", "other_role1"
        ],
        "full_name": "Jack Nicholson",
        "email": "jacknich@example.com",
        "metadata": { "intelligence" : 7 },
        "enabled": true
      }
    }

省略用户名以检索所有用户：

    
    
    GET /_security/user

[« Get user privileges API](security-api-get-user-privileges.md) [Grant API
key API »](security-api-grant-api-key.md)
