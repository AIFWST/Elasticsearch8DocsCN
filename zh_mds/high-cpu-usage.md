

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix common cluster issues](fix-
common-cluster-issues.md)

[« Circuit breaker errors](circuit-breaker-errors.md) [High JVM memory
pressure »](high-jvm-memory-pressure.md)

## 高 CPU 使用率

Elasticsearch 使用线程池来管理并发操作的 CPU 资源。高 CPU 使用率通常意味着一个或多个线程池运行不足。

如果线程池耗尽，Elasticsearch 将拒绝与线程池相关的请求。例如，如果"search"线程池耗尽，Elasticsearch 将拒绝搜索请求，直到有更多线程可用。

#### 诊断高 CPU 使用率

**检查 CPU 使用率**

弹性搜索服务 自我管理

从部署菜单中，单击"**性能**"。该页面的"CPU 使用率"图表以百分比形式显示部署的 CPU 使用率。

高 CPU 使用率也会耗尽您的 CPU 积分。CPU 积分让 Elasticsearch Service 在需要时为较小的集群提供性能提升。"CPU 积分"图表显示剩余的 CPU 积分，以秒为单位的 CPU 时间。

您还可以使用 cat 节点 API 获取每个节点的当前 CPU 使用率。

    
    
    response = client.cat.nodes(
      v: true,
      s: 'cpu:desc'
    )
    puts response
    
    
    GET _cat/nodes?v=true&s=cpu:desc

响应的"cpu"列以百分比形式包含当前 CPU 使用率。"名称"列包含节点的名称。

使用 cat 节点 API 获取每个节点的当前 CPU 使用率。

    
    
    response = client.cat.nodes(
      v: true,
      s: 'cpu:desc'
    )
    puts response
    
    
    GET _cat/nodes?v=true&s=cpu:desc

响应的"cpu"列以百分比形式包含当前 CPU 使用率。"名称"列包含节点的名称。

**检查热线程**

如果节点的 CPU 使用率较高，请使用节点热线程 API 检查节点上运行的资源密集型线程。

    
    
    response = client.nodes.hot_threads(
      node_id: 'my-node,my-other-node'
    )
    puts response
    
    
    GET _nodes/my-node,my-other-node/hot_threads

此 API 以纯文本形式返回任何热线程的细分。

#### 降低 CPU 使用率

以下提示概述了高 CPU 使用率的最常见原因及其解决方案。

**扩展群集**

繁重的索引和搜索负载可能会耗尽较小的线程池。为了更好地处理繁重的工作负载，请向群集添加更多节点或升级现有节点以增加容量。

**分散批量请求**

虽然比单个请求更有效，但大型批量索引或多搜索请求仍然需要 CPU 资源。如果可能，请提交较小的请求，并在它们之间留出更多时间。

**取消长时间运行的搜索**

长时间运行的搜索可能会阻止"搜索"线程池中的线程。要检查这些搜索，请使用任务管理 API。

    
    
    response = client.tasks.list(
      actions: '*search',
      detailed: true
    )
    puts response
    
    
    GET _tasks?actions=*search&detailed

响应的"说明"包含搜索请求及其查询。"running_time_in_nanos"显示搜索运行了多长时间。

    
    
    {
      "nodes" : {
        "oTUltX4IQMOUUVeiohTt8A" : {
          "name" : "my-node",
          "transport_address" : "127.0.0.1:9300",
          "host" : "127.0.0.1",
          "ip" : "127.0.0.1:9300",
          "tasks" : {
            "oTUltX4IQMOUUVeiohTt8A:464" : {
              "node" : "oTUltX4IQMOUUVeiohTt8A",
              "id" : 464,
              "type" : "transport",
              "action" : "indices:data/read/search",
              "description" : "indices[my-index], search_type[QUERY_THEN_FETCH], source[{\"query\":...}]",
              "start_time_in_millis" : 4081771730000,
              "running_time_in_nanos" : 13991383,
              "cancellable" : true
            }
          }
        }
      }
    }

要取消搜索并释放资源，请使用 API 的"_cancel"终结点。

    
    
    response = client.tasks.cancel(
      task_id: 'oTUltX4IQMOUUVeiohTt8A:464'
    )
    puts response
    
    
    POST _tasks/oTUltX4IQMOUUVeiohTt8A:464/_cancel

有关如何跟踪和避免资源密集型搜索的其他提示，请参阅避免昂贵的搜索。

[« Circuit breaker errors](circuit-breaker-errors.md) [High JVM memory
pressure »](high-jvm-memory-pressure.md)
