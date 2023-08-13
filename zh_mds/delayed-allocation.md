

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md) ›[Index Shard Allocation](index-modules-
allocation.md)

[« Index-level shard allocation filtering](shard-allocation-filtering.md)
[Index recovery prioritization »](recovery-prioritization.md)

## 节点离开时延迟分配

当节点出于任何有意或无意的原因离开集群时，主节点的反应是：

* 将副本分片提升为主分片，以替换节点上的任何主分片。  * 分配副本分片以替换缺少的副本(假设有足够的节点)。  * 在其余节点之间均匀地重新平衡分片。

这些操作旨在通过确保尽快完全复制每个分片来保护集群免受数据丢失。

尽管我们在节点级别和集群级别都限制了并发恢复，但这种"分片洗牌"仍然会给集群带来大量额外负载，如果丢失的节点可能很快就会返回，这可能就没有必要了。想象一下这样的场景：

* 节点 5 失去网络连接。  * 主节点将节点 5 上的每个主节点的副本分片提升为主节点。  * 主节点将新副本分配给群集中的其他节点。  * 每个新副本都会在网络上创建主分片的完整副本。  * 将更多分片移动到不同的节点以重新平衡集群。  * 节点 5 在几分钟后返回。  * 主节点通过将分片分配给节点 5 来重新平衡集群。

如果主节点只是等待了几分钟，那么丢失的分片可以以最少的网络流量重新分配给节点 5。对于已自动刷新的空闲分片(未接收索引请求的分片)，此过程会更快。

由于节点离开而变为未分配的副本分片的分配可以使用"index.unassigned.node_left.delayed_timeout"动态设置延迟，该设置默认为"1m"。

可以在实时索引(或所有索引)上更新此设置：

    
    
    response = client.indices.put_settings(
      index: '_all',
      body: {
        settings: {
          "index.unassigned.node_left.delayed_timeout": '5m'
        }
      }
    )
    puts response
    
    
    PUT _all/_settings
    {
      "settings": {
        "index.unassigned.node_left.delayed_timeout": "5m"
      }
    }

启用延迟分配后，上述方案将更改为如下所示：

* 节点 5 失去网络连接。  * 主节点将节点 5 上的每个主节点的副本分片提升为主节点。  * 主节点记录一条消息，指出未分配分片的分配已延迟，以及延迟了多长时间。  * 集群保持黄色，因为存在未分配的副本分片。  * 节点 5 在"超时"到期之前的几分钟后返回。  * 丢失的副本将重新分配给节点 5(同步刷新的分片几乎会立即恢复)。

此设置不会影响将副本提升为主副本，也不会影响以前未分配的副本的分配。特别是，延迟分配在完整群集重新启动后不会生效。此外，在主故障转移情况下，经过的延迟时间将被遗忘(即重置为完全初始延迟)。

### 取消分片搬迁

如果延迟分配超时，主节点会将缺少的分片分配给另一个将开始恢复的节点。如果缺少的节点重新加入集群，并且其分片仍与主节点具有相同的同步 ID，则分片重定位将被取消，同步的分片将用于恢复。

出于这个原因，默认的"超时"设置为一分钟：即使分片重新定位开始，取消恢复以支持同步的分片也是便宜的。

### 监控延迟的未分配分片

可以使用集群运行状况 API 查看分配因此超时设置而延迟的分片数：

    
    
    response = client.cluster.health
    puts response
    
    
    GET _cluster/health __

__

|

此请求将返回"delayed_unassigned_shards"值。   ---|--- ### 删除节点永久编辑

如果一个节点不打算返回，并且您希望 Elasticsearch 立即分配缺少的分片，只需将超时更新为零：

    
    
    response = client.indices.put_settings(
      index: '_all',
      body: {
        settings: {
          "index.unassigned.node_left.delayed_timeout": '0'
        }
      }
    )
    puts response
    
    
    PUT _all/_settings
    {
      "settings": {
        "index.unassigned.node_left.delayed_timeout": "0"
      }
    }

您可以在丢失的分片开始恢复后立即重置超时。

[« Index-level shard allocation filtering](shard-allocation-filtering.md)
[Index recovery prioritization »](recovery-prioritization.md)
