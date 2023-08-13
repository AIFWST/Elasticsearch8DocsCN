

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« Maximum size virtual memory check](max-size-virtual-memory-check.md)
[Client JVM check »](_client_jvm_check.md)

## 最大地图计数检查

继续上一点，为了有效地使用"mmap"，Elasticsearch还需要能够创建许多内存映射区域。最大映射计数检查检查内核是否允许进程至少具有 262，144 个内存映射区域，并且仅在 Linux 上强制执行。要通过最大映射计数检查，您必须通过"sysctl"将"vm.max_map_count"配置为至少"262144"。

或者，仅当您使用"mmapfs"或"hybridfs"作为索引的存储类型时，才需要检查最大映射计数。如果您不允许使用"mmap"，则不会强制执行此引导程序检查。

[« Maximum size virtual memory check](max-size-virtual-memory-check.md)
[Client JVM check »](_client_jvm_check.md)
