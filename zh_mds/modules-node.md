

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Monitoring settings in Elasticsearch](monitoring-settings.md) [Networking
»](modules-network.md)

##Node

每当你启动一个 Elasticsearch 的实例时，你就会开始a_node_。连接节点的集合称为群集。如果您运行的是 Elasticsearch 的单个节点，那么您将拥有一个由单节点组成的集群。

默认情况下，群集中的每个节点都可以处理 HTTP 和传输流量。传输层专门用于节点之间的通信;HTTP 层由 REST 客户端使用。

所有节点都知道群集中的所有其他节点，并且可以将客户端请求转发到相应的节点。

### 节点角色

您可以通过在"elasticsearch.yml"中设置"node.roles"来定义节点的角色。如果设置了"node.roles"，则仅为节点分配您指定的角色。如果未设置"node.roles"，则会为节点分配以下角色：

* "主" * "数据" * "data_content" * "data_hot" * "data_warm" * "data_cold" * "data_frozen" * "摄取" * "ml" * "remote_cluster_client" * "转换"

如果设置"节点角色"，请确保指定群集所需的每个节点角色。每个群集都需要以下节点角色：

* "主"* "data_content"和"data_hot"或"数据"

某些弹性堆栈功能还需要特定的节点角色：

* 跨集群搜索和跨集群复制需要"remote_cluster_client"角色。  * 堆栈监控和摄取管道需要"摄取"角色。  * 队列、Elastic 安全应用和转型需要"转换"角色。还需要"remote_cluster_client"角色才能将跨集群搜索与这些功能一起使用。  * 机器学习功能(如异常检测)需要"ml"角色。

随着群集的增长，特别是如果您有大型机器学习作业或连续转换，请考虑将专用的主节点与专用数据节点、机器学习节点和转换节点分开。

符合主节点条件的节点

     A node that has the `master` role, which makes it eligible to be [elected as the _master_ node](modules-discovery.html "Discovery and cluster formation"), which controls the cluster. 
