

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Create or update roles API](security-api-put-role.md) [Create service
account token API »](security-api-create-service-token.md)

## 创建或更新用户接口

在本机域中添加和更新用户。这些用户通常称为_native users_。

###Request

"发布/_security/用户/<username>"

'把/_security/用户/<username>'

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

添加新用户需要"密码"，但在更新现有用户时是可选的。要在不更新任何其他字段的情况下更改用户的密码，请使用更改密码 API。

有关本机域的更多信息，请参阅域和本机用户身份验证。

### 路径参数

`username`

    

(必需，字符串)用户的标识符。

用户名必须至少为 1 个字符且不超过 507 个字符。它们可以包含字母数字字符("a-z"、"A-Z"、"0-9")、空格、标点符号和基本拉丁语 (ASCII) 块中的可打印符号)。不允许使用前导或尾随空格。

### 查询参数

`refresh`

     (string) One of `true`, `false`, or `wait_for`. These values have the same meaning as in the [Index API](docs-refresh.html "?refresh"), but the default value for this API (Put User) is `true`. 

### 请求正文

可以在 POST 或 PUTrequest 的正文中指定以下参数：

`enabled`

     (Boolean) Specifies whether the user is enabled. The default value is `true`. 
`email`

     (string) The email of the user. 
`full_name`

     (string) The full name of the user. 
`metadata`

     (object) Arbitrary metadata that you want to associate with the user. 
`password`

    

(必填*，字符串)用户的密码。密码长度必须至少为 6 个字符。

添加用户时，需要"密码"或"password_hash"之一。更新现有用户时，密码是可选的，因此可以在不修改用户密码的情况下更新用户的其他字段(例如其角色)。

`password_hash`

    

(字符串)用户密码的 _hash_。这必须使用与为密码存储配置的相同哈希算法生成。有关详细信息，请参阅用户缓存和密码哈希算法中的"xpack.security.authc.password_hashing.algorithm"设置的说明。

使用此参数允许客户端出于性能和/或机密性原因对密码进行预哈希处理。

"password"参数和"password_hash"参数不能在同一请求中使用。

`roles`

     (Required, list) A set of roles the user has. The roles determine the user's access permissions. To create a user without any roles, specify an empty list: `[]`. 

*表示在某些(但不是所有)情况下都需要该设置。

###Examples

以下示例创建一个用户"jacknich"：

    
    
    POST /_security/user/jacknich
    {
      "password" : "l0ng-r4nd0m-p@ssw0rd",
      "roles" : [ "admin", "other_role1" ],
      "full_name" : "Jack Nicholson",
      "email" : "jacknich@example.com",
      "metadata" : {
        "intelligence" : 7
      }
    }

成功的调用会返回一个 JSON 结构，该结构显示用户是否已创建或更新。

    
    
    {
      "created": true __}

__

|

更新现有用户时，"已创建"设置为 false。   ---|--- 添加用户后，可以对该用户的请求进行身份验证。例如：

    
    
    curl -u jacknich:l0ng-r4nd0m-p@ssw0rd http://localhost:9200/_cluster/health

[« Create or update roles API](security-api-put-role.md) [Create service
account token API »](security-api-create-service-token.md)
