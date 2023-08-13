

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Discovery and cluster formation](modules-
discovery.md)

[« Publishing the cluster state](cluster-state-publishing.md) [Add and
remove nodes in your cluster »](add-elasticsearch-nodes.md)

## 集群故障检测

当选的主节点会定期检查群集中的每个节点，以确保它们仍处于连接状态且运行良好。群集中的每个节点还会定期检查所选主节点的运行状况。这些检查分别称为_follower checks_和_leader checks_。

Elasticsearch 允许这些检查偶尔失败或超时，而无需执行任何操作。只有在多次连续检查失败后，它才会认为节点有故障。您可以使用"cluster.fault_detection.*"设置来控制故障检测行为。

但是，如果选定的主节点检测到节点已断开连接，则这种情况将被视为立即故障。主节点绕过超时并重试设置值，并尝试从集群中删除节点。同样，如果节点检测到选定的主节点已断开连接，则这种情况将被视为立即失败。节点绕过超时和重试设置，并重新启动其发现阶段以尝试查找或选择新的主节点。

此外，每个节点都会定期验证其数据路径是否正常，方法是将小文件写入磁盘，然后再次将其删除。如果节点发现其数据路径不正常，则会将其从群集中删除，直到数据路径恢复。您可以使用"monitor.fs.health"设置来控制此行为。

如果节点无法在合理的时间内应用更新的集群状态，则选定的主节点还将从集群中删除节点。超时默认为从群集状态更新开始算起 2 分钟。有关更详细的说明，请参阅发布群集状态。

### 排查不稳定集群问题

通常，节点只有在故意关闭时才会离开集群。如果阳极意外离开群集，请务必解决原因。节点意外离开的集群不稳定，可能会产生多个问题。例如：

* 群集运行状况可能为黄色或红色。  * 某些分片将初始化，而其他分片可能会失败。  * 搜索、索引和监视操作可能会失败，并在日志中报告异常。  * ".security"索引可能不可用，从而阻止对集群的访问。  * 由于频繁的集群状态更新，主服务器可能会显得繁忙。

要对处于此状态的集群进行故障排除，请首先确保集群具有不稳定的主节点。接下来，将重点放在意外离开群集的节点上，而不是所有其他问题。在集群具有稳定的主节点和稳定的节点成员资格之前，将无法解决其他问题。

诊断和统计信息在不稳定的群集中通常没有用。这些工具仅提供单个时间点群集状态的视图。相反，请查看群集日志以了解超时行为模式。特别关注当选主人的日志。当节点离开集群时，所选主节点的日志将包含如下消息(添加了换行符以使其更易于阅读)：

    
    
    [2022-03-21T11:02:35,513][INFO ][o.e.c.c.NodeLeftExecutor] [instance-0000000000]
        node-left: [{instance-0000000004}{bfcMDTiDRkietFb9v_di7w}{aNlyORLASam1ammv2DzYXA}{172.27.47.21}{172.27.47.21:19054}{m}]
        with reason [disconnected]

此消息表示，所选主节点("instance-00000000000")上的"NodeLeftExecutor"处理了"节点左"任务，标识了已删除的节点及其删除原因。当节点再次加入集群时，所选主节点的日志将包含如下消息(添加了换行符以使其更易于阅读)：

    
    
    [2022-03-21T11:02:59,892][INFO ][o.e.c.c.NodeJoinExecutor] [instance-0000000000]
        node-join: [{instance-0000000004}{bfcMDTiDRkietFb9v_di7w}{UNw_RuazQCSBskWZV8ID_w}{172.27.47.21}{172.27.47.21:19054}{m}]
        with reason [joining after restart, removed [24s] ago with reason [disconnected]]

此消息指出，所选主节点("instance-00000000000")上的"NodeJoinExecutor"处理了"节点加入"任务，标识了添加到集群的节点以及任务的原因。

其他节点可能会记录类似的消息，但报告的详细信息较少：

    
    
    [2020-01-29T11:02:36,985][INFO ][o.e.c.s.ClusterApplierService]
        [instance-0000000001] removed {
            {instance-0000000004}{bfcMDTiDRkietFb9v_di7w}{aNlyORLASam1ammv2DzYXA}{172.27.47.21}{172.27.47.21:19054}{m}
            {tiebreaker-0000000003}{UNw_RuazQCSBskWZV8ID_w}{bltyVOQ-RNu20OQfTHSLtA}{172.27.161.154}{172.27.161.154:19251}{mv}
        }, term: 14, version: 1653415, reason: Publication{term=14, version=1653415}

