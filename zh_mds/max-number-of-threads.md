

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Important system configuration](system-
config.md)

[« Virtual memory](vm-max-map-count.md) [DNS cache settings
»](networkaddress-cache-ttl.md)

## 线程数

Elasticsearch 使用许多线程池进行不同类型的操作。重要的是，它能够在需要时创建新线程。确保 Elasticsearch 用户可以创建的线程数至少为 4096。

这可以通过在启动 Elasticsearch 之前将 'ulimit -u 4096' 设置为 root 来完成，或者在 '/etc/security/limits.conf' 中将 'nproc' 设置为 '4096' 来完成。

当在"systemd"下作为服务运行时，软件包分发将自动配置 Elasticsearch 进程的线程数。无需其他配置。

[« Virtual memory](vm-max-map-count.md) [DNS cache settings
»](networkaddress-cache-ttl.md)
