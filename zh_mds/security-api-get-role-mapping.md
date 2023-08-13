

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get builtin privileges API](security-api-get-builtin-privileges.md) [Get
roles API »](security-api-get-role.md)

## 获取角色映射接口

检索角色映射。

###Request

"获取/_security/role_mapping"

'获取/_security/role_mapping/<name>"

###Prerequisites

* 要使用此 API，您必须至少具有"read_security"群集权限。

###Description

角色映射定义分配给每个用户的角色。有关详细信息，请参阅将用户和组映射到角色。

角色映射 API 通常是管理角色映射的首选方法，而不是使用角色映射文件。获取角色映射 API 无法检索角色映射文件中定义的角色映射。

### 路径参数

`name`

     (Optional, string) The distinct name that identifies the role mapping. The name is used solely as an identifier to facilitate interaction via the API; it does not affect the behavior of the mapping in any way. You can specify multiple mapping names as a comma-separated list. If you do not specify this parameter, the API returns information about all role mappings. 

### 响应正文

成功的调用会检索一个对象，其中键是请求映射的名称，值是这些映射的 JSON 表示形式。有关详细信息，请参阅角色映射资源。

### 响应码

如果没有与请求名称的映射，则响应的状态代码为"404"。

###Examples

下面的示例检索有关"mapping1"角色映射的信息：

    
    
    GET /_security/role_mapping/mapping1
    
    
    {
      "mapping1": {
        "enabled": true,
        "roles": [
          "user"
        ],
        "rules": {
          "field": {
            "username": "*"
          }
        },
        "metadata": {}
      }
    }

[« Get builtin privileges API](security-api-get-builtin-privileges.md) [Get
roles API »](security-api-get-role.md)
