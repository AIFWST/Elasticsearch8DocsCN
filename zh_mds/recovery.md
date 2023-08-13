

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Index management settings](index-management-settings.md) [Indexing buffer
settings »](indexing-buffer.md)

## 索引恢复设置

对等恢复将数据从主分片同步到新的或现有的分片副本。

当 Elasticsearch 出现以下情况时，对等恢复会自动发生：

* 重新创建节点故障期间丢失的分片 * 由于集群重新平衡或分片分配设置更改，将分片重新定位到另一个节点

您可以使用 catrecovery API 查看正在进行的恢复和已完成的恢复列表。

#### 恢复设置

`indices.recovery.max_bytes_per_sec`

    

(动态)限制每个节点的总入站和出站恢复流量。适用于对等恢复和快照恢复(即从快照恢复)。默认为"40mb"，除非节点是专用的冷节点或冻结节点，在这种情况下，默认值与节点可用的总内存有关：

总内存 |冷节点和冻结节点的默认恢复速率 ---|--- ≤ 4 GB

|

4 GB ≤和 8 GB > 40 MB/秒

|

60 MB/秒> 8 GB 和 ≤ 16 GB

|

90 MB/秒> 16 GB 和 ≤ 32 GB

|

125 MB/秒 > 32 GB

|

250 MB/秒 此限制分别适用于每个节点。如果群集中的多个节点同时执行恢复，则群集的总恢复流量可能会超过此限制。

如果此限制过高，正在进行的恢复可能会消耗过多的带宽和其他资源，从而可能破坏群集的稳定性。

这是一个动态设置，这意味着您可以在每个节点的"elasticsearch.yml"配置文件中设置它，并且可以使用群集更新设置 API 动态更新它。如果动态设置，则相同的限制适用于群集中的每个节点。如果不动态设置，则可以在每个节点上设置不同的限制，如果某些节点的带宽比其他节点好，这将非常有用。例如，如果您使用的是索引生命周期管理，则可以为热节点提供比温节点更高的恢复带宽限制。

#### 专家对等恢复设置

您可以使用以下 _expert_ 设置来管理对等恢复的资源。

`indices.recovery.max_concurrent_file_chunks`

    

(动态，专家)每次恢复并行发送的文件区块数。默认为"2"。

当单个分片的恢复未达到"index.recovery.max_bytes_per_sec"设置的流量限制时，您可以增加此设置的值，最多为"8"。

`indices.recovery.max_concurrent_operations`

    

(动态，专家)为每个恢复并行发送的操作数。默认为"1"。

在恢复期间并发重播操作可能会占用大量资源，并且可能会干扰群集中的索引、搜索和其他活动。在未仔细验证群集是否具有可用于处理将产生的额外负载的资源之前，请勿增加此设置。

`indices.recovery.use_snapshots`

    

(动态，专家)启用基于快照的对等恢复。

Elasticsearch 使用 _peerrecovery_ 过程恢复副本并重新定位主分片，该过程涉及在目标节点上构建分片的新副本。当 'indices.recovery.use_snapshots' 为 'false' 时，Elasticsearch 将通过从当前主数据库传输索引数据来构造这个新副本。当此设置为"true"时，Elasticsearch 将首先尝试从最近的快照中复制索引数据，并且只有在无法识别合适的快照时才从主快照复制数据。默认为"真"。

如果群集在节点到节点数据传输成本高于从快照恢复数据的成本的环境中运行，则将此选项设置为"true"可降低运营成本。它还减少了主数据库在恢复期间必须执行的工作量。

此外，在恢复分片时，将参考设置为"use_for_peer_recovery=true"的存储库以查找良好的快照。如果所有已注册的存储库均未定义此设置，则将从源节点恢复索引文件。

`indices.recovery.max_concurrent_snapshot_file_downloads`

    

(动态，专家)每次恢复时并行发送到目标节点的快照文件下载请求数。默认为"5"。

在未仔细验证群集是否具有可用于处理将产生的额外负载的资源之前，请勿增加此设置。

`indices.recovery.max_concurrent_snapshot_file_downloads_per_node`

    

(动态，专家)针对所有恢复在目标节点中并行执行的快照文件下载请求数。默认为"25"。

在未仔细验证群集是否具有可用于处理将产生的额外负载的资源之前，请勿增加此设置。

#### 托管服务的恢复设置

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

将 Elasticsearch 作为托管服务运行时，以下设置允许服务为每个节点上的磁盘读取、磁盘写入和网络流量指定绝对最大带宽，并允许您根据这些绝对最大值控制每个节点上的最大恢复带宽。它们有两个效果：

1. 如果未设置"index.recovery.max_bytes_per_sec"，它们确定用于恢复的带宽，覆盖上述默认行为。  2. 它们对恢复带宽施加了节点范围的限制，该限制与"index.recovery.max_bytes_per_sec"的值无关。

