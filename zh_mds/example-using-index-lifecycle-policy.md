

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« ILM: Manage the index lifecycle](index-lifecycle-management.md)
[Tutorial: Automate rollover with ILM »](getting-started-index-lifecycle-
management.md)

## 教程：自定义内置 ILM 策略

Elasticsearch 包括以下内置的 ILM 策略：

* "日志" * "指标" * "合成"

弹性代理使用这些策略来管理其数据流的后备索引。本教程介绍如何使用 Kibana 的索引生命周期策略**根据应用程序的性能、弹性和保留要求自定义这些策略。

###Scenario

您希望将日志文件发送到 Elasticsearch 集群，以便可视化和分析数据。此数据具有以下保留要求：

* 当写入索引达到 50GB 或存在 30 天时，将滚动到新索引。  * 滚动更新后，将索引保留在热数据层中 30 天。  * 展期后30天：

    * Move indices to the warm data tier. 
    * Set replica shards to 1. 
    * [Force merge](indices-forcemerge.html "Force merge API") multiple index segments to free up the space used by deleted documents. 

* 展期后 90 天删除索引。

###Prerequisites

若要完成本教程，需要：

* 具有热数据和温数据层的 Elasticsearch 集群。

    * Elasticsearch Service: Elastic Stack deployments on Elasticsearch Service include a hot tier by default. To add a warm tier, edit your deployment and click **Add capacity** for the warm data tier.

!向部署添加暖数据层

    * Self-managed cluster: Assign `data_hot` and `data_warm` roles to nodes as described in [_Data tiers_](data-tiers.html "Data tiers").

例如，在暖层中每个节点的"elasticsearch.yml"文件中包括"data_warm"节点角色：

        
                node.roles: [ data_warm ]

* 已安装并配置了 Elastic 代理以将日志发送到您的 Elasticsearch 集群的主机。

### 查看策略

弹性代理使用索引模式为"logs-*-*"的数据流来存储日志监控数据。内置的"日志"ILM 策略会自动管理这些数据流的后备索引。

要查看 Kibana 中的"日志"政策，请执行以下操作：

1. 打开菜单并转到**堆栈管理>索引生命周期策略**。  2. 选择**包括托管系统策略**。  3. 选择"日志"策略。

"logs"策略使用建议的滚动更新默认值：当当前写入索引达到 50GB 或变为 30 天时，开始写入新索引。

要查看或更改变换图像设置，请单击热相的"**高级设置**"。然后禁用**使用建议的默认值**以显示变换设置。

!查看翻转默认值

请注意，Kibana 会显示一条警告，指出编辑托管策略可能会破坏 Kibana。在本教程中，您可以忽略该警告并继续修改策略。

### 修改策略

默认的"日志"策略旨在防止创建许多微小的每日索引。您可以修改策略以满足性能要求并管理资源使用情况。

1. 激活暖相，然后单击**高级设置**。

    1. Set **Move data into phase when** to **30 days old**. This moves indices to the warm tier 30 days after rollover. 
    2. Enable **Set replicas** and change **Number of replicas** to **1**. 
    3. Enable **Force merge data** and set **Number of segments** to **1**. 

!使用自定义设置添加暖相

2. 在暖阶段，单击垃圾桶图标以启用删除阶段。

!启用删除阶段

在删除阶段，将数据移动到阶段时间**设置为90天前**。这将在滚动更新 90 天后删除索引。

!添加删除阶段

3. 单击"**保存策略**"。

[« ILM: Manage the index lifecycle](index-lifecycle-management.md)
[Tutorial: Automate rollover with ILM »](getting-started-index-lifecycle-
management.md)
