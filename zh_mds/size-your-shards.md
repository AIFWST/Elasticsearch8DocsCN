

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[How
to](how-to.md)

[« Tune for disk usage](tune-for-disk-usage.md) [Use Elasticsearch for time
series data »](use-elasticsearch-for-time-series-data.md)

## 大小你的分片

Elasticsearch 中的每个索引都分为一个或多个分片，每个分片可以跨多个节点复制，以防止硬件故障。如果您使用的是_Data streams_则每个数据流都由一系列索引提供支持。您可以在单个节点上存储的数据量存在限制，因此您可以通过添加节点并增加要匹配的索引和分片数量来增加集群的容量。但是，每个索引和分片都有一些开销，如果将数据划分到太多分片上，则开销可能会变得不堪重负。具有太多索引或分片的集群被称为遭受_过度分片_的影响。过度分片的集群在响应搜索时效率会降低，在极端情况下，它甚至可能变得不稳定。

### 创建分片策略

防止过度分片和其他与分片相关的问题的最佳方法是创建分片策略。分片策略可帮助您确定和维护集群的最佳分片数量，同时限制这些分片的大小。

不幸的是，没有一刀切的分片策略。在一个环境中有效的策略可能无法在另一个环境中扩展。一个好的分片策略必须考虑您的基础设施、用例和性能预期。

创建分片策略的最佳方法是使用与生产中相同的查询和索引负载，在生产硬件上对生产数据进行基准测试。有关我们推荐的方法，请观看定量聚类大小调整视频。在测试不同的分片配置时，请使用 Kibana 的 Elasticsearchmonitoring 工具来跟踪集群的稳定性和性能。

以下部分提供了在设计分片策略时应考虑的一些提醒和准则。如果您的集群已分片，请参阅减少集群的分片计数。

### 大小调整注意事项

在构建分片策略时，请记住以下事项。

#### 搜索在单个线程 pershard 上运行

大多数搜索会命中多个分片。每个分片在单个 CPU 线程上运行搜索。虽然一个分片可以运行多个并发搜索，但跨大量分片的搜索可能会耗尽节点的搜索线程池。这可能会导致吞吐量低和搜索速度变慢。

#### 每个索引、分片、段和字段都有开销

每个索引和每个分片都需要一些内存和 CPU 资源。在大多数情况下，一小组大型分片比许多小分片使用更少的资源。

段在分片的资源使用中起着重要作用。大多数分片包含多个段，这些段存储其索引数据。Elasticsearch 将一些段元数据保留在堆内存中，以便可以快速检索以进行搜索。随着 ashard 的增长，其段被合并为更少、更大的段。这减少了段的数量，这意味着堆内存中保留了无元数据。

每个映射字段还会在内存使用和磁盘空间方面产生一些开销。默认情况下，Elasticsearch 会自动为其索引的每个文档中的每个字段创建一个映射，但您可以关闭此行为来控制映射。

此外，每个段都需要为每个映射字段提供少量的堆内存。此每个字段段的堆开销包括字段名称的副本，如果适用，则使用 ISO-8859-1 进行编码，否则使用 UTF-16 进行编码。通常这并不明显，但是如果您的分片具有高段计数并且相应的映射包含高字段计数和/或非常长的字段名称，则可能需要考虑此开销。

#### Elasticsearch 自动平衡数据层内的分片

群集的节点分组到数据层中。在每个层中，Elasticsearch 尝试将索引的分片分布在尽可能多的节点上。当您添加新节点或节点失败时，Elasticsearch 会自动在层的剩余节点之间重新平衡索引的分片。

### 最佳实践

如果适用，请使用以下最佳实践作为强化策略的起点。

#### 删除索引，不删除文档

删除的文档不会立即从 Elasticsearch 的文件系统中删除。相反，Elasticsearch 在每个相关分片上将文档标记为已删除。标记的文档将继续使用资源，直到在非定期段合并期间将其删除。

如果可能，请改为删除整个索引。Elasticsearch 可以立即直接从文件系统中删除已删除的索引并释放资源。

#### 将数据流和 ILM 用于时序数据

