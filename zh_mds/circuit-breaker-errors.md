

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix common cluster issues](fix-
common-cluster-issues.md)

[« Fix watermark errors](fix-watermark-errors.md) [High CPU usage »](high-
cpu-usage.md)

## 断路器错误

Elasticsearch 使用断路器来防止节点耗尽 JVM 堆内存。如果 Lasticsearch 估计某个操作将超过断路器，它将停止该操作并返回错误。

缺省情况下，父断路器在 95% 的 JVM 内存使用率时触发。为了防止错误，我们建议在使用率持续超过 85% 时采取措施降低内存压力。

#### 诊断断路器错误

**错误消息**

如果请求触发了断路器，Elasticsearch 会返回一个错误，其中包含"429"HTTP 状态代码。

    
    
    {
      'error': {
        'type': 'circuit_breaking_exception',
        'reason': '[parent] Data too large, data for [<http_request>] would be [123848638/118.1mb], which is larger than the limit of [123273216/117.5mb], real usage: [120182112/114.6mb], new bytes reserved: [3666526/3.4mb]',
        'bytes_wanted': 123848638,
        'bytes_limit': 123273216,
        'durability': 'TRANSIENT'
      },
      'status': 429
    }

Elasticsearch还将断路器错误写入'elasticsearch.log。当自动化进程(如分配)触发断路器时，这很有用。

    
    
    Caused by: org.elasticsearch.common.breaker.CircuitBreakingException: [parent] Data too large, data for [<transport_request>] would be [num/numGB], which is larger than the limit of [num/numGB], usages [request=0/0b, fielddata=num/numKB, in_flight_requests=num/numGB, accounting=num/numGB]

**检查 JVM 内存使用情况**

如果已启用堆栈监控，则可以在主菜单中查看 JVM 内存使用情况 Kibana.In，单击**堆栈监控**。在堆栈监控概览页面，单击节点管理。"JVM 堆"列列出了每个节点的当前内存使用情况。

您还可以使用 cat nodes API 获取每个节点的当前"heap.percent"。

    
    
    response = client.cat.nodes(
      v: true,
      h: 'name,node*,heap*'
    )
    puts response
    
    
    GET _cat/nodes?v=true&h=name,node*,heap*

要获取每个断路器的 JVM 内存使用情况，请使用节点统计信息 API。

    
    
    response = client.nodes.stats(
      metric: 'breaker'
    )
    puts response
    
    
    GET _nodes/stats/breaker

#### 防止断路器错误

**降低 JVM 内存压力**

高 JVM 内存压力通常会导致断路器错误。请参阅高 JVM内存压力。

**避免在"文本"字段上使用字段数据**

对于高基数"文本"字段，字段数据可以使用大量的 JVM内存。为了避免这种情况，Elasticsearch 默认禁用"文本"字段上的字段数据。如果您已启用字段数据并触发了字段数据断路器，请考虑禁用它并改用"关键字"字段。请参阅"字段数据"映射参数。

**清除字段数据缓存**

如果已触发字段数据断路器且无法禁用字段数据，请使用清除缓存 API 清除字段数据缓存。这可能会中断任何使用字段数据的飞行中搜索。

    
    
    response = client.indices.clear_cache(
      fielddata: true
    )
    puts response
    
    
    POST _cache/clear?fielddata=true

[« Fix watermark errors](fix-watermark-errors.md) [High CPU usage »](high-
cpu-usage.md)
