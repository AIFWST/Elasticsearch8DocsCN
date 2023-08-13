

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Authenticate API](security-api-authenticate.md) [Clear cache API
»](security-api-clear-cache.md)

## 更改密码接口

更改本机域中的用户和内置用户的密码。

###Request

"发布/_security/用户/_password"

"发布/_security/用户/<username>/_password"

###Prerequisites

*每个用户都可以更改自己的密码。具有"manage_security"权限的用户可以更改其他用户的密码。

###Description

您可以使用创建用户 API 更新除用户的"用户名"和"密码"之外的所有内容。此接口更改用户的密码。

有关本机域的更多信息，请参阅域和本机用户身份验证。

### 路径参数

`username`

     (Optional, string) The user whose password you want to change. If you do not specify this parameter, the password is changed for the current user. 

### 请求正文

`password`

    

(字符串)新密码值。密码长度必须至少为 6 个字符。

需要"密码"或"password_hash"之一。

`password_hash`

    

(字符串)新密码值的 _hash_。这必须使用为密码存储配置的相同哈希算法生成。有关详细信息，请参阅用户缓存和密码哈希算法中的"xpack.security.authc.password_hashing.algorithm"设置的说明。

使用此参数允许客户端出于性能和/或机密性原因对密码进行预哈希处理。

"password"参数和"password_hash"参数不能在同一请求中使用。

###Examples

以下示例更新"jacknich"用户的密码：

    
    
    POST /_security/user/jacknich/_password
    {
      "password" : "new-test-password"
    }

成功的调用会返回一个空的 JSON 结构。

    
    
    {}

[« Authenticate API](security-api-authenticate.md) [Clear cache API
»](security-api-clear-cache.md)
