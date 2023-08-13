

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-keystore](elasticsearch-keystore.md) [elasticsearch-
reconfigure-node »](reconfigure-node.md)

## 弹性搜索节点

"elasticsearch-node"命令使您能够在节点上执行某些不安全操作，这些操作只有在节点关闭时才能进行。此命令允许您调整节点的角色，不安全地编辑集群设置，并且即使与磁盘上的数据不兼容，也可以在灾难发生后恢复一些数据或启动节点。

###Synopsis

    
    
    bin/elasticsearch-node repurpose|unsafe-bootstrap|detach-cluster|override-version
      [-E <KeyValuePair>]
      [-h, --help] ([-s, --silent] | [-v, --verbose])

###Description

此工具具有多种模式：

* "elasticsearch-node repurpose"可用于从节点中删除不需要的数据，如果它曾经是数据节点或符合主节点条件的节点，但已被重新利用为没有这些角色中的一个或另一个。  * "弹性搜索节点删除设置"可用于从集群状态中删除持久设置，以防它包含阻止集群形成的不兼容设置。  * "elasticsearch-node remove-customs"可用于从集群状态中删除自定义元数据，以防它包含阻止加载集群状态的损坏元数据。  * "elasticsearch-node unsafe-bootstrap"可用于执行_unsafe集群bootstrapping_。它强制其中一个节点使用其群集元数据的本地副本自行形成全新的群集。  * "elasticsearch-node detach-cluster"使您能够将节点从一个集群移动到另一个集群。这可用于将节点移动到使用"elasticsearch-node unsafe-bootstrap"命令创建的新集群中。如果无法进行不安全的群集引导，它还使您能够将节点移动到全新的群集中。  * "elasticsearch-node override-version"使您能够启动节点，即使数据路径中的数据是由不兼容的 Elasticsearch 版本写入的。这有时可能允许您降级到早期版本的 Elasticsearch。

#### JVMoptions

CLI 工具使用 64MB 的堆运行。对于大多数工具，此值都很好。但是，如果需要，可以通过设置CLI_JAVA_OPTS环境变量来覆盖它。例如，以下内容将"节点"工具使用的堆大小增加到 1GB。

    
    
    export CLI_JAVA_OPTS="-Xmx1g"
    bin/elasticsearch-node ...

#### 改变阳极的作用

在某些情况下，您可能希望在不遵循正确的重新调整过程的情况下重新调整节点的用途。"弹性搜索节点重新利用"工具允许您删除磁盘上任何多余的数据，并在重新调整节点用途后启动节点。

预期用途是：

* 停止节点 * 根据需要设置"node.roles"来更新"elasticsearch.yml"。  * 在节点上运行"弹性搜索节点重新利用" * 启动节点

如果您在没有"data"角色和"master"角色的节点上运行"elasticsearch-node repurpose"，那么它将删除该节点上任何剩余的分片数据，但会保留索引和集群元数据。如果您在没有"data"和"master"角色的节点上运行"elasticsearch-node repurpose"，那么它将删除任何剩余的分片数据和索引元数据，但它将保留集群元数据。

如果包含的数据在群集中的其他节点上不可用，则运行此命令可能会导致上述索引的数据丢失。仅当您了解并接受可能的后果时，并且仅在确定节点无法完全重新调整用途后，才运行此工具。

该工具提供要删除的数据的摘要，并在进行任何更改之前要求确认。您可以通过传递详细 ('-v') 选项来获取有关受影响索引和分片的详细信息。

#### 删除持久性群集设置

在某些情况下，节点包含阻止群集形成的持久群集设置。由于无法形成群集，因此无法使用群集更新设置 API 删除这些设置。

"弹性搜索节点删除设置"工具允许您从磁盘群集状态中强制删除这些持久设置。该工具将设置列表作为应删除的参数，并且还支持通配符模式。

预期用途是：

* 停止节点 * 在节点上运行"弹性搜索节点删除设置名称设置删除" * 对所有其他符合主节点条件的节点重复此操作 * 启动节点

