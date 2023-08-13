

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Important system configuration](system-
config.md)

[« Number of threads](max-number-of-threads.md) [Ensure JNA temporary
directory permits executables »](executable-jna-tmpdir.md)

## DNS 缓存设置

Elasticsearch在安全管理器到位的情况下运行。使用安全管理器后，JVM 默认无限期缓存正主机名解析，默认缓存负主机名解析 10 秒。Elasticsearch 使用默认值覆盖此行为，以缓存正查找 60 秒，并将负查找缓存 10 秒。这些值应适用于大多数环境，包括 DNS 解析随时间变化的环境。如果没有，您可以在 JVM 选项中编辑值 'es.networkaddress.cache.ttl' 和 'es.networkaddress.cache.negative.ttl'。请注意，Java 安全策略中的值'networkaddress.cache.ttl='<timeout>and'networkaddress.cache.negative.ttl='将被<timeout>Elasticsearch忽略，除非您删除'es.networkaddress.cache.ttl'和'es.networkaddress.cache.negative.ttl'的设置。

[« Number of threads](max-number-of-threads.md) [Ensure JNA temporary
directory permits executables »](executable-jna-tmpdir.md)