数据流允许您跨多个基于时间的支持索引存储时间序列数据。您可以使用索引生命周期管理 (ILM) 自动管理这些后备索引。

此设置的一个优点是自动滚动更新，当当前写入索引达到定义的"max_primary_shard_size"、"max_age"、"max_docs"或"max_size"阈值时，它会创建新的写入索引。当不再需要索引时，您可以使用 ILM 自动删除索引并释放资源。

ILM 还使随着时间的推移更改分片策略变得容易：

* **想要减少新索引的分片计数？** 更改数据流的匹配索引模板中的"index.number_of_shards"设置。

* **需要更大的分片或更少的后备索引？** 提高 ILM 策略的滚动更新阈值。

* **需要跨越较短间隔的索引？** 通过更快地删除旧索引来抵消增加的分片计数。您可以通过降低策略删除阶段的"min_age"阈值来执行此操作。

每个新的支持指数都是进一步调整策略的机会。

#### 目标是最多 200M 个文档的分片，或者大小在 10GB 到 50GB 之间

在集群管理和搜索性能方面，每个分片都有一些相关的开销。搜索一千个 50MB 分片将比搜索包含相同数据的单个 50GB 分片昂贵得多。但是，非常大的分片也可能导致搜索速度变慢，并且在失败后需要更长的时间才能恢复。

分片的物理大小没有硬性限制，理论上每个分片最多可以包含超过 20 亿个文档。但是，经验表明，只要每个分片的文档计数保持在 2 亿以下，10GB 到 50GB 之间的分片通常适用于许多用例。

根据您的网络和用例，您可能能够使用较大的分片，较小的分片可能适用于 EnterpriseSearch 和类似用例。

如果使用 ILM，请将翻转操作的"max_primary_shard_size"阈值设置为"50GB"，以避免分片大于 50GB。

要查看分片的当前大小，请使用猫分片 API。

    
    
    response = client.cat.shards(
      v: true,
      h: 'index,prirep,shard,store',
      s: 'prirep,store',
      bytes: 'gb'
    )
    puts response
    
    
    GET _cat/shards?v=true&h=index,prirep,shard,store&s=prirep,store&bytes=gb

"pri.store.size"值显示索引的所有主分片的组合大小。

    
    
    index                                 prirep shard store
    .ds-my-data-stream-2099.05.06-000001  p      0      50gb
    ...

#### 符合主节点条件的节点每 3000 个索引应至少有 1GB 的堆

主节点可以管理的索引数量与其堆大小成正比。每个索引所需的确切堆内存量取决于各种因素，例如映射的大小和每个索引的分片数。

作为一般经验法则，主节点上每 GB 堆的索引数应少于 3000 个。例如，如果您的集群具有专用主节点，每个节点的堆数为 4GB，则索引数应少于 12000 个。如果您的主节点不是专用主节点，则适用相同的大小调整指南：您应该在每个符合主节点条件的节点上为集群中的每 3000 个索引保留至少 1GB 的堆。

请注意，此规则定义了 amaster 节点可以管理的绝对最大索引数，但不能保证涉及这么多索引的搜索或索引的性能。您还必须确保数据节点有足够的资源用于工作负载，并且整体分片策略满足所有性能要求。另请参阅在每个分片的单个线程上运行搜索和每个索引、分片、段和字段都有开销。

要检查每个节点堆的配置大小，请使用 cat 节点 API。

    
    
    response = client.cat.nodes(
      v: true,
      h: 'heap.max'
    )
    puts response
    
    
    GET _cat/nodes?v=true&h=heap.max

您可以使用 cat 分片 API 检查每个节点的分片数量。

    
    
    response = client.cat.shards(
      v: true
    )
    puts response
    
    
    GET _cat/shards?v=true

#### 为字段映射器和开销留出足够的堆

映射字段在每个节点上消耗一些堆内存，并且需要额外的堆 on data 节点。确保每个节点都有足够的堆用于映射，并为与其工作负载关联的开销留出额外的空间。以下各节演示如何确定这些堆要求。

##### 在群集状态中映射元数据

