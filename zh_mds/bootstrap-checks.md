

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« TCP retransmission timeout](system-config-tcpretries.md) [Heap size check
»](_heap_size_check.md)

## 引导检查

总的来说，我们有很多经验，用户遇到意外问题，因为他们没有配置重要的设置。在以前版本的 Elasticsearch 中，其中一些设置的错误配置被记录为警告。可以理解的是，用户有时会错过这些日志消息。为了确保这些设置得到应有的关注，Elasticsearch 会在启动时进行引导检查。

这些引导检查检查各种 Elasticsearch 和系统设置，并将它们与 Elasticsearch 操作安全的值进行比较。如果 Elasticsearch 处于开发模式，则任何失败的引导程序检查都会在 Elasticsearch 日志中显示为警告。如果 Elasticsearch 处于生产模式，任何失败的引导检查都会导致 Elasticsearch 拒绝启动。

有一些引导程序检查总是被强制执行，以防止Elasticsearch在不兼容的设置下运行。这些检查是单独记录的。

### 开发与生产模式

默认情况下，Elasticsearch 绑定到 HTTP 和传输(内部)通信的环回地址。这对于下载和使用Elasticsearch以及日常开发来说很好，但对于生产系统来说毫无用处。要加入集群，Elasticsearchnode必须可以通过传输通信到达。要通过非环回地址加入集群，节点必须将传输绑定到非环回地址，并且不能使用单节点发现。因此，如果 Elasticsearch 节点不能通过非环回地址与另一台机器形成集群，则我们认为该节点处于开发模式，如果它可以通过非环回地址加入集群，则认为该节点处于生产模式。

请注意，HTTP 和传输可以通过"http.host"和"transport.host"独立配置;这对于将单个节点配置为可通过 HTTP 访问以进行测试而不触发生产模式非常有用。

### 单节点发现

我们认识到某些用户需要将传输绑定到外部接口以测试远程群集配置。对于这种情况，我们提供发现类型"单节点"(通过将"发现.type"设置为"单节点"来配置它);在这种情况下，节点将自行选择为主节点，并且不会将群集与任何其他节点一起加入。

### 强制引导检查

如果在生产环境中运行单个节点，则可以逃避引导程序检查(通过不将传输绑定到外部接口，或者通过将传输绑定到外部接口并将发现类型设置为"单节点")。对于这种情况，您可以通过在 JVM 选项中将系统属性 'es.enforce.bootstrap.checks'设置为 'true' 来强制执行引导程序检查。如果您处于这种特定情况，我们强烈建议您这样做。此系统属性可用于强制执行独立于节点配置的引导程序检查。

[« TCP retransmission timeout](system-config-tcpretries.md) [Heap size check
»](_heap_size_check.md)
