

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Important system configuration](system-
config.md)

[« Disable swapping](setup-configuration-memory.md) [Virtual memory »](vm-
max-map-count.md)

## 文件描述符

这只与Linux和macOS相关，如果在Windows上运行Elasticsearch，可以安全地忽略它。在 Windows 上，JVM 使用 API.aspx) 仅受可用资源限制。

Elasticsearch使用了很多文件描述符或文件句柄。文件描述符不足可能是灾难性的，并且很可能导致数据丢失。确保将运行 Elasticsearch 的用户的打开文件描述符数量限制增加到 65，536 或更高。

对于 '.zip' 和 '.tar.gz' 包，在启动 Elasticsearch 之前将 'ulimit -n 65535' 设置为 root，或者在 '/etc/security/limits.conf' 中将 'nofile' 设置为 '65535'。

在 macOS 上，您还必须将 JVM 选项 '-XX：-MaxFDLimit' 传递给 Elasticsearch，以便它使用更高的文件描述符限制。

RPM 和 Debian 软件包已经默认文件描述符的最大数量为 65535，不需要进一步配置。

您可以使用节点统计信息 API 检查为每个节点配置的"max_file_descriptors"，如下所示：

    
    
    response = client.nodes.stats(
      metric: 'process',
      filter_path: '**.max_file_descriptors'
    )
    puts response
    
    
    GET _nodes/stats/process?filter_path=**.max_file_descriptors

[« Disable swapping](setup-configuration-memory.md) [Virtual memory »](vm-
max-map-count.md)