#### 从群集状态中删除自定义元数据

在某些情况下，节点包含自定义元数据(通常由插件提供)会阻止节点从磁盘启动和加载群集。

"弹性搜索节点删除自定义"工具允许您强制删除有问题的自定义元数据。该工具将自定义元数据名称列表作为应删除的参数，并且还支持通配符模式。

预期用途是：

* 停止节点 * 在节点上运行"弹性搜索节点删除自定义名称删除" * 对所有其他符合主节点条件的节点重复此操作 * 启动节点

#### 灾后恢复数据

有时 Elasticsearch 节点会暂时停止，可能是因为需要执行一些维护活动，也可能是因为硬件故障。解决临时情况并重启节点后，节点将重新加入集群并正常运行。根据您的配置，您的集群可能能够保持完全可用，即使其一个或多个节点停止。

有时，在节点停止后可能无法重新启动节点。例如，节点的主机可能会遇到无法修复的硬件问题。如果集群仍然可用，那么您可以在另一台主机上启动一个新节点，Elasticsearch 会将这个节点引入集群中，代替故障节点。

每个节点将其数据存储在由"path.data"设置定义的数据目录中。这意味着在灾难中，您还可以通过将节点的数据目录移动到另一台主机来重新启动节点，前提是这些数据目录可以从故障主机中恢复。

Elasticsearch 需要大多数符合主节点条件的响应才能选择主节点并更新集群状态。这意味着，如果您有三个符合主节点条件的节点，则即使其中一个节点发生故障，群集仍将保持可用。但是，如果三个符合主节点条件的节点中的两个发生故障，则在重新启动其中至少一个节点之前，群集将不可用。

在极少数情况下，可能无法重新启动足够的节点来恢复群集的可用性。如果发生此类灾难，您应该从最近的快照构建一个新集群，并重新导入自拍摄该快照以来引入的任何数据。

但是，如果灾难足够严重，那么也可能无法从最近的快照中恢复。不幸的是，在这种情况下，没有办法不冒数据丢失的风险，但可以使用"弹性搜索节点"工具来构建一个新集群，其中包含来自失败集群的一些数据。

#### 绕过版本检查

Elasticsearch 写入磁盘的数据旨在由当前版本和一组有限的未来版本读取。它通常不能被旧版本读取，也不能被多个主要版本更新的版本读取。存储在磁盘上的数据包括写入它的节点的版本，Elasticsearch 在启动时会检查它是否与此版本兼容。

在极少数情况下，可能需要绕过此检查并使用由不兼容版本写入的数据启动 Elasticsearch 节点。如果存储数据的格式已更改，则这可能不起作用，并且这是一个冒险的过程，因为格式可能会以Elasticsearch可能误解的方式更改，从而无声地导致数据丢失。

要绕过此检查，您可以使用"elasticsearch-node override-version"工具将存储在数据路径中的版本号与当前版本覆盖，从而使 Elasticsearch 认为它与磁盘上的数据兼容。

##### 不安全的集群引导

如果至少有一个剩余的主节点，但无法重新启动其中的大多数节点，则"elasticsearch-node unsafe-bootstrap"命令将不安全地覆盖集群的投票配置，就像执行另一个集群引导过程一样。然后，目标节点可以使用目标节点上本地保存的群集元数据自行形成新群集。

这些步骤可能会导致任意数据丢失，因为目标节点可能无法保存最新的集群元数据，并且这种过时的元数据可能无法使用集群中的部分或全部索引。

由于不安全的引导会形成一个包含单个节点的新集群，因此一旦运行它，您必须使用"elasticsearch-node detach-cluster"工具将任何其他幸存的节点从故障集群迁移到这个新集群中。

当您运行"elasticsearch-node unsafe-bootstrap"工具时，它将分析节点的状态，并在采取任何操作之前要求确认。在请求确认之前，它会报告运行它的节点上群集状态的术语和版本，如下所示：

    
    
    Current node cluster state (term, version) pair is (4, 12)

