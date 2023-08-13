

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix common cluster issues](fix-
common-cluster-issues.md)

[« Red or yellow cluster status](red-yellow-cluster-status.md) [Task queue
backlog »](task-queue-backlog.md)

## 被拒绝的请求

当 Elasticsearch 拒绝请求时，它会停止操作并返回带有"429"响应代码的错误。请求被拒绝通常是由以下原因引起的：

* 线程池耗尽。耗尽的"搜索"或"写入"线程池返回"TOO_MANY_REQUESTS"错误消息。  * 断路器错误。  * 超过"indexing_pressure.memory.limit"的高索引压力。

#### 检查被拒绝的任务

要检查每个线程池的拒绝任务数，请使用 catthread pool API。"拒绝"与"已完成"任务的比例很高，特别是在"搜索"和"写入"线程池中，这意味着 Elasticsearch 会定期拒绝请求。

    
    
    response = client.cat.thread_pool(
      v: true,
      h: 'id,name,active,rejected,completed'
    )
    puts response
    
    
    GET /_cat/thread_pool?v=true&h=id,name,active,rejected,completed

#### 防止请求被拒绝

**修复高 CPU 和内存使用率问题**

如果 Elasticsearch 定期拒绝请求和其他任务，则您的集群可能存在较高的 CPU 使用率或较高的 JVM 内存压力。有关提示，请参阅高 CPU 使用率和高 JVM 内存压力。

**防止断路器错误**

如果您经常触发断路器错误，请参阅断路器错误以获取有关诊断和预防它们的提示。

[« Red or yellow cluster status](red-yellow-cluster-status.md) [Task queue
backlog »](task-queue-backlog.md)
