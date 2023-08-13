

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Circuit breaker settings](circuit-breaker.md) [Miscellaneous cluster
settings »](misc-cluster-settings.md)

## 集群级分片分配和路由设置

_Shard allocation_是将分片分配给节点的过程。这可能在初始恢复、副本分配、重新平衡或添加或删除节点时发生。

主节点的主要作用之一是决定将哪些分片分配给哪些节点，以及何时在节点之间移动分片以重新平衡集群。

有许多设置可用于控制分片分配过程：

* 集群级分片分配设置控制分配和重新平衡操作。  * 基于磁盘的分片分配设置解释了 Elasticsearch 如何考虑可用磁盘空间以及相关设置。  * 分片分配感知和强制感知控制如何在不同的机架或可用区之间分配分片。  * 集群级分片分配过滤允许从分配中排除某些节点或节点组，以便可以停用它们。

除此之外，还有其他一些杂项群集级别设置。

### 集群级分片分配设置

您可以使用以下设置来控制分片分配和恢复：

`cluster.routing.allocation.enable`

    

(动态)启用或禁用特定类型的分片分配：

* 'all' \-(默认)允许为所有类型的分片分配分片。  * "主分片" \- 仅允许为主分片分配分片。  * 'new_primaries' \- 仅允许为新索引的主分片分配分片。  * 'none' \- 不允许对任何索引进行任何类型的分片分配。

此设置不会影响重启节点时本地主分片的恢复。具有未分配的主分片副本的重新启动节点将立即恢复该主节点，前提是其分配 ID 与集群状态中的活动分配 ID 之一匹配。

