

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Change passwords API](security-api-change-password.md) [Clear roles cache
API »](security-api-clear-role-cache.md)

## 清除缓存接口

从用户缓存中逐出用户。您可以完全清除缓存或逐出特定用户。

###Request

'POST /_security/realm/<realms>/_clear_cache'

'POST /_security/realm/<realms>/_clear_cache？用户名=<usernames>'

###Description

用户凭据缓存在每个节点的内存中，以避免连接到远程身份验证服务或为每个传入请求访问磁盘。您可以使用领域设置来配置用户缓存。有关详细信息，请参阅控制用户缓存。

若要从角色缓存中逐出角色，请参阅清除角色缓存 API。要从权限缓存中逐出权限，请参阅清除权限缓存 API。要从 API 密钥缓存中逐出 API 密钥，请参阅清除 API 密钥缓存 API。

### 路径参数

`<realms>`

     (Required, string) Comma-separated list of realms to clear. To clear all realms, use `*`. Does not support other wildcard patterns. 
`usernames`

     (Optional, list) A comma-separated list of the users to clear from the cache. If you do not specify this parameter, the API evicts all users from the user cache. 

###Examples

例如，要逐出由"file"域缓存的所有用户，请执行以下操作：

    
    
    POST /_security/realm/default_file/_clear_cache

要逐出选定的用户，请指定"用户名"参数：

    
    
    POST /_security/realm/default_file/_clear_cache?usernames=rdeniro,alpacino

要清除多个领域的缓存，请将领域指定为逗号分隔的列表：

    
    
    POST /_security/realm/default_file,ldap1/_clear_cache

要清除所有领域的缓存，请使用"*"。

    
    
    POST /_security/realm/*/_clear_cache

[« Change passwords API](security-api-change-password.md) [Clear roles cache
API »](security-api-clear-role-cache.md)
