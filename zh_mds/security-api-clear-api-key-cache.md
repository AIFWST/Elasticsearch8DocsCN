

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Clear privileges cache API](security-api-clear-privilege-cache.md) [Clear
service account token caches API »](security-api-clear-service-token-
caches.md)

## 清除 API 密钥缓存API

从 API 密钥缓存中逐出所有条目的子集。还会在安全索引的状态更改时自动清除缓存。

###Request

"发布/_security/api_key<ids>//_clear_cache"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

有关 API 密钥的更多信息，请参阅创建 API 密钥、获取 API 密钥信息和使 API 密钥失效。

### 路径参数

`<ids>`

     (Required, string) Comma-separated list of API key IDs to evict from the API key cache. To evict all API keys, use `*`. Does not support other wildcard patterns. 

###Examples

清除的 API 密钥缓存 API 从 API 密钥缓存中逐出条目。例如，清除 ID 为"yVGMr3QByxdh1MSaicYx"的 API 密钥条目。

    
    
    POST /_security/api_key/yVGMr3QByxdh1MSaicYx/_clear_cache

将多个 API 密钥指定为逗号分隔的列表。

    
    
    POST /_security/api_key/yVGMr3QByxdh1MSaicYx,YoiMaqREw0YVpjn40iMg/_clear_cache

要清除 API 密钥缓存中的所有条目，请使用"*"。

    
    
    POST /_security/api_key/*/_clear_cache

[« Clear privileges cache API](security-api-clear-privilege-cache.md) [Clear
service account token caches API »](security-api-clear-service-token-
caches.md)
