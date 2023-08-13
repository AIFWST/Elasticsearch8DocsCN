

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« File descriptor check](_file_descriptor_check.md) [Maximum number of
threads check »](max-number-threads-check.md)

## 内存锁定检查

当 JVM 进行大型垃圾回收时，它会触及堆的每一页。如果这些页面中的任何一个被换出到磁盘，它们将不得不换回内存。这会导致大量的磁盘抖动，Elasticsearch更愿意使用这些磁盘来服务请求。有服务器总是将系统配置为不允许交换。一种方法是请求JVM通过"mlockall"(Unix)或虚拟锁(Windows)将堆锁定在内存中。这是通过Elasticsearch设置'bootstrap.memory_lock'完成的。但是，在某些情况下，可以将此设置传递给 Elasticsearch，但 Elasticsearch 无法锁定堆(例如，如果 'elasticsearch' 用户没有 'memlockunlimited')。内存锁定检查验证是否启用了"bootstrap.memory_lock"设置，JVM 是否能够成功锁定堆。要通过内存锁定检查，您可能需要配置"bootstrap.memory_lock"。

[« File descriptor check](_file_descriptor_check.md) [Maximum number of
threads check »](max-number-threads-check.md)
