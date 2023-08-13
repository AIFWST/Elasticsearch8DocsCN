

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Clear roles cache API](security-api-clear-role-cache.md) [Clear API key
cache API »](security-api-clear-api-key-cache.md)

## 清除权限缓存API

从本机应用程序权限缓存中逐出权限。对于具有更新权限的应用程序，也会自动清除缓存。

###Request

"发布/_security/特权/<applications>/_clear_cache"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

有关本机域的更多信息，请参阅域和本机用户身份验证。

### 路径参数

`<applications>`

     (Required, string) Comma-separated list of applications to clear. To clear all applications, use `*`. Does not support other wildcard patterns. 

###Examples

清除权限缓存 API 从本机应用程序权限缓存中逐出权限。例如，要清除"myapp"的缓存：

    
    
    POST /_security/privilege/myapp/_clear_cache

将多个应用程序指定为逗号分隔的列表。

    
    
    POST /_security/privilege/myapp,my-other-app/_clear_cache

要清除所有应用程序的缓存，请使用"*"。

    
    
    POST /_security/privilege/*/_clear_cache

[« Clear roles cache API](security-api-clear-role-cache.md) [Clear API key
cache API »](security-api-clear-api-key-cache.md)
