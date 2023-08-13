

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« Maximum map count check](_maximum_map_count_check.md) [Use serial
collector check »](_use_serial_collector_check.md)

## 客户端 JVMcheck

OpenJDK 派生的 JVM 提供了两种不同的 JVM：客户端 JVM 和服务器 JVM。这些 JVM 使用不同的编译器从 Java 字节码生成可执行机器代码。客户机 JVM 针对启动时间和内存占用进行了调整，而服务器 JVM 则针对最大化性能进行了调优。两个 VM 之间的性能差异可能很大。客户端 JVM 检查确保 Elasticsearch 未在客户端 JVM 内运行。要通过客户端 JVM 检查，您必须使用服务器虚拟机启动 Elasticsearch。在新式系统和操作系统上，服务器 VM 是默认值。

[« Maximum map count check](_maximum_map_count_check.md) [Use serial
collector check »](_use_serial_collector_check.md)
