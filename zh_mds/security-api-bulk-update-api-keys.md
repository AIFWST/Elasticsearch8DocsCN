

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Update API key API](security-api-update-api-key.md) [SAML prepare
authentication API »](security-api-saml-prepare-authentication.md)

## 批量更新 API 密钥API

###Request

"发布/_security/api_key/_bulk_update"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_own_api_key"群集权限。用户只能更新他们创建或授予他们的 API 密钥。要更新其他用户的 API 密钥，请使用"run_as"功能代表其他用户提交请求。

不能使用 API 密钥作为此 API 的身份验证凭据。要更新 API 密钥，需要所有者用户的凭据。

###Description

此 API 类似于更新单个 API 密钥，但允许您在一个 API 调用中将**相同的更新**应用于多个 API 密钥。与进行单个更新相比，此操作可以大大提高性能。

无法更新过期或无效的 API 密钥。

此 API 支持更新 API 密钥访问范围和元数据。每个 API 密钥的访问范围派生自您在请求中指定的"role_descriptors"，以及请求时所有者用户权限的快照。所有者权限的快照会在每次调用时自动更新。

如果未在请求中指定"role_descriptors"，则对此 API 的调用仍可能更改 API 密钥的访问范围。如果所有者用户的权限在创建或上次修改 APIkey 后发生更改，则可能会发生此更改。

### 请求正文

您可以在请求正文中指定以下参数。

`ids`

     (Required, list) The IDs of the API keys to update. 

`role_descriptors`

     (Optional, object) The role descriptors to assign to the API keys. An API key's effective permissions are an intersection of its assigned privileges and the point-in-time snapshot of permissions of the owner user. You can assign new privileges by specifying them in this parameter. To remove assigned privileges, supply the `role_descriptors` parameter as an empty object `{}`. If an API key has no assigned privileges, it inherits the owner user's full permissions. The snapshot of the owner's permissions is always updated, whether you supply the `role_descriptors` parameter or not. The structure of a role descriptor is the same as the request for the [create API keys API](security-api-create-api-key.html#api-key-role-descriptors). 
`metadata`

     (Optional, object) Arbitrary, nested metadata to associate with the API keys. 

在"元数据"对象中，以下划线('_')开头的顶级键保留供系统使用。使用此参数指定的任何信息都将完全替换以前与 API 密钥关联的元数据。

### 响应正文

成功的请求会返回一个 JSON 结构，其中包含所有更新的 API 密钥的 ID、已具有请求的更改且不需要更新的 API 密钥的 ID，以及任何失败更新的错误详细信息。

###Examples

