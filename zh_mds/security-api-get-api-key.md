

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Enroll Node API](security-api-node-enrollment.md) [Get application
privileges API »](security-api-get-privileges.md)

## 获取接口密钥信息API

检索一个或多个 API 密钥的信息。

###Request

"获取/_security/api_key"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_own_api_key"或"read_security"群集权限。

    * If you only have the `manage_own_api_key` privilege, this API only returns the API keys that you own.

使用具有"manage_own_api_key"权限的 API 密钥进行身份验证不允许检索经过身份验证的用户自己的密钥。相反，使用基本凭据对用户进行身份验证。

    * If you have `read_security`, `manage_api_key` or greater privileges (including `manage_security`), this API returns all API keys regardless of ownership. 

###Description

可以使用此 API 检索由创建 API 密钥创建的 API 密钥的信息。

### 路径参数

可以在 GETrequest 的查询参数中指定以下参数，这些参数与检索 api 密钥有关：

`id`

     (Optional, string) An API key id. This parameter cannot be used with any of `name`, `realm_name` or `username` are used. 
`name`

     (Optional, string) An API key name. This parameter cannot be used with any of `id`, `realm_name` or `username` are used. It supports prefix search with wildcard. 
`realm_name`

     (Optional, string) The name of an authentication realm. This parameter cannot be used with either `id` or `name` or when `owner` flag is set to `true`. 
`username`

     (Optional, string) The username of a user. This parameter cannot be used with either `id` or `name` or when `owner` flag is set to `true`. 
`owner`

     (Optional, Boolean) A boolean flag that can be used to query API keys owned by the currently authenticated user. Defaults to false. The _realm_name_ or _username_ parameters cannot be specified when this parameter is set to _true_ as they are assumed to be the currently authenticated ones. 
`with_limited_by`

     (Optional, Boolean) A boolean flag to return the snapshot of the owner user's role descriptors associated with the API key. An API key's actual permission is the intersection of its [assigned role descriptors](security-api-create-api-key.html#api-key-role-descriptors) and the owner user's role descriptors (effectively limited by it). An API key must have `manage_api_key` or higher privileges to retrieve the limited-by role descriptors of any API key, including itself. 

当没有指定任何参数"id"，"name"，"用户名"和"realm_name"，并且"所有者"设置为false时，如果用户获得授权，它将检索所有API密钥。如果用户无权检索其他用户的 API 密钥，则将返回错误。

###Examples

如果按如下方式创建 API 密钥：

    
    
    POST /_security/api_key
    {
      "name": "my-api-key",
      "role_descriptors": {},
      "metadata": {
        "application": "myapp"
      }
    }

成功的调用会返回提供 API 密钥信息的 JSON 结构。例如：

    
    
    {
      "id":"VuaCfGcBCdbkQm-e5aOx",
      "name":"my-api-key",
      "api_key":"ui2lp2axTNmsyakw9tvNnw",
      "encoded": "VnVhQ2ZHY0JDZGJrUW0tZTVhT3g6dWkybHAyYXhUTm1zeWFrdzl0dk5udw=="
    }

您可以使用以下示例按 ID 检索 API 密钥：

    
    
    GET /_security/api_key?id=VuaCfGcBCdbkQm-e5aOx&with_limited_by=true

成功的调用会返回一个 JSON 结构，其中包含 API 密钥的信息：

    
    
    {
      "api_keys": [ __{
          "id": "VuaCfGcBCdbkQm-e5aOx", __"name": "my-api-key", __"creation": 1548550550158, __"expiration": 1548551550158, __"invalidated": false, __"username": "myuser", __"realm": "native1", __"metadata": { __"application": "myapp"
          },
          "role_descriptors": { }, __"limited_by": [ __{
              "role-power-user": {
                "cluster": [
                  "monitor"
                ],
                "indices": [
                  {
                    "names": [
                      "*"
                    ],
                    "privileges": [
                      "read"
                    ],
                    "allow_restricted_indices": false
                  }
                ],
                "applications": [ ],
                "run_as": [ ],
                "metadata": { },
                "transient_metadata": {
                  "enabled": true
                }
              }
            }
          ]
        }
      ]
    }

__

|

为此请求检索的 API 密钥的列表。   ---|---    __

|

API 密钥的 ID __

|

API 密钥的名称 __

|

API 密钥的创建时间(以毫秒为单位) __

|

API 密钥的可选过期时间(以毫秒为单位) __

|

API 密钥的失效状态。如果密钥已失效，则其值为"true"。否则，它是"假的"。   __

|

为其创建此 API 密钥的主体 __

|

为其创建此 API 密钥的主体的领域名称 __

|

API 密钥的元数据 __

|

创建或上次更新时分配给此 API 密钥的角色描述符。空角色描述符表示 API 密钥继承所有者用户的权限。   __

|

所有者用户与 API 密钥关联的权限。它是在创建和后续更新时捕获的时间点快照。API 密钥的有效权限是其分配的权限和所有者用户权限的交集。   您可以使用以下示例按名称检索 API 密钥：

    
    
    GET /_security/api_key?name=my-api-key

API 密钥名称支持使用通配符进行前缀搜索：

    
    
    GET /_security/api_key?name=my-*

以下示例检索"native1"域的所有 API 密钥：

    
    
    GET /_security/api_key?realm_name=native1

以下示例检索 allrealms 中用户"myuser"的所有 API 密钥：

    
    
    GET /_security/api_key?username=myuser

以下示例检索当前经过身份验证的用户拥有的所有 API 密钥：

    
    
    GET /_security/api_key?owner=true

以下示例检索所有 API 密钥(如果用户有权这样做)：

    
    
    GET /_security/api_key

以下创建 API 密钥

    
    
    POST /_security/api_key
    {
      "name": "my-api-key-1",
      "metadata": {
        "application": "my-application"
      }
    }

以下示例检索由指定的"id"标识的 API 密钥(如果该密钥由当前经过身份验证的用户拥有)：

    
    
    GET /_security/api_key?id=VuaCfGcBCdbkQm-e5aOx&owner=true

最后，以下示例立即检索"native1"领域中用户"myuser"的所有 API 密钥：

    
    
    GET /_security/api_key?username=myuser&realm_name=native1

成功的调用会返回一个 JSON 结构，其中包含检索到的一个或多个 API 密钥的信息。

    
    
    {
      "api_keys": [
        {
          "id": "0GF5GXsBCXxz2eDxWwFN",
          "name": "hadoop_myuser_key",
          "creation": 1548550550158,
          "expiration": 1548551550158,
          "invalidated": false,
          "username": "myuser",
          "realm": "native1",
          "metadata": {
            "application": "myapp"
          },
          "role_descriptors": {
            "role-a": {
              "cluster": [
                "monitor"
              ],
              "indices": [
                {
                  "names": [
                    "index-a"
                  ],
                  "privileges": [
                    "read"
                  ],
                  "allow_restricted_indices": false
                }
              ],
              "applications": [ ],
              "run_as": [ ],
              "metadata": { },
              "transient_metadata": {
                "enabled": true
              }
            }
          }
        },
        {
          "id": "6wHJmcQpReKBa42EHV5SBw",
          "name": "api-key-name-2",
          "creation": 1548550550158,
          "invalidated": false,
          "username": "user-y",
          "realm": "realm-2",
          "metadata": {},
          "role_descriptors": { }
        }
      ]
    }

[« Enroll Node API](security-api-node-enrollment.md) [Get application
privileges API »](security-api-get-privileges.md)