如果可以选择运行此工具的节点，则应选择一个具有尽可能大的术语的节点。如果有多个节点具有相同的术语，请选择具有最大版本的节点。此信息标识具有最新群集状态的节点，从而最大程度地减少可能丢失的数据量。例如，如果第一个节点报告'(4， 12)'，第二个节点报告'(5， 3)'，则第二个节点是首选节点，因为它的项更大。但是，如果第二个节点报告"(3，17)"，则首选第一个节点，因为它的项更大。如果第二个节点报告"(4， 10)"，则它与第一个节点具有相同的术语，但版本较小，因此首选第一个节点。

运行此命令可能会导致任意数据丢失。仅当您了解并接受可能的后果，并且已用尽恢复群集的所有其他可能性时，才运行此工具。

使用此工具的操作顺序如下：

1. 确保您确实无法访问群集中至少一半的符合主节点条件的节点，并且无法通过将其数据路径移动到正常运行的硬件来修复或恢复这些节点。  2. 停止所有剩余节点。  3. 选择剩余的符合主节点条件的节点之一，成为如上所述的新当选主节点。  4. 在此节点上，运行"弹性搜索节点不安全引导程序"命令，如下所示。验证该工具是否报告"主节点已成功引导"。  5. 启动此节点并验证它是否被选为主节点。  6. 在集群中的每个其他节点上运行"弹性搜索节点分离集群"工具，如下所述。  7. 启动所有其他节点并验证每个节点是否加入群集。  8. 调查群集中的数据，以发现在此过程中是否丢失了任何数据。

运行该工具时，它将确保用于引导群集的节点未运行。在此工具运行时，所有其他符合主节点条件的节点也会停止，但该工具不会对此进行检查，这一点很重要。

消息"主节点已成功引导"并不意味着没有数据丢失，它只是意味着该工具能够完成其作业。

##### 从群集中分离节点

节点在群集之间移动是不安全的，因为不同的群集具有完全不同的群集元数据。无法安全地将两个集群中的元数据合并在一起。

为了防止无意中加入错误的群集，每个群集在首次启动时都会创建一个唯一标识符，称为 _cluster UUID_。每个节点都会记录其集群的 UUID，并拒绝加入具有不同 UUID 的集群。

但是，如果节点的群集永久失败，则可能需要尝试将其移动到新群集中。'elasticsearch-node detach-cluster'命令允许您通过重置集群来将节点与其集群分离 UUID.It 然后可以使用不同的 UUI 加入另一个集群。

例如，在不安全的集群引导之后，您需要将所有其他幸存的节点从其旧集群中分离出来，以便它们可以加入新的、不安全的引导集群。

仅当至少有一个幸存的主节点符合条件时，才可以进行不安全的群集引导。如果没有剩余的主节点，则群集元数据将完全丢失。但是，个人数据节点还包含与其分片对应的索引元数据的副本。这有时允许新集群导入这些分片作为悬空索引。有时，您可以在集群中所有符合主条件的节点丢失后恢复一些索引，方法是创建一个新集群，然后使用"弹性搜索节点分离集群"命令将任何幸存的节点移动到这个新集群中。新集群完全形成后，使用 Danglingindex API 列出、导入或删除任何悬空索引。

导入浮动索引时存在数据丢失的风险，因为数据节点可能没有索引元数据的最新副本，并且没有关于哪些分片副本同步的任何信息。这意味着可能会选择过时的分片副本作为主分片副本，并且某些分片可能与导入的映射不兼容。

执行此命令可能会导致任意数据丢失。仅当您了解并接受可能的后果，并且已用尽恢复群集的所有其他可能性时，才运行此工具。

使用此工具的操作顺序如下：

