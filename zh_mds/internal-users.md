

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Service accounts](service-accounts.md) [Token-based authentication
services »](token-authentication-services.md)

## 内部用户

这些用户仅供 Elasticsearch 内部使用。不支持对这些用户进行身份验证。

Elastic Stack 安全功能使用六个 _internal_ 用户("_system"、"_xpack"、"_xpack_security"、"_async_search"、"_security_profile"和"_storage")，这些用户负责在 Elasticsearch 集群内执行的操作。

这些用户仅由来自群集内的请求使用。因此，它们不能用于针对 API 进行身份验证，并且没有密码可供管理或重置。

有时，您可能会在日志中找到对其中一个用户的引用，包括审核日志。

[« Service accounts](service-accounts.md) [Token-based authentication
services »](token-authentication-services.md)