群集中的每个节点都有一个群集状态的副本。群集状态包括有关每个索引的字段映射的信息。此信息具有堆积量。您可以使用集群统计信息 API 获取重复数据删除和压缩后所有映射的总大小的堆开销。

    
    
    response = client.cluster.stats(
      human: true,
      filter_path: 'indices.mappings.total_deduplicated_mapping_size*'
    )
    puts response
    
    
    GET _cluster/stats?human&filter_path=indices.mappings.total_deduplicated_mapping_size*

这将向您显示如下例输出中的信息：

    
    
    {
      "indices": {
        "mappings": {
          "total_deduplicated_mapping_size": "1gb",
          "total_deduplicated_mapping_size_in_bytes": 1073741824
        }
      }
    }

##### 检索堆大小和字段映射器开销

您可以使用节点统计信息 API 获取每个节点的两个相关指标：

* 每个节点上的堆大小。  * 每个节点的字段的任何额外估计堆开销。这是特定于数据节点的，除了上面提到的集群状态字段信息之外，数据节点持有的索引的每个映射字段都有额外的堆开销。对于不是数据节点的节点，此字段可能为零。

    
    
    response = client.nodes.stats(
      human: true,
      filter_path: 'nodes.*.name,nodes.*.indices.mappings.total_estimated_overhead*,nodes.*.jvm.mem.heap_max*'
    )
    puts response
    
    
    GET _nodes/stats?human&filter_path=nodes.*.name,nodes.*.indices.mappings.total_estimated_overhead*,nodes.*.jvm.mem.heap_max*

对于每个节点，这将向您显示如下例输出中的信息：

    
    
    {
      "nodes": {
        "USpTGYaBSIKbgSUJR2Z9lg": {
          "name": "node-0",
          "indices": {
            "mappings": {
              "total_estimated_overhead": "1gb",
              "total_estimated_overhead_in_bytes": 1073741824
            }
          },
          "jvm": {
            "mem": {
              "heap_max": "4gb",
              "heap_max_in_bytes": 4294967296
            }
          }
        }
      }
    }

##### 考虑额外的堆积压

除了上述两个字段开销指标之外，您还必须为 Elasticsearch 的基准使用情况以及您的工作负载(如索引、搜索和聚合)留出足够的堆。0.5GB 的额外堆足以满足任何合理的工作负载，如果您的工作负载非常轻，而繁重的工作负载可能需要更多，则可能需要更少。

#####Example

例如，请考虑上述数据节点的输出。节点的堆至少需要：

* 1 GB 用于群集状态字段信息。  * 1 GB 用于数据节点字段的额外估计堆开销。  * 0.5 GB 的额外堆用于其他开销。

由于节点在示例中的最大堆大小为 4GB，因此对于所需的总堆 2.5GB 来说已经足够了。

如果节点的堆最大大小不足，请考虑避免使用不必要的字段、纵向扩展集群或重新分发索引分片。

请注意，上述规则不一定保证涉及大量索引的搜索或索引的性能。您还必须确保数据节点有足够的资源用于工作负载，并且整体分片策略满足所有性能要求。另请参阅搜索在每个分片的单个线程上运行，并且每个索引、分片、段和字段都有开销。

#### 避免节点热点

如果分配给特定节点的分片过多，则该节点可能会成为热点。例如，如果单个节点包含太多分片，索引量较高，则该节点可能会出现问题。