这些消息对于故障排除并不是特别有用，因此请关注"NodeLeftExecutor"和"NodeJoinExecutor"中的消息，它们仅在选定的主服务器上发出，并且包含更多详细信息。如果您没有看到来自"NodeLeftExecutor"和"NodeJoinExecutor"的消息，请检查：

* 您正在查看所选主节点的日志。  * 日志涵盖正确的时间段。  * 日志记录在"信息"级别启用。

节点还将记录一条消息，其中包含"主节点已更改"，只要它们开始或停止跟随选定的主节点。您可以使用这些消息来确定每个节点在一段时间内主节点状态的视图。

如果节点重新启动，它将离开集群，然后再次加入集群。当它重新加入时，"NodeJoinExecutor"将记录它处理了一个"节点加入"任务，指示节点正在"重新启动后加入"。如果节点意外重新启动，请查看节点的日志以了解其关闭原因。

受影响节点上的运行状况 API 还将提供有关情况的一些有用信息。

如果节点没有重新启动，那么您应该更仔细地查看其离开的原因。每个原因都有不同的故障排除步骤，如下所述。有三个可能的原因：

* "断开连接"：从主节点到已删除节点的连接已关闭。  * "滞后"：主节点发布了集群状态更新，但已删除的节点未在允许的超时内应用该更新。默认情况下，此超时为 2 分钟。有关控制此机制的设置的信息，请参阅发现和群集形成设置。  * "超出追随者检查重试计数"：主节点向已删除的节点发送了多次连续的运行状况检查。这些检查被拒绝或超时。默认情况下，每次运行状况检查在 10 秒后超时，Elasticsearch 会在连续三次运行状况检查失败后删除节点。有关控制此机制的设置的信息，请参阅发现和群集形成设置。

#### 诊断"断开连接"的节点

节点通常在关闭时以"断开连接"的原因离开集群，但如果它们在没有重新启动的情况下重新加入集群，则存在其他问题。

Elasticsearch被设计为在一个相当可靠的网络上运行。它在节点之间打开许多TCP连接，并期望这些连接永远保持打开状态。如果连接关闭，那么 Elasticsearch 将尝试重新连接，因此即使受影响的节点短暂离开集群，偶尔的 blip 对集群的影响也应该有限。相反，反复断开的连接将严重影响其运行。

从选定的主节点到集群中所有其他节点的连接尤为重要。当选的主节点从不自发关闭与其他节点的出站连接。同样，一旦连接完全建立，节点永远不会自发关闭其入站连接，除非节点正在关闭。

如果您看到某个节点意外地以"断开连接"的原因离开集群，则可能是 Elasticsearch 以外的其他原因导致连接关闭。一个常见的原因是防火墙配置错误，超时不正确，或者其他策略与 Elasticsearch 不兼容。它也可能是由一般连接问题引起的，例如由于硬件故障或网络拥塞而导致的数据包丢失。如果您是高级用户，则可以通过配置以下记录器来获取有关网络异常的更多详细信息：

    
    
    logger.org.elasticsearch.transport.TcpTransport: DEBUG
    logger.org.elasticsearch.xpack.core.security.transport.netty4.SecurityNetty4Transport: DEBUG

在极端情况下，您可能需要使用"tcpdump"进行数据包捕获，以确定节点之间的消息是否被网络上的其他设备丢弃或拒绝。

#### 诊断"滞后"节点

Elasticsearch 需要每个节点合理快速地处理集群状态更新。如果节点处理群集状态更新的时间过长，则可能对群集有害。主节点将以"滞后"的原因删除这些节点。有关控制此机制的设置的信息，请参阅发现和集群形成设置。

滞后通常是由已删除节点上的性能问题引起的。但是，节点也可能由于严重的网络延迟而滞后。要排除网络延迟，请确保正确配置"net.ipv4.tcp_retries2"。包含"警告阈值"的日志消息可能会提供有关根本原因的详细信息。

如果您是高级用户，则可以通过配置以下记录器来获取有关节点在删除时正在执行的操作的更多详细信息：

    
    
    logger.org.elasticsearch.cluster.coordination.LagDetector: DEBUG

启用此记录器后，Elasticsearch 将尝试在故障节点上运行节点热线程 API，并在所选主节点的日志中报告结果。结果被压缩、编码并拆分为块以避免截断：

    
    
    [DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] [part 1]: H4sIAAAAAAAA/x...
    [DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] [part 2]: p7x3w1hmOQVtuV...
    [DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] [part 3]: v7uTboMGDbyOy+...
    [DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] [part 4]: 4tse0RnPnLeDNN...
    [DEBUG][o.e.c.c.LagDetector      ] [master] hot threads from node [{node}{g3cCUaMDQJmQ2ZLtjr-3dg}{10.0.0.1:9300}] lagging at version [183619] despite commit of cluster state version [183620] (gzip compressed, base64-encoded, and split into 4 parts on preceding log lines)

