

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Cluster-level shard allocation and routing settings](modules-cluster.md)
[Cross-cluster replication settings »](ccr-settings.md)

## 杂项群集设置

####Metadata

可以使用以下设置将整个群集设置为只读：

`cluster.blocks.read_only`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Make the whole cluster read only (indices do not accept write operations), metadata is not allowed to be modified (create or delete indices). 
`cluster.blocks.read_only_allow_delete`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Identical to `cluster.blocks.read_only` but allows to delete indices to free up resources. 

不要依赖此设置来阻止对群集进行更改。有权访问群集更新设置 API 的任何用户都可以再次使群集读写。

#### 集群分片限制

根据集群中的节点数，集群中的分片数量存在软限制。这是为了防止可能无意中破坏群集稳定的操作。

此限制旨在作为安全网，而不是大小调整建议。您的集群可以安全支持的分片的确切数量取决于您的硬件配置和工作负载，但在几乎所有情况下都应远低于此限制，因为默认限制设置得相当高。

如果某个操作(例如创建新索引、还原 anindex 的快照或打开已关闭的索引)会导致集群中的分片数超过此限制，则该操作将失败，并显示指示分片限制的错误。

如果集群已经超过限制，由于节点成员身份的变化或设置的更改，所有创建或打开索引的操作都将失败，直到限制如下所述增加，或者关闭或删除某些索引以使分片数低于限制。

对于普通(非冻结)索引，集群分片限制默认为每个非冻结数据节点 1，000 个分片，对于冻结索引，每个冻结数据节点 3000 个分片。所有开放索引的主分片和副本分片都计入限制，包括未分配的分片。例如，具有 5 个主分片和 2 个副本的开放索引计为 15 个分片。封闭索引不计入分片计数。

您可以使用以下设置动态调整集群分片限制：

`cluster.max_shards_per_node`

    

(动态)限制集群的主分片和副本分片的总数。Elasticsearch 计算极限如下：

"cluster.max_shards_per_node * 非冻结数据节点数"

封闭索引的分片不计入此限制。默认为"1000"。没有数据节点的集群是无限的。

Elasticsearch 拒绝任何创建超过此限制允许的分片的请求。例如，"cluster.max_shards_per_node"设置为"100"且三个数据节点的集群的分片限制为 300。如果集群已经包含 296 个分片，Elasticsearch 将拒绝向集群添加 5 个或更多分片的任何请求。

请注意，冻结的分片有其自己的独立限制。

`cluster.max_shards_per_node.frozen`

    

(动态)限制集群的主分片和副本冻结分片的总数。Elasticsearch 计算限制如下：

'cluster.max_shards_per_node.frozen * 冻结数据节点数"

封闭索引的分片不计入此限制。默认为"3000"。没有冻结数据节点的集群是无限的。

Elasticsearch 拒绝任何创建超过此限制的冻结分片的请求。例如，将"cluster.max_shards_per_node.frozen"设置为"100"且三个冻结数据节点的集群的冻结分片限制为 300。如果集群已经包含 296 个分片，Elasticsearch 会拒绝任何向集群添加五个或更多冻结分片的请求。

这些设置不会限制单个节点的分片。要限制每个节点的分片数量，请使用"cluster.routing.allocation.total_shards_per_node"设置。

#### 用户定义的群集元数据

可以使用群集设置 API 存储和检索用户定义的元数据。这可用于存储有关群集的任意、不经常更改的数据，而无需创建索引来存储它。可以使用任何前缀为"cluster.metadata"的键存储此数据。例如，要将集群管理员的电子邮件地址存储在密钥"cluster.metadata.administrator"下，请发出以下请求：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.metadata.administrator": 'sysadmin@example.com'
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent": {
        "cluster.metadata.administrator": "sysadmin@example.com"
      }
    }

用户定义的群集元数据不用于存储敏感或机密信息。存储在用户定义的集群元数据中的任何信息都可以被任何有权访问集群 GetSettings API 的人查看，并记录在 Elasticsearch 日志中。

#### 索引逻辑删除

群集状态维护索引逻辑删除以显式表示已删除的索引。在群集状态下维护的逻辑删除数由以下设置控制：

`cluster.indices.tombstones.size`

     ([Static](settings.html#static-cluster-setting)) Index tombstones prevent nodes that are not part of the cluster when a delete occurs from joining the cluster and reimporting the index as though the delete was never issued. To keep the cluster state from growing huge we only keep the last `cluster.indices.tombstones.size` deletes, which defaults to 500. You can increase it if you expect nodes to be absent from the cluster and miss more than 500 deletes. We think that is rare, thus the default. Tombstones don't take up much space, but we also think that a number like 50,000 is probably too big. 

如果 Elasticsearch 遇到当前集群状态中缺少的索引数据，则认为这些索引处于悬空状态。例如，如果您在 Elasticsearch 节点处于脱机状态时删除了多个 'cluster.indices.tombstones.size' 索引，则可能会发生这种情况。

您可以使用悬空索引 API 来管理这种情况。

####Logger

控制日志记录的设置可以使用"logger."前缀动态更新。例如，要将"index.recovery"模块的日志记录级别提高到"DEBUG"，请发出以下请求：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "logger.org.elasticsearch.indices.recovery": 'DEBUG'
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent": {
        "logger.org.elasticsearch.indices.recovery": "DEBUG"
      }
    }

#### 持久任务分配

插件可以创建一种称为持久任务的任务。这些任务通常是长期任务，并以群集状态存储，允许在完全群集重新启动后恢复任务。

每次创建持久任务时，主节点负责将任务分配给集群的节点，然后分配的节点将选取任务并在本地执行。将持久任务分配给节点的过程由以下设置控制：

`cluster.persistent_tasks.allocation.enable`

    

(动态)启用或禁用持久性任务的分配：

* 'all' \-(默认)允许将持久任务分配给节点 * "无" \- 不允许为任何类型的持久任务分配

此设置不会影响已在执行的持久任务。只有新创建的持久任务或必须重新分配的任务(例如，在节点离开群集之后)才会受到此设置的影响。

`cluster.persistent_tasks.allocation.recheck_interval`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The master node will automatically check whether persistent tasks need to be assigned when the cluster state changes significantly. However, there may be other factors, such as memory usage, that affect whether persistent tasks can be assigned to nodes but do not cause the cluster state to change. This setting controls how often assignment checks are performed to react to these factors. The default is 30 seconds. The minimum permitted value is 10 seconds. 

[« Cluster-level shard allocation and routing settings](modules-cluster.md)
[Cross-cluster replication settings »](ccr-settings.md)