为防止热点，请使用"index.routing.allocation.total_shards_per_node"索引设置明确限制单个节点上的分片数量。您可以使用更新索引设置 API 配置"index.routing.allocation.total_shards_per_node"。

    
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        index: {
          "routing.allocation.total_shards_per_node": 5
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_settings
    {
      "index" : {
        "routing.allocation.total_shards_per_node" : 5
      }
    }

#### 避免不必要的映射字段

默认情况下，Elasticsearch 会自动为其索引的每个文档中的每个字段创建映射。每个映射的字段对应于磁盘上的一些数据结构，这些结构是在此字段上进行有效搜索、检索和聚合所必需的。有关每个映射字段的详细信息也保存在内存中。在许多情况下，此开销是不必要的，因为字段未在任何搜索或聚合中使用。使用_Explicit mapping_而不是动态映射来避免创建从未使用的字段。如果字段集合通常一起使用，请考虑使用"copy_to"在索引时合并它们。如果 afield 很少使用，则最好将其设为运行时字段。

您可以获取有关哪些字段正在与字段使用情况统计信息 API 一起使用的信息，并且可以使用分析索引磁盘使用情况 API 分析映射字段的磁盘使用情况。但是请注意，不必要的映射字段也会带来一些内存开销及其磁盘使用情况。

### 减少集群的分片计数

如果您的集群已经分片过多，您可以使用以下一种或多种方法来减少其分片计数。

#### 创建涵盖较长时间段的索引

如果使用 ILM 并且保留策略允许，请避免对滚动更新操作使用"max_age"阈值。相反，请使用"max_primary_shard_size"以避免创建空索引或许多小分片。

如果保留策略需要"max_age"阈值，请将其增加到覆盖较长时间间隔的创建索引。例如，您可以每周或每月创建索引，而不是创建每日索引。

#### 删除空索引或不需要的索引

如果您使用的是 ILM 并基于"max_age"阈值滚动更新索引，则可能会无意中创建没有文档的索引。这些空索引不提供任何好处，但仍会消耗资源。

您可以使用猫计数 API 找到这些空索引。

    
    
    response = client.cat.count(
      index: 'my-index-000001',
      v: true
    )
    puts response
    
    
    GET _cat/count/my-index-000001?v=true

获得空索引列表后，可以使用 deleteindex API 将其删除。您还可以删除任何其他不需要的索引。

    
    
    response = client.indices.delete(
      index: 'my-index-000001'
    )
    puts response
    
    
    DELETE my-index-000001

#### 在非高峰时段强制合并

如果您不再写入索引，则可以使用强制合并 API 将较小的段合并为较大的段。这可以减少分片开销并提高搜索速度。但是，强制合并会占用大量资源。如果可能，请在非高峰时段运行强制合并。

    
    
    response = client.indices.forcemerge(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST my-index-000001/_forcemerge

#### 将现有索引缩减为更少的分片

如果您不再写入索引，则可以使用收缩索引 API 来减少其分片计数。

ILM 还对处于暖期的索引具有收缩操作。

#### 组合较小的索引

您还可以使用重新索引 API 将具有类似映射的索引合并到单个大型索引中。对于时间序列数据，您可以将短时间段的索引重新索引为涵盖较长时间段的新索引。例如，您可以将 10 月份的每日指数(如"my-index-2099.10.11")重新编制索引为每月"my-index-2099.10"索引。重新索引后，删除较小的索引。

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-index-2099.10.*'
        },
        dest: {
          index: 'my-index-2099.10'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "index": "my-index-2099.10.*"
      },
      "dest": {
        "index": "my-index-2099.10"
      }
    }

### 排查分片相关错误

下面介绍了如何解决常见的分片相关错误。

#### 此操作将添加 x] 个分片总数，但此集群当前具有 [y]/[z] 个最大分片打开数;[

"cluster.max_shards_per_node"集群设置限制了集群的最大开放分片数。此错误表示操作将超过此限制。

如果您确信更改不会破坏集群的稳定性，则可以使用集群更新设置 API 暂时提高限制，然后重试该操作。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.max_shards_per_node": 1200
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node": 1200
      }
    }

这种增加应该只是暂时的。作为长期解决方案，建议将节点添加到分片过多的数据层或减少群集的分片计数。要在进行更改后获取集群的当前分片计数，请使用集群统计信息 API。

    
    
    response = client.cluster.stats(
      filter_path: 'indices.shards.total'
    )
    puts response
    
    
    GET _cluster/stats?filter_path=indices.shards.total

当长期解决方案到位时，我们建议您重置"cluster.max_shards_per_node"限制。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.max_shards_per_node": nil
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.max_shards_per_node": null
      }
    }

[« Tune for disk usage](tune-for-disk-usage.md) [Use Elasticsearch for time
series data »](use-elasticsearch-for-time-series-data.md)
