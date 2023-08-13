

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Delete role mappings API](security-api-delete-role-mapping.md) [Delete
service account tokens API »](security-api-delete-service-token.md)

## 删除角色接口

删除本机域中的角色。

###Request

"删除/_security/角色/<name>"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

角色管理 API 通常是管理角色的首选方式，而不是使用基于文件的角色管理。删除角色 API 无法删除角色文件中定义的角色。

### 路径参数

`name`

     (string) The name of the role. 

###Examples

以下示例删除"my_admin_role"角色：

    
    
    DELETE /_security/role/my_admin_role

如果成功删除角色，请求将返回"{"找到"：true}"。否则，"已找到"将设置为 false。

    
    
    {
      "found" : true
    }

[« Delete role mappings API](security-api-delete-role-mapping.md) [Delete
service account tokens API »](security-api-delete-service-token.md)
