

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Query API key information API](security-api-query-api-key.md) [Bulk
update API keys API »](security-api-bulk-update-api-keys.md)

## 更新接口密钥接口

###Request

"放/_security/api_key/<id>"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_own_api_key"群集权限。用户只能更新他们创建或授予他们的 API 密钥。要更新其他用户的 API 密钥，请使用"run_as"功能代表其他用户提交请求。

不能使用 API 密钥作为此 API 的身份验证凭据。要更新 API 密钥，需要所有者用户的凭据。

###Description

使用此 API 更新由创建 API 密钥创建的 API 密钥或授予 API 密钥 API。如果需要将相同的更新应用于多个 API 密钥，则可以使用批量更新 API 密钥来减少开销。

无法更新过期的 API 密钥或因使 API 密钥失效而失效的 API 密钥。

此 API 支持更新 API 密钥的访问范围和元数据。API 密钥的访问范围派生自您在请求中指定的"role_descriptors"，以及请求时所有者用户权限的快照。所有者权限的快照会在每次调用时自动更新。

如果未在请求中指定"role_descriptors"，则对此 API 的调用可能仍会更改 API 密钥的访问范围。如果所有者用户的权限自创建或上次修改 API 密钥以来发生更改，则可能会发生此更改。

### 路径参数

`id`

     (Required, string) The ID of the API key to update. 

### 请求正文

您可以在请求正文中指定以下参数，这是可选的。

`role_descriptors`

     (Optional, object) The role descriptors to assign to this API key. The API key's effective permissions are an intersection of its assigned privileges and the point in time snapshot of permissions of the owner user. You can assign new privileges by specifying them in this parameter. To remove assigned privileges, you can supply an empty `role_descriptors` parameter, i.e., an empty object `{}`. If an API key has no assigned privileges, it inherits the owner user's full permissions. The snapshot of the owner's permissions is always updated, whether you supply the `role_descriptors` parameter or not. The structure of a role descriptor is the same as the request for the [create API keys API](security-api-create-api-key.html#api-key-role-descriptors). 
`metadata`

     (Optional, object) Arbitrary metadata that you want to associate with the API key. It supports nested data structure. Within the `metadata` object, top-level keys beginning with `_` are reserved for system usage. When specified, this fully replaces metadata previously associated with the API key. 

### 响应正文

`updated`

     (boolean) If `true`, the API key was updated. If `false`, the API key didn't change because no change was detected. 

###Examples

如果按如下方式创建 API 密钥：

    
    
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

成功的调用会返回提供 API 密钥信息的 JSON 结构。例如：

    
    
    {
      "id": "VuaCfGcBCdbkQm-e5aOx",
      "name": "my-api-key",
      "api_key": "ui2lp2axTNmsyakw9tvNnw",
      "encoded": "VnVhQ2ZHY0JDZGJrUW0tZTVhT3g6dWkybHAyYXhUTm1zeWFrdzl0dk5udw=="
    }

对于以下示例，假定所有者用户的权限为：

    
    
    {
      "cluster": ["all"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["all"]
        }
      ]
    }

以下示例更新上面创建的 API 密钥，为其分配新的角色描述符和元数据：

    
    
    PUT /_security/api_key/VuaCfGcBCdbkQm-e5aOx
    {
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
      "updated": true
    }

更新后 API 密钥的有效权限将是提供的角色描述符和所有者用户权限的交集：

    
    
    {
      "indices": [
        {
          "names": ["*"],
          "privileges": ["write"]
        }
      ]
    }

以下示例删除 API 密钥以前分配的权限，使其继承所有者用户的完全权限。

    
    
    PUT /_security/api_key/VuaCfGcBCdbkQm-e5aOx
    {
      "role_descriptors": {}
    }

返回响应：

    
    
    {
      "updated": true
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

以下请求自动更新与 API 密钥关联的用户权限的快照：

    
    
    PUT /_security/api_key/VuaCfGcBCdbkQm-e5aOx

返回响应：

    
    
    {
      "updated": true
    }

导致 API 密钥具有以下有效权限：

    
    
    {
      "cluster": ["manage_security"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["read"]
        }
      ]
    }

[« Query API key information API](security-api-query-api-key.md) [Bulk
update API keys API »](security-api-bulk-update-api-keys.md)