1. 确保您确实无法访问群集中每个符合主节点条件的节点，并且无法通过将其数据路径移动到正常运行的硬件来修复或恢复这些节点。  2. 启动新集群并验证其是否正常运行。该集群可以包含一个或多个全新的符合主节点条件的节点，也可以是如上所述形成的不安全的自举集群。  3. 停止所有剩余数据节点。  4. 在每个数据节点上，运行"弹性搜索节点分离集群"工具，如下所示。验证该工具是否报告"节点已成功从群集分离"。  5. 如有必要，请配置每个数据节点以发现新集群。  6. 启动每个数据节点并验证它是否已加入新集群。  7. 等待所有恢复完成，并调查集群中的数据以发现在此过程中是否丢失了任何数据。使用悬空索引 API 列出、导入或删除任何悬空索引。

消息"节点已成功从群集中分离"并不意味着没有数据丢失，它只是意味着该工具能够完成其作业。

###Parameters

`repurpose`

     Delete excess data when a node's roles are changed. 
`unsafe-bootstrap`

     Specifies to unsafely bootstrap this node as a new one-node cluster. 
`detach-cluster`

     Specifies to unsafely detach this node from its cluster so it can join a different cluster. 
`override-version`

     Overwrites the version number stored in the data path so that a node can start despite being incompatible with the on-disk data. 
`remove-settings`

     Forcefully removes the provided persistent cluster settings from the on-disk cluster state. 
`-E <KeyValuePair>`

     Configures a setting. 
`-h, --help`

     Returns all of the command parameters. 
`-s, --silent`

     Shows minimal output. 
`-v, --verbose`

     Shows verbose output. 

###Examples

#### 将节点重新用作专用主节点

在此示例中，以前的数据节点被重新用作专用主节点。首先将节点的设置更新为"node.roles： [ "master" ]' 在其 'elasticsearch.yml' 配置文件中。然后运行 'elasticsearch-node repurpose' 命令来查找并删除多余的分片数据：

    
    
    node$ ./bin/elasticsearch-node repurpose
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
    Found 2 shards in 2 indices to clean up
    Use -v to see list of paths and indices affected
    Node is being re-purposed as master and no-data. Clean-up of shard data will be performed.
    Do you want to proceed?
    Confirm [y/N] y
    Node successfully repurposed to master and no-data.

#### 将节点重新用作仅协调节点

在此示例中，以前保存数据的节点被重新用作仅协调节点。首先在其"elasticsearch.yml"配置文件中将节点的设置更新为"node.roles： []"。然后运行 'elasticsearch-noderepurpose' 命令来查找并删除多余的分片数据和索引元数据：

    
    
    node$./bin/elasticsearch-node repurpose
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
    Found 2 indices (2 shards and 2 index meta data) to clean up
    Use -v to see list of paths and indices affected
    Node is being re-purposed as no-master and no-data. Clean-up of index data will be performed.
    Do you want to proceed?
    Confirm [y/N] y
    Node successfully repurposed to no-master and no-data.

#### 删除持久性群集设置

如果节点包含阻止群集形成的持久群集设置(即无法使用群集更新设置 API 删除)，则可以运行以下命令来删除一个或多个群集设置。

    
    
    node$ ./bin/elasticsearch-node remove-settings xpack.monitoring.exporters.my_exporter.host
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
    The following settings will be removed:
    xpack.monitoring.exporters.my_exporter.host: "10.1.2.3"
    
    You should only run this tool if you have incompatible settings in the
    cluster state that prevent the cluster from forming.
    This tool can cause data loss and its use should be your last resort.
    
    Do you want to proceed?
    
    Confirm [y/N] y
    
    Settings were successfully removed from the cluster state

您还可以使用通配符删除多个设置，例如使用

    
    
    node$ ./bin/elasticsearch-node remove-settings xpack.monitoring.*

#### 从群集状态中删除自定义元数据

如果磁盘上的群集状态包含阻止节点启动和加载群集状态的自定义元数据，则可以运行以下命令来删除此自定义元数据。

    
    
    node$ ./bin/elasticsearch-node remove-customs snapshot_lifecycle
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
    The following customs will be removed:
    snapshot_lifecycle
    
    You should only run this tool if you have broken custom metadata in the
    cluster state that prevents the cluster state from being loaded.
    This tool can cause data loss and its use should be your last resort.
    
    Do you want to proceed?
    
    Confirm [y/N] y
    
    Customs were successfully removed from the cluster state

