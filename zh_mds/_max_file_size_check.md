

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« Maximum number of threads check](max-number-threads-check.md) [Maximum
size virtual memory check »](max-size-virtual-memory-check.md)

## 最大文件大小检查

作为单个分片组件的段文件和作为 translog 组件的 translog 生成可能会变大(超过数 GB)。在 Elasticsearch 进程可以创建的最大文件大小有限的系统上，这可能会导致写入失败。因此，这里最安全的选择是最大文件大小是无限的，这就是最大文件大小引导程序检查强制执行的。要通过最大文件检查，您必须将系统配置为允许 Elasticsearchprocess 写入无限大小的文件。这可以通过'/etc/security/limits.conf'使用"fsize"设置为"unlimited"来完成(请注意，您可能也必须增加"root"用户的限制)。

[« Maximum number of threads check](max-number-threads-check.md) [Maximum
size virtual memory check »](max-size-virtual-memory-check.md)
