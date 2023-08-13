

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Clear API key cache API](security-api-clear-api-key-cache.md) [Create API
key API »](security-api-create-api-key.md)

## 清除服务帐户令牌缓存API

从服务帐户令牌缓存中逐出所有条目的子集。

###Request

`POST
/_security/service/{namespace}/{service}/credential/token/{token_name}/_clear_cache`

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

服务帐户令牌存在两个单独的缓存：一个缓存用于由"service_tokens"文件支持的令牌，另一个缓存用于由".security"索引支持的令牌。此 API 从两个缓存中清除匹配的条目。

由".security"索引支持的服务帐户令牌的缓存会在安全索引的状态更改时自动清除。由"service_tokens"文件支持的缓存令牌将在文件更改时自动清除。

有关详细信息，请参阅服务帐户。

### 路径参数

`namespace`

     (Required, string) Name of the namespace. 
`service`

     (Required, string) Name of the service name. 
`token_name`

     (Required, string) Comma-separated list of token names to evict from the service account token caches. Use a wildcard (`*`) to evict all tokens that belong to a service account. Does not support other wildcard patterns. 

###Examples

以下请求清除"token1"令牌的服务帐户令牌缓存：

    
    
    POST /_security/service/elastic/fleet-server/credential/token/token1/_clear_cache

将多个令牌名称指定为逗号分隔的列表：

    
    
    POST /_security/service/elastic/fleet-server/credential/token/token1,token2/_clear_cache

若要清除服务帐户令牌缓存中的所有条目，请使用通配符 ("*") 代替令牌名称：

    
    
    POST /_security/service/elastic/fleet-server/credential/token/*/_clear_cache

[« Clear API key cache API](security-api-clear-api-key-cache.md) [Create API
key API »](security-api-create-api-key.md)
