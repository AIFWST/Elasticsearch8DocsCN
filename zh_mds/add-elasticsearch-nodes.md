

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Cluster fault detection](cluster-fault-detection.md) [Full-cluster
restart and rolling restart »](restart-cluster.md)

## 在群集中添加和删除节点

当你启动一个 Elasticsearch 的实例时，你正在启动一个 _node_。AnElasticsearch _cluster_ 是一组具有相同"cluster.name"属性的节点。当节点加入或离开群集时，群集会自动重组自身，以在可用节点之间均匀分布数据。

如果您运行的是 Elasticsearch 的单个实例，那么您将拥有一个节点的集群。所有主分片都驻留在单个节点上。无法分配副本分片，因此集群状态保持黄色。群集功能齐全，但在发生故障时存在数据丢失的风险。

!具有一个节点和三个主分片的集群

您可以向群集添加节点以提高其容量和可靠性。默认情况下，节点既是数据节点，又有资格被选为控制集群的主节点。您还可以为特定目的配置新节点，例如处理引入请求。更多信息，请参见节点。

当您向集群添加更多节点时，它会自动分配副本分片。当所有主分片和副本分片都处于活动状态时，集群状态将更改为绿色。

!具有三个节点的群集

### 在现有群集中注册节点

您可以在本地计算机上注册其他节点，以试验具有多个节点行为的 howan Elasticsearch 集群。

要将节点添加到在多台计算机上运行的群集，还必须设置"discovery.seed_hosts"，以便新节点可以发现其群集的其余部分。

当 Elasticsearch 首次启动时，安全自动配置过程会将 HTTP 层绑定到 '0.0.0.0'，但只将传输层绑定到 localhost。此预期行为可确保您可以在默认情况下启用安全性的情况下启动单节点群集，而无需任何其他配置。

在注册新节点之前，在生产集群中通常需要执行其他操作，例如绑定到地址而不是"localhost"或满足引导程序检查。在此期间，自动生成的注册令牌可能会过期，这就是不会自动生成注册令牌的原因。

此外，只有同一主机上的节点才能加入群集，而无需其他配置。如果您希望来自其他主机的节点加入您的集群，则需要将"transport.host"设置为支持的值(例如取消注释建议值"0.0.0.0")，或者绑定到其他主机可以访问的接口的 IP 地址。有关详细信息，请参阅传输设置。

要在群集中注册新节点，请在群集中的任何现有节点上使用"弹性搜索-创建-注册令牌"工具创建注册令牌。然后，您可以使用"--enrollment-token"参数启动新节点，以便它加入现有集群。

1. 在运行 Elasticsearch 的单独终端中，导航到安装 Elasticsearch 的目录，然后运行"elasticsearch-create-enrollment-token"工具，为您的新节点生成注册令牌。           bin\elasticsearch-create-enrollment-token -s 节点

复制注册令牌，您将使用该令牌向 Elasticsearch 集群注册新节点。

2. 在新节点的安装目录中，启动 Elasticsearch 并使用"--enrollment-token"参数传递注册令牌。           bin\elasticsearch --enrollment-token <enrollment-token>

Elasticsearch 会在以下目录中自动生成证书和密钥：

    
        config\certs

3. 对要注册的任何新节点重复上一步。

有关发现和分片分配的更多信息，请参阅 to_Discovery 和集群formation_ 和集群级分片分配和路由设置。

### 主节点

添加或删除节点时，Elasticsearch 通过自动更新集群的_voting configuration_来保持最佳的容错级别，集群是一组符合主节点条件的节点，在做出诸如选择新主节点或提交新集群状态等决策时，会计算其响应。

建议在群集中具有少量固定数量的符合主节点条件的节点，并通过仅添加和删除不符合主节点条件的节点来扩展和缩减群集。但是，在某些情况下，可能需要在群集中添加或删除一些符合主节点条件的节点。

#### 添加符合主节点条件的节点

如果要向群集添加一些节点，只需配置新节点即可找到现有群集并启动它们。Elasticsearch将newnodes添加到投票配置中，如果这样做是合适的。

在主节点选举期间或加入现有形成的集群时，节点向主节点发送加入请求，以便正式添加到集群中。

#### 删除符合主节点条件的节点

删除符合主节点条件的节点时，重要的是不要同时删除太多节点。例如，如果当前有七个符合主节点条件的节点，并且您希望将其减少到三个，则不可能简单地一次停止四个节点：这样做只会留下三个节点，这不到投票配置的一半，这意味着集群无法采取任何进一步的操作。

