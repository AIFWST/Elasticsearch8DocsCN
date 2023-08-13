

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Has privileges API](security-api-has-privileges.md) [Invalidate token API
»](security-api-invalidate-token.md)

## 使 API 密钥接口失效

使一个或多个 API 密钥失效。

###Request

"删除/_security/api_key"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_api_key"或"manage_own_api_key"群集权限。"manage_api_key"权限允许删除任何 API 密钥。"manage_own_api_key"仅允许删除用户拥有的 API 密钥。此外，使用"manage_own_api_key"权限，必须以以下三种格式之一发出无效请求：

    1. Set the parameter `owner=true`
    2. Or, set both `username` and `realm_name` to match the user's identity. 
    3. Or, if the request is issued by an API key, i.e. an API key invalidates itself, specify its ID in the `ids` field. 

###Description

创建 API 密钥创建的 API 密钥可以使用此 API 失效。

### 请求正文

可以在 DELETE 请求的正文中指定以下参数，这些参数与使 api 密钥失效有关：

`ids`

     (Optional, array of string) A list of API key ids. This parameter cannot be used when any of `name`, `realm_name`, `username` are used 
`name`

     (Optional, string) An API key name. This parameter cannot be used with any of `ids`, `realm_name` or `username` are used. 
`realm_name`

     (Optional, string) The name of an authentication realm. This parameter cannot be used with either `ids` or `name` or when `owner` flag is set to `true`. 
`username`

     (Optional, string) The username of a user. This parameter cannot be used with either `ids` or `name` or when `owner` flag is set to `true`. 
`owner`

     (Optional, Boolean) A boolean flag that can be used to query API keys owned by the currently authenticated user. Defaults to false. The _realm_name_ or _username_ parameters cannot be specified when this parameter is set to _true_ as they are assumed to be the currently authenticated ones. 

如果"所有者"为"假"(默认值)，则必须至少指定"id"、"名称"、"用户名"和"realm_name"之一。

### 响应正文

成功的调用会返回一个 JSON 结构，其中包含已失效的 API 密钥的 ID、已失效的 API 密钥的 ID，以及可能出现的使特定 api 密钥失效时遇到的错误列表。

###Examples

如果按如下方式创建 API 密钥：

    
    
    POST /_security/api_key
    {
      "name": "my-api-key"
    }

成功的调用会返回提供 API 密钥信息的 JSON 结构。例如：

    
    
    {
      "id": "VuaCfGcBCdbkQm-e5aOx",
      "name": "my-api-key",
      "api_key": "ui2lp2axTNmsyakw9tvNnw",
      "encoded": "VnVhQ2ZHY0JDZGJrUW0tZTVhT3g6dWkybHAyYXhUTm1zeWFrdzl0dk5udw=="
    }

以下示例立即使由指定的"ids"标识的 API 密钥失效：

    
    
    DELETE /_security/api_key
    {
      "ids" : [ "VuaCfGcBCdbkQm-e5aOx" ]
    }

以下示例立即使由指定的"名称"标识的 API 密钥失效：

    
    
    DELETE /_security/api_key
    {
      "name" : "my-api-key"
    }

以下示例立即使"native1"领域的所有 API 密钥失效：

    
    
    DELETE /_security/api_key
    {
      "realm_name" : "native1"
    }

以下示例立即使所有领域中用户"myuser"的所有 API 密钥失效：

    
    
    DELETE /_security/api_key
    {
      "username" : "myuser"
    }

以下示例使由指定的"ids"标识的 API 密钥失效，如果该密钥立即由当前经过身份验证的用户拥有：

    
    
    DELETE /_security/api_key
    {
      "ids" : ["VuaCfGcBCdbkQm-e5aOx"],
      "owner" : "true"
    }

以下示例立即使当前经过身份验证的用户拥有的所有 API 密钥失效：

    
    
    DELETE /_security/api_key
    {
      "owner" : "true"
    }

最后，以下示例立即使"native1"领域中用户"myuser"的所有 API 密钥失效：

    
    
    DELETE /_security/api_key
    {
      "username" : "myuser",
      "realm_name" : "native1"
    }
    
    
    {
      "invalidated_api_keys": [ __"api-key-id-1"
      ],
      "previously_invalidated_api_keys": [ __"api-key-id-2",
        "api-key-id-3"
      ],
      "error_count": 2, __"error_details": [ __{
          "type": "exception",
          "reason": "error occurred while invalidating api keys",
          "caused_by": {
            "type": "illegal_argument_exception",
            "reason": "invalid api key id"
          }
        },
        {
          "type": "exception",
          "reason": "error occurred while invalidating api keys",
          "caused_by": {
            "type": "illegal_argument_exception",
            "reason": "invalid api key id"
          }
        }
      ]
    }

__

|

作为此请求的一部分而失效的 API 密钥的 ID。   ---|---    __

|

已失效的 API 密钥的 ID。   __

|

使 API 密钥失效时遇到的错误数。   __

|

有关这些错误的详细信息。当"error_count"为 0 时，响应中不存在此字段。   « 具有特权 API 使令牌 API 无效»