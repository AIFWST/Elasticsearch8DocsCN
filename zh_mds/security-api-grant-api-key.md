

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get users API](security-api-get-user.md) [Has privileges API »](security-
api-has-privileges.md)

## 授予 API 密钥接口

代表其他用户创建 API 密钥。

###Request

"发布/_security/api_key/授予"

###Prerequisites

* 要使用此 API，您必须具有"grant_api_key"群集权限。

###Description

此 API 类似于创建 API 密钥，但它为与运行 API 的用户不同的用户创建的 API 密钥。

调用方必须具有将代表其创建 API 密钥的用户的身份验证凭据(访问令牌或用户名和密码)。如果没有该用户的凭据，则无法使用此 API 创建 API 密钥。

为其提供身份验证凭据的用户可以选择"以"(模拟)其他用户身份运行。在这种情况下，将代表模拟用户创建 API 密钥。

此 API 适用于需要为最终用户创建和管理 API 密钥的应用程序，但不能保证这些用户有权代表自己创建 API 密钥(请参阅先决条件)。API 密钥由自动启用的 Elasticsearch API 密钥服务创建。

成功的授权 API 密钥 API 调用会返回一个 JSON 结构，其中包含 API 密钥、其唯一 ID 和名称。如果适用，它还返回 API 密钥的到期信息(以毫秒为单位)。

默认情况下，API 密钥永不过期。您可以在创建 API 密钥时指定过期信息。

有关与 API 密钥服务相关的配置设置，请参阅 API 密钥服务设置。

### 请求正文

可以在 POST 请求的正文中指定以下参数：

`access_token`

     (Required*, string) The user's access token. If you specify the `access_token` grant type, this parameter is required. It is not valid with other grant types. 
`api_key`

    

(必填，对象)定义 API 密钥。

`expiration`

     (Optional, string) Expiration time for the API key. By default, API keys never expire. 
`name`

     (Required, string) Specifies the name for this API key. 
`role_descriptors`

     (Optional, object) The role descriptors for this API key. This parameter is optional. When it is not specified or is an empty array, the API key has a point in time snapshot of permissions of the specified user or access token. If you supply role descriptors, the resultant permissions are an intersection of API keys permissions and the permissions of the user or access token. The structure of a role descriptor is the same as the request for [create API keys API](security-api-create-api-key.html#api-key-role-descriptors). 
`metadata`

     (Optional, object) Arbitrary metadata that you want to associate with the API key. It supports nested data structure. Within the `metadata` object, keys beginning with `_` are reserved for system usage. 

`grant_type`

    

(必需，字符串)赠款的类型。支持的授权类型包括："access_token"、"密码"。

`access_token`

     (Required*, string) In this type of grant, you must supply an access token that was created by the Elasticsearch token service. For more information, see [Get token](security-api-get-token.html "Get token API") and [Encrypt HTTP client communications for Elasticsearch](security-basic-setup-https.html#encrypt-http-communication "Encrypt HTTP client communications for Elasticsearch"). 
`password`

     In this type of grant, you must supply the user ID and password for which you want to create the API key. 

`password`

     (Optional*, string) The user's password. If you specify the `password` grant type, this parameter is required. It is not valid with other grant types. 
`username`

     (Optional*, string) The user name that identifies the user. If you specify the `password` grant type, this parameter is required. It is not valid with other grant types. 
`run_as`

     (Optional, string) The name of the user to be [impersonated](run-as-privilege.html "Submitting requests on behalf of other users"). 

###Examples

    
    
    POST /_security/api_key/grant
    {
      "grant_type": "password",
      "username" : "test_admin",
      "password" : "x-pack-test-password",
      "api_key" : {
        "name": "my-api-key",
        "expiration": "1d",
        "role_descriptors": {
          "role-a": {
            "cluster": ["all"],
            "indices": [
              {
              "names": ["index-a*"],
              "privileges": ["read"]
              }
            ]
          },
          "role-b": {
            "cluster": ["all"],
            "indices": [
              {
              "names": ["index-b*"],
              "privileges": ["all"]
              }
            ]
          }
        },
        "metadata": {
          "application": "my-application",
          "environment": {
             "level": 1,
             "trusted": true,
             "tags": ["dev", "staging"]
          }
        }
      }
    }

提供凭据的用户("test_admin")可以"以"其他用户("test_user")身份运行。API 密钥将授予模拟用户("test_user")。

    
    
    POST /_security/api_key/grant
    {
      "grant_type": "password",
      "username" : "test_admin",  __"password" : "x-pack-test-password", __"run_as": "test_user", __"api_key" : {
        "name": "another-api-key"
      }
    }

__

|

为其提供凭据并执行"运行身份"的用户。   ---|---    __

|

上述用户的凭据 __

|

将为其创建 API 密钥的模拟用户。   « 获取用户 API 具有权限 API »