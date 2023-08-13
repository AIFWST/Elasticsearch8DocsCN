

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up a
cluster for high availability](high-availability.md) ›[Cross-cluster
replication](xpack-ccr.md)

[« Tutorial: Set up cross-cluster replication](ccr-getting-started-
tutorial.md) [Manage auto-follow patterns »](ccr-auto-follow.md)

## 管理跨集群复制

使用以下信息管理跨集群复制任务，例如检查复制进度、暂停和恢复复制、重新创建追随者索引和终止复制。

要开始使用跨集群复制，请访问 Kibana 并转到**管理>堆栈管理**。在侧面导航栏中，选择"**跨群集复制**"。

### 检查复制统计信息

要检查关注程序索引的复制进度并查看详细的分片统计信息，请访问跨集群复制并选择"**追随者索引**"选项卡。

选择要查看其复制详细信息的从属索引的名称。滑出面板显示追随者索引的设置和复制统计信息，包括由追随者分片管理的读取和写入操作。

要查看更详细的统计信息，请单击"**在索引管理中查看**"，然后在"索引管理"中选择关注者索引的名称。打开选项卡以获取有关关注者索引的详细统计信息。

接口示例

使用获取关注者统计信息 API 在分片级别检查复制进度。此 API 提供对追随者分片管理的读取和写入的见解。API 还会报告可重试的读取异常和需要用户干预的致命异常。

### 暂停和恢复复制

要暂停和恢复领导索引的复制，请访问跨集群复制并选择"追随者索引"选项卡。

选择要暂停的关注点索引，然后选择"**管理>暂停复制**"。关注者索引状态更改为已暂停。

要恢复复制，请选择从属索引，然后选择**恢复复制**。

接口示例

您可以使用暂停关注程序 API 暂停复制，然后使用恢复关注程序 API 恢复复制。结合使用这些 API 使您能够在初始配置不适合您的使用案例时调整从属分片任务上的读取和写入参数。

### 重新创建追随者索引

更新或删除文档时，基础操作将在 Lucene 索引中保留一段时间，该时间段由"index.soft_deletes.retention_lease.period"参数定义。您可以在领导者索引上配置此设置。

当追随者索引启动时，它会从领导者索引获取保留租约。此租约通知领导者，在追随者指示它已收到操作或租约到期之前，它不应允许修剪软删除。

如果追随者索引远远落后于领导者并且无法复制操作，则 Elasticsearch 会报告"index].fatal_exception"错误。要解决此问题，请重新创建追随者索引。当新的关注索引启动时，[远程恢复过程从领导者重新复制 Lucene 段文件。

重新创建关注者索引是一种破坏性操作。所有现有的 Lucenesegment 文件都将在包含追随者索引的集群上被删除。

要重新创建关注者索引，请访问跨集群复制并选择**追随者索引**选项卡。

选择从属索引并暂停复制。当从属索引状态更改为"已暂停"时，重新选择从属者索引并选择取消关注领导索引。

关注者索引将转换为标准索引，并且不再显示在"跨集群复制"页面上。

在侧边导航中，选择"**索引管理**"。从前面的步骤中选择关注者索引并关闭从属索引。

然后，您可以重新创建追随者索引以重新启动复制过程。

使用接口

使用暂停跟随 API 对复制过程进行优化。然后，关闭关注者索引并重新创建它。例如：

    
    
    response = client.ccr.pause_follow(
      index: 'follower_index'
    )
    puts response
    
    response = client.indices.close(
      index: 'follower_index'
    )
    puts response
    
    response = client.ccr.follow(
      index: 'follower_index',
      wait_for_active_shards: 1,
      body: {
        remote_cluster: 'remote_cluster',
        leader_index: 'leader_index'
      }
    )
    puts response
    
    
    POST /follower_index/_ccr/pause_follow
    
    POST /follower_index/_close
    
    PUT /follower_index/_ccr/follow?wait_for_active_shards=1
    {
      "remote_cluster" : "remote_cluster",
      "leader_index" : "leader_index"
    }

### 终止复制

您可以取消关注领导者索引以终止复制并将追随者索引转换为标准索引。

访问跨集群复制，然后选择**追随者索引**选项卡。

选择从属索引并暂停复制。当从属索引状态更改为"已暂停"时，重新选择从属者索引并选择取消关注领导索引。

关注者索引将转换为标准索引，并且不再显示在"跨集群复制"页面上。

然后，您可以选择"**索引管理**"，选择前面步骤中的关注者索引，然后关闭关注者索引。

使用接口

您可以使用取消关注 API 终止复制。此 API 将关注者索引转换为标准(非关注者)索引。

[« Tutorial: Set up cross-cluster replication](ccr-getting-started-
tutorial.md) [Manage auto-follow patterns »](ccr-auto-follow.md)
