

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Important system configuration](system-
config.md)

[« Ensure JNA temporary directory permits executables](executable-jna-
tmpdir.md) [Bootstrap Checks »](bootstrap-checks.md)

## TCP 重新传输超时

每对 Elasticsearch 节点通过多个 TCP 连接进行通信，这些连接保持打开状态，直到其中一个节点关闭或节点之间的通信因底层基础架构故障而中断。

TCP 通过对通信应用程序隐藏临时网络中断，在偶尔不可靠的网络上提供可靠的通信。您的操作系统将在通知发件人任何问题之前多次重新传输任何丢失的消息。Elasticsearch必须在传输发生时等待，并且只有在操作系统决定放弃时才能做出反应。因此，用户还必须等待一系列重传完成。

大多数 Linux 发行版默认重新传输丢失的数据包 15 次。重新传输呈指数级下降，因此这 15 次重新传输需要 900 秒以上才能完成。这意味着 Linux 需要花费很多分钟才能使用此方法检测网络分区或故障节点。Windows 默认仅重新传输 5 次，对应于大约 6 秒的超时。

Linux 默认值允许通过可能会经历很长时间数据包丢失的网络进行通信，但此默认值对于大多数 Elasticsearch 安装使用的高质量网络来说都是过度的，甚至是有害的。当集群检测到节点故障时，它会通过重新分配丢失的分片、重新路由搜索以及可能选择新的主节点来做出反应。高可用性集群必须能够及时检测节点故障，这可以通过减少允许的重新传输次数来实现。与远程群集的连接也应该比 Linux 默认值允许的速度更快地检测故障。因此，Linux 用户应减少 TCP 重新传输的最大次数。

您可以通过以"root"身份运行以下命令，将 TCP 重新传输的最大次数减少到"5"。五次重传对应大约六秒的超时。

    
    
    sysctl -w net.ipv4.tcp_retries2=5

要永久设置此值，请更新"/etc/sysctl.conf"中的"net.ipv4.tcp_retries2"设置。要在重新启动后进行验证，请运行"sysctlnet.ipv4.tcp_retries2"。

此设置适用于所有 TCP 连接，并且也会影响与 Elasticsearch 集群以外的系统通信的可靠性。如果您的集群通过低质量网络与外部系统通信，则可能需要为"net.ipv4.tcp_retries2"选择更高的值。因此，Elasticsearch 不会自动调整此设置。

### 相关配置

Elasticsearch 还实现了自己的内部健康检查，其超时时间比 Linux 上默认的重新传输超时短得多。由于这些是应用程序级运行状况检查，因此它们的超时必须允许应用程序级影响，例如垃圾回收暂停。您不应减少与这些应用程序级运行状况检查相关的任何超时。

您还必须确保网络基础结构不会干扰节点之间的长期连接，即使这些连接看起来是空闲的。在达到一定年龄时断开连接的设备是 Elasticsearch 集群问题的常见来源，不得使用。

[« Ensure JNA temporary directory permits executables](executable-jna-
tmpdir.md) [Bootstrap Checks »](bootstrap-checks.md)
