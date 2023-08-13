

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Transforms settings in Elasticsearch](transform-settings.md) [Watcher
settings in Elasticsearch »](notification-settings.md)

## 线程池

一个节点使用多个线程池来管理内存消耗。与许多线程池关联的队列允许保留而不是丢弃挂起的请求。

有几个线程池，但重要的线程池包括：

`generic`

     For generic operations (for example, background node discovery). Thread pool type is `scaling`. 

`search`

     For count/search/suggest operations. Thread pool type is `fixed` with a size of `int((`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")` * 3) / 2) + 1`, and queue_size of `1000`. 
`search_throttled`

     For count/search/suggest/get operations on `search_throttled indices`. Thread pool type is `fixed` with a size of `1`, and queue_size of `100`. 
`search_coordination`

     For lightweight search-related coordination operations. Thread pool type is `fixed` with a size of a max of `min(5, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 2)`, and queue_size of `1000`. 
`get`

     For get operations. Thread pool type is `fixed` with a size of `int((`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")` * 3) / 2) + 1`, and queue_size of `1000`. 
`analyze`

     For analyze requests. Thread pool type is `fixed` with a size of `1`, queue size of `16`. 
`write`

     For single-document index/delete/update and bulk requests. Thread pool type is `fixed` with a size of [`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting"), queue_size of `10000`. The maximum size for this pool is `1 + `[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting"). 
`snapshot`

     For snapshot/restore operations. Thread pool type is `scaling` with a keep-alive of `5m`. On nodes with at least 750MB of heap the maximum size of this pool is `10` by default. On nodes with less than 750MB of heap the maximum size of this pool is `min(5, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 2)` by default. 
`snapshot_meta`

     For snapshot repository metadata read operations. Thread pool type is `scaling` with a keep-alive of `5m` and a max of `min(50, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`* 3))`. 
`warmer`

     For segment warm-up operations. Thread pool type is `scaling` with a keep-alive of `5m` and a max of `min(5, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 2)`. 
`refresh`

     For refresh operations. Thread pool type is `scaling` with a keep-alive of `5m` and a max of `min(10, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 2)`. 
`fetch_shard_started`

     For listing shard states. Thread pool type is `scaling` with keep-alive of `5m` and a default maximum size of `2 * `[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting"). 
`fetch_shard_store`

     For listing shard stores. Thread pool type is `scaling` with keep-alive of `5m` and a default maximum size of `2 * `[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting"). 
`flush`

     For [flush](indices-flush.html "Flush API") and [translog](index-modules-translog.html "Translog") `fsync` operations. Thread pool type is `scaling` with a keep-alive of `5m` and a default maximum size of `min(5, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 2)`. 
`force_merge`

     For [force merge](indices-forcemerge.html "Force merge API") operations. Thread pool type is `fixed` with a size of `max(1, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 8)` and an unbounded queue size. 
`management`

     For cluster management. Thread pool type is `scaling` with a keep-alive of `5m` and a default maximum size of `5`. 
`system_read`

     For read operations on system indices. Thread pool type is `fixed` with a default maximum size of `min(5, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 2)`. 
`system_write`

     For write operations on system indices. Thread pool type is `fixed` with a default maximum size of `min(5, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 2)`. 
`system_critical_read`

     For critical read operations on system indices. Thread pool type is `fixed` with a default maximum size of `min(5, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 2)`. 
`system_critical_write`

     For critical write operations on system indices. Thread pool type is `fixed` with a default maximum size of `min(5, (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`) / 2)`. 
`watcher`

     For [watch executions](xpack-alerting.html "Watcher"). Thread pool type is `fixed` with a default maximum size of `min(5 * (`[`# of allocated processors`](modules-threadpool.html#node.processors "Allocated processors setting")`), 50)` and queue_size of `1000`. 

线程池设置是静态的，可以通过编辑"elasticsearch.yml"进行更改。更改特定线程池可以通过设置其特定于类型的参数来完成;例如，更改"写入"线程池中的线程数：

    
    
    thread_pool:
        write:
            size: 30

### 线程池类型

以下是线程池的类型及其各自的参数：

####'固定'

"固定"线程池拥有固定大小的线程来处理请求，队列(可选有界)用于没有线程为它们提供服务的挂起请求。

"size"参数控制线程数。

"queue_size"允许控制没有线程来执行它们的待处理请求队列的大小。默认情况下，它设置为"-1"，这意味着它是无界的。当请求进入并且队列已满时，它将中止请求。

    
    
    thread_pool:
        write:
            size: 30
            queue_size: 1000

####'缩放'

"缩放"线程池包含动态数量的线程。此数字与工作负载成正比，并在"核心"和"最大"参数的值之间变化。

"keep_alive"参数确定线程应在线程池中保留多长时间而不执行任何工作。

    
    
    thread_pool:
        warmer:
            core: 1
            max: 8
            keep_alive: 2m

### 分配的处理器设置

自动检测处理器数量，并基于它自动设置线程池设置。在某些情况下，覆盖检测到的处理器数可能很有用。这可以通过显式设置"node.processor"设置来完成。此设置受可用处理器数量的限制，并接受浮点数，这在 Elasticsearch 节点配置为在 CPU 限制下运行的环境中非常有用，例如 CPU 份额或"Cgroups"下的配额。

    
    
    node.processors: 2

有一些用例可以显式覆盖"node.processor"设置：

1. 如果您在同一主机上运行多个 Elasticsearch 实例，但希望 Elasticsearch 调整其线程池的大小，就好像它只有一小部分 CPU，则应将"node.processor"设置覆盖为所需的部分，例如，如果您在一台 16 核机器上运行两个 Elasticsearch 实例，请将"node.processor"设置为 8。请注意，这是一个专家级用例，除了设置"node.processor"设置之外，还有许多其他注意事项，例如更改垃圾回收器线程数、将进程固定到内核等。  2. 有时会错误地检测到处理器的数量，在这种情况下，显式设置"node.processor"设置将解决这些问题。

要检查检测到的处理器数量，请使用带有"os"标志的节点信息 API。

[« Transforms settings in Elasticsearch](transform-settings.md) [Watcher
settings in Elasticsearch »](notification-settings.md)
