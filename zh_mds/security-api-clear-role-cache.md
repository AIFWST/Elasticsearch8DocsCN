

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Clear cache API](security-api-clear-cache.md) [Clear privileges cache API
»](security-api-clear-privilege-cache.md)

## 清除角色缓存API

从本机角色缓存中逐出角色。

###Request

"发布/_security/角色/<roles>/_clear_cache"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

有关本机域的更多信息，请参阅域和本机用户身份验证。

### 路径参数

`<roles>`

     (Required, string) Comma-separated list of roles to evict from the role cache. To evict all roles, use `*`. Does not support other wildcard patterns. 

###Examples

清除角色缓存 API 从本机角色缓存中逐出角色。例如，要清除"my_admin_role"的缓存：

    
    
    POST /_security/role/my_admin_role/_clear_cache

将多个角色指定为逗号分隔的列表。

    
    
    POST /_security/role/my_admin_role,my_test_role/_clear_cache

要从缓存中清除所有角色，请使用"*"。

    
    
    POST /_security/role/*/_clear_cache

[« Clear cache API](security-api-clear-cache.md) [Clear privileges cache API
»](security-api-clear-privilege-cache.md)
