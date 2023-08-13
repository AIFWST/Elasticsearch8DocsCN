

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix common cluster issues](fix-
common-cluster-issues.md)

[« Mapping explosion](mapping-explosion.md) [Diagnose unassigned shards
»](diagnose-unassigned-shards.md)

## 热点

计算机热点)可能发生在 Elasticsearch 中，当资源利用率在节点之间分布不均匀时。临时峰值通常不被认为是有问题的，但持续显著独特的利用率可能会导致集群瓶颈，应进行审查。

#### 检测热点

热点最常见的表现是节点子集中的资源利用率("磁盘百分比"、"堆百分比"或"CPU")，如通过 cat 节点报告的那样。单个峰值不一定有问题，但如果利用率反复峰值或随着时间的推移始终保持高位(例如超过 30 秒)，则可能会出现有问题的热点。

例如，让我们展示使用 cat 节点的两个独立的合理问题：

    
    
    response = client.cat.nodes(
      v: true,
      s: 'master,name',
      h: 'name,master,node.role,heap.percent,disk.used_percent,cpu'
    )
    puts response
    
    
    GET _cat/nodes?v&s=master,name&h=name,master,node.role,heap.percent,disk.used_percent,cpu

假设在五分钟内拉取了两次相同的输出：

    
    
    name   master node.role heap.percent disk.used_percent cpu
    node_1 *      hirstm              24                20  95
    node_2 -      hirstm              23                18  18
    node_3 -      hirstmv             25                90  10

在这里，我们看到两个非常独特的利用率：主节点位于"cpu：95"，热节点位于"disk.used_percent：90%"。这将表明这两个节点上发生了热点，而不一定来自相同的根本原因。

####Causes

从历史上看，集群经历热点主要是由于硬件、分片分布和/或任务负载的影响。我们将按其潜在影响范围的顺序依次进行审查。

####Hardware

以下是一些可能导致热点的常见不正确硬件设置：

* 资源分配不统一。例如，如果一个热节点的 CPU 是其对等节点的一半。Elasticsearch 希望数据层上的所有节点共享相同的硬件配置文件或规格。  * 资源由主机上的其他服务消耗，包括其他 Elasticsearch 节点。请参阅我们的专用主机推荐。  * 资源体验不同的网络或磁盘吞吐量。例如，如果一个节点的 I/O 低于其对等节点。有关详细信息，请参阅使用更快的硬件。  * 配置了大于 31GB 的堆的 JVM。有关更多信息，请参阅设置 JVM 堆大小。  * 有问题的资源唯一报告内存交换。

#### 分片分布

Elasticsearch 索引分为一个或多个分片)，有时分布不佳。Elasticsearch 通过跨数据节点平衡分片计数来解释这一点。正如版本 8.6 中引入的那样，默认情况下，Elasticsearch 还支持所需的平衡以考虑摄取负载。节点可能仍会遇到热点，这可能是由于写入密集型索引或其托管的整体分片造成的。

##### 节点级别

您可以通过 cat 分配检查分片平衡，但从版本 8.6 开始，所需的平衡可能不再完全期望平衡分片。请注意，这两种方法在集群稳定性问题期间都可能暂时显示有问题的不平衡。

例如，让我们使用 catallocation 展示两个独立的合理问题：

    
    
    response = client.cat.allocation(
      v: true,
      s: 'node',
      h: 'node,shards,disk.percent,disk.indices,disk.used'
    )
    puts response
    
    
    GET _cat/allocation?v&s=node&h=node,shards,disk.percent,disk.indices,disk.used

其中可以返回：

    
    
    node   shards disk.percent disk.indices disk.used
    node_1    446           19      154.8gb   173.1gb
    node_2     31           52       44.6gb   372.7gb
    node_3    445           43      271.5gb   289.4gb

在这里，我们看到两种非常独特的情况。"node_2"最近重新启动，因此它的分片数量比所有其他节点少得多。这也与"disk.index"比"disk.used"小得多有关，而分片正在恢复，如通过cat恢复看到的那样。虽然"node_2"的分片计数较低，但由于持续的 ILM 滚动更新，它可能会成为写入热点。这是下一节中介绍的写入热点的常见根本原因。

第二种情况是"node_3"的"disk.percent"高于"node_1"，即使它们拥有大致相同数量的分片。当分片大小不均匀(请参阅瞄准最多 200M 个文档的分片，或大小在 10GB 到 50GB 之间的分片)或存在大量空索引时，会发生这种情况。

基于所需平衡的集群重新平衡可以完成使节点远离热点的大部分繁重工作。它可能受到节点命中水印(请参阅修复磁盘水印错误)或写入密集型索引的总分片数远低于写入节点的限制。

您可以通过节点统计信息 API 确认热点节点，可能会随着时间的推移轮询两次，以仅检查它们之间的统计信息差异，而不是轮询一次，为您提供节点完整节点正常运行时间的统计信息。例如，要检查所有节点索引统计信息，请执行以下操作：

    
    
    response = client.nodes.stats(
      human: true,
      filter_path: 'nodes.*.name,nodes.*.indices.indexing'
    )
    puts response
    
    
    GET _nodes/stats?human&filter_path=nodes.*.name,nodes.*.indices.indexing

##### 索引级

