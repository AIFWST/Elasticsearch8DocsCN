

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix common cluster issues](fix-
common-cluster-issues.md)

[« High CPU usage](high-cpu-usage.md) [Red or yellow cluster status »](red-
yellow-cluster-status.md)

## JVM 内存压力大

高 JVM 内存使用率会降低集群性能并触发断路器错误。为了防止这种情况，我们建议在节点的 JVM 内存使用量始终超过 85% 时采取措施来降低内存压力。

#### 诊断 JVM 内存压力过高

**检查 JVM 内存压力**

弹性搜索服务 自我管理

从部署菜单中，单击"弹性搜索"。在 实例 下，每个实例都显示一个 JVM 内存压力指示器。当 JVM 内存压力达到 75% 时，指示灯变为红色。

您还可以使用节点统计信息 API 来计算每个节点的当前 JVM 内存压力。

    
    
    response = client.nodes.stats(
      filter_path: 'nodes.*.jvm.mem.pools.old'
    )
    puts response
    
    
    GET _nodes/stats?filter_path=nodes.*.jvm.mem.pools.old

使用响应计算内存压力，如下所示：

JVM 内存压力 = "used_in_bytes" / "max_in_bytes"

要计算每个节点的当前 JVM 内存压力，请使用 nodesstats API。

    
    
    response = client.nodes.stats(
      filter_path: 'nodes.*.jvm.mem.pools.old'
    )
    puts response
    
    
    GET _nodes/stats?filter_path=nodes.*.jvm.mem.pools.old

使用响应计算内存压力，如下所示：

JVM 内存压力 = "used_in_bytes" / "max_in_bytes"

**检查垃圾回收日志**

随着内存使用量的增加，垃圾回收变得更加频繁，并且花费的时间更长。您可以在"elasticsearch.log"中跟踪垃圾回收事件的频率和长度。例如，以下事件表明 Elasticsearch 在过去 40 秒中花费了超过 50%(21 秒)的时间执行垃圾回收。

    
    
    [timestamp_short_interval_from_last][INFO ][o.e.m.j.JvmGcMonitorService] [node_id] [gc][number] overhead, spent [21s] collecting in the last [40s]

捕获 JVM 堆转储**

要确定 JVM 内存压力较高的确切原因，请在 JVM 内存使用率较高时捕获其堆转储。

#### 减少 JVM 内存压力

本节包含一些减少 JVM 内存压力的常见建议。

**减少分片数量**

每个分片都使用内存。在大多数情况下，一小组大型分片比许多小分片使用更少的资源。有关减少分片计数的提示，请see_Size shards_。

**避免昂贵的搜索**

昂贵的搜索可能会使用大量内存。为了更好地跟踪集群上昂贵的搜索，请启用慢日志。

昂贵的搜索可能具有较大的"大小"参数，使用具有大量存储桶的聚合，或包含昂贵的查询。若要防止搜索开销大，请考虑以下设置更改：

* 使用"index.max_result_window"索引设置降低"大小"限制。  * 使用 search.max_buckets 集群设置减少允许的最大聚合存储桶数。  * 使用"search.allow_expensive_queries"群集设置禁用昂贵的查询。

    
    
    response = client.indices.put_settings(
      body: {
        "index.max_result_window": 5000
      }
    )
    puts response
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "search.max_buckets": 20_000,
          "search.allow_expensive_queries": false
        }
      }
    )
    puts response
    
    
    PUT _settings
    {
      "index.max_result_window": 5000
    }
    
    PUT _cluster/settings
    {
      "persistent": {
        "search.max_buckets": 20000,
        "search.allow_expensive_queries": false
      }
    }

**防止映射爆炸**

定义过多字段或嵌套字段太深可能会导致映射爆炸，从而占用大量内存。为防止映射爆炸，请使用映射限制设置来限制字段映射的数量。

**分散批量请求**

虽然比单个请求更有效，但大型批量索引或多搜索请求仍会产生较高的 JVM 内存压力。如果可能，请提交较小的请求，并在它们之间留出更多时间。

**升级节点内存**

繁重的索引和搜索负载会导致较高的 JVM 内存压力。为了更好地处理繁重的工作负载，请升级节点以增加其内存容量。

[« High CPU usage](high-cpu-usage.md) [Red or yellow cluster status »](red-
yellow-cluster-status.md)