[Data node](modules-node.html#data-node "Data node")

     A node that has the `data` role. Data nodes hold data and perform data related operations such as CRUD, search, and aggregations. A node with the `data` role can fill any of the specialised data node roles. 
[Ingest node](modules-node.html#node-ingest-node "Ingest node")

     A node that has the `ingest` role. Ingest nodes are able to apply an [ingest pipeline](ingest.html "Ingest pipelines") to a document in order to transform and enrich the document before indexing. With a heavy ingest load, it makes sense to use dedicated ingest nodes and to not include the `ingest` role from nodes that have the `master` or `data` roles. 
[Remote-eligible node](modules-node.html#remote-node "Remote-eligible node")

     A node that has the `remote_cluster_client` role, which makes it eligible to act as a remote client. 
[Machine learning node](modules-node.html#ml-node "Machine learning node")

     A node that has the `ml` role. If you want to use machine learning features, there must be at least one machine learning node in your cluster. For more information, see [Machine learning settings](ml-settings.html "Machine learning settings in Elasticsearch") and [Machine learning in the Elastic Stack](/guide/en/machine-learning/8.9/index.html). 
[Transform node](modules-node.html#transform-node "Transform node")

     A node that has the `transform` role. If you want to use transforms, there must be at least one transform node in your cluster. For more information, see [Transforms settings](transform-settings.html "Transforms settings in Elasticsearch") and [_Transforming data_](transforms.html "Transforming data"). 

### 协调节点

搜索请求或批量索引请求等请求可能涉及保存在不同数据节点上的数据。例如，搜索请求分两个阶段执行，由接收客户端请求的节点(_coordinating node_)协调。

在 _scatter_ 阶段，协调节点将请求转发到保存数据的数据节点。每个数据节点在本地执行请求，并将其结果返回给协调节点。在 _gather_ 阶段，协调节点将每个数据节点的结果简化为单个全局结果集。

每个节点都是一个协调节点。这意味着通过"node.roles"具有显式空角色列表的节点将仅充当协调节点，无法禁用。因此，这样的节点需要有足够的内存和 CPU 来处理聚集阶段。

### 主节点

主节点负责轻量级集群范围的操作，例如创建或删除索引、跟踪哪些节点是集群的一部分，以及决定将哪些分片分配给哪些节点。对于集群运行状况而言，拥有稳定的主节点非常重要。

任何非投票节点的主节点都可以通过主选举过程被选为主节点。

主节点必须有一个"path.data"目录，其内容在重新启动后持续存在，就像数据节点一样，因为这是存储集群元数据的位置。群集元数据描述如何读取存储在数据节点上的数据，因此如果数据丢失，则无法读取存储在数据节点上的数据。

#### 专用主节点

对于集群的运行状况而言，选定的主节点拥有履行其职责所需的资源非常重要。如果选定的主节点因其他任务而过载，则集群将无法正常运行。避免主节点因其他任务而过载的最可靠方法是将所有符合主节点条件的节点配置为仅具有"主"角色的主节点_dedicated eligiblenodes_，从而使它们能够专注于管理集群。符合主节点条件的节点仍将充当将请求从客户端路由到集群中其他节点的协调节点，但您应该为此目的_not_use专用主节点。

如果符合主节点条件的节点具有其他角色和职责，则小型或负载较轻的集群可能会运行良好，但是一旦您的集群包含多个节点，通常使用专用的主节点是有意义的。

要创建专用的主节点，请设置：

    
    
    node.roles: [ master ]

#### 仅投票主节点

仅投票的主节点是参与主选举但不充当集群的选定主节点的节点。特别是，仅投票节点可以作为选举中的决胜局。

使用术语"主节点资格"来描述仅投票节点似乎令人困惑，因为这样的节点实际上根本没有资格成为主节点。这个术语是历史的不幸后果：符合主节点条件的节点是在群集状态发布期间参与选举并执行某些任务的节点，而仅投票节点即使永远无法成为当选的主节点，也具有相同的职责。

要将符合主节点条件的节点配置为仅投票节点，请在角色列表中包括"主节点"和"voting_only"。例如，要创建仅投票数据节点：

    
    
    node.roles: [ data, master, voting_only ]

只有具有"主"角色的节点才能标记为具有"voting_only"角色。

高可用性 (HA) 群集至少需要三个符合主节点条件的节点，其中至少两个不是仅投票节点。即使其中一个节点发生故障，这样的集群也能够选择主节点。

仅符合投票条件的主节点也可以填充集群中的其他角色。例如，节点可能既是数据节点，也可以是仅投票的主节点。_dedicated_ 仅投票的主节点是仅投票的主节点，不会在群集中填充其他角色。要创建专用的仅投票主节点，请设置：

    
    
    node.roles: [ master, voting_only ]

由于专用仅投票节点从不充当集群的选定主节点，因此与真正的主节点相比，它们可能需要更少的堆和更弱的 CPU。但是，所有符合主节点条件的节点(包括仅投票节点)都位于发布群集状态更新的关键路径上。群集状态更新通常独立于性能关键型工作负荷(如索引或搜索)，但它们涉及管理活动，例如索引创建和滚动更新、映射更新和故障后恢复。这些活动的性能特征是每个符合主节点条件的存储速度的函数，以及所选主节点与群集中其他节点之间网络互连的可靠性和延迟。因此，必须确保群集中节点可用的存储和网络足以满足性能目标。

### 数据节点

数据节点保存包含已编制索引的文档的分片。数据节点处理与数据相关的操作，如 CRUD、搜索和聚合。这些操作是 I/O、内存和 CPU 密集型操作。监视这些资源并在它们过载时添加更多数据节点非常重要。

拥有专用数据节点的主要好处是主角色和数据角色的分离。

要创建专用数据节点，请设置：

    
    
    node.roles: [ data ]

在多层部署体系结构中，您可以使用专用数据角色将数据节点分配给特定层："data_content"、"data_hot"、"data_warm"、"data_cold"或"data_frozen"。一个节点可以属于多个层，但具有专用数据角色之一的节点不能具有通用的"数据"角色。

### 内容数据节点

内容数据节点是内容层的一部分。存储在内容层中的数据通常是项目(如产品目录或文章存档)的集合。与时序数据不同，内容的值随着时间的推移保持相对恒定，因此随着时间的流逝，将其移动到具有不同性能特征的层是没有意义的。内容数据通常具有较长的数据保留要求，并且您希望能够快速检索项目，无论其有多旧。

内容层节点通常针对查询性能进行优化 - 它们优先考虑处理能力而不是 IO 吞吐量，以便它们可以处理复杂的搜索和聚合并快速返回结果。虽然它们还负责索引，但内容数据的摄取率通常不如日志和指标等时序数据那样高。从复原能力的角度来看，此层中的索引应配置为使用一个或多个副本。

内容层是必需的。不属于数据流的系统索引和其他索引会自动分配给内容层。

要创建专用内容节点，请设置：

    
    
    node.roles: [ data_content ]

### 热数据节点

热数据节点是热层的一部分。热层是时序数据的 Elasticsearch入口点，保存最新、最常搜索的时间时序数据。热层中的节点需要快速进行 bo线程和写入，这需要更多的硬件资源和更快的存储 (SSD)。为了实现复原能力，应将热层中的索引配置为使用一个或多个副本。

热层是必需的。作为数据流一部分的新索引会自动分配到热层。

要创建专用热节点，请设置：

    
    
    node.roles: [ data_hot ]

### 暖数据节点

暖数据节点是暖层的一部分。时序数据的查询频率低于热层中最近编制索引的数据后，可以移动到暖层。暖层通常保存最近几周的数据。仍然允许更新，但可能不频繁。暖层中的节点通常不需要像热层中的节点一样快。对于复原能力，应将暖层中的索引配置为使用一个或多个副本。

要创建专用温节点，请设置：

    
    
    node.roles: [ data_warm ]

### 冷数据节点

冷数据节点是冷层的一部分。当您不再需要定期搜索时间序列数据时，它可以从暖层移动到冷层。虽然仍可搜索，但此层通常针对较低的存储成本而不是搜索速度进行了优化。

为了更好地节省存储，可以在冷层上保留可搜索快照的完全装载索引。与常规索引不同，这些完全挂载的索引不需要副本即可实现可靠性。如果发生故障，他们可以从底层快照中恢复数据。这可能会使数据所需的本地存储减半。需要快照存储库才能在冷层中使用完全挂载的索引。完全挂载的索引是只读的。

或者，可以使用冷层来存储带有副本的常规索引，而不是使用可搜索的快照。这使你可以在较便宜的硬件上存储较旧的数据，但与暖层相比，不会减少所需的磁盘空间。

要创建专用冷节点，请设置：

    
    
    node.roles: [ data_cold ]

### 冻结数据节点

冻结的数据节点是冻结层的一部分。一旦数据不再被查询，或者很少被查询，它可能会从冷层移动到冻结层，在那里它会在余生中停留。

冻结层需要快照存储库。冻结层使用部分装载的索引来存储和加载快照存储库中的数据。这降低了本地存储和运营成本，同时仍允许您搜索冻结的数据。由于Elasticsearch有时必须从快照存储库中获取冻结的数据，因此冻结层上的搜索通常比冷层上的搜索慢。

要创建专用冻结节点，请设置：

    
    
    node.roles: [ data_frozen ]

### 采集节点

采集节点可以执行由一个或多个采集处理器组成的预处理管道。根据摄取处理器执行的操作类型和所需资源，拥有专用的节点(仅执行此特定任务)可能是有意义的。

要创建专用采集节点，请设置：

    
    
    node.roles: [ ingest ]

### 协调仅节点

如果您取消了能够处理主职责、保存数据和预处理文档的能力，那么您将剩下一个只能路由请求、处理搜索缩减阶段和分发批量索引的 _coordinating_ 节点。从本质上讲，仅协调节点的行为就像智能负载均衡器一样。

仅协调节点可以通过从数据和符合主节点条件的节点中卸载协调节点角色来使大型集群受益。它们加入群集并接收完整的群集状态，就像其他每个节点一样，它们使用群集状态将请求直接路由到适当的位置。

向集群添加过多的仅协调节点会增加整个集群的负担，因为选定的主节点必须等待来自每个节点的集群状态更新的确认！只协调节点的好处不应该被夸大 - 数据节点可以愉快地服务于相同的目的。

要创建专用协调节点，请设置：

    
    
    node.roles: [ ]

### 远程合格节点

符合远程条件的节点充当跨群集客户端并连接到远程群集。连接后，您可以使用跨集群搜索搜索远程集群。您还可以使用跨集群复制在集群之间同步数据。

    
    
    node.roles: [ remote_cluster_client ]

### 机器学习节点

机器学习节点运行作业并处理机器学习 API 请求。有关详细信息，请参阅机器学习设置。

若要创建专用机器学习节点，请设置：

    
    
    node.roles: [ ml, remote_cluster_client]

"remote_cluster_client"角色是可选的，但强烈建议使用。否则，在机器学习作业或数据源中使用跨集群搜索时会失败。如果在异常情况检测作业中使用跨集群搜索，则所有符合主节点条件的节点上也需要"remote_cluster_client"角色。否则，数据馈送无法启动。请参阅符合远程条件的节点。

### 转换节点

转换节点运行转换并处理转换 API 请求。有关详细信息，请参阅转换设置。

要创建专用转换节点，请设置：

    
    
    node.roles: [ transform, remote_cluster_client ]

"remote_cluster_client"角色是可选的，但强烈建议使用。否则，在转换中使用跨集群搜索时将失败。请参阅符合远程条件的节点。

### 改变阳极的角色

每个数据节点在磁盘上维护以下数据：

* 分配给该节点的每个分片的分片数据，* 与分配给该节点的每个分片对应的索引元数据，以及 * 集群范围的元数据，例如设置和索引模板。

同样，每个符合主节点条件的节点在磁盘上维护以下数据：

* 集群中每个索引的索引元数据，以及 * 集群范围的元数据，例如设置和索引模板。

每个节点在启动时检查其数据路径的内容。如果它发现意外数据，那么它将拒绝启动。这是为了避免导入不需要的悬空索引，这可能导致红色群集运行状况。更准确地说，没有"data"角色的节点如果在启动时发现磁盘上有任何分片数据，将拒绝启动，而没有"master"和"data"角色的节点如果在启动时磁盘上有任何索引元数据，将拒绝启动。

可以通过调整节点的"elasticsearch.yml"文件并重新启动它来更改节点的角色。这被称为_重新调整用途_阳极。为了满足上述意外数据的检查，您必须执行一些额外的步骤来准备节点，以便在启动没有"data"或"master"角色的节点时重新调整用途。

* 如果要通过删除"data"角色来重新调整数据节点的用途，则应首先使用分配筛选器将所有分片数据安全地迁移到集群中的其他节点上。  * 如果要重新调整节点的用途，使其既没有"数据"角色，也没有"主"角色，那么最简单的方法是使用空数据路径和所需角色启动一个全新的节点。您可能会发现，首先使用分配筛选器将分片数据迁移到集群中的其他位置是最安全的。

如果无法执行这些额外的步骤，那么您可以使用"弹性搜索节点重新利用"工具来删除任何阻止阳极启动的多余数据。

### 节点数据路径设置

###'路径.数据'

每个符合主节点条件的数据节点都需要访问一个数据目录，其中将存储分片、索引和集群元数据。"path.data"默认为"$ES_HOME/data"，但可以在"elasticsearch.yml"配置文件中配置绝对路径或相对于"$ES_HOME"的路径，如下所示：

    
    
    path.data:  /var/elasticsearch/data

与所有节点设置一样，也可以在命令行上将其指定为：

    
    
    ./bin/elasticsearch -Epath.data=/var/elasticsearch/data

"path.data"目录的内容必须在重新启动后保留，因为这是存储数据的位置。Elasticsearch 要求文件系统的行为就像它由本地磁盘备份一样，但这意味着只要远程存储的行为与本地存储没有什么不同，它就可以在正确配置的远程块设备(例如 SAN)和远程文件系统(例如 NFS)上正常工作。您可以在同一个文件系统上运行多个 Elasticsearch 节点，但每个 Elasticsearch 节点必须有自己的数据路径。

Elasticsearch 集群的性能通常受到底层存储性能的限制，因此您必须确保您的存储支持可接受的性能。一些远程存储的性能非常差，尤其是在 Elasticsearch 施加的那种负载下，因此在提交到特定的存储架构之前，请务必仔细对系统进行基准测试。

使用 '.zip' 或 '.tar.gz' 发行版时，应将 'path.data' 设置配置为在 Elasticsearchhome 目录之外定位数据目录，这样就可以在不删除数据的情况下删除主目录！RPM 和 Debian 发行版已经为您做到了这一点。

不要修改数据目录中的任何内容，也不要运行可能干扰其内容的进程。如果 Elasticsearch 以外的内容修改了数据目录的内容，那么 Elasticsearch 可能会失败，报告损坏或其他数据不一致，或者看起来工作正常，因为静默丢失了一些数据。不要尝试对数据目录进行文件系统备份;没有受支持的方法来还原此类备份。请改用快照和还原来安全地进行备份。不要在数据目录上运行病毒扫描程序。病毒扫描程序可能会阻止 Elasticsearch 正常工作，并可能修改数据目录的内容。数据目录不包含可执行文件，因此病毒扫描只会发现误报。

### 其他节点设置

更多节点设置可以在_Configuring Elasticsearch_和重要 Elasticsearchconfiguration 中找到，包括：

* "cluster.name" * "node.name" * 网络设置

[« Monitoring settings in Elasticsearch](monitoring-settings.md) [Networking
»](modules-network.md)