热点节点经常通过 cat 线程池的"写入"和"搜索"队列备份出现。例如：

    
    
    response = client.cat.thread_pool(
      thread_pool_patterns: 'write,search',
      v: true,
      s: 'n,nn',
      h: 'n,nn,q,a,r,c'
    )
    puts response
    
    
    GET _cat/thread_pool/write,search?v=true&s=n,nn&h=n,nn,q,a,r,c

其中可以返回：

    
    
    n      nn       q a r    c
    search node_1   3 1 0 1287
    search node_2   0 2 0 1159
    search node_3   0 1 0 1302
    write  node_1 100 3 0 4259
    write  node_2   0 4 0  980
    write  node_3   1 5 0 8714

在这里，您可以看到两种非常独特的情况。首先，与其他节点相比，"node_1"严重备份了写入队列。其次，"node_3"显示历史上完成的写入，这些写入是任何其他节点的两倍。这两者都可能是由于写入密集型索引分布不佳，或者分配给同一节点的多个写入密集型索引。由于主写入和副本写入的集群工作量大致相同，因此我们通常建议设置"index.routing.allocation.total_shards_per_node"，以便在将上行索引分片计数排列到节点总数后强制索引扩展。

我们通常建议重写入索引具有足够的主number_of_shards"和副本"number_of_replicas"，以均匀分布在索引节点之间。或者，您可以将分片重新路由到更安静的节点，以缓解节点的写入热点。

如果不清楚哪些索引有问题，您可以通过索引统计信息 API 进一步内省，方法是运行：

    
    
    response = client.indices.stats(
      level: 'shards',
      human: true,
      expand_wildcards: 'all',
      filter_path: 'indices.*.total.indexing.index_total'
    )
    puts response
    
    
    GET _stats?level=shards&human&expand_wildcards=all&filter_path=indices.*.total.indexing.index_total

对于更高级的分析，您可以轮询分片级统计信息，从而比较联合索引级别和节点级别的统计信息。此分析不会考虑节点重启和/或分片重新路由，但可作为概述：

    
    
    response = client.indices.stats(
      metric: 'indexing,search',
      level: 'shards',
      human: true,
      expand_wildcards: 'all'
    )
    puts response
    
    
    GET _stats/indexing,search?level=shards&human&expand_wildcards=all

例如，您可以使用第三方 JQtool 来处理保存为 'indices_stats.json' 的输出：

    
    
    cat indices_stats.json | jq -rc ['.indices|to_entries[]|.key as $i|.value.shards|to_entries[]|.key as $s|.value[]|{node:.routing.node[:4], index:$i, shard:$s, primary:.routing.primary, size:.store.size, total_indexing:.indexing.index_total, time_indexing:.indexing.index_time_in_millis, total_query:.search.query_total, time_query:.search.query_time_in_millis } | .+{ avg_indexing: (if .total_indexing>0 then (.time_indexing/.total_indexing|round) else 0 end), avg_search: (if .total_search>0 then (.time_search/.total_search|round) else 0 end) }'] > shard_stats.json
    
    # show top written-to shard simplified stats which contain their index and node references
    cat shard_stats.json | jq -rc 'sort_by(-.avg_indexing)[]' | head

#### 任务加载

分片分布问题最有可能以任务负载的形式出现，如上文 cat 线程池示例中所示。任务也可能由于单个定性成本或整体定量流量负载而热点节点。

例如，如果 cat 线程池报告"较暖"线程池上的队列较高，则您将查找受影响节点的热线程。假设它报告了与"GlobalOrdinalsBuilder"相关的"100% cpu"的"较热"线程。这将使您知道检查字段数据的全局序数。

或者，假设 cat 节点显示热点主节点，而 cat 线程池显示跨节点的一般队列。这表明主节点不堪重负。若要解决此问题，请首先确保硬件高可用性设置，然后查找临时原因。在此示例中，节点热线程 API 报告"其他"中的多个线程，这表明它们正在等待或被垃圾回收或 I/O 阻止。

对于这些示例情况中的任何一种，确认有问题任务的一个好方法是通过 [cat 任务管理] 查看运行时间最长的非连续(指定为"c]")任务。这可以补充通过 cat 挂起任务检查运行时间最长的集群同步任务。使用第三个例子，

    
    
    response = client.cat.tasks(
      v: true,
      s: 'time:desc',
      h: 'type,action,running_time,node,cancellable'
    )
    puts response
    
    
    GET _cat/tasks?v&s=time:desc&h=type,action,running_time,node,cancellable

这可能会返回：

    
    
    type   action                running_time  node    cancellable
    direct indices:data/read/eql 10m           node_1  true
    ...

这会显示有问题的 EQL 查询。我们可以通过任务管理 API 进一步了解它。它的响应包含一个报告此查询的"描述"：

    
    
    indices[winlogbeat-*,logs-window*], sequence by winlog.computer_name with maxspan=1m\n\n[authentication where host.os.type == "windows" and event.action:"logged-in" and\n event.outcome == "success" and process.name == "svchost.exe" ] by winlog.event_data.TargetLogonId

这让您知道要检查哪些索引('winlogbeat-*，logs-window*')，以及 EQL 搜索请求正文。这很可能与 SIEM 相关。您可以根据需要将其与审核日志记录结合使用，以跟踪请求源。

[« Mapping explosion](mapping-explosion.md) [Diagnose unassigned shards
»](diagnose-unassigned-shards.md)
