

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« System call filter check](_system_call_filter_check.md) [Early-access
check »](_early_access_check.md)

## OnError 和 OnOutOfMemoryErrorcheck

JVM 选项"OnError"和"OnOutOfMemoryError"允许在 JVM 遇到致命错误("OnError")或"OutOfMemoryError"("OnOutOfMemoryError")时执行任意命令。但是，默认情况下，Elasticsearchsystem 调用过滤器 (seccomp) 处于启用状态，这些过滤器会阻止分叉。因此，使用"OnError"或"OnOutOfMemoryError"和系统调用过滤器是不兼容的。"OnError"和"OnOutOfMemoryError"检查会阻止Elasticsearch启动，前提是使用了这些JVM选项中的任何一个，并且启用了系统调用过滤器。始终强制执行此检查。要通过此检查，请不要启用"OnError"或"OnOfMemoryError";相反，升级到 Java 8u92 并使用 JVM 标志"ExitOnOutOfMemoryError"。虽然这没有"OnError"或"OnOutOfMemoryError"的全部功能，但启用seccomp将不支持任意分叉。

[« System call filter check](_system_call_filter_check.md) [Early-access
check »](_early_access_check.md)
