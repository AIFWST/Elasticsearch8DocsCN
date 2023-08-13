

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Bootstrap Checks](bootstrap-checks.md)

[« Heap size check](_heap_size_check.md) [Memory lock check
»](_memory_lock_check.md)

## 文件描述符检查

文件描述符是用于跟踪打开的"文件"的Unix结构。在Unix中，一切都是有文件的。例如，"文件"可以是物理文件、虚拟文件(例如，'/proc/loadavg')或网络套接字。Elasticsearch需要大量的文件描述符(例如，每个分片都由多个段和其他文件组成，加上与其他节点的连接等)。此引导程序检查在 OS X 和 Linux 上强制执行。要通过文件描述符检查，您可能需要配置文件描述符。

[« Heap size check](_heap_size_check.md) [Memory lock check
»](_memory_lock_check.md)
