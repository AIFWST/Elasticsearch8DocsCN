

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« Defining roles](defining-roles.md) [Security privileges »](security-
privileges.md)

## 角色限制

角色限制可用于指定角色应有效的条件。如果不满足条件，该角色将被禁用，这将导致访问被拒绝。不指定限制意味着角色不受限制，因此始终有效。这是默认行为。

目前，仅 API 密钥支持角色限制，但 API 密钥只能具有一个角色描述符。

###Workflows

工作流允许将角色限制为仅在调用某些 REST API 时有效。调用工作流不允许的 REST API 将导致角色被禁用。以下部分列出了可以将角色限制为的工作流：

`search_application_query`

     This workflow restricts the role to the [Search Application Search API](search-application-search.html "Search Application Search") only. 

工作流名称区分大小写。

####Examples

以下示例创建一个 API 密钥，该密钥限制为"search_application_query"工作流，该工作流仅允许调用搜索应用程序搜索 API：

    
    
    POST /_security/api_key
    {
      "name": "my-restricted-api-key",
      "role_descriptors": {
        "my-restricted-role-descriptor": {
          "indices": [
            {
              "names": ["my-search-app"],
              "privileges": ["read"]
            }
          ],
          "restriction":  {
            "workflows": ["search_application_query"]
          }
        }
      }
    }

[« Defining roles](defining-roles.md) [Security privileges »](security-
privileges.md)
