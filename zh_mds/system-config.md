

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Advanced configuration](advanced-configuration.md) [Configuring system
settings »](setting-system-settings.md)

## 重要系统配置

理想情况下，Elasticsearch应该在服务器上单独运行，并使用所有可用的资源。为此，您需要配置操作系统，以允许运行 Elasticsearch 的用户访问比默认允许的更多的资源。

在投入生产之前，必须考虑以下设置：

* 配置系统设置 * 禁用交换 * 增加文件描述符 * 确保足够的虚拟内存 * 确保足够的线程 * JVM DNS 缓存设置 * 临时目录未挂载"noexec" * TCP 重传超时

### 开发模式与生产模式

默认情况下，Elasticsearch 假定您是在开发模式下工作。如果上述任何设置配置不正确，则会在日志文件中写入警告，但您将能够启动并运行您的 Elasticsearch 节点。

一旦您配置了像"network.host"这样的网络设置，Elasticsearch就会假定您要迁移到生产环境，并将上述警告升级到异常。这些异常将阻止您的 Elasticsearch 节点启动。这是一项重要的安全措施，可确保不会因服务器配置错误而丢失数据。

[« Advanced configuration](advanced-configuration.md) [Configuring system
settings »](setting-system-settings.md)
