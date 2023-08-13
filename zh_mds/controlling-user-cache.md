

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Looking up users without authentication](user-lookup.md) [Configuring
SAML single-sign-on on the Elastic Stack »](saml-guide-stack.md)

## 控制用户缓存

用户凭据缓存在每个节点的内存中，以避免连接到远程身份验证服务或为每个传入请求访问磁盘。您可以使用"cache.ttl"、"cache.max_users"和"cache.hash_algo"领域设置来配置用户缓存的特征。

JWT realms 使用 'jwt.cache.ttl' 和 'jwt.cache.size' realm settings。

PKI 和 JWT 领域不缓存用户凭据，但会缓存已解析的用户对象，以避免不必要地需要对每个请求执行角色映射。

缓存的用户凭据在内存中进行哈希处理。默认情况下，Elasticsearch 安全功能使用加盐的"sha-256"哈希算法。您可以通过设置"cache.hash_algo"领域设置来使用不同的哈希算法。请参阅用户缓存和密码哈希算法。

### 从缓存中逐出用户

您可以使用清除缓存 API 强制逐出缓存的用户。例如，以下请求从"ad1"域中逐出所有用户：

    
    
    $ curl -XPOST 'http://localhost:9200/_security/realm/ad1/_clear_cache'

要清除多个领域的缓存，请将领域指定为逗号分隔的列表：

    
    
    $ curl -XPOST 'http://localhost:9200/_security/realm/ad1,ad2/_clear_cache'

您还可以逐出特定用户：

    
    
    $ curl -XPOST 'http://localhost:9200/_security/realm/ad1/_clear_cache?usernames=rdeniro,alpacino'

[« Looking up users without authentication](user-lookup.md) [Configuring
SAML single-sign-on on the Elastic Stack »](saml-guide-stack.md)