更准确地说，如果您同时关闭一半或更多符合主节点条件的节点，则集群通常会变得不可用。如果发生这种情况，则可以通过再次启动已删除的节点使群集重新联机。

只要集群中至少有三个符合主节点条件的节点，作为一般规则，最好一次删除一个节点，让集群有足够的时间自动调整投票配置，并使容错级别适应新的节点集。

如果只剩下两个符合主节点条件的节点，则无法安全地删除这两个节点，因为两者都需要可靠地取得进展。要删除其中一个节点，您必须首先通知 Elasticsearch 它不应该成为投票配置的一部分，而应该将投票权交给另一个节点。然后，您可以将排除的节点脱机，而不会阻止其他节点取得进展。添加到投票配置排除列表中的节点仍然可以正常工作，但 Elasticsearch 会尝试将其从投票配置中删除，因此不再需要投票。重要的是，Elasticsearch 永远不会自动将投票排除列表中的节点移回投票配置。一旦排除的节点成功地从投票配置中自动重新配置，就可以安全地将其关闭，而不会影响集群的主级可用性。可以使用投票配置排除 API 将节点添加到投票配置排除列表中。例如：

    
    
    # Add node to voting configuration exclusions list and wait for the system
    # to auto-reconfigure the node out of the voting configuration up to the
    # default timeout of 30 seconds
    POST /_cluster/voting_config_exclusions?node_names=node_name
    
    # Add node to voting configuration exclusions list and wait for
    # auto-reconfiguration up to one minute
    POST /_cluster/voting_config_exclusions?node_names=node_name&timeout=1m

应添加到排除列表中的节点通过使用"？node_names"查询参数命名，或使用"？node_ids"查询参数通过其持久节点 ID 指定。如果对投票配置排除 API 的调用失败，您可以安全地重试它。只有成功的响应才能保证节点实际上已从投票配置中删除，并且不会恢复。如果选定的主节点被排除在投票配置之外，那么它将退位到另一个仍处于投票配置中的主节点(如果此类节点可用)。

尽管投票配置排除 API 对于将双节点群集缩减为单节点群集最有用，但也可以使用它同时删除多个符合主节点条件的节点。将多个节点添加到排除列表会让系统尝试自动重新配置所有这些节点，使其在保持群集可用的同时安全地关闭。在上面描述的示例中，将一个 7 个主节点集群缩小到只有三个主节点，您可以将四个节点添加到排除列表中，等待确认，然后同时关闭它们。

仅当在短时间内从集群中删除至少一半的主节点时，才需要投票排除。删除不符合主节点条件的节点时不需要它们，删除少于一半的主节点时也不需要它们。

为节点添加排除项会在投票配置排除列表中为该节点创建一个条目，该列表使系统自动尝试重新配置投票配置以删除该节点，并防止其在删除后返回到投票配置。当前排除项列表存储在群集状态中，可以按如下方式进行检查：

    
    
    response = client.cluster.state(
      filter_path: 'metadata.cluster_coordination.voting_config_exclusions'
    )
    puts response
    
    
    GET /_cluster/state?filter_path=metadata.cluster_coordination.voting_config_exclusions

此列表的大小受"cluster.max_voting_config_exclusions"设置的限制，该设置默认为"10"。请参阅发现和集群形成设置。由于投票配置排除项是永久性的且数量有限，因此必须清理它们。通常，在群集上执行某些维护时会添加排除项，维护完成后应清除排除项。在正常操作中，集群不应有投票配置排除项。

如果节点因要永久关闭而被排除在投票配置之外，则可以在关闭并从群集中删除该节点的排除项。如果排除项是错误创建的，或者只是通过指定"？wait_for_removal=false"暂时需要排除项，也可以清除排除项。

    
    
    # Wait for all the nodes with voting configuration exclusions to be removed from
    # the cluster and then remove all the exclusions, allowing any node to return to
    # the voting configuration in the future.
    DELETE /_cluster/voting_config_exclusions
    
    # Immediately remove all the voting configuration exclusions, allowing any node
    # to return to the voting configuration in the future.
    DELETE /_cluster/voting_config_exclusions?wait_for_removal=false

[« Cluster fault detection](cluster-fault-detection.md) [Full-cluster
restart and rolling restart »](restart-cluster.md)