要重建输出，base64-解码数据并使用"gzip"解压缩。例如，在类Unix系统上：

    
    
    cat lagdetector.log | sed -e 's/.*://' | base64 --decode | gzip --decompress

#### 诊断"超出追随者检查重试计数"节点

节点有时会在关闭时以"追随者检查重试计数超过"的原因离开集群，但如果它们在没有重新启动的情况下重新加入集群，则存在其他问题。

Elasticsearch 需要每个节点都能成功且合理快速地响应网络消息。如果节点拒绝请求或根本没有响应，则可能对集群有害。如果足够多的连续检查失败，则 master 将删除节点，原因为"超出追随者检查重试计数"，并将在"节点左"消息中指示有多少连续不成功的检查失败以及其中有多少超时。有关控制此机制的设置的信息，请参阅发现和集群形成设置。

超时和故障可能是由于受影响节点上的网络延迟或性能问题造成的。确保正确配置"net.ipv4.tcp_retries2"，以消除网络延迟作为此类不稳定的可能原因。包含"警告阈值"的日志消息可能会提供有关不稳定原因的进一步线索。

如果上次检查失败并出现异常，则会报告异常，并且通常指示需要解决的问题。如果任何检查超时，则按如下方式缩小问题范围。

* GC 暂停记录在 Elasticsearch 默认发出的 GC 日志中，通常也记录在主节点日志中的"JvmMonitorService"中。使用这些日志确认 GC 是否会导致延迟。  * VM 暂停也会影响同一主机上的其他进程。虚拟机暂停通常也会导致系统时钟的不连续性，Elasticsearch 将在其日志中报告。  * 数据包捕获将显示系统级和网络级故障，尤其是在选定主节点和故障节点上同时捕获网络流量时。用于追随者检查的连接不用于任何其他流量，因此即使使用了TLS，也可以仅从流模式中轻松识别：几乎每秒都会发送几百字节，首先是主站的请求，然后是追随者的响应。您应该能够观察到此类连接上的任何重新传输、数据包丢失或其他延迟。  * 特定线程可用的长时间等待可以通过在相关日志消息之前的几秒钟内进行堆栈转储(例如，使用"jstack")或分析跟踪(例如，使用 Java Flight Recorder)来识别。

节点热线程 API 有时会生成有用的信息，但请记住，此 API 还需要跨群集中所有节点的"transport_worker"和"泛型"线程。API 可能会受到您重新尝试诊断的问题的影响。"jstack"更可靠，因为它不需要任何JVM线程。

发现和群集成员资格中涉及的线程主要是"transport_worker"和"cluster_coordination"线程，这些线程不应该有很长的等待时间。在 Elasticsearch 日志中，也可能有长时间等待线程的证据。有关详细信息，请参阅网络线程模型。

默认情况下，从属检查将在 30 秒后超时，因此如果节点离开不可预测，则每 15 秒捕获一次堆栈转储，以确保在正确的时间至少进行一次堆栈转储。

#### 诊断"ShardLockContaintainFailedException"失败

如果一个节点离开并重新加入集群，那么 Elasticsearch 通常会关闭并重新初始化其分片。如果分片没有足够快地关闭，那么Elasticsearch可能无法由于"ShardLockObtainFailedException"而无法重新初始化它们。

要收集有关分片关闭缓慢原因的更多信息，请配置以下记录器：

    
    
    logger.org.elasticsearch.env.NodeEnvironment: DEBUG

启用此记录器后，Elasticsearch 将尝试在遇到"ShardLockObtainFailedException"时运行 Nodes hotthreads API。结果被压缩、编码并拆分为块以避免截断：

    
    
    [DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] [part 1]: H4sIAAAAAAAA/x...
    [DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] [part 2]: p7x3w1hmOQVtuV...
    [DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] [part 3]: v7uTboMGDbyOy+...
    [DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] [part 4]: 4tse0RnPnLeDNN...
    [DEBUG][o.e.e.NodeEnvironment    ] [master] hot threads while failing to obtain shard lock for [index][0] (gzip compressed, base64-encoded, and split into 4 parts on preceding log lines)

要重建输出，base64-解码数据并使用"gzip"解压缩。例如，在类Unix系统上：

    
    
    cat shardlock.log | sed -e 's/.*://' | base64 --decode | gzip --decompress

[« Publishing the cluster state](cluster-state-publishing.md) [Add and
remove nodes in your cluster »](add-elasticsearch-nodes.md)
