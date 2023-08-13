

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« Bootstrap Checks](bootstrap-checks.md) [File descriptor check
»](_file_descriptor_check.md)

## 堆大小检查

默认情况下，Elasticsearch 会根据节点的角色和总内存自动调整 JVM 堆的大小。如果您手动覆盖缺省大小调整并使用不同的初始和最大堆大小启动 JVM，那么 JVM 可能会在系统使用期间调整堆大小时暂停。如果启用"bootstrap.memory_lock"，JVM将在启动时锁定初始堆大小。如果初始堆大小不等于最大堆大小，那么某些 JVM 堆在调整大小后可能不会被锁定。要避免这些问题，请在初始堆大小等于最大堆大小的情况下启动 JVM。

[« Bootstrap Checks](bootstrap-checks.md) [File descriptor check
»](_file_descriptor_check.md)
