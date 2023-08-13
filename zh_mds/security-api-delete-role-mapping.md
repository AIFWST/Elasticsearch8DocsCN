

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Delete application privileges API](security-api-delete-privilege.md)
[Delete roles API »](security-api-delete-role.md)

## 删除角色映射接口

删除角色映射。

###Request

"删除/_security/role_mapping/<name>"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

角色映射定义分配给每个用户的角色。有关详细信息，请参阅将用户和组映射到角色。

角色映射 API 通常是管理角色映射的首选方法，而不是使用角色映射文件。删除角色映射 API 无法删除角色映射文件中定义的角色映射。

### 路径参数

`name`

     (string) The distinct name that identifies the role mapping. The name is used solely as an identifier to facilitate interaction via the API; it does not affect the behavior of the mapping in any way. 

###Examples

以下示例删除角色映射：

    
    
    DELETE /_security/role_mapping/mapping1

如果映射成功删除，请求将返回"{"找到"：true}"。否则，"已找到"将设置为 false。

    
    
    {
      "found" : true
    }

[« Delete application privileges API](security-api-delete-privilege.md)
[Delete roles API »](security-api-delete-role.md)
