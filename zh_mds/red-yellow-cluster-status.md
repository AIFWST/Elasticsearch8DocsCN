

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix common cluster issues](fix-
common-cluster-issues.md)

[« High JVM memory pressure](high-jvm-memory-pressure.md) [Rejected requests
»](rejected-requests.md)

## 红色或黄色簇状态

红色或黄色集群状态表示一个或多个分片缺失或未分配。这些未分配的分片会增加数据丢失的风险，并降低集群性能。

#### 诊断群集状态

**检查群集状态**

使用群集运行状况 API。

    
    
    response = client.cluster.health(
      filter_path: 'status,*_shards'
    )
    puts response
    
    
    GET _cluster/health?filter_path=status,*_shards

运行状况良好的群集具有绿色"状态"和零"unassigned_shards"。黄色状态表示仅未分配副本。红色状态表示一个或多个主分片未分配。

**查看未分配的分片**

要查看未分配的分片，请使用猫分片 API。

    
    
    response = client.cat.shards(
      v: true,
      h: 'index,shard,prirep,state,node,unassigned.reason',
      s: 'state'
    )
    puts response
    
    
    GET _cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state

未分配的分片具有"未分配"的"状态"。对于主分片，"prirep"值为"p"，对于副本，值为"r"。

要了解未分配分片未分配的原因以及必须采取哪些操作才能允许 Elasticsearch 分配该分片，请使用集群分配说明 API。

    
    
    GET _cluster/allocation/explain?filter_path=index,node_allocation_decisions.node_name,node_allocation_decisions.deciders.*
    {
      "index": "my-index",
      "shard": 0,
      "primary": false
    }

#### 修复红色或黄色群集状态

分片可能由于多种原因而未分配。以下提示概述了最常见的原因及其解决方案。

##### 重新启用分片分配

通常在重新启动或其他群集维护期间禁用分配。如果您之后忘记重新启用分配，Elasticsearch 将无法分配分片。要重新启用分配，请重置"cluster.routing.allocation.enable"群集设置。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.enable": nil
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.routing.allocation.enable" : null
      }
    }

##### 恢复丢失的节点

当数据节点离开集群时，分片通常会变为未分配状态。发生这种情况的原因有多种，从连接问题到硬件故障。解决问题并恢复节点后，它将重新加入群集。然后，Elasticsearch 将自动分配任何未分配的分片。

为了避免在临时问题上浪费资源，Elasticsearch 默认延迟分配一分钟。如果已恢复节点并且不想等待延迟期，则可以调用不带参数的群集重新路由 API 来启动分配过程。该过程在后台异步运行。

    
    
    response = client.cluster.reroute(
      metric: 'none'
    )
    puts response
    
    
    POST _cluster/reroute?metric=none

##### 修复分配设置

配置错误的分配设置可能会导致未分配的主分片。这些设置包括：

* 分片分配索引设置 * 分配筛选群集设置 * 分配感知群集设置

若要查看分配设置，请使用获取索引设置和群集获取设置 API。

    
    
    response = client.indices.get_settings(
      index: 'my-index',
      flat_settings: true,
      include_defaults: true
    )
    puts response
    
    response = client.cluster.get_settings(
      flat_settings: true,
      include_defaults: true
    )
    puts response
    
    
    GET my-index/_settings?flat_settings=true&include_defaults=true
    
    GET _cluster/settings?flat_settings=true&include_defaults=true

可以使用更新索引设置和群集更新设置 API 更改设置。

##### 分配或减少副本

为了防止硬件故障，Elasticsearch 不会将副本分配给与其主分片相同的节点。如果没有其他数据节点可用于托管副本，则副本将保持未分配状态。要解决此问题，您可以：

* 将数据节点添加到同一层以托管副本。  * 更改"index.number_of_replicas"索引设置以减少每个主分片的副本数量。建议每个主数据库至少保留一个副本。

    
    
    response = client.indices.put_settings(
      body: {
        "index.number_of_replicas": 1
      }
    )
    puts response
    
    
    PUT _settings
    {
      "index.number_of_replicas": 1
    }

##### 释放或增加磁盘空间

Elasticsearch 使用低磁盘水位线来确保数据节点有足够的磁盘空间来存储传入的分片。默认情况下，Elasticsearch 不会将分片分配给使用超过 85% 磁盘空间的节点。

要检查节点的当前磁盘空间，请使用 cat 分配 API。

    
    
    response = client.cat.allocation(
      v: true,
      h: 'node,shards,disk.*'
    )
    puts response
    
    
    GET _cat/allocation?v=true&h=node,shards,disk.*

如果您的节点磁盘空间不足，您有以下几种选择：

* 升级节点以增加磁盘空间。  * 删除不需要的索引以释放空间。如果使用 ILM，则可以更新生命周期策略以使用可搜索的快照或添加删除阶段。如果不再需要搜索数据，可以使用快照将其存储在群集外。  * 如果您不再写入索引，请使用强制合并 API 或 ILM 的强制合并操作将其段合并为更大的段。           响应 = client.index.forcemerge( index： 'my-index' ) 把响应 POST my-index/_forcemerge

* 如果索引是只读的，请使用收缩索引 API 或 ILM 的收缩操作来减少其主分片计数。           响应 = client.indices.shrink( index： 'my-index'， target： 'my-shrinkken-index' ) put response POST my-index/_shrink/my-shrinkken-index

* 如果您的节点磁盘容量较大，您可以增加低磁盘水位线或将其设置为显式字节值。           PUT _cluster/settings { "persistent"： { "cluster.routing.allocation.disk.watermark.low"： "30gb" } }

##### 降低 JVM 内存压力

分片分配需要 JVM 堆内存。高 JVM 内存压力会触发断路器，从而停止分配并使分片未分配。请参阅高 JVM 内存压力。

##### 恢复丢失的主分片的数据

如果包含主分片的节点丢失，Elasticsearch 通常可以使用另一个节点上的副本替换它。如果无法恢复节点，并且副本不存在或无法恢复，则需要从快照或原始数据源重新添加缺少的数据。

仅当节点恢复不再可能时才使用此选项。此过程分配一个空的主分片。如果节点稍后重新加入集群，Elasticsearch 将用这个较新的 emptyshard 中的数据覆盖其主分片，从而导致数据丢失。

使用集群重新路由 API 手动将未分配的主分片分配到同一层中的另一个数据节点。将"accept_data_loss"设置为"真"。

    
    
    POST _cluster/reroute?metric=none
    {
      "commands": [
        {
          "allocate_empty_primary": {
            "index": "my-index",
            "shard": 0,
            "node": "my-node",
            "accept_data_loss": "true"
          }
        }
      ]
    }

如果将缺少的索引数据备份到快照，请使用还原快照 API 还原单个索引。或者，您可以为原始数据源中缺少的数据编制索引。

[« High JVM memory pressure](high-jvm-memory-pressure.md) [Rejected requests
»](rejected-requests.md)
