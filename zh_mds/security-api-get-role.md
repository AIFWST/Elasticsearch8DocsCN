

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get role mappings API](security-api-get-role-mapping.md) [Get service
accounts API »](security-api-get-service-accounts.md)

## 获取角色接口

检索本机领域中的角色。

###Request

"获取/_security/角色"

'获取/_security/角色/<name>"

###Prerequisites

* 要使用此 API，您必须至少具有"read_security"群集权限。

###Description

角色管理 API 通常是管理角色的首选方式，而不是使用基于文件的角色管理。获取角色 API 无法检索角色文件中定义的角色。

### 路径参数

`name`

     (Optional, string) The name of the role. You can specify multiple roles as a comma-separated list. If you do not specify this parameter, the API returns information about all roles. 

### 响应正文

成功的调用会返回一个角色数组，其中包含角色的 JSON 表示形式。

### 响应码

如果未在本机域中定义角色，则请求将返回 404。

###Examples

以下示例检索有关本机领域中"my_admin_role"角色的信息：

    
    
    GET /_security/role/my_admin_role
    
    
    {
      "my_admin_role": {
        "cluster" : [ "all" ],
        "indices" : [
          {
            "names" : [ "index1", "index2" ],
            "privileges" : [ "all" ],
            "allow_restricted_indices" : false,
            "field_security" : {
              "grant" : [ "title", "body" ]}
          }
        ],
        "applications" : [ ],
        "run_as" : [ "other_user" ],
        "metadata" : {
          "version" : 1
        },
        "transient_metadata": {
          "enabled": true
        }
      }
    }

若要检索所有角色，请省略角色名称：

    
    
    GET /_security/role

[« Get role mappings API](security-api-get-role-mapping.md) [Get service
accounts API »](security-api-get-service-accounts.md)