#### 不安全的集群引导

假设您的集群有五个符合主节点条件的节点，并且您永久丢失了其中三个节点，剩下两个节点。

* 在剩余的第一个节点上运行该工具，但在确认步骤中回答"n"。

    
    
    node_1$ ./bin/elasticsearch-node unsafe-bootstrap
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
    Current node cluster state (term, version) pair is (4, 12)
    
    You should only run this tool if you have permanently lost half or more
    of the master-eligible nodes in this cluster, and you cannot restore the
    cluster from a snapshot. This tool can cause arbitrary data loss and its
    use should be your last resort. If you have multiple surviving master
    eligible nodes, you should run this tool on the node with the highest
    cluster state (term, version) pair.
    
    Do you want to proceed?
    
    Confirm [y/N] n

* 在剩余的第二个节点上运行该工具，并在确认步骤中再次回答"n"。

    
    
    node_2$ ./bin/elasticsearch-node unsafe-bootstrap
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
    Current node cluster state (term, version) pair is (5, 3)
    
    You should only run this tool if you have permanently lost half or more
    of the master-eligible nodes in this cluster, and you cannot restore the
    cluster from a snapshot. This tool can cause arbitrary data loss and its
    use should be your last resort. If you have multiple surviving master
    eligible nodes, you should run this tool on the node with the highest
    cluster state (term, version) pair.
    
    Do you want to proceed?
    
    Confirm [y/N] n

* 由于第二个节点具有更大的术语，因此它具有更新鲜的集群状态，因此最好使用此节点不安全地引导集群：

    
    
    node_2$ ./bin/elasticsearch-node unsafe-bootstrap
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
    Current node cluster state (term, version) pair is (5, 3)
    
    You should only run this tool if you have permanently lost half or more
    of the master-eligible nodes in this cluster, and you cannot restore the
    cluster from a snapshot. This tool can cause arbitrary data loss and its
    use should be your last resort. If you have multiple surviving master
    eligible nodes, you should run this tool on the node with the highest
    cluster state (term, version) pair.
    
    Do you want to proceed?
    
    Confirm [y/N] y
    Master node was successfully bootstrapped

#### 从群集中分离节点

在不安全地引导新集群后，运行"elasticsearch-nodedetach-cluster"命令以从故障集群中分离所有剩余节点，以便它们可以加入新集群：

    
    
    node_3$ ./bin/elasticsearch-node detach-cluster
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
    You should only run this tool if you have permanently lost all of the
    master-eligible nodes in this cluster and you cannot restore the cluster
    from a snapshot, or you have already unsafely bootstrapped a new cluster
    by running `elasticsearch-node unsafe-bootstrap` on a master-eligible
    node that belonged to the same cluster as this node. This tool can cause
    arbitrary data loss and its use should be your last resort.
    
    Do you want to proceed?
    
    Confirm [y/N] y
    Node was successfully detached from the cluster

#### 绕过版本检查

运行"弹性搜索节点覆盖版本"命令以覆盖存储在数据路径中的版本，以便节点可以在与数据路径中存储的数据不兼容的情况下启动：

    
    
    node$ ./bin/elasticsearch-node override-version
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
    This data path was last written by Elasticsearch version [x.x.x] and may no
    longer be compatible with Elasticsearch version [y.y.y]. This tool will bypass
    this compatibility check, allowing a version [y.y.y] node to start on this data
    path, but a version [y.y.y] node may not be able to read this data or may read
    it incorrectly leading to data loss.
    
    You should not use this tool. Instead, continue to use a version [x.x.x] node
    on this data path. If necessary, you can use reindex-from-remote to copy the
    data from here into an older cluster.
    
    Do you want to proceed?
    
    Confirm [y/N] y
    Successfully overwrote this node's metadata to bypass its version compatibility checks.

[« elasticsearch-keystore](elasticsearch-keystore.md) [elasticsearch-
reconfigure-node »](reconfigure-node.md)
