

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« Max file size check](_max_file_size_check.md) [Maximum map count check
»](_maximum_map_count_check.md)

## 最大大小虚拟内存检查

Elasticsearch 和 Lucene 使用 'mmap' 将 anindex 的一部分映射到 Elasticsearch 地址空间中，效果很好。这使某些索引数据远离 JVM 堆，而是在内存中，以实现极快的访问。为了有效，Elasticsearch应该有无限的地址空间。最大大小虚拟内存检查强制 Elasticsearch 进程具有无限的地址空间，并且仅在 Linux 上强制执行。要通过最大大小虚拟内存检查，您必须将系统配置为允许 Elasticsearch 进程具有无限的地址空间。这可以通过将"<user> - as unlimited"添加到"/etc/security/limits.conf"来完成。这可能还需要您增加"root"用户的限制。

[« Max file size check](_max_file_size_check.md) [Maximum map count check
»](_maximum_map_count_check.md)