对于以下示例，假设用户创建了两个 API 密钥。用户创建第一个 API 密钥：

    
    
    POST /_security/api_key
    {
      "name": "my-api-key",
      "role_descriptors": {
        "role-a": {
          "cluster": ["all"],
          "indices": [
            {
              "names": ["index-a*"],
              "privileges": ["read"]
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

这将生成包含以下 API 密钥信息的响应。

    
    
    {
      "id": "VuaCfGcBCdbkQm-e5aOx",
      "name": "my-api-key",
      "api_key": "ui2lp2axTNmsyakw9tvNnw",
      "encoded": "VnVhQ2ZHY0JDZGJrUW0tZTVhT3g6dWkybHAyYXhUTm1zeWFrdzl0dk5udw=="
    }

用户创建第二个 API 密钥：

    
    
    POST /_security/api_key
    {
      "name": "my-other-api-key",
      "metadata": {
        "application": "my-application",
        "environment": {
           "level": 2,
           "trusted": true,
           "tags": ["dev", "staging"]
        }
      }
    }

生成以下 API 密钥信息。

    
    
    {
      "id": "H3_AhoIBA9hmeQJdg7ij",
      "name": "my-other-api-key",
      "api_key": "134G4ilmT_uGWXHRfJfXXA",
      "encoded": "SDNfQWhvSUJBOWhtZVFKZGc3aWo6MTM0RzRpbG1UX3VHV1hIUmZKZlhYQQ=="
    }

此外，假设所有者用户的权限为：

    
    
    {
      "cluster": ["all"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["all"]
        }
      ]
    }

以下示例更新上面创建的 API 密钥，为其分配新角色描述符和元数据。

    
    
    POST /_security/api_key/_bulk_update
    {
      "ids": [
        "VuaCfGcBCdbkQm-e5aOx",
        "H3_AhoIBA9hmeQJdg7ij"
      ],
      "role_descriptors": {
        "role-a": {
          "indices": [
            {
              "names": ["*"],
              "privileges": ["write"]
            }
          ]
        }
      },
      "metadata": {
        "environment": {
           "level": 2,
           "trusted": true,
           "tags": ["production"]
        }
      }
    }

成功的调用会返回一个 JSON 结构，指示 API 密钥已更新：

    
    
    {
      "updated": [
        "VuaCfGcBCdbkQm-e5aOx",
        "H3_AhoIBA9hmeQJdg7ij"
      ],
      "noops": []
    }

更新后，两个 API 密钥的有效权限将是提供的角色描述符和所有者用户权限的交集：

    
    
    {
      "indices": [
        {
          "names": ["*"],
          "privileges": ["write"]
        }
      ]
    }

以下示例删除 API 密钥以前分配的权限，使其继承所有者用户的完全权限。

    
    
    POST /_security/api_key/_bulk_update
    {
      "ids": [
        "VuaCfGcBCdbkQm-e5aOx",
        "H3_AhoIBA9hmeQJdg7ij"
      ],
      "role_descriptors": {}
    }

返回响应：

    
    
    {
      "updated": [
        "VuaCfGcBCdbkQm-e5aOx",
        "H3_AhoIBA9hmeQJdg7ij"
      ],
      "noops": []
    }

更新后 API 密钥的有效权限将与所有者用户的有效权限相同：

    
    
    {
      "cluster": ["all"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["all"]
        }
      ]
    }

对于下一个示例，假设所有者用户的权限已从原始权限更改为：

    
    
    {
      "cluster": ["manage_security"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["read"]
        }
      ]
    }

以下请求自动更新与两个 API 密钥关联的用户权限的快照。

    
    
    POST /_security/api_key/_bulk_update
    {
      "ids": [
        "VuaCfGcBCdbkQm-e5aOx",
        "H3_AhoIBA9hmeQJdg7ij"
      ]
    }

返回响应：

    
    
    {
      "updated": [
        "VuaCfGcBCdbkQm-e5aOx",
        "H3_AhoIBA9hmeQJdg7ij"
      ],
      "noops": []
    }

为两个 API 密钥生成以下有效权限：

    
    
    {
      "cluster": ["manage_security"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["read"]
        }
      ]
    }

如果任何 API 密钥更新失败，错误详细信息将包含在"错误"字段中。例如：

    
    
    {
      "updated": ["VuaCfGcBCdbkQm-e5aOx"],
      "noops": [],
      "errors": { __"count": 3,
        "details": {
           "g_PqP4IBcBaEQdwM5-WI": { __"type": "resource_not_found_exception",
             "reason": "no API key owned by requesting user found for ID [g_PqP4IBcBaEQdwM5-WI]"
           },
           "OM4cg4IBGgpHBfLerY4B": {
             "type": "illegal_argument_exception",
             "reason": "cannot update invalidated API key [OM4cg4IBGgpHBfLerY4B]"
           },
           "Os4gg4IBGgpHBfLe2I7j": {
             "type": "exception",
             "reason": "bulk request execution failure",
             "caused_by": { __"type" : "version_conflict_engine_exception",
               "reason" : "[1]: version conflict, required seqNo [1], primary term [1]. current document has seqNo [2] and primary term [1]"
             }
           }
        }
      }
    }

__

|

当"count"为 0 时，响应中不存在此字段。   ---|---    __

|

发生错误的 API 密钥的 ID。   __

|

错误详细信息还可能包括"caused_by"字段。   « 更新 API 密钥 API SAML 准备身份验证 API »