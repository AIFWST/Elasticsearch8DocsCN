

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Important system configuration](system-
config.md)

[« File Descriptors](file-descriptors.md) [Number of threads »](max-number-
of-threads.md)

## 虚拟内存

Elasticsearch默认使用'mmapfs'目录来存储其索引。mmapcount 的默认操作系统限制可能太低，这可能会导致内存不足异常。

在 Linux 上，您可以通过以 'root' 身份运行以下命令来增加限制：

    
    
    sysctl -w vm.max_map_count=262144

要永久设置此值，请更新"/etc/sysctl.conf"中的"vm.max_map_count"设置。要在重新启动后进行验证，请运行"sysctl vm.max_map_count"。

RPM 和 Debian 软件包将自动配置此设置。无需进一步配置。

[« File Descriptors](file-descriptors.md) [Number of threads »](max-number-
of-threads.md)
