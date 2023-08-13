

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Troubleshooting index lifecycle management errors](index-lifecycle-error-
handling.md) [Manage existing indices »](ilm-with-existing-indices.md)

## 启动和停止索引生命周期管理

默认情况下，ILM 服务处于"正在运行"状态，并管理具有生命周期策略的所有索引。

您可以停止索引生命周期管理以暂停所有索引的管理操作。例如，在执行计划维护或对群集进行更改时，可能会影响 ILM 操作的执行，您可能会停止索引生命周期管理。

停止 ILM 时，SLM 操作也会挂起。在重新启动 ILM 之前，不会按计划创建任何快照。正在进行的快照不受影响。

### 获取 ILM 状态

若要查看 ILM 服务的当前状态，请使用获取状态 API：

    
    
    response = client.ilm.get_status
    puts response
    
    
    GET _ilm/status

在正常操作下，响应显示 ILM 为"正在运行"：

    
    
    {
      "operation_mode": "RUNNING"
    }

### StopILM

要停止 ILM 服务并暂停所有生命周期策略的执行，请使用停止 API：

    
    
    response = client.ilm.stop
    puts response
    
    
    POST _ilm/stop

ILM 服务将所有策略运行到可以安全停止的程度。当 ILM 服务关闭时，状态 API 显示 ILM 处于"停止"模式：

    
    
    {
      "operation_mode": "STOPPING"
    }

一旦所有策略都处于安全的停止点，ILM 就会进入"已停止"模式：

    
    
    {
      "operation_mode": "STOPPED"
    }

### 启动ILM

要重新启动 ILM 并继续执行策略，请使用启动 API。这会将 ILM 服务置于"正在运行"状态，ILM 将从中断的位置开始执行策略。

    
    
    response = client.ilm.start
    puts response
    
    
    POST _ilm/start

[« Troubleshooting index lifecycle management errors](index-lifecycle-error-
handling.md) [Manage existing indices »](ilm-with-existing-indices.md)