`cluster.routing.allocation.node_concurrent_incoming_recoveries`

     ([Dynamic](settings.html#dynamic-cluster-setting)) How many concurrent incoming shard recoveries are allowed to happen on a node. Incoming recoveries are the recoveries where the target shard (most likely the replica unless a shard is relocating) is allocated on the node. Defaults to `2`. 
`cluster.routing.allocation.node_concurrent_outgoing_recoveries`

     ([Dynamic](settings.html#dynamic-cluster-setting)) How many concurrent outgoing shard recoveries are allowed to happen on a node. Outgoing recoveries are the recoveries where the source shard (most likely the primary unless a shard is relocating) is allocated on the node. Defaults to `2`. 
`cluster.routing.allocation.node_concurrent_recoveries`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A shortcut to set both `cluster.routing.allocation.node_concurrent_incoming_recoveries` and `cluster.routing.allocation.node_concurrent_outgoing_recoveries`. Defaults to 2. 
`cluster.routing.allocation.node_initial_primaries_recoveries`

     ([Dynamic](settings.html#dynamic-cluster-setting)) While the recovery of replicas happens over the network, the recovery of an unassigned primary after node restart uses data from the local disk. These should be fast so more initial primary recoveries can happen in parallel on the same node. Defaults to `4`. 

`cluster.routing.allocation.same_shard.host`

     ([Dynamic](settings.html#dynamic-cluster-setting)) If `true`, forbids multiple copies of a shard from being allocated to distinct nodes on the same host, i.e. which have the same network address. Defaults to `false`, meaning that copies of a shard may sometimes be allocated to nodes on the same host. This setting is only relevant if you run multiple nodes on each host. 

### 分片重新平衡设置

当集群在每个节点上具有相同数量的分片时，集群是_平衡的_，所有节点都需要相同的资源，而没有任何节点上任何索引的分片集中。Elasticsearch 运行一个名为 _rebalancing_ 的自动进程，该过程在集群中的节点之间移动分片以提高其平衡性。重新平衡遵循所有其他分片分配规则，例如分配过滤和强制感知，这可能会阻止它完全平衡集群。在这种情况下，重新平衡会努力在您配置的规则内实现最平衡的集群。如果您使用的是数据层，那么 Elasticsearch 会自动应用分配过滤规则，将每个分片放置在适当的层中。这些规则意味着平衡器在每个层中独立工作。

您可以使用以下设置来控制集群中分片的重新平衡：

`cluster.routing.rebalance.enable`

    

(动态)启用或禁用特定类型的分片的重新平衡：

* 'all' \-(默认)允许对各种分片进行分片平衡。  * "主分片" \- 仅允许主分片的分片均衡。  * "副本" \- 仅允许副本分片的分片平衡。  * 'none' \- 任何索引都不允许任何形式的分片平衡。

`cluster.routing.allocation.allow_rebalance`

    

(动态)指定何时允许分片重新平衡：

* "始终" \- 始终允许重新平衡。  * "indices_primaries_active" \- 仅当分配了集群中的所有主节点时。  * "indices_all_active" \-(默认值)仅当分配了集群中的所有分片(主分片和副本分片)时。

`cluster.routing.allocation.cluster_concurrent_rebalance`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Defines the number of concurrent shard rebalances are allowed across the whole cluster. Defaults to `2`. Note that this setting only controls the number of concurrent shard relocations due to imbalances in the cluster. This setting does not limit shard relocations due to [allocation filtering](modules-cluster.html#cluster-shard-allocation-filtering "Cluster-level shard allocation filtering") or [forced awareness](modules-cluster.html#forced-awareness "Forced awareness"). 
`cluster.routing.allocation.type`

    

选择用于计算集群余额的算法。默认为"desired_balance"，选择_desired余额allocator_。此分配器运行一个后台任务，该任务计算集群中所需的分片平衡。一旦这个后台任务完成，Elasticsearch就会将分片移动到它们想要的位置。

也可以设置为"平衡"以选择旧版_balanced allocator_。在 Elasticsearch 版本中，这个分配器是 8.6.0.It 在前台运行之前的默认分配器，防止主节点并行执行其他工作。它的工作原理是选择少量的分片移动，这会立即改善集群的平衡，当这些分片移动完成时，它会再次运行并选择另外几个分片进行移动。由于 thisallocator 仅根据集群的当前状态做出决策，因此在平衡集群时有时会多次移动分片。

### 分片平衡启发式设置

重新平衡的工作原理是根据分片的分配为每个节点计算一个 _weight_，然后在节点之间移动分片以减轻较重节点的权重并增加较轻节点的权重。当没有可能的分片移动可以使任何节点的权重接近任何其他节点的权重超过可配置的阈值时，集群是平衡的。

节点的权重取决于它持有的分片数量以及这些分片的总估计资源使用量，以磁盘上分片的大小和支持向分片的写入流量所需的线程数表示。Elasticsearch 估计属于数据流的分片在通过滚动更新创建时的资源使用情况。新分片的估计磁盘大小是数据流中其他分片的平均大小。新分片的估计写入负载是数据流中最近分片的实际写入负载的加权平均值。不属于数据流写入索引的分片的估计写入负载为零。

以下设置控制 Elasticsearch 如何将这些值组合成每个节点权重的总体度量。

`cluster.routing.allocation.balance.shard`

     (float, [Dynamic](settings.html#dynamic-cluster-setting)) Defines the weight factor for the total number of shards allocated to each node. Defaults to `0.45f`. Raising this value increases the tendency of Elasticsearch to equalize the total number of shards across nodes ahead of the other balancing variables. 
`cluster.routing.allocation.balance.index`

     (float, [Dynamic](settings.html#dynamic-cluster-setting)) Defines the weight factor for the number of shards per index allocated to each node. Defaults to `0.55f`. Raising this value increases the tendency of Elasticsearch to equalize the number of shards of each index across nodes ahead of the other balancing variables. 
`cluster.routing.allocation.balance.disk_usage`

     (float, [Dynamic](settings.html#dynamic-cluster-setting)) Defines the weight factor for balancing shards according to their predicted disk size in bytes. Defaults to `2e-11f`. Raising this value increases the tendency of Elasticsearch to equalize the total disk usage across nodes ahead of the other balancing variables. 
`cluster.routing.allocation.balance.write_load`

     (float, [Dynamic](settings.html#dynamic-cluster-setting)) Defines the weight factor for the write load of each shard, in terms of the estimated number of indexing threads needed by the shard. Defaults to `10.0f`. Raising this value increases the tendency of Elasticsearch to equalize the total write load across nodes ahead of the other balancing variables. 
`cluster.routing.allocation.balance.threshold`

     (float, [Dynamic](settings.html#dynamic-cluster-setting)) The minimum improvement in weight which triggers a rebalancing shard movement. Defaults to `1.0f`. Raising this value will cause Elasticsearch to stop rebalancing shards sooner, leaving the cluster in a more unbalanced state. 

无论平衡算法的结果如何，由于强制感知和分配筛选等分配规则，都可能不允许重新平衡。

### 基于磁盘的分片分配设置

基于磁盘的分片分配器可确保所有节点都有足够的磁盘空间，而无需执行不必要的分片移动。它根据一对称为_low watermark_和_highwater_的阈值分配分片。其主要目标是确保没有节点超过高水位线，或者至少任何此类超额只是暂时的。如果一个节点超过高水位线，那么Elasticsearch将通过将其部分分片移动到集群中的其他节点来解决这个问题。

节点不时暂时超过高水位线是正常的。

分配器还试图通过禁止向超过低水位线的节点分配更多分片来保持节点远离高水位线。重要的是，如果所有节点都超过了低水位线，则无法分配新的分片，Elasticsearch 将无法在节点之间移动任何分片，以保持磁盘使用率低于高水位线。必须确保群集总共有足够的磁盘空间，并且始终有一些节点低于低水位线。

由基于磁盘的分片分配器触发的分片移动还必须满足所有其他分片分配规则，例如分配过滤和强制感知。如果这些规则过于严格，那么它们还可以阻止保持节点磁盘使用不受控制所需的分片移动。如果您使用的是数据层，那么 Elasticsearch 会自动配置分配过滤规则，以将分片放置在适当的层中，这意味着基于磁盘的分片分配器在每个层中独立工作。

如果一个节点填满磁盘的速度比Elasticsearch将分片移动到其他地方的速度快，那么磁盘就有完全填满的风险。为了防止这种情况，作为最后的手段，一旦磁盘使用率达到 _flood-stage_watermark Elasticsearch 将阻止对受影响节点上带有分片的索引的写入。它还将继续将分片移动到集群中的其他节点上。当受影响节点上的磁盘使用率低于高水位线时，Elasticsearch 会自动删除写入块。请参阅修复水印错误以解决持久性水印错误。

群集中的节点使用非常不同的磁盘空间量是正常的。集群的余额仅取决于每个节点上的分片数量以及这些分片所属的索引。它既不考虑这些分片的大小，也不考虑每个节点上的可用磁盘空间，原因如下：

* 磁盘使用情况随时间变化。平衡单个节点的磁盘使用情况需要更多的分片移动，甚至可能浪费地撤消早期的移动。移动分片会消耗 I/O 和网络带宽等资源，并可能从文件系统缓存中逐出数据。在可能的情况下，这些资源最好用于处理搜索和索引。  * 每个节点上磁盘使用量相等的集群通常不会比磁盘使用率不相等的集群的性能更好，只要没有磁盘太满。

可以使用以下设置来控制基于磁盘的分配：

`cluster.routing.allocation.disk.threshold_enabled`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Defaults to `true`. Set to `false` to disable the disk allocation decider. Upon disabling, it will also remove any existing `index.blocks.read_only_allow_delete` index blocks. 

'cluster.routing.allocation.disk.watermark.low' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) Controls the low watermark for disk usage. It defaults to `85%`, meaning that Elasticsearch will not allocate shards to nodes that have more than 85% disk used. It can alternatively be set to a ratio value, e.g., `0.85`. It can also be set to an absolute byte value (like `500mb`) to prevent Elasticsearch from allocating shards if less than the specified amount of space is available. This setting has no effect on the primary shards of newly-created indices but will prevent their replicas from being allocated. 
`cluster.routing.allocation.disk.watermark.low.max_headroom`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Controls the max headroom for the low watermark (in case of a percentage/ratio value). Defaults to 200GB when `cluster.routing.allocation.disk.watermark.low` is not explicitly set. This caps the amount of free space required. 

'cluster.routing.allocation.disk.watermark.high' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) Controls the high watermark. It defaults to `90%`, meaning that Elasticsearch will attempt to relocate shards away from a node whose disk usage is above 90%. It can alternatively be set to a ratio value, e.g., `0.9`. It can also be set to an absolute byte value (similarly to the low watermark) to relocate shards away from a node if it has less than the specified amount of free space. This setting affects the allocation of all shards, whether previously allocated or not. 
`cluster.routing.allocation.disk.watermark.high.max_headroom`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Controls the max headroom for the high watermark (in case of a percentage/ratio value). Defaults to 150GB when `cluster.routing.allocation.disk.watermark.high` is not explicitly set. This caps the amount of free space required. 
`cluster.routing.allocation.disk.watermark.enable_for_single_data_node`

     ([Static](settings.html#static-cluster-setting)) In earlier releases, the default behaviour was to disregard disk watermarks for a single data node cluster when making an allocation decision. This is deprecated behavior since 7.14 and has been removed in 8.0. The only valid value for this setting is now `true`. The setting will be removed in a future release. 

"cluster.routing.allocation.disk.watermark.flood_stage"！[徽标云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

    

(动态)控制泛洪阶段水印，默认为 95%。Elasticsearch 在节点上分配了一个或更多分片且至少有一个磁盘超过泛洪阶段的每个索引上强制实施只读索引块 ('index.blocks.read_only_allow_delete')。此设置是防止节点磁盘空间不足的最后手段。当磁盘利用率低于高水位线时，将自动释放索引块。与低水位线和高水位线值类似，也可以将其设置为比率值，例如"0.95"或绝对字节值。

重置"my-index-000001"索引上的只读索引块的示例：

    
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        "index.blocks.read_only_allow_delete": nil
      }
    )
    puts response
    
    
    PUT /my-index-000001/_settings
    {
      "index.blocks.read_only_allow_delete": null
    }

`cluster.routing.allocation.disk.watermark.flood_stage.max_headroom`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Controls the max headroom for the flood stage watermark (in case of a percentage/ratio value). Defaults to 100GB when `cluster.routing.allocation.disk.watermark.flood_stage` is not explicitly set. This caps the amount of free space required. 

您不能在"cluster.routing.allocation.disk.watermark.low"、"cluster.routing.allocation.disk.watermark.high"和"cluster.routing.allocation.disk.watermark.flood_stage"设置中混合使用百分比/比率值和字节值。所有值都设置为百分比/比率值，或者所有值都设置为字节值。这种实施是为了让 Elasticsearch 可以验证设置在内部是否一致，确保磁盘低阈值小于高磁盘阈值，磁盘高阈值小于泛洪阶段阈值。对最大净空值进行了类似的比较检查。

"cluster.routing.allocation.disk.watermark.flood_stage.冻结"！[徽标云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) Controls the flood stage watermark for dedicated frozen nodes, which defaults to 95%. 
`cluster.routing.allocation.disk.watermark.flood_stage.frozen.max_headroom`
[![logo cloud](https://doc-icons.s3.us-
east-2.amazonaws.com/logo_cloud.svg)](https://www.elastic.co/cloud/elasticsearch-
service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) Controls the max headroom for the flood stage watermark (in case of a percentage/ratio value) for dedicated frozen nodes. Defaults to 20GB when `cluster.routing.allocation.disk.watermark.flood_stage.frozen` is not explicitly set. This caps the amount of free space required on dedicated frozen nodes. 
`cluster.info.update.interval`

     ([Dynamic](settings.html#dynamic-cluster-setting)) How often Elasticsearch should check on disk usage for each node in the cluster. Defaults to `30s`. 

百分比值是指已用磁盘空间，而字节值是指可用磁盘空间。这可能会令人困惑，因为它颠倒了高低的含义。例如，将低水位线设置为 10gb，将高水位线设置为 5gb 是有意义的，但反之则不然。

将低水位线更新为至少 100 GB 可用水位线、至少 50 GB 可用水位线和 10 GB 可用泛洪阶段水印的示例，并每分钟更新有关群集的信息：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.disk.watermark.low": '100gb',
          "cluster.routing.allocation.disk.watermark.high": '50gb',
          "cluster.routing.allocation.disk.watermark.flood_stage": '10gb',
          "cluster.info.update.interval": '1m'
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.disk.watermark.low": "100gb",
        "cluster.routing.allocation.disk.watermark.high": "50gb",
        "cluster.routing.allocation.disk.watermark.flood_stage": "10gb",
        "cluster.info.update.interval": "1m"
      }
    }

关于水印的最大净空设置，请注意，这些设置仅适用于水印设置为百分比/比率的情况。最大净空值的目的是在达到相应的水位线之前限制所需的可用磁盘空间。这对于具有较大磁盘的服务器特别有用，其中百分比/比率水印可以转换为较大的可用磁盘空间要求，并且最大空间可用于限制所需的可用磁盘空间量。例如，让我们采用洪水水印的默认设置。它具有 95% 的默认值，洪水最大净空设置的默认值为 100GB。这意味着：

* 对于较小的磁盘，例如 100GB，泛洪水位线将达到 95%，这意味着 5GB 的可用空间，因为 5GB 小于 100GB 的最大动态余量值。  * 对于较大的磁盘，例如 100TB，泛洪水位线将达到 100GB 的可用空间。这是因为仅 95% 的泛洪水位线就需要 5TB 的可用磁盘空间，但这被最大净空设置为 100GB 的限制。

最后，仅当未明确设置水印设置时，最大净空设置才具有其默认值(因此，它们具有默认百分比值)。如果显式设置了水印，则最大净空设置没有其默认值，如果需要，则需要显式设置。

### 分片分配意识

您可以使用自定义节点属性作为_awareness attributes_，使 Elasticsearch 在分配分片时考虑您的物理硬件配置。如果 Elasticsearch 知道哪些节点位于同一物理服务器上、同一机架或同一区域中，它可以分发主分片及其副本分片，以最大程度地降低发生故障时丢失所有分片副本的风险。

当使用动态"cluster.routing.allocation.awareness.attributes"设置启用分片分配感知时，分片仅分配给具有为指定感知属性设置值的节点。如果您使用多个感知属性，Elasticsearch 在分配分片时会单独考虑每个属性。

属性值的数量决定了在每个位置分配的分片副本数。如果每个位置的节点数量不平衡，并且存在大量副本，则副本分片可能会未分配。

#### 启用分片分配感知

要启用分片分配感知，请执行以下操作：

1. 使用自定义节点属性指定每个节点的位置。例如，如果您希望 Elasticsearch 将分片分布在不同的机架上，您可以在每个节点的 'elasticsearch.yml' 配置文件中设置一个名为 'rack_id' 的感知属性。           node.attr.rack_id：rack_one

您还可以在启动节点时设置自定义属性：

    
        ./bin/elasticsearch -Enode.attr.rack_id=rack_one

2. 告诉 Elasticsearch 在分配分片时考虑一个或多个感知属性，方法是在每个符合主节点条件的 'elasticsearch.yml' 配置文件中设置 'cluster.routing.allocation.awareness.attributes'。           cluster.routing.allocation.awareness.attributes： rack_id __

__

|

将多个属性指定为逗号分隔的列表。   ---|--- 您还可以使用群集更新设置 API 来设置或更新群集的感知属性。

使用此示例配置，如果启动两个将"node.attr.rack_id"设置为"rack_one"的节点，并创建一个包含 5 个主分片和每个主节点的 1 个副本的索引，则所有主节点和副本都分布在这两个节点上。

如果添加两个将"node.attr.rack_id"设置为"rack_two"的节点，Elasticsearch 会将分片移动到新节点，确保(如果可能)同一分片的两个副本不会在同一机架中。

如果"rack_two"失败并关闭了其两个节点，默认情况下，Elasticsearch会将丢失的分片副本分配给"rack_one"中的节点。要防止在同一位置分配特定分片的多个副本，您可以启用强制感知。

#### 强制感知

默认情况下，如果一个位置发生故障，Elasticsearch 会将所有缺失的副本分片分配给其余位置。虽然您可能在所有位置都有足够的资源来托管主分片和副本分片，但单个位置可能无法托管分片的 **ALL**。

为了防止单个位置在发生故障时过载，您可以设置"cluster.routing.allocation.awareness.force"，以便在节点在另一个位置可用之前不分配副本。

例如，如果您有一个名为"zone"的感知属性，并且在"zone1"和"zone2"中配置节点，则可以使用强制感知来阻止Elasticsearch在只有一个可用区域时分配副本：

    
    
    cluster.routing.allocation.awareness.attributes: zone
    cluster.routing.allocation.awareness.force.zone.values: zone1,zone2 __

__

|

指定意识属性的所有可能值。   ---|--- 在此示例配置中，如果您启动两个节点，并将"node.attr.zone"设置为"zone1"，并创建一个包含 5 个分片和 1 个副本的索引，Elasticsearch 会创建索引并分配 5 个主分片，但不分配副本。仅当"node.attr.zone"设置为"zone2"的节点可用时，才会分配副本。

### 集群级分片分配过滤

您可以使用集群级分片分配过滤器来控制 Elasticsearch 从任何索引分配分片的位置。这些群集范围的筛选器与每个索引的分配筛选和分配感知结合使用。

分片分配过滤器可以基于自定义节点属性或内置的"_name"、"_host_ip"、"_publish_ip"、"_ip"、"_host"、"_id"和"_tier"属性。

"cluster.routeting.allocation"设置是动态的，允许将实时索引从一组节点移动到另一组节点。只有在可以这样做而不破坏另一个路由约束的情况下重新定位分片，例如从不在同一节点上分配主分片和副本分片。

集群级分片分配筛选的最常见用例是当您想要停用节点时。要在关闭节点之前将分片移出节点，您可以创建一个过滤器，通过节点的 IP 地址排除该节点：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.exclude._ip": '10.0.0.1'
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.routing.allocation.exclude._ip" : "10.0.0.1"
      }
    }

#### 群集路由设置

`cluster.routing.allocation.include.{attribute}`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Allocate shards to a node whose `{attribute}` has at least one of the comma-separated values. 
`cluster.routing.allocation.require.{attribute}`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Only allocate shards to a node whose `{attribute}` has _all_ of the comma-separated values. 
`cluster.routing.allocation.exclude.{attribute}`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Do not allocate shards to a node whose `{attribute}` has _any_ of the comma-separated values. 

群集分配设置支持以下内置属性：

`_name`

|

按节点名称匹配节点 ---|--- '_host_ip'

|

按主机 IP 地址(与主机名关联的 IP)"_publish_ip"匹配节点

|

通过发布 IP 地址"_ip"匹配节点

|

匹配"_host_ip"或"_publish_ip""_host"

|

按主机名"_id"匹配节点

|

按节点 ID "_tier"匹配节点

|

按节点的数据层角色匹配节点 "_tier"筛选基于节点角色。只有一部分角色是数据层角色，通用数据角色将与任何层筛选匹配。作为数据层角色的角色子集，但通用数据角色将与任何层筛选匹配。

指定属性值时可以使用通配符，例如：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.exclude._ip": '192.168.2.*'
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.exclude._ip": "192.168.2.*"
      }
    }

[« Circuit breaker settings](circuit-breaker.md) [Miscellaneous cluster
settings »](misc-cluster-settings.md)
