

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« SSL certificate API](security-api-ssl.md) [Disable user profile API
»](security-api-disable-user-profile.md)

## 激活用户配置文件API

用户配置文件功能仅供 Kibana 和 Elastic 的可观测性、企业级搜索和 Elastic 安全解决方案使用。个人用户和外部应用程序不应直接调用此 API。Elastic 保留在未来版本中更改或删除此功能的权利，恕不另行通知。

代表其他用户创建或更新用户配置文件。

###Request

"发布/_security/个人资料/_activate"

###Prerequisites

* 要使用此 API，您必须具有"manage_user_profile"群集权限。

###Description

激活用户配置文件 API 使用从用户的身份验证对象中提取的信息(包括"用户名"、"full_name"、"角色"和身份验证领域)为最终用户创建或更新配置文件文档。

更新配置文件文档时，如果文档已禁用，API 将启用该文档。任何更新都不会更改"标签"或"数据"字段的现有内容。

此 API 仅供需要为最终用户创建或更新配置文件的应用程序(例如 Kibana)使用。

调用应用程序必须具有配置文件文档所针对的用户的"access_token"或"用户名"和"密码"的组合。

### 请求正文

`access_token`

     (Required*, string) The user's access token. If you specify the `access_token` grant type, this parameter is required. It is not valid with other grant types. 
`grant_type`

    

(必需，字符串)赠款的类型。

"grant_type"的有效值

`access_token`

     (Required*, string) In this type of grant, you must supply an access token that was created by the Elasticsearch token service. For more information, see [Get token](security-api-get-token.html "Get token API") and [Token service settings](security-settings.html#token-service-settings "Token service settings"). 
`password`

     (Required*, string) In this type of grant, you must supply the `username` and `password` for the user that you want to create the API key for. 

`password`

     (Optional*, string) The user's password. If you specify the `password` grant type, this parameter is required. It is not valid with other grant types. 
`username`

     (Optional*, string) The username that identifies the user. If you specify the `password` grant type, this parameter is required. It is not valid with other grant types. 

*表示在某些(但不是所有)情况下都需要该设置。

### 响应正文

成功的激活用户配置文件 API 调用将返回一个 JSON 结构，其中包含配置文件唯一 ID、用户信息、操作时间戳和版本控制编号。

###Examples

    
    
    POST /_security/profile/_activate
    {
      "grant_type": "password",
      "username" : "jacknich",
      "password" : "l0ng-r4nd0m-p@ssw0rd"
    }

API 返回以下响应：

    
    
    {
      "uid": "u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0",
      "enabled": true,
      "last_synchronized": 1642650651037,
      "user": {
        "username": "jacknich",
        "roles": [
          "admin", "other_role1"
        ],
        "realm_name": "native",
        "full_name": "Jack Nicholson",
        "email": "jacknich@example.com"
      },
      "labels": {},
      "data": {},
      "_doc": {
        "_primary_term": 88,
        "_seq_no": 66
      }
    }

[« SSL certificate API](security-api-ssl.md) [Disable user profile API
»](security-api-disable-user-profile.md)