如果未设置"index.recovery.max_bytes_per_sec"，则最大恢复带宽将计算为绝对最大带宽的比例。计算分别针对读取和写入流量执行。该服务分别使用"node.bandwidth.recovery.disk.read"、"node.bandwidth.recovery.disk.write"和"node.bandwidth.recovery.network"定义磁盘读取、磁盘写入和网络传输的绝对最大带宽，您可以通过调整"node.bandwidth.recovery.factor.read"和"node.bandwidth.recovery.factor.write"来设置可用于恢复的绝对最大带宽的比例。如果启用了操作员权限功能，则服务还可以使用这些设置的仅限操作员变体设置默认比例。

如果您设置了"index.recovery.max_bytes_per_sec"，那么Elasticsearch将使用它的值作为最大恢复带宽，只要这不超过节点范围的限制。Elasticsearch通过将绝对最大带宽乘以"node.bandwidth.recovery.operator.factor.max_overcommit"因子来计算节点范围的限制。如果设置的"index.recovery.max_bytes_per_sec"超过节点范围的限制，则节点范围的限制优先。

服务应通过试验确定绝对最大带宽设置的值，使用类似恢复的工作负载，其中有多个并发工作线程，每个工作线程以 512kiB 的块顺序处理文件。

`node.bandwidth.recovery.disk.read`

     ([byte value](api-conventions.html#byte-units "Byte size units") per second) The absolute maximum disk read speed for a recovery-like workload on the node. If set, `node.bandwidth.recovery.disk.write` and `node.bandwidth.recovery.network` must also be set. 
`node.bandwidth.recovery.disk.write`

     ([byte value](api-conventions.html#byte-units "Byte size units") per second) The absolute maximum disk write speed for a recovery-like workload on the node. If set, `node.bandwidth.recovery.disk.read` and `node.bandwidth.recovery.network` must also be set. 
`node.bandwidth.recovery.network`

     ([byte value](api-conventions.html#byte-units "Byte size units") per second) The absolute maximum network throughput for a recovery-like workload on the node, which applies to both reads and writes. If set, `node.bandwidth.recovery.disk.read` and `node.bandwidth.recovery.disk.write` must also be set. 
`node.bandwidth.recovery.factor.read`

     (float, [dynamic](settings.html#dynamic-cluster-setting)) The proportion of the maximum read bandwidth that may be used for recoveries if `indices.recovery.max_bytes_per_sec` is not set. Must be greater than `0` and not greater than `1`. If not set, the value of `node.bandwidth.recovery.operator.factor.read` is used. If no factor settings are set then the value `0.4` is used. 
`node.bandwidth.recovery.factor.write`

     (float, [dynamic](settings.html#dynamic-cluster-setting)) The proportion of the maximum write bandwidth that may be used for recoveries if `indices.recovery.max_bytes_per_sec` is not set. Must be greater than `0` and not greater than `1`. If not set, the value of `node.bandwidth.recovery.operator.factor.write` is used. If no factor settings are set then the value `0.4` is used. 
`node.bandwidth.recovery.operator.factor.read`

     (float, [dynamic](settings.html#dynamic-cluster-setting)) The proportion of the maximum read bandwidth that may be used for recoveries if `indices.recovery.max_bytes_per_sec` and `node.bandwidth.recovery.factor.read` are not set. Must be greater than `0` and not greater than `1`. If not set, the value of `node.bandwidth.recovery.operator.factor` is used. If no factor settings are set then the value `0.4` is used. When the operator privileges feature is enabled, this setting can be updated only by operator users. 
`node.bandwidth.recovery.operator.factor.write`

     (float, [dynamic](settings.html#dynamic-cluster-setting)) The proportion of the maximum write bandwidth that may be used for recoveries if `indices.recovery.max_bytes_per_sec` and `node.bandwidth.recovery.factor.write` are not set. Must be greater than `0` and not greater than `1`. If not set, the value of `node.bandwidth.recovery.operator.factor` is used. If no factor settings are set then the value `0.4` is used. When the operator privileges feature is enabled, this setting can be updated only by operator users. 
`node.bandwidth.recovery.operator.factor`

     (float, [dynamic](settings.html#dynamic-cluster-setting)) The proportion of the maximum bandwidth that may be used for recoveries if neither `indices.recovery.max_bytes_per_sec` nor any other factor settings are set. Must be greater than `0` and not greater than `1`. Defaults to `0.4`. When the operator privileges feature is enabled, this setting can be updated only by operator users. 
`node.bandwidth.recovery.operator.factor.max_overcommit`

     (float, [dynamic](settings.html#dynamic-cluster-setting)) The proportion of the absolute maximum bandwidth that may be used for recoveries regardless of any other settings. Must be greater than `0`. Defaults to `100`. When the operator privileges feature is enabled, this setting can be updated only by operator users. 

[« Index management settings](index-management-settings.md) [Indexing buffer
settings »](indexing-buffer.md)
