

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning APIs](ml-apis.md)

[« Get machine learning memory stats API](get-ml-memory.md) [Machine
learning anomaly detection APIs »](ml-ad-apis.md)

## 设置升级模式API

设置群集范围的upgrade_mode设置，为升级准备机器学习索引。

###Request

"发布_ml/set_upgrade_mode"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

升级集群时，在某些情况下，必须重新启动节点并重新索引机器学习索引。在这些情况下，必须没有机器学习作业在运行。您可以关闭机器学习作业，执行升级，然后再次打开所有作业。或者，您可以使用此 API 暂时停止与作业和数据馈送关联的任务，并阻止打开新作业。您还可以在不需要重新索引机器学习索引的升级期间使用此 API，但在这种情况下不需要停止作业。

有关更多信息，请参阅 升级弹性堆栈。

当"enabled=true"时，此 API 会暂时停止所有作业和数据馈送任务，并禁止启动新的作业和数据馈送任务。

随后，您可以在启用参数设置为 false 的情况下调用 API，这会导致机器学习作业和数据馈送返回到其所需状态。

可以使用 get机器学习信息 API 查看"upgrade_mode"设置的当前值。

当"upgrade_mode"设置为"true"时，无法打开新的机器学习作业。

### 查询参数

`enabled`

     (Optional, Boolean) When `true`, this enables `upgrade_mode`. Defaults to `false`. 
`timeout`

     (Optional, time) The time to wait for the request to be completed. The default value is 30 seconds. 

###Examples

以下示例为群集启用"upgrade_mode"：

    
    
    response = client.ml.set_upgrade_mode(
      enabled: true,
      timeout: '10m'
    )
    puts response
    
    
    POST _ml/set_upgrade_mode?enabled=true&timeout=10m

调用成功后，将返回已确认的响应。例如：

    
    
    {
      "acknowledged": true
    }

只有在所有机器学习作业和数据馈送完成对机器学习内部索引的写入后，才会返回已确认的响应。这意味着可以安全地重新索引这些内部索引，而不会导致故障。在重新编制索引之前，必须等待确认的响应，以确保完成所有写入。

升级完成后，必须将"upgrade_mode"设置为"false"，机器学习作业才能再次开始运行。例如：

    
    
    response = client.ml.set_upgrade_mode(
      enabled: false,
      timeout: '10m'
    )
    puts response
    
    
    POST _ml/set_upgrade_mode?enabled=false&timeout=10m

[« Get machine learning memory stats API](get-ml-memory.md) [Machine
learning anomaly detection APIs »](ml-ad-apis.md)
