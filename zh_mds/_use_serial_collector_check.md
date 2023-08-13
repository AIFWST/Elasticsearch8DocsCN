

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« Client JVM check](_client_jvm_check.md) [System call filter check
»](_system_call_filter_check.md)

## 使用串行收集器检查

OpenJDK 派生的 JVM 有各种垃圾收集器，针对不同的工作负载。特别是串行收集器最适合单个逻辑 CPU 机器或极小的堆，两者都不适合运行 Elasticsearch。将串行收集器与Elasticsearch一起使用可能会对性能造成毁灭性的影响。串行收集器检查确保 Elasticsearch 未配置为与串行收集器一起运行。要通过串行收集器检查，您不得使用串行收集器启动 Elasticsearch(无论是来自您正在重用的 JVM 的默认值，还是您使用 '-XX：+UseSerialGC' 显式指定它)。请注意，Elasticsearch 附带的默认 JVM 配置将 Elasticsearch 配置为在 JDK14 及更高版本中使用 G1GC 垃圾回收器。对于早期的 JDK 版本，配置默认为 CMS 收集器。

[« Client JVM check](_client_jvm_check.md) [System call filter check
»](_system_call_filter_check.md)
