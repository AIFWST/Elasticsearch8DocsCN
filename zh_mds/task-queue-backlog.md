

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix common cluster issues](fix-
common-cluster-issues.md)

[« Rejected requests](rejected-requests.md) [Mapping explosion »](mapping-
explosion.md)

## 任务队列积压工作

积压的任务队列可能会阻止任务完成，并使群集进入不正常状态。资源限制、一次触发的大量任务以及长时间运行的任务都可能导致积压任务队列。

#### 诊断任务队列积压工作

**检查线程池状态**

耗尽的线程池可能会导致请求被拒绝。

您可以使用 cat 线程池 API 查看每个线程池中的活动线程数，以及排队的任务数、被拒绝的任务数以及已完成的任务数。

    
    
    response = client.cat.thread_pool(
      v: true,
      s: 't,n',
      h: 'type,name,node_name,active,queue,rejected,completed'
    )
    puts response
    
    
    GET /_cat/thread_pool?v&s=t,n&h=type,name,node_name,active,queue,rejected,completed

**检查每个节点上的热线程**

如果备份了特定的线程池队列，则可以定期轮询节点热线程 API，以确定线程是否有足够的资源来推进并衡量其进度。

    
    
    response = client.nodes.hot_threads
    puts response
    
    
    GET /_nodes/hot_threads

**查找长时间运行的任务**

长时间运行的任务也可能导致积压。您可以使用任务管理 API 获取有关正在运行的任务的信息。检查"running_time_in_nanos"以识别花费过多时间才能完成的任务。

    
    
    response = client.tasks.list(
      filter_path: 'nodes.*.tasks'
    )
    puts response
    
    
    GET /_tasks?filter_path=nodes.*.tasks

#### 解决任务队列积压工作

**增加可用资源**

如果任务进展缓慢且队列正在备份，则可能需要采取措施来降低 CPU 使用率。

在某些情况下，增加线程池大小可能会有所帮助。例如，"force_merge"线程池默认为单个线程。将大小增加到 2 可能有助于减少强制合并请求的积压。

**取消卡住的任务**

如果发现活动任务的热线程没有进展并且存在积压，请考虑取消该任务。

[« Rejected requests](rejected-requests.md) [Mapping explosion »](mapping-
explosion.md)
