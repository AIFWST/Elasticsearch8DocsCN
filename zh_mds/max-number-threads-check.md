

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« Memory lock check](_memory_lock_check.md) [Max file size check
»](_max_file_size_check.md)

## 最大线程数检查

Elasticsearch 通过将请求分解为多个阶段并将这些阶段交给不同的线程池执行器来执行请求。Elasticsearch 中有不同的线程池执行器用于各种任务。因此，Elasticsearch需要能够创建大量线程。最大线程数检查可确保 Elasticsearch 进程有权在正常使用下创建足够的线程。此检查仅在 Linux 上强制执行。如果您使用的是 Linux，要通过最大线程数检查，您必须将系统配置为允许 Elasticsearch 进程创建至少 4096 个线程的能力。这可以通过"/etc/security/limits.conf"使用"nproc"设置(请注意，您可能也必须增加"root"用户的限制)。

[« Memory lock check](_memory_lock_check.md) [Max file size check
»](_max_file_size_check.md)
