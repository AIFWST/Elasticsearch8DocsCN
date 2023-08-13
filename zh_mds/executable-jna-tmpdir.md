

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Important system configuration](system-
config.md)

[« DNS cache settings](networkaddress-cache-ttl.md) [TCP retransmission
timeout »](system-config-tcpretries.md)

## 确保 JNA 临时目录允许可执行文件

这只与Linux相关。

Elasticsearch使用Java Native Access(JNA)库和另一个名为"libffi"的库来执行一些依赖于平台的原生代码。在 Linux 上，支持这些库的原生代码在运行时被提取到临时目录中，然后映射到 Elasticsearch 地址空间中的可执行页面。这要求底层文件不在挂载的文件系统上，使用"noexec"选项挂载。

默认情况下，Elasticsearch 将在 '/tmp' 中创建其临时目录。但是，一些强化的 Linux 安装默认使用"noexec"选项挂载"/tmp"。这会阻止 JNA 和 'libffi' 正常工作。例如，在启动时，JNA 可能无法加载并显示"java.lang.UnsatisfiedLinkerError"异常或显示类似于"无法从共享对象映射段"的消息，或者"libffi"可能会报告诸如"无法分配闭包"之类的消息。请注意，异常消息在 JVM 版本之间可能有所不同。此外，依赖于通过 JNA 执行本机代码的 Elasticsearch 组件可能会失败，并显示消息指示它"因为 JNA 不可用"。

要解决这些问题，请从"/tmp"文件系统中删除"noexec"选项，或者通过设置"$ES_TMPDIR"环境变量将Elasticsearch配置为为其临时目录使用不同的位置。例如：

* 如果您直接从 shell 运行 Elasticsearch，请按如下方式设置 '$ES_TMPDIR：export ES_TMPDIR=/usr/share/elasticsearch/tmp

* 对于通过 RPM 或 DEB 软件包完成的安装，需要通过系统配置文件设置环境变量。  * 如果您使用 'systemd' 将 Elasticsearch 作为服务运行，请将以下行添加到 [服务覆盖文件： Environment=ES_TMPDIR=/usr/share/elasticsearch/tmp 的 'Service]' 部分

如果您需要对这些临时文件的位置进行更精细的控制，您还可以使用 JVM 标志 '-Djna.tmpdir=' 配置 JNA 使用的路径<path>，并且您可以通过配置"libffi"用于其临时文件的路径 'LIBFFI_TMPDIR' 环境变量。Elasticsearch 的未来版本可能需要额外的配置，因此您应该尽可能设置"ES_TMPDIR"。

Elasticsearch 不会删除其临时目录。你应该在 Elasticsearch 未运行时删除剩余的临时目录。最好自动执行此操作，例如在每次重新启动时。如果你在Linux上运行，你可以通过使用thetmpfs文件系统来实现这一点。

[« DNS cache settings](networkaddress-cache-ttl.md) [TCP retransmission
timeout »](system-config-tcpretries.md)
