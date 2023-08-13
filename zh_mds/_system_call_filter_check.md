

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« Use serial collector check](_use_serial_collector_check.md) [OnError and
OnOutOfMemoryError checks »](_onerror_and_onoutofmemoryerror_checks.md)

## 系统调用过滤器检查

Elasticsearch根据操作系统(例如Linux上的seccomp)安装各种风格的系统调用过滤器。安装这些系统调用过滤器是为了防止执行与分叉相关的系统调用，作为防御机制抵御 Elasticsearch 上的任意代码执行攻击。系统调用过滤器检查可确保如果启用了系统调用过滤器，则成功安装了这些过滤器。要通过系统调用过滤器检查，您必须修复系统上阻止安装系统调用过滤器的任何配置错误(检查日志)。

[« Use serial collector check](_use_serial_collector_check.md) [OnError and
OnOutOfMemoryError checks »](_onerror_and_onoutofmemoryerror_checks.md)
